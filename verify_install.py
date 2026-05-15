#!/usr/bin/env python3
"""
OmniVoice AMD GPU Edition - 快速测试脚本
验证安装是否成功并测试GPU性能
"""

import os
import pathlib

# Setup model directory with cross-platform support
model_dir = pathlib.Path.home() / "OmniVoice_models"
model_dir.mkdir(parents=True, exist_ok=True)

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HOME"] = str(model_dir)
os.environ["MIOPEN_FIND_MODE"] = "fast"
os.environ["MIOPEN_LOG_LEVEL"] = "6"

import time
import torch

print("=" * 60)
print("OmniVoice AMD GPU Edition - 安装验证")
print("=" * 60)

# 检查GPU
print(f"\n[GPU信息]")
print(f"  PyTorch版本: {torch.__version__}")
print(f"  CUDA可用: {torch.cuda.is_available()}")

if not torch.cuda.is_available():
    print("\n[错误] 未检测到GPU，请检查ROCm安装")
    exit(1)

print(f"  设备名称: {torch.cuda.get_device_name(0)}")
print(f"  显存: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")

# 加载模型
print(f"\n[加载模型]")
from omnivoice import OmniVoice

model = OmniVoice.from_pretrained(
    "k2-fsa/OmniVoice",
    device_map="cuda:0",
    dtype=torch.float16
)
print("  模型加载成功")

# 预热
print(f"\n[预热模型]")
_ = model.generate(text="预热测试", num_step=8)
torch.cuda.synchronize()
print("  预热完成")

# 测试推理
print(f"\n[性能测试]")
torch.cuda.synchronize()
start = time.perf_counter()

audio = model.generate(
    text="你好，这是OmniVoice AMD GPU版本的测试。",
    instruct="female, low pitch",
    num_step=32
)

torch.cuda.synchronize()
elapsed = time.perf_counter() - start
duration = len(audio[0]) / 24000
rtf = elapsed / duration

print(f"  推理时间: {elapsed:.3f}秒")
print(f"  音频时长: {duration:.2f}秒")
print(f"  RTF: {rtf:.3f} ({1/rtf:.1f}x实时)")

# 保存音频
import soundfile as sf
sf.write("test_output.wav", audio[0], 24000)
print(f"  输出文件: test_output.wav")

print(f"\n" + "=" * 60)
print("验证完成！OmniVoice AMD GPU版本工作正常")
print("=" * 60)
print(f"\n[Info] 模型缓存目录: {model_dir}")
