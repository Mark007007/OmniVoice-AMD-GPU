#!/usr/bin/env python3
"""OmniVoice 性能对比测试 - AMD ROCm vs ONNX DirectML"""

import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HOME"] = "D:/OmniVoice/models"
os.environ["HUGGINGFACE_HUB_CACHE"] = "D:/OmniVoice/models"
os.environ["MIOPEN_FIND_MODE"] = "fast"
os.environ["MIOPEN_LOG_LEVEL"] = "6"

import time
import torch
import soundfile as sf

print("=" * 70)
print("OmniVoice 性能测试 - AMD ROCm (RX 9070 XT)")
print("=" * 70)

# GPU信息
print(f"\n[GPU] {torch.cuda.get_device_name(0)}")
print(f"      显存: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
print(f"      架构: {torch.cuda.get_device_properties(0).gcnArchName}")

# 加载模型
print(f"\n[加载模型]...")
from omnivoice import OmniVoice
model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cuda:0", dtype=torch.float16)

# 预热
print(f"[预热] 缓存MIOpen算法...")
_ = model.generate(text="预热", num_step=8)
torch.cuda.synchronize()

print(f"\n" + "=" * 70)
print("RTF 性能测试 (预热后)")
print("=" * 70)

test_cases = [
    ("短文本(32步)", "你好，欢迎使用OmniVoice。", None, 32),
    ("短文本(16步)", "你好，欢迎使用OmniVoice。", None, 16),
    ("中等文本(32步)", "OmniVoice是一个支持六百多种语言的零样本文本转语音模型，采用扩散语言模型架构。", "female, low pitch", 32),
    ("长文本(32步)", "OmniVoice是一个支持六百多种语言的零样本文本转语音模型。它采用扩散语言模型架构，能够生成高质量的语音，并支持声音克隆和声音设计功能。该模型具有出色的推理速度，实时因子可低至零点零二五。", None, 32),
]

results = []
for name, text, instruct, num_step in test_cases:
    torch.cuda.synchronize()
    torch.cuda.empty_cache()
    
    start = time.perf_counter()
    if instruct:
        audio = model.generate(text=text, instruct=instruct, num_step=num_step)
    else:
        audio = model.generate(text=text, num_step=num_step)
    torch.cuda.synchronize()
    
    elapsed = time.perf_counter() - start
    duration = len(audio[0]) / 24000
    rtf = elapsed / duration
    results.append((name, elapsed, duration, rtf, num_step))
    
    print(f"\n  {name}")
    print(f"    推理: {elapsed:.3f}秒 | 音频: {duration:.2f}秒 | RTF: {rtf:.3f} ({1/rtf:.1f}x实时)")

print(f"\n" + "=" * 70)
print("性能汇总")
print("=" * 70)
print(f"\n  {'测试':<18} {'推理时间':<12} {'音频时长':<12} {'RTF':<10} {'实时倍速':<10}")
print("  " + "-" * 62)
for name, t, d, rtf, steps in results:
    print(f"  {name:<18} {t:>8.3f}秒   {d:>8.2f}秒   {rtf:>8.3f}   {1/rtf:>6.1f}x")

avg_rtf = sum(r[3] for r in results) / len(results)
print("  " + "-" * 62)
print(f"  {'平均':<18} {'':<12} {'':<12} {avg_rtf:>8.3f}   {1/avg_rtf:>6.1f}x")

print(f"\n" + "=" * 70)
print("与 ONNX + DirectML 方案对比")
print("=" * 70)
print(f"""
  方案                    RTF范围      实时倍速
  ─────────────────────────────────────────────
  ONNX + DirectML         0.4-0.6      1.7-2.5x
  ROCm PyTorch (本机)     {min(r[3] for r in results):.2f}-{max(r[3] for r in results):.2f}      {1/max(r[3] for r in results):.1f}-{1/min(r[3] for r in results):.1f}x
  
  ✓ ROCm版本比ONNX快约 {0.5/avg_rtf:.0f} 倍！
""")
