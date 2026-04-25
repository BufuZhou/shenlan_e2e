#!/usr/bin/env python3
"""
Carla 摄像头视频录制脚本
使用 Carla API 读取摄像头数据并保存为视频文件
"""

import glob
import os
import sys
import time
import cv2
import numpy as np
import carla
from datetime import datetime

# Carla 连接配置
HOST = 'localhost'
PORT = 30002

def main():
    try:
        # 连接 Carla 客户端
        print(f"连接到 Carla 服务器: {HOST}:{PORT}")
        client = carla.Client(HOST, PORT)
        
        # 等待CARLA服务器就绪
        max_retries = 30
        retry_count = 0
        connected = False
        
        while retry_count < max_retries and not connected:
            try:
                client.set_timeout(30.0)
                world = client.get_world()
                connected = True
                print(f"成功连接到世界: {world.get_map().name}")
                
                # 打印CARLA服务器详细信息
                print("\n" + "="*60)
                print("CARLA 仿真器配置信息")
                print("="*60)
                
                # 地图信息
                map_name = world.get_map().name
                print(f"地图名称: {map_name}")
                
                # 仿真设置
                settings = world.get_settings()
                sync_mode = "同步模式 (Synchronous)" if settings.synchronous_mode else "异步模式 (Asynchronous)"
                print(f"仿真模式: {sync_mode}")
                if settings.fixed_delta_seconds > 0:
                    fps = 1.0 / settings.fixed_delta_seconds
                    print(f"固定时间步长: {settings.fixed_delta_seconds:.4f} 秒")
                    print(f"目标帧率: {fps:.1f} FPS")
                else:
                    print("固定时间步长: 未设置（可变帧率）")
                
                # 车辆信息
                vehicles = list(world.get_actors().filter('vehicle.*'))
                print(f"\n车辆数量: {len(vehicles)}")
                if len(vehicles) > 0:
                    for i, vehicle in enumerate(vehicles[:5]):  # 只显示前5辆车
                        transform = vehicle.get_transform()
                        velocity = vehicle.get_velocity()
                        speed = (velocity.x**2 + velocity.y**2 + velocity.z**2)**0.5 * 3.6  # m/s to km/h
                        print(f"  [{i+1}] {vehicle.type_id}")
                        print(f"      位置: ({transform.location.x:.1f}, {transform.location.y:.1f}, {transform.location.z:.1f})")
                        print(f"      速度: {speed:.1f} km/h")
                    if len(vehicles) > 5:
                        print(f"  ... 还有 {len(vehicles) - 5} 辆车")
                
                # 其他Actor信息
                sensors = world.get_actors().filter('sensor.*')
                print(f"\n传感器数量: {len(sensors)}")
                
                pedestrians = world.get_actors().filter('walker.*')
                print(f"行人数量: {len(pedestrians)}")
                
                traffic_lights = world.get_actors().filter('traffic.traffic_light')
                print(f"交通灯数量: {len(traffic_lights)}")
                
                print("="*60 + "\n")
            except RuntimeError as e:
                retry_count += 1
                if retry_count >= max_retries:
                    print(f"错误: 无法连接到CARLA服务器 ({e})")
                    return
                print(f"等待CARLA服务器启动... ({retry_count}/{max_retries})")
                time.sleep(2)
        
        # 获取蓝图库
        blueprint_library = world.get_blueprint_library()
        
        # 获取摄像头蓝图
        camera_bp = blueprint_library.find('sensor.camera.rgb')
        
        # 配置俯视图摄像头参数
        camera_bp.set_attribute('image_size_x', '1920')
        camera_bp.set_attribute('image_size_y', '1080')
        camera_bp.set_attribute('fov', '90')
        
        # 获取当前世界的帧率设置
        settings = world.get_settings()
        if settings.synchronous_mode and settings.fixed_delta_seconds > 0:
            current_fps = 1.0 / settings.fixed_delta_seconds
        else:
            # 异步模式，使用默认帧率
            current_fps = 20.0
        print(f"CARLA仿真帧率: {current_fps:.1f} FPS")
        
        # 视频帧率应该与CARLA仿真帧率一致
        fps = current_fps
        
        # 获取玩家车辆（必须使用已有车辆）
        print("等待车辆出现...")
        vehicle = None
        while vehicle is None:
            vehicles = world.get_actors().filter('vehicle.*')
            if len(vehicles) > 0:
                vehicle = vehicles[0]
                print(f"找到车辆: {vehicle.type_id}")
            else:
                print("未找到车辆，等待中... (按 Ctrl+C 退出)")
                world.wait_for_tick()
        
        # 获取车辆位置作为俯视图中心
        vehicle_location = vehicle.get_transform().location
        print(f"俯视图中心位置: x={vehicle_location.x:.1f}, y={vehicle_location.y:.1f}, z={vehicle_location.z:.1f}")
        
        # 创建俯视图摄像头（不绑定到车辆，固定位置）
        print("创建俯视图摄像头...")
        # 摄像头位置：车辆上方50米，向下90度俯拍
        camera_transform = carla.Transform(
            carla.Location(
                x=vehicle_location.x,
                y=vehicle_location.y,
                z=vehicle_location.z + 50.0  # 高度50米
            ),
            carla.Rotation(pitch=-90, yaw=0, roll=0)  # pitch=-90 表示垂直向下
        )
        
        camera = world.spawn_actor(
            camera_bp,
            camera_transform
            # 不绑定到车辆，固定在世界坐标系中
        )
        
        # 视频保存配置
        output_dir = './carla_recordings'
        os.makedirs(output_dir, exist_ok=True)
        
        # 根据创建时间生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        video_file = os.path.join(output_dir, f'carla_bev_{timestamp}.mp4')
        width = 1920
        height = 1080
        # fps已经在前面设置为CARLA的仿真帧率
        
        # 使用 OpenCV 创建视频写入器
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(video_file, fourcc, fps, (width, height))
        
        if not video_writer.isOpened():
            print("错误: 无法创建视频写入器")
            return
        
        print(f"视频将保存到: {video_file}")
        print(f"视频帧率: {fps:.1f} FPS")
        print("开始录制... (按 Ctrl+C 停止)")
        print("提示: 录制时间建议不少于10秒以获得完整视频")
        
        # 图像回调函数
        frame_count = 0
        start_time = time.time()
        last_report_time = start_time
        
        def camera_callback(image):
            nonlocal frame_count, last_report_time
            
            # 将 Carla 图像转换为 numpy 数组
            array = np.frombuffer(image.raw_data, dtype=np.uint8)
            array = array.reshape((image.height, image.width, 4))  # BGRA 格式
            
            # Carla 使用 BGRA，OpenCV VideoWriter 需要 BGR 格式
            array = array[:, :, :3]  # 去掉 alpha 通道，保留 BGR
            
            # 写入视频帧
            video_writer.write(array)
            frame_count += 1
            
            # 每秒打印一次进度
            current_time = time.time()
            if current_time - last_report_time >= 1.0:
                elapsed = current_time - start_time
                actual_fps = frame_count / elapsed if elapsed > 0 else 0
                print(f"已录制 {frame_count} 帧 | 录制时长: {elapsed:.1f} 秒 | 平均帧率: {actual_fps:.1f} FPS")
                last_report_time = current_time
        
        # 注册回调
        camera.listen(camera_callback)
        
        # 等待录制
        try:
            while True:
                # 使用 tick() 主动推进仿真，确保稳定获取帧
                world.tick()
        except KeyboardInterrupt:
            print("\n停止录制...")
        
        # 清理
        print(f"总共录制 {frame_count} 帧")
        video_writer.release()
        camera.stop()
        camera.destroy()
        
        print(f"视频已保存: {video_file}")
        print(f"视频时长: {frame_count/fps:.1f} 秒")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("清理完成")

if __name__ == '__main__':
    main()
