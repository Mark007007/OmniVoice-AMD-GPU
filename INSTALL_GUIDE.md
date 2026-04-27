# OmniVoice AMD GPU Edition - 详细安装指南

## 目录

1. [系统要求](#1-系统要求)
2. [安装步骤](#2-安装步骤)
3. [环境配置](#3-环境配置)
4. [验证安装](#4-验证安装)
5. [快速开始](#5-快速开始)
6. [常见问题](#6-常见问题)

---

# 1. 系统要求

# 硬件要求

| 项目 | 最低要求 | 推荐配置 |
|------|----------|----------|
| GPU | AMD RX 6000系列 | AMD RX 7000/9000系列 |
| 显存 | 8 GB | 16 GB |
| 内存 | 16 GB | 32 GB |
| 存储 | 10 GB | 20 GB (含模型缓存) |

#软件要求

| 软件 | 版本要求 | 说明 |
|------|----------|------|
| 操作系统 | Windows 10/11 64位 | Linux也支持 |
| **Python** | **3.12.x** | ⚠️ ROCm 7.2.1 仅支持 Python 3.12 |
| AMD驱动 | 最新版 Adrenalin | 建议使用最新版 |

# 支持的AMD GPU架构

- **GFX1100** - RX 7900 XT, RX 7900 XTX
- **GFX1101** - RX 7900 GRE
- **GFX1102** - RX 7800 XT, RX 7700 XT
- **GFX1200** - RX 9070, RX 9070 XT
- **GFX1201** - RX 9070 XT (本测试机型)

---

# 2. 安装步骤

### 步骤 1: 检查Python版本

打开命令提示符(CMD)或PowerShell：

```cmd
python --version
```

确保显示 `Python 3.12.x`

如果未安装Python，从 [python.org](https://www.python.org/downloads/) 下载安装。

### 步骤 2: 创建虚拟环境 (推荐)

```cmd
# 创建虚拟环境
python -m venv D:\omnivoice_env

# 激活虚拟环境
D:\omnivoice_env\Scripts\activate

# 升级pip
python -m pip install --upgrade pip
```

### 步骤 3: 安装 AMD ROCm PyTorch

**重要**: 
- 必须先安装ROCm版PyTorch，再安装OmniVoice
- **ROCm 7.2.1 仅支持 Python 3.12**，其他版本无法安装

#### 安装命令

```cmd
pip install --upgrade ^
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/rocm_sdk_core-7.2.1-py3-none-win_amd64.whl ^
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/rocm_sdk_libraries_custom-7.2.1-py3-none-win_amd64.whl ^
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/rocm-7.2.1.tar.gz ^
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/torch-2.9.1%2Brocm7.2.1-cp312-cp312-win_amd64.whl ^
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/torchaudio-2.9.1%2Brocm7.2.1-cp312-cp312-win_amd64.whl ^
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/torchvision-0.24.1%2Brocm7.2.1-cp312-cp312-win_amd64.whl
```

> ⚠️ 注意: URL中的 `cp312` 表示 Python 3.12，ROCm 7.2.1 目前只提供此版本。

#### 验证PyTorch安装

```cmd
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0)}')"
```

预期输出：
```
PyTorch: 2.9.1+rocm7.2.1
CUDA: True
GPU: AMD Radeon RX xxxx```

### 步骤 4: 安装 OmniVoice AMD 版

```cmd
pip install omnivoice_amd-0.1.4-py3-none-any.whl
```

或从源码安装：

```cmd
git clone https://github.com/k2-fsa/OmniVoice.git
cd OmniVoice
pip install -e .
```

---

## 3. 环境配置

### 3.1 必需的环境变量

创建一个启动脚本 `setup_env.bat`：

```batch
@echo off
REM HuggingFace镜像 (国内用户必需)
set HF_ENDPOINT=https://hf-mirror.com

REM 模型缓存路径 (避免下载到C盘)
set HF_HOME=D:\OmniVoice\models
set HUGGINGFACE_HUB_CACHE=D:\OmniVoice\models

REM MIOpen优化设置
set MIOPEN_FIND_MODE=fast
set MIOPEN_LOG_LEVEL=6

REM 可选: MIOpen缓存路径
set MIOPEN_USER_DB_PATH=D:\OmniVoice\miopen_cache

echo 环境变量已设置
```

### 3.2 PowerShell 环境变量

```powershell
$env:HF_ENDPOINT = "https://hf-mirror.com"
$env:HF_HOME = "D:\OmniVoice\models"
$env:MIOPEN_FIND_MODE = "fast"
$env:MIOPEN_LOG_LEVEL = "6"
```

### 3.3 Linux/Mac 环境变量

```bash
export HF_ENDPOINT="https://hf-mirror.com"
export HF_HOME="/path/to/models"
export MIOPEN_FIND_MODE="fast"
export MIOPEN_LOG_LEVEL="6"
```

---

## 4. 验证安装

### 4.1 快速验证

```cmd
python -c "from omnivoice import OmniVoice; print('OmniVoice安装成功')"
```

### 4.2 完整验证脚本

创建 `verify.py`：

```python
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HOME"] = "./models"
os.environ["MIOPEN_LOG_LEVEL"] = "6"

import torch
print(f"PyTorch: {torch.__version__}")
print(f"GPU: {torch.cuda.get_device_name(0)}")

from omnivoice import OmniVoice
model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cuda:0", dtype=torch.float16)

# 预热
_ = model.generate(text="测试", num_step=8)

# 正式推理
import time
import soundfile as sf

start = time.perf_counter()
audio = model.generate(text="验证安装成功", num_step=32)
elapsed = time.perf_counter() - start

print(f"RTF: {elapsed / (len(audio[0])/24000):.3f}")
sf.write("verify_output.wav", audio[0], 24000)
print("音频已保存: verify_output.wav")
```

运行验证：

```cmd
python verify.py
```

---

## 5. 快速开始

### 5.1 Python API

```python
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HOME"] = "./models"

from omnivoice import OmniVoice
import torch
import soundfile as sf

# 加载模型
model = OmniVoice.from_pretrained(
    "k2-fsa/OmniVoice",
    device_map="cuda:0",
    dtype=torch.float16
)

# Voice Design - 设计声音
audio = model.generate(
    text="你好，欢迎使用OmniVoice语音合成系统。",
    instruct="female, low pitch",  # 女声，低音调
    num_step=32
)
sf.write("output.wav", audio[0], 24000)

# Voice Cloning - 声音克隆
audio = model.generate(
    text="这是克隆的声音。",
    ref_audio="reference.wav",     # 参考音频
    ref_text="参考音频的文字内容",  # 可选，不填会自动识别
    num_step=32
)
sf.write("cloned.wav", audio[0], 24000)

# Auto Voice - 自动声音
audio = model.generate(
    text="This is auto generated voice.",
    num_step=32
)
sf.write("auto.wav", audio[0], 24000)
```

### 5.2 命令行工具

```cmd
# 启动Web UI
omnivoice-demo --ip 0.0.0.0 --port 8001

# 单条推理
omnivoice-infer --model k2-fsa/OmniVoice --text "你好世界" --output hello.wav

# Voice Design
omnivoice-infer --model k2-fsa/OmniVoice --text "你好" --instruct "female, low pitch" --output output.wav

# Voice Cloning
omnivoice-infer --model k2-fsa/OmniVoice --text "克隆文本" --ref_audio ref.wav --ref_text "参考文本" --output cloned.wav
```

### 5.3 支持的Voice Design属性

**英文属性** (用逗号分隔):
- 性别: `female`, `male`
- 年龄: `child`, `teenager`, `young adult`, `middle-aged`, `elderly`
- 音调: `very low pitch`, `low pitch`, `moderate pitch`, `high pitch`, `very high pitch`
- 口音: `american accent`, `british accent`, `australian accent`, `chinese accent`
- 风格: `whisper`

**中文属性** (用全角逗号分隔):
- 性别: `女`, `男`
- 年龄: `儿童`, `少年`, `青年`, `中年`, `老年`
- 音调: `极低音调`, `低音调`, `中音调`, `高音调`, `极高音调`
- 方言: `四川话`, `东北话`, `河南话`, `陕西话`
- 风格: `耳语`

### 5.4 情感标签

在文本中插入情感标签：

```python
text = "[laughter] 今天真开心！[sigh] 可是明天要上班。"
```

支持的标签:
- `[laughter]` - 笑声
- `[sigh]` - 叹气
- `[surprise-ah]`, `[surprise-oh]`, `[surprise-wa]` - 惊讶
- `[question-ah]`, `[question-oh]` - 疑问
- `[dissatisfaction-hnn]` - 不满

---

## 6. 常见问题

### Q1: HuggingFace连接超时

**原因**: 国内访问HuggingFace受限

**解决**: 设置镜像
```cmd
set HF_ENDPOINT=https://hf-mirror.com
```

### Q2: 模型下载到C盘

**原因**: 默认缓存路径在用户目录

**解决**: 设置缓存路径
```cmd
set HF_HOME=D:\OmniVoice\models
```

### Q3: MIOpen警告信息

**现象**: 大量 `MIOpen(HIP): Warning` 输出

**解决**: 设置日志级别
```cmd
set MIOPEN_LOG_LEVEL=6
```

或在Python中：
```python
os.environ["MIOPEN_LOG_LEVEL"] = "6"
```

### Q4: 第一次推理很慢

**原因**: MIOpen需要编译卷积算法并缓存

**解决**: 这是正常现象，预热后速度会大幅提升

```python
# 预热模型
_ = model.generate(text="预热", num_step=8)
```

### Q5: CUDA not available

**检查步骤**:

1. 确认AMD驱动已安装
```cmd
# 查看驱动版本
dxdiag
```

2. 确认安装的是ROCm版PyTorch
```cmd
python -c "import torch; print(torch.__version__)"
# 应显示: 2.9.1+rocm7.2.1
```

3. 如果显示CUDA版本，说明安装了错误的PyTorch
```cmd
# 卸载错误版本
pip uninstall torch torchvision torchaudio -y

# 重新安装ROCm版本
pip install --upgrade https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/torch-2.9.1%2Brocm7.2.1-cp312-cp312-win_amd64.whl
```

### Q6: RTF性能不佳

**检查项**:

1. 确认使用GPU
```python
model = OmniVoice.from_pretrained(..., device_map="cuda:0")
```

2. 使用float16
```python
model = OmniVoice.from_pretrained(..., dtype=torch.float16)
```

3. 预热模型后再测试

4. 减少扩散步数
```python
audio = model.generate(..., num_step=16)  # 更快但质量略降
```

### Q7: 显存不足

**解决**:
1. 使用更小的数据类型
2. 减少batch size
3. 清理显存
```python
import torch
torch.cuda.empty_cache()
```

---

## 性能参考

| GPU | RTF (32步) | RTF (16步) | 实时倍速 |
|-----|------------|------------|----------|
| RX 9070 XT | 0.06-0.28 | 0.06-0.12 | 3.6-16.7x |
| RX 7900 XTX | ~0.08 | ~0.05 | ~12-20x |

---

## 技术支持

- 原始项目: https://github.com/k2-fsa/OmniVoice
- AMD GPU支持: PR #92
- 问题反馈: GitHub Issues

---

## 更新日志

**v0.1.4 (2026-04-27)**
- 添加AMD ROCm支持
- 优化MIOpen配置
- 添加一键安装脚本
