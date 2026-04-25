#!/usr/bin/env python3
"""
Carla 摄像头视频录制脚本
使用 Carla API 读取摄像头数据并保存为视频文件
"""

import glob
import os
import sys
import cv2
import numpy as np
import carla

# Carla 连接配置
HOST = 'localhost'
PORT = 3002

def main():
    try:
        # 连接 Carla 客户端
        print(f"连接到 Carla 服务器: {HOST}:{PORT}")
        client = carla.Client(HOST, PORT)
        client.set_timeout(10.0)
        
        # 获取世界
        world = client.get_world()
        print(f"成功连接到世界: {world.get_map().name}")
        
        # 获取蓝图库
        blueprint_library = world.get_blueprint_library()
        
        # 获取摄像头蓝图
        camera_bp = blueprint_library.find('sensor.camera.rgb')
        
        # 配置摄像头参数
        camera_bp.set_attribute('image_size_x', '1280')
        camera_bp.set_attribute('image_size_y', '720')
        camera_bp.set_attribute('fov', '90')
        
        # 获取玩家车辆（如果没有，则使用第一个找到的车辆）
        vehicles = world.get_actors().filter('vehicle.*')
        vehicle = None
        
        if len(vehicles) > 0:
            vehicle = vehicles[0]
            print(f"使用已有车辆: {vehicle.type_id}")
        else:
            # 如果没有车辆，生成一辆新车
            print("未找到现有车辆，正在生成新车...")
            vehicle_bp = blueprint_library.find('vehicle.tesla.model3')
            if vehicle_bp is None:
                # 备用车辆
                vehicle_bp = blueprint_library.filter('vehicle.*')[0]
            
            spawn_points = world.get_map().get_spawn_points()
            if not spawn_points:
                print("错误: 找不到出生点")
                return
            
            spawn_point = spawn_points[0]
            vehicle = world.spawn_actor(vehicle_bp, spawn_point)
            print(f"已生成车辆: {vehicle.type_id}")
        
        # 创建 RGB 摄像头
        print("创建 RGB 摄像头...")
        camera_transform = carla.Transform(
            carla.Location(x=1.5, z=2.0),
            carla.Rotation(pitch=0, yaw=0, roll=0)
        )
        
        camera = world.spawn_actor(
            camera_bp,
            camera_transform,
            attach_to=vehicle
        )
        
        # 视频保存配置
        output_dir = './carla_recordings'
        os.makedirs(output_dir, exist_ok=True)
        
        video_file = os.path.join(output_dir, f'carla_video_{os.getpid()}.mp4')
        width = 1280
        height = 720
        fps = 30.0
        
        # 使用 OpenCV 创建视频写入器
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(video_file, fourcc, fps, (width, height))
        
        if not video_writer.isOpened():
            print("错误: 无法创建视频写入器")
            return
        
        print(f"视频将保存到: {video_file}")
        print("开始录制... (按 Ctrl+C 停止)")
        
        # 图像回调函数
        frame_count = 0
        
        def camera_callback(image):
            nonlocal frame_count
            
            # 将 Carla 图像转换为 numpy 数组
            array = np.frombuffer(image.raw_data, dtype=np.uint8)
            array = array.reshape((image.height, image.width, 4))  # BGRA 格式
            
            # Carla 使用 BGRA，需要转换为 RGB（OpenCV 需要 RGB）
            array = array[:, :, :3]  # 去掉 alpha 通道
            array = array[:, :, ::-1]  # BGR -> RGB
            
            # 写入视频帧
            video_writer.write(array)
            frame_count += 1
            
            # 每 100 帧打印一次进度
            if frame_count % 100 == 0:
                print(f"已录制 {frame_count} 帧")
        
        # 注册回调
        camera.listen(camera_callback)
        
        # 等待录制
        try:
            while True:
                world.wait_for_tick()
        except KeyboardInterrupt:
            print("\n停止录制...")
        
        # 清理
        print(f"总共录制 {frame_count} 帧")
        video_writer.release()
        camera.stop()
        camera.destroy()
        print(f"视频已保存: {video_file}")
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("清理完成")

if __name__ == '__main__':
    main()
