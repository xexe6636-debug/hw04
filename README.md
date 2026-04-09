# hw04 作业目录

## 目录结构

```
hw04/
├── README.md              ← 本文件，总览说明
├── text_gen.md            ← 任务一：大模型生成文稿
├── jianying.md            ← 任务二：剪映声音克隆说明
├── tts_output.mp3         ← 任务二：配音音频（若文件过大则见网盘链接）
├── asr_report.md          ← 任务三：ASR 方案对比与选型报告
├── whisper_asr.py         ← 任务三：Whisper 识别脚本
├── requirements.txt       ← 任务三：Python 依赖列表
└── experiment_log.md      ← 任务三：实验记录
```

---

## 任务一：大模型生成文稿

- 文件：[text_gen.md](./text_gen.md)
- 标题：《人工智能正在悄悄重塑我们的学习方式》
- 所用模型：Claude（Anthropic）
- 字数：约 450 字

---

## 任务二：剪映声音克隆

- 说明文件：[jianying.md](./jianying.md)
- 配音脚本：任务一全文
- 导出格式：MP3 音频
- 音频文件：`tts_output.mp3`（仓库内）或网盘链接（见 jianying.md）

---

## 任务三：开源 ASR 调研与实现

- 对比报告：[asr_report.md](./asr_report.md)
- 选用方案：OpenAI Whisper base 模型
- 实验记录：[experiment_log.md](./experiment_log.md)

### 快速开始

#### 环境要求

- Python 3.9 ~ 3.11
- 系统已安装 [ffmpeg](https://ffmpeg.org/download.html)（用于音频解码）
- 内存 ≥ 4 GB（base 模型约占 500 MB 运行内存）

#### 安装步骤

```bash
# 第一步：安装 Python 依赖
pip install -r requirements.txt

# 若需要麦克风录音功能，额外安装：
pip install sounddevice scipy
```

> **macOS 安装 ffmpeg**：`brew install ffmpeg`  
> **Windows 安装 ffmpeg**：`winget install ffmpeg`（或从官网下载后添加到 PATH）

#### 运行示例

```bash
# 对音频文件进行识别（推荐先用任务二导出的 tts_output.mp3 测试）
python whisper_asr.py --audio tts_output.mp3

# 使用更大的模型提升精度（需要更多时间）
python whisper_asr.py --audio tts_output.mp3 --model small

# 麦克风实时录音并识别（录 15 秒）
python whisper_asr.py --mic --duration 15
```

#### 预期输出

运行后终端将打印：
1. 完整识别文本
2. 分段时间戳（每句开始/结束时间）
3. 识别耗时

识别结果同时保存为 `音频文件名_transcript.txt`。

---

## 注意事项

1. 首次运行会自动从网络下载 Whisper 模型（base 约 140 MB），请确保网络畅通或开启代理。
2. 若下载速度慢，可手动将模型文件放入 `~/.cache/whisper/` 目录（模型文件名如 `base.pt`）。
3. 所有识别在本地完成，音频数据**不会上传至任何服务器**，隐私安全。
