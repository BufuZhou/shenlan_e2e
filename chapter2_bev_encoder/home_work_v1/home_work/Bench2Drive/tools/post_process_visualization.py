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
        try:
            with open(detections_file, 'r') as f:
                frame_detections = json.load(f)
            
            od_results["frames"] = frame_detections
            print(f"从 detections.json 加载了 {len(frame_detections)} 帧的检测结果")
        except json.JSONDecodeError as e:
            print(f"警告: detections.json 解析失败: {e}")
            print("将创建基础结构")
            frame_detections = []
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


def find_scenario_directories(save_path):
    """
    查找所有场景目录
    
    Args:
        save_path: 保存路径
    
    Returns:
        list: 场景目录列表
    """
    scenario_dirs = []
    
    # 检查是否有子目录
    for item in os.listdir(save_path):
        item_path = os.path.join(save_path, item)
        if os.path.isdir(item_path):
            # 检查是否包含 rgb_front 等子文件夹
            if os.path.exists(os.path.join(item_path, 'rgb_front')):
                scenario_dirs.append(item_path)
    
    # 如果没有找到子目录，使用 save_path 本身
    if not scenario_dirs:
        if os.path.exists(os.path.join(save_path, 'rgb_front')):
            scenario_dirs.append(save_path)
    
    return scenario_dirs


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
    
    # 查找所有场景目录
    scenario_dirs = find_scenario_directories(args.save_path)
    
    if not scenario_dirs:
        print(f"错误: 在 {args.save_path} 中未找到有效的场景目录")
        return
    
    print(f"找到 {len(scenario_dirs)} 个场景目录")
    
    # 处理每个场景
    for scenario_idx, scenario_dir in enumerate(scenario_dirs, 1):
        scenario_name = os.path.basename(scenario_dir)
        print(f"\n{'='*60}")
        print(f"处理场景 {scenario_idx}/{len(scenario_dirs)}: {scenario_name}")
        print(f"{'='*60}")
        
        # 为每个场景创建输出目录
        scenario_output_dir = os.path.join(args.output_dir, scenario_name)
        os.makedirs(scenario_output_dir, exist_ok=True)
        
        # 1. 生成BEV视角视频
        print("\n[1/4] 生成BEV俯视图视频...")
        bev_video = create_bev_video(scenario_dir, scenario_output_dir)
        
        # 1.5. 如果 BEV 文件夹为空，尝试合成 BEV 视频
        if not bev_video:
            print("  尝试从检测结果合成 BEV 视频...")
            try:
                from tools.generate_bev_video import generate_bev_video
                bev_video = generate_bev_video(scenario_dir, scenario_output_dir, fps=20)
            except Exception as e:
                print(f"  ⚠️ BEV 合成失败: {e}")
        
        # 2. 生成RGB前视视角视频
        print("\n[2/4] 生成RGB前视视角视频...")
        rgb_video = create_rgb_front_video(scenario_dir, scenario_output_dir)
        
        # 3. 生成OD感知结果JSON
        print("\n[3/4] 生成OD感知结果JSON...")
        output_json = os.path.join(scenario_output_dir, "od_results.json")
        generate_od_json(scenario_dir, output_json)
        
        # 4. 输出当前场景的结果摘要
        print(f"\n场景 {scenario_name} 处理完成：")
        if bev_video:
            print(f"  ✓ BEV俯视图视频: {bev_video}")
        else:
            print(f"  ⚠ BEV俯视图视频: 未生成（缺少数据）")
        if rgb_video:
            print(f"  ✓ RGB前视视角视频: {rgb_video}")
        print(f"  ✓ OD感知结果JSON: {output_json}")
    
    # 输出总体结果摘要
    print("\n" + "=" * 60)
    print("所有场景处理完成！")
    print("=" * 60)
    print(f"总共处理了 {len(scenario_dirs)} 个场景")
    print(f"输出目录: {args.output_dir}")
    print("=" * 60)


if __name__ == '__main__':
    main()
