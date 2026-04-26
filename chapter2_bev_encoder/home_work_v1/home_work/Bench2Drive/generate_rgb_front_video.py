import cv2
import os
import glob
from pathlib import Path

def images_to_video(image_folder, output_video_path, fps=20):
    """
    将图像序列转换为视频
    
    Args:
        image_folder: 包含图像文件的文件夹路径
        output_video_path: 输出视频的路径
        fps: 视频帧率
    """
    # 获取所有PNG文件并按名称排序
    image_paths = sorted(glob.glob(os.path.join(image_folder, '*.png')))
    
    if not image_paths:
        print(f"在 {image_folder} 中未找到PNG图像")
        return
    
    print(f"找到 {len(image_paths)} 张图像")
    
    # 读取第一张图像以获取尺寸
    first_frame = cv2.imread(image_paths[0])
    if first_frame is None:
        print(f"无法读取图像: {image_paths[0]}")
        return
    
    height, width, layers = first_frame.shape
    print(f"图像尺寸: {width}x{height}")
    
    # 定义视频编解码器和创建VideoWriter对象
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4格式
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    
    # 遍历所有图像并写入视频
    for i, image_path in enumerate(image_paths):
        frame = cv2.imread(image_path)
        if frame is not None:
            video_writer.write(frame)
            if (i + 1) % 10 == 0:  # 每10帧打印一次进度
                print(f"处理进度: {i + 1}/{len(image_paths)}")
        else:
            print(f"警告: 无法读取图像 {image_path}")
    
    # 释放资源
    video_writer.release()
    print(f"视频已保存到: {output_video_path}")
    print(f"视频总帧数: {len(image_paths)}, 帧率: {fps}fps, 时长: {len(image_paths)/fps:.2f}秒")

if __name__ == "__main__":
    # 设置输入和输出路径
    base_path = "/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/save_path/drivetransformer_bench2drive_dev10_RouteScenario_2091_rep0_Town12_NonSignalizedJunctionLeftTurn_1_5_04_26_22_41_57"
    rgb_front_folder = os.path.join(base_path, "rgb_front")
    output_video = os.path.join(base_path, "rgb_front_video.mp4")
    
    # 转换图像为视频
    images_to_video(rgb_front_folder, output_video, fps=20)
