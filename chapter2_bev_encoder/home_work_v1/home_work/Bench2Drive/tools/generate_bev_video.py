#!/usr/bin/env python3
"""
生成 BEV 俯视图视频
基于检测框、自车位置和轨迹数据合成鸟瞰图
"""

import os
import json
import cv2
import numpy as np
import argparse
from pathlib import Path


def load_detections(scenario_dir):
    """加载检测结果"""
    detections_file = os.path.join(scenario_dir, "detections.json")
    if os.path.exists(detections_file):
        with open(detections_file, 'r') as f:
            return json.load(f)
    return []


def load_meta_frames(scenario_dir):
    """加载元数据帧"""
    meta_dir = os.path.join(scenario_dir, "meta")
    if not os.path.exists(meta_dir):
        return []
    
    meta_files = sorted([f for f in os.listdir(meta_dir) if f.endswith('.json')])
    meta_frames = []
    
    for meta_file in meta_files:
        meta_path = os.path.join(meta_dir, meta_file)
        with open(meta_path, 'r') as f:
            meta_data = json.load(f)
            meta_frames.append(meta_data)
    
    return meta_frames


def create_bev_frame(frame_idx, detections, meta_data, canvas_size=512, scale=4.0):
    """
    创建单帧 BEV 图像
    
    Args:
        frame_idx: 帧索引
        detections: 当前帧的检测框
        meta_data: 当前帧的元数据（包含自车位置）
        canvas_size: 画布大小
        scale: 像素/米 比例
    
    Returns:
        BEV 图像 (numpy array)
    """
    # 创建空白画布（深色背景）
    bev_img = np.zeros((canvas_size, canvas_size, 3), dtype=np.uint8)
    bev_img[:] = (40, 40, 50)  # 深蓝灰色背景，稍微亮一点
    
    center_x, center_y = canvas_size // 2, canvas_size // 2
    
    # 绘制网格线
    grid_spacing = int(10 * scale)  # 每 10 米一条网格线
    for i in range(0, canvas_size, grid_spacing):
        cv2.line(bev_img, (i, 0), (i, canvas_size), (70, 70, 80), 1)
        cv2.line(bev_img, (0, i), (canvas_size, i), (70, 70, 80), 1)
    
    # 绘制自车位置（中心点）
    cv2.circle(bev_img, (center_x, center_y), 8, (0, 255, 0), -1)  # 绿色圆点
    cv2.drawMarker(bev_img, (center_x, center_y), (0, 255, 0), cv2.MARKER_CROSS, 20, 2)
    
    # 如果有自车朝向信息，绘制方向箭头
    if meta_data and 'forward_vector' in meta_data:
        forward = meta_data['forward_vector']
        arrow_length = 30
        end_x = int(center_x + forward[0] * arrow_length)
        end_y = int(center_y - forward[1] * arrow_length)  # Y轴翻转
        cv2.arrowedLine(bev_img, (center_x, center_y), (end_x, end_y), (0, 255, 0), 2)
    
    # 绘制检测框
    det_count = 0
    if detections and 'detections' in detections:
        for det in detections['detections']:
            bbox_3d = det['bbox_3d']
            center = bbox_3d['center']
            size = bbox_3d['size']
            rotation = bbox_3d['rotation']
            score = det.get('score', 0)
            
            # 过滤低置信度检测框
            if score < 0.1:
                continue
            
            # 转换到 BEV 坐标系（相对于自车）
            # X: 前后方向，Y: 左右方向
            rel_x = center[0]  # 前后
            rel_y = -center[1]  # 左右（翻转）
            
            # 转换到像素坐标
            pixel_x = int(center_x + rel_x * scale)
            pixel_y = int(center_y + rel_y * scale)
            
            # 检查是否在画布范围内
            if 0 <= pixel_x < canvas_size and 0 <= pixel_y < canvas_size:
                det_count += 1
                # 根据类别选择颜色
                label = det.get('label', 0)
                class_name = det.get('class_name', 'unknown')
                score = det.get('score', 0)
                
                # 过滤低置信度检测框
                if score < 0.1:
                    continue
                
                # 颜色映射（支持多种类别名称）
                color_map = {
                    'vehicle': (255, 200, 0),      # 黄色
                    'car': (255, 200, 0),          # 黄色 - 车辆
                    'truck': (255, 200, 0),        # 黄色 - 卡车
                    'bus': (255, 200, 0),          # 黄色 - 公交车
                    'pedestrian': (0, 165, 255),   # 橙色
                    'person': (0, 165, 255),       # 橙色 - 行人
                    'cyclist': (255, 0, 255),      # 紫色
                    'bicycle': (255, 0, 255),      # 紫色 - 自行车
                    'motorcycle': (255, 0, 255),   # 紫色 - 摩托车
                    'traffic_cone': (128, 128, 128), # 灰色
                    'unknown': (255, 255, 255),    # 白色 - 未知
                }
                color = color_map.get(class_name, (255, 255, 255))
                
                # 绘制矩形框（简化为 2D）
                width_px = int(size[0] * scale)
                length_px = int(size[1] * scale)
                
                # 考虑旋转
                cos_r = np.cos(rotation)
                sin_r = np.sin(rotation)
                
                # 计算四个角点
                corners = [
                    (-length_px/2, -width_px/2),
                    (length_px/2, -width_px/2),
                    (length_px/2, width_px/2),
                    (-length_px/2, width_px/2),
                ]
                
                rotated_corners = []
                for cx, cy in corners:
                    rx = cx * cos_r - cy * sin_r + pixel_x
                    ry = cx * sin_r + cy * cos_r + pixel_y
                    rotated_corners.append((int(rx), int(ry)))
                
                # 绘制旋转矩形
                pts = np.array(rotated_corners, np.int32)
                cv2.polylines(bev_img, [pts], True, color, 2)
                
                # 填充半透明（增强可见性）
                overlay = bev_img.copy()
                cv2.fillPoly(overlay, [pts], color)
                cv2.addWeighted(overlay, 0.5, bev_img, 0.5, 0, bev_img)
    
    # 添加文字信息
    cv2.putText(bev_img, f"Frame: {frame_idx}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(bev_img, f"Detections: {det_count}", (10, 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # 添加比例尺
    scale_bar_length = int(10 * scale)  # 10米
    cv2.rectangle(bev_img, (10, canvas_size-40), (10+scale_bar_length, canvas_size-30), (255, 255, 255), -1)
    cv2.putText(bev_img, "10m", (10, canvas_size-20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    return bev_img


def generate_bev_video(scenario_dir, output_dir, fps=20, canvas_size=512, scale=4.0):
    """
    生成 BEV 视频
    
    Args:
        scenario_dir: 场景目录
        output_dir: 输出目录
        fps: 帧率
        canvas_size: 画布大小
        scale: 像素/米 比例
    """
    print(f"\n生成 BEV 视频...")
    print(f"  场景目录: {scenario_dir}")
    print(f"  输出目录: {output_dir}")
    
    # 加载数据
    detections = load_detections(scenario_dir)
    meta_frames = load_meta_frames(scenario_dir)
    
    if not detections:
        print("  ⚠️ 警告: 未找到检测结果")
        return None
    
    num_frames = len(detections)
    print(f"  总帧数: {num_frames}")
    
    # 创建视频写入器
    output_video = os.path.join(output_dir, "bev_synthesized_video.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video, fourcc, fps, (canvas_size, canvas_size))
    
    # 逐帧生成 BEV 图像
    for frame_idx in range(num_frames):
        # 获取当前帧数据
        frame_det = detections[frame_idx] if frame_idx < len(detections) else {}
        frame_meta = meta_frames[frame_idx] if frame_idx < len(meta_frames) else {}
        
        # 创建 BEV 帧
        bev_frame = create_bev_frame(frame_idx, frame_det, frame_meta, canvas_size, scale)
        
        # 写入视频
        video_writer.write(bev_frame)
        
        # 进度显示
        if (frame_idx + 1) % 50 == 0:
            print(f"  处理进度: {frame_idx + 1}/{num_frames}")
    
    video_writer.release()
    print(f"  ✓ BEV 视频已保存: {output_video}")
    
    return output_video


def main():
    parser = argparse.ArgumentParser(description='生成 BEV 俯视图视频')
    parser.add_argument('--scenario_dir', type=str, required=True,
                       help='场景目录路径')
    parser.add_argument('--output_dir', type=str, default=None,
                       help='输出目录 (默认: scenario_dir/../visualization)')
    parser.add_argument('--fps', type=int, default=20,
                       help='视频帧率 (默认: 20)')
    parser.add_argument('--canvas_size', type=int, default=512,
                       help='画布大小 (默认: 512)')
    parser.add_argument('--scale', type=float, default=4.0,
                       help='像素/米 比例 (默认: 4.0)')
    
    args = parser.parse_args()
    
    # 设置输出目录
    if args.output_dir is None:
        args.output_dir = os.path.join(os.path.dirname(args.scenario_dir), "visualization", 
                                       os.path.basename(args.scenario_dir))
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    print("=" * 60)
    print("BEV 俯视图视频生成")
    print("=" * 60)
    
    # 生成视频
    output_video = generate_bev_video(
        args.scenario_dir, 
        args.output_dir,
        args.fps,
        args.canvas_size,
        args.scale
    )
    
    print("\n" + "=" * 60)
    if output_video:
        print(f"✓ 完成！BEV 视频: {output_video}")
    else:
        print("✗ 失败：无法生成 BEV 视频")
    print("=" * 60)


if __name__ == '__main__':
    main()
