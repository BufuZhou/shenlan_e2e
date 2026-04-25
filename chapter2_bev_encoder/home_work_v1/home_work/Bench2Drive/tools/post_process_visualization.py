#!/usr/bin/env python3
"""
可视化结果后处理脚本
将保存的图片序列转换为视频，并生成OD感知结果的JSON文件
"""

import os
import json
import cv2
import numpy as np
import argparse
from pathlib import Path
from PIL import Image

def images_to_video(image_folder, output_video, fps=20, prefix=""):
    """
    将图片序列转换为视频
    
    Args:
        image_folder: 包含图片的文件夹
        output_video: 输出视频路径
        fps: 帧率
        prefix: 图片文件名前缀
    """
    # 获取所有图片文件
    image_files = sorted([f for f in os.listdir(image_folder) 
                         if f.endswith(('.png', '.jpg', '.jpeg')) and f.startswith(prefix)])
    
    if not image_files:
        print(f"警告: 在 {image_folder} 中未找到以 '{prefix}' 开头的图片")
        return
    
    print(f"找到 {len(image_files)} 张图片")
    
    # 读取第一张图片获取尺寸
    first_img = cv2.imread(os.path.join(image_folder, image_files[0]))
    height, width, _ = first_img.shape
    
    # 创建视频写入器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
    
    # 写入所有帧
    for img_file in image_files:
        img_path = os.path.join(image_folder, img_file)
        frame = cv2.imread(img_path)
        video_writer.write(frame)
    
    video_writer.release()
    print(f"视频已保存: {output_video}")


def generate_od_json(save_path, output_json):
    """
    生成OD感知结果的JSON文件
    
    Args:
        save_path: 保存路径
        output_json: 输出JSON文件路径
    """
    od_results = {
        "metadata": {
            "description": "OD感知结果 - 每帧的检测框和预测轨迹",
            "save_path": str(save_path)
        },
        "frames": []
    }
    
    # 检查是否有检测结果文件
    detections_file = os.path.join(save_path, "detections.json")
    if os.path.exists(detections_file):
        with open(detections_file, 'r') as f:
            frame_detections = json.load(f)
        
        od_results["frames"] = frame_detections
        print(f"从 detections.json 加载了 {len(frame_detections)} 帧的检测结果")
    else:
        # 如果没有现成的检测结果，创建一个基础结构
        print("未找到 detections.json，创建基础结构")
        
        # 获取所有帧的信息
        rgb_front_folder = os.path.join(save_path, "rgb_front")
        if os.path.exists(rgb_front_folder):
            frames = sorted([f for f in os.listdir(rgb_front_folder) if f.endswith('.png')])
            for idx, frame_file in enumerate(frames):
                frame_info = {
                    "frame_id": idx,
                    "timestamp": idx * 0.05,  # 假设20fps
                    "detections": [],
                    "ego_trajectory": {},
                    "image_file": frame_file
                }
                od_results["frames"].append(frame_info)
    
    # 保存JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(od_results, f, indent=2, ensure_ascii=False)
    
    print(f"OD感知结果JSON已保存: {output_json}")
    print(f"总共 {len(od_results['frames'])} 帧")


def create_bev_video(save_path, output_dir):
    """
    创建BEV视角视频
    
    Args:
        save_path: 保存路径
        output_dir: 输出目录
    """
    bev_folder = os.path.join(save_path, "bev")
    if not os.path.exists(bev_folder):
        print(f"警告: BEV文件夹不存在: {bev_folder}")
        return None
    
    output_video = os.path.join(output_dir, "bev_detection_video.mp4")
    images_to_video(bev_folder, output_video, fps=20)
    return output_video


def create_rgb_front_video(save_path, output_dir):
    """
    创建RGB前视视角视频
    
    Args:
        save_path: 保存路径
        output_dir: 输出目录
    """
    rgb_folder = os.path.join(save_path, "rgb_front")
    if not os.path.exists(rgb_folder):
        print(f"警告: RGB前视文件夹不存在: {rgb_folder}")
        return None
    
    output_video = os.path.join(output_dir, "rgb_front_detection_video.mp4")
    images_to_video(rgb_folder, output_video, fps=20)
    return output_video


def main():
    parser = argparse.ArgumentParser(description='可视化结果后处理')
    parser.add_argument('--save_path', type=str, required=True,
                       help='仿真结果保存路径')
    parser.add_argument('--output_dir', type=str, default=None,
                       help='输出目录 (默认: save_path/visualization)')
    parser.add_argument('--fps', type=int, default=20,
                       help='视频帧率 (默认: 20)')
    
    args = parser.parse_args()
    
    # 设置输出目录
    if args.output_dir is None:
        args.output_dir = os.path.join(args.save_path, "visualization")
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("=" * 60)
    print("可视化结果后处理")
    print("=" * 60)
    print(f"输入路径: {args.save_path}")
    print(f"输出目录: {args.output_dir}")
    print(f"帧率: {args.fps}")
    print("=" * 60)
    
    # 1. 生成BEV视角视频
    print("\n[1/3] 生成BEV视角视频...")
    bev_video = create_bev_video(args.save_path, args.output_dir)
    
    # 2. 生成RGB前视视角视频
    print("\n[2/3] 生成RGB前视视角视频...")
    rgb_video = create_rgb_front_video(args.save_path, args.output_dir)
    
    # 3. 生成OD感知结果JSON
    print("\n[3/3] 生成OD感知结果JSON...")
    output_json = os.path.join(args.output_dir, "od_results.json")
    generate_od_json(args.save_path, output_json)
    
    # 输出结果摘要
    print("\n" + "=" * 60)
    print("处理完成！")
    print("=" * 60)
    if bev_video:
        print(f"✓ BEV视角视频: {bev_video}")
    if rgb_video:
        print(f"✓ RGB前视视角视频: {rgb_video}")
    print(f"✓ OD感知结果JSON: {output_json}")
    print("=" * 60)


if __name__ == '__main__':
    main()
