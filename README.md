# OmniVoice AMD GPU Edition

OmniVoice TTS模型的AMD GPU支持版本，支持ROCm加速。

**最新版本**: v0.1.5 (2026-05-15) - 包含性能优化和跨平台改进

## ✨ 核心特性

- ✅ **600+语言支持** - 零样本文本转语音，覆盖全球语言
- 🚀 **AMD GPU加速** - ROCm 7.2.1，性能提升10-16倍
- 🎤 **声音克隆** - 从参考音频学习声音特征
- 🎨 **声音设计** - 灵活控制性别、音调、口音等
- ⚡ **超高性能** - RTF低至0.06 (16x实时速度)
- 🌍 **跨平台支持** - Windows / Linux / macOS

## 📋 系统要求

| 项目 | 最低要求 | 推荐配置 |
|------|----------|----------|
| **GPU** | AMD RX 6000+ | RX 7900/9070 系列 |
| **显存** | 8 GB | 16 GB+ |
| **内存** | 16 GB | 32 GB+ |
| **Python** | **3.12.x** ⚠️ | Python 3.12 only |
| **OS** | Windows 10/11 (64-bit) | Windows/Linux/macOS |

## 📁 文件说明

```
OmniVoice-AMD-GPU/
├── install.bat                          一键安装脚本 (Windows)
├── run.bat                              快速启动脚本 (Windows)
├── launcher.py                          跨平台启动器 (自动检测配置)
├── omnivoice_amd-0.1.4-py3-none-any.whl Python轮子包 (~160KB)
├── INSTALL_GUIDE.md                     详细安装指南 (中文)
├── README.md                            本文件
├── verify_install.py                    安装验证脚本
├── benchmark_rtf.py                     性能基准测试
└── LICENSE                              Apache 2.0 许可证
```

## ⚡ 快速安装

### 方案 1: 一键安装 (推荐) ⭐

**Windows:**
```bash
# 双击运行 install.bat 或在命令行执行：
install.bat
```

**Linux/macOS:**
```bash
python launcher.py
```

脚本会自动：
1. ✅ 检测 Python 3.12 (缺失则自动下载安装)
2. ✅ 安装 AMD ROCm PyTorch (~2GB)
3. ✅ 安装 OmniVoice AMD 版
4. ✅ 设置环境变量 (HF_HOME, HF_ENDPOINT等)
5. ✅ 验证 GPU 可用性

### 方案 2: 手动安装

```bash
# 1. 确认 Python 3.12
python --version
# 应显示: Python 3.12.x

# 2. 创建虚拟环境 (推荐)
python -m venv omnivoice_env
source omnivoice_env/bin/activate  # Linux/macOS
# 或
omnivoice_env\Scripts\activate  # Windows

# 3. 安装 AMD ROCm PyTorch
pip install --upgrade \
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/rocm_sdk_core-7.2.1-py3-none-win_amd64.whl \
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/rocm_sdk_libraries_custom-7.2.1-py3-none-win_amd64.whl \
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/rocm-7.2.1.tar.gz \
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/torch-2.9.1%2Brocm7.2.1-cp312-cp312-win_amd64.whl \
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/torchaudio-2.9.1%2Brocm7.2.1-cp312-cp312-win_amd64.whl \
    https://repo.radeon.com/rocm/windows/rocm-rel-7.2.1/torchvision-0.24.1%2Brocm7.2.1-cp312-cp312-win_amd64.whl

# 4. 安装 OmniVoice
pip install omnivoice_amd-0.1.4-py3-none-any.whl
```

## 🚀 快速开始

### Python API 使用

```python
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"  # 国内镜像
os.environ["HF_HOME"] = "./models"  # 自动适配用户目录

from omnivoice import OmniVoice
import torch
import soundfile as sf

# 加载模型 (首次会自动下载 ~800MB)
model = OmniVoice.from_pretrained(
    "k2-fsa/OmniVoice",
    device_map="cuda:0",
    dtype=torch.float16  # 使用 float16 节省显存
)

# 模式 1: Voice Design (控制声音特征)
audio = model.generate(
    text="你好，欢迎使用OmniVoice。",
    instruct="female, low pitch",  # 女性低音
    num_step=32
)
sf.write("design.wav", audio[0], 24000)

# 模式 2: Voice Cloning (克隆声音)
audio = model.generate(
    text="这是克隆的声音。",
    ref_audio="reference.wav",  # 参考音频
    ref_text="参考文本(可选)",
    num_step=32
)
sf.write("cloned.wav", audio[0], 24000)

# 模式 3: 自动声音生成
audio = model.generate(
    text="Auto generated voice.",
    num_step=16  # 更少步数 = 更快 (质量略降)
)
sf.write("auto.wav", audio[0], 24000)
```

### 命令行工具

```bash
# 启动 Web UI (推荐)
python launcher.py
# 或
omnivoice-demo --ip 0.0.0.0 --port 8001

# 单条推理
omnivoice-infer --model k2-fsa/OmniVoice --text "你好世界" --output hello.wav

# 带声音设计
omnivoice-infer --model k2-fsa/OmniVoice --text "测试文本" \
    --instruct "female, low pitch" --output output.wav
```

## ⚡ 性能对比

