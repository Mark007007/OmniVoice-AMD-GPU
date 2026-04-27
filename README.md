# OmniVoice AMD GPU Edition

OmniVoice TTS模型的AMD GPU支持版本，支持ROCm加速。

## 特性

- 支持600+语言的零样本文本转语音
- AMD GPU加速 (ROCm 7.2+)
- 声音克隆和声音设计
- RTF低至0.06 (16x实时)

## 系统要求

- **Python 3.12.x** (一键脚本会自动安装)
- AMD GPU (RX 7000系列 / GFX1100架构推荐)
- Windows 10/11 或 Linux
- 文件说明
- ├── omnivoice_amd-0.1.4-py3-none-any.whl  (160KB)
- ├── install.bat                            (一键安装，自动检查Python版本)
- ├── run.bat                  （快速启动）
- ├── launcher.py 启动器（含自动检测）
- ├── INSTALL_GUIDE.md                       (详细安装指南)
- ├── README.md                              (使用说明)
- ├── verify_install.py                      (安装验证)
- └── benchmark_rtf.py                       (性能测试)

## 安装

### 一键安装 (推荐)

双击运行 `install.bat`，脚本会自动：

1. 检测Python 3.12，如未安装则自动下载安装
2. 安装AMD ROCm PyTorch
3. 安装OmniVoice AMD版
4. 验证GPU是否可用

```bash
# 直接双击运行，或命令行执行：
install.bat
```

### 手动安装

如果一键脚本无法正常工作，可手动执行：

```bash
# 1. 安装Python 3.12 (如未安装)
# 下载: https://www.python.org/ftp/python/3.12.9/python-3.12.9-amd64.exe

# 2. 确认Python版本
py -3.12 --version
# 应显示: Python 3.12.x

# 3. 安装AMD ROCm PyTorch
py -3.12 -m pip install --upgrade https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/rocm_sdk_core-7.2.1-py3-none-win_amd64.whl https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/rocm_sdk_libraries_custom-7.2.1-py3-none-win_amd64.whl https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/rocm-7.2.1.tar.gz https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/torch-2.9.1%2Brocm7.2.1-cp312-cp312-win_amd64.whl https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/torchaudio-2.9.1%2Brocm7.2.1-cp312-cp312-win_amd64.whl https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/torchvision-0.24.1%2Brocm7.2.1-cp312-cp312-win_amd64.whl

# 4. 安装OmniVoice AMD版
py -3.12 -m pip install omnivoice_amd-0.1.4-py3-none-any.whl
```

## 快速开始

```python
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"  # 国内镜像
os.environ["HF_HOME"] = "./models"  # 模型缓存路径

from omnivoice import OmniVoice
import torch

# 加载模型
model = OmniVoice.from_pretrained(
    "k2-fsa/OmniVoice",
    device_map="cuda:0",
    dtype=torch.float16
)

# Voice Design模式
audio = model.generate(
    text="你好，欢迎使用OmniVoice。",
    instruct="female, low pitch",
    num_step=32
)

# 保存音频
import soundfile as sf
sf.write("output.wav", audio[0], 24000)
```

## 性能

| GPU | RTF | 实时倍速 |
|-----|-----|----------|
| AMD RX 9070 XT | 0.06-0.28 | 3.6-16.7x |

## 环境变量

```bash
# HuggingFace镜像 (国内用户)
export HF_ENDPOINT="https://hf-mirror.com"

# 模型缓存路径
export HF_HOME="/path/to/models"

# MIOpen优化
export MIOPEN_FIND_MODE="fast"
export MIOPEN_LOG_LEVEL="6"
```

## 命令行工具

```bash
# 启动Web UI
omnivoice-demo --ip 0.0.0.0 --port 8001

# 单条推理
omnivoice-infer --model k2-fsa/OmniVoice --text "你好世界" --output hello.wav

# 批量推理
omnivoice-infer-batch --model k2-fsa/OmniVoice --test_list test.jsonl --res_dir results/
```

## 支持的Voice Design属性

**英文**: `female`, `male`, `child`, `elderly`, `young adult`, `low pitch`, `high pitch`, `british accent`, `american accent`, `whisper`...

**中文**: `女`, `男`, `儿童`, `老年`, `青年`, `低音调`, `高音调`, `四川话`, `东北话`, `耳语`...

## 情感标签

支持在文本中插入情感标签:
- `[laughter]` - 笑声
- `[sigh]` - 叹气
- `[surprise-wa]` - 惊讶
- `[question-ah]` - 疑问语气

## 致谢

- 原始项目: [k2-fsa/OmniVoice](https://github.com/k2-fsa/OmniVoice)
- AMD GPU支持: PR #92 by Alexander-Ger-Reich（https://github.com/k2-fsa/OmniVoice/pull/92）

## License

Apache-2.0