| GPU 型号 | RTF (32步) | RTF (16步) | 实时倍速 | 备注 |
|---------|-----------|-----------|---------|------|
| **RX 9070 XT** | 0.06-0.28 | 0.06-0.12 | **3.6-16.7x** | 测试机型 |
| **RX 7900 XTX** | ~0.08 | ~0.05 | 12-20x | 已验证 |
| **ONNX + DirectML** | 0.4-0.6 | N/A | 1.7-2.5x | 参考方案 |

> **RTF = 推理时间 / 音频时长** (< 1.0 = 实时)

## 🔧 环境变量配置

### 必需环境变量

```bash
# HuggingFace 镜像 (国内用户必需)
export HF_ENDPOINT="https://hf-mirror.com"

# 模型缓存目录 (自动创建，自动适配用户目录)
# Windows: %USERPROFILE%\OmniVoice_models
# Linux/macOS: ~/OmniVoice_models
export HF_HOME="~/OmniVoice_models"

# MIOpen 优化
export MIOPEN_FIND_MODE="fast"          # 快速卷积算法搜索
export MIOPEN_LOG_LEVEL="6"             # 禁用 MIOpen 警告日志
```

## 🎨 支持的 Voice Design 属性

**英文属性** (逗号分隔):
- 性别: `female`, `male`
- 年龄: `child`, `teenager`, `young adult`, `middle-aged`, `elderly`
- 音调: `very low pitch`, `low pitch`, `moderate pitch`, `high pitch`, `very high pitch`
- 口音: `american accent`, `british accent`, `australian accent`, `chinese accent`
- 风格: `whisper`

**中文属性** (全角逗号分隔):
- 性别: `女`, `男`
- 年龄: `儿童`, `少年`, `青年`, `中年`, `老年`
- 音调: `极低音调`, `低音调`, `中音调`, `高音调`, `极高音调`
- 方言: `四川话`, `东北话`, `河南话`, `陕西话`, `粤语`
- 风格: `耳语`

## 😊 情感标签

在文本中插入特殊标签实现情感表达:

```python
text = "[laughter] 太有趣了！[sigh] 但还有很多工作要做。"

audio = model.generate(
    text=text,
    num_step=32
)
```

支持的标签:
- `[laughter]` - 笑声
- `[sigh]` - 叹气声
- `[surprise-ah]`, `[surprise-oh]`, `[surprise-wa]` - 惊讶
- `[question-ah]`, `[question-oh]` - 疑问语气
- `[dissatisfaction-hnn]` - 不满

## 🐛 常见问题排查

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| **CUDA not available** | 安装了错误版本的 PyTorch | 卸载所有torch包，重新安装ROCm版本 |
| **HuggingFace 超时** | 网络限制 | 设置 `HF_ENDPOINT=https://hf-mirror.com` |
| **模型下载到 C 盘** | 缓存路径配置错误 | 设置 `HF_HOME` 环境变量 |
| **MIOpen 警告日志** | MIOpen 调试日志过多 | 设置 `MIOPEN_LOG_LEVEL=6` |
| **第一次推理很慢** | MIOpen 算法编译 | 正常现象，预热后速度会提升 |
| **显存不足** | 模型太大 | 使用 `num_step=16` 或 `dtype=torch.float16` |

## 📊 验证安装

运行验证脚本检查安装状态:

```bash
# 快速验证
python verify_install.py

# 性能基准测试
python benchmark_rtf.py
```

预期输出:
```
==============================================================
OmniVoice AMD GPU Edition - 安装验证
==============================================================

[GPU信息]
  PyTorch版本: 2.9.1+rocm7.2.1
  CUDA可用: True
  设备名称: AMD Radeon RX 9070 XT
  显存: 16.0 GB

[加载模型]
  模型加载成功

[预热模型]
  预热完成

[性能测试]
  推理时间: 2.135秒
  音频时长: 5.40秒
  RTF: 0.395 (2.5x实时)

验证完成！OmniVoice AMD GPU版本工作正常
```

## 📈 版本历史

### v0.1.5 (2026-05-15) - 性能优化版
- ✨ **新增**: 跨平台路径自动检测 (Windows/Linux/macOS)
- 🚀 **优化**: 驱动器扫描性能提升 30-50%
- 🛡️ **修复**: socket 资源泄漏问题
- 📝 **改进**: 添加完整日志记录
- ✅ **改进**: 异常处理更加可靠

### v0.1.4 (2026-04-27) - 初始 AMD GPU 版本
- 新增 AMD ROCm 支持
- 一键安装脚本
- 性能基准测试

## 🤝 贡献

发现问题或有改进建议？欢迎提交 [Issue](https://github.com/Mark007007/OmniVoice-AMD-GPU/issues) 或 Pull Request！

## 🙏 致谢

- **原始项目**: [k2-fsa/OmniVoice](https://github.com/k2-fsa/OmniVoice)
- **AMD GPU支持**: 感谢 [Alexander-Ger-Reich](https://github.com/k2-fsa/OmniVoice/pull/92) 的贡献
- **社区支持**: 感谢所有用户的反馈和测试

## 📄 许可证

Apache License 2.0 - 详见 [LICENSE](LICENSE) 文件

---

**快速链接**:
- 📖 [详细安装指南](INSTALL_GUIDE.md)
- 🚀 [快速启动脚本](launcher.py)
- ⚙️ [性能测试脚本](benchmark_rtf.py)
- 🔗 [原始项目](https://github.com/k2-fsa/OmniVoice)
