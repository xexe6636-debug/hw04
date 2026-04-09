# ASR 开源语音识别方案调研与对比报告

## 一、调研背景

本报告对比三种主流开源自动语音识别（ASR）方案，并选取其中一种在本地环境完成可运行的识别程序实现。

---

## 二、方案对比

### 2.1 方案概览

| 维度 | OpenAI Whisper | Vosk | FunASR（阿里达摩院） |
|------|---------------|------|---------------------|
| 仓库 / 来源 | [github.com/openai/whisper](https://github.com/openai/whisper) | [github.com/alphacep/vosk-api](https://github.com/alphacep/vosk-api) | [github.com/modelscope/FunASR](https://github.com/modelscope/FunASR) |
| 版本（调研时） | v20231117 | 0.3.45 | 1.1.x |
| 许可协议 | MIT | Apache 2.0 | MIT |
| 语言支持 | 99 种语言（中文支持良好） | 中、英、俄等 20+ 语言 | 中文（普通话、方言）为主，兼顾英文 |
| 方言支持 | 粤语、台湾普通话等 | 有限 | 上海话、粤语、四川话等 |
| 最小模型体量 | tiny: 39 MB | 中文模型: 约 40 MB | 离线小模型: 约 200 MB |
| 最大/精度最高模型 | large-v3: 约 1.5 GB | large: 约 1.8 GB | Paraformer-large: 约 900 MB |
| 推理速度（CPU，普通 PC） | tiny 快，large 慢（约 0.5～5× 实时） | 快（约 5～10× 实时） | 中等（约 2～4× 实时） |
| 支持流式 / 实时 | ❌ 官方不支持（需第三方适配） | ✅ 原生支持 | ✅ 支持（需流式版本） |
| 依赖复杂度 | 低（pip install openai-whisper） | 低（pip install vosk） | 中（需安装 funasr + modelscope） |
| GPU 加速 | ✅ CUDA / MPS | ❌ CPU 专用 | ✅ CUDA |
| 主要优势 | 精度高，多语言，易上手 | 轻量，流式，离线友好 | 中文精度最优，标点恢复好 |
| 主要劣势 | 不支持流式；large 模型慢 | 中文精度不如 Whisper | 对国际用户不够友好 |

---

### 2.2 各方案详细说明

#### ① OpenAI Whisper

Whisper 是 OpenAI 于 2022 年开源的端到端语音识别模型，基于 Transformer 编码器-解码器架构，在 68 万小时多语言音频数据上训练。提供 tiny / base / small / medium / large 五个规模，可按精度/速度需求选择。

- **中文表现**：small 及以上模型中文识别准确率较高，能较好处理带口音普通话。  
- **局限**：不支持原生流式识别；large 模型在无 GPU 的普通笔记本上推理较慢（1 分钟音频约需 2～5 分钟处理）。

#### ② Vosk

Vosk 是俄罗斯公司 Alpha Cephei 开发的离线 ASR 工具包，底层使用 Kaldi 框架，支持多平台（Linux / Windows / macOS / Android / iOS）。其最大特点是**原生支持流式识别**，适合需要实时字幕或低延迟场景。

- **中文表现**：中文模型精度弱于 Whisper，尤其在长句、专有名词方面差距明显。  
- **优势**：资源占用极低，Raspberry Pi 上也可流畅运行；API 简洁，几十行代码即可实现麦克风实时识别。

#### ③ FunASR（达摩院）

FunASR 是阿里巴巴达摩院开源的工业级 ASR 框架，包含 Paraformer、Conformer 等多种模型架构，尤其在**中文普通话识别、标点恢复、时间戳预测**上表现突出，是目前开源中文 ASR 中综合效果最好的方案之一。

- **中文表现**：Paraformer-large 在多个中文基准上优于 Whisper large-v3。  
- **局限**：环境配置相对复杂，初次拉取模型（需 ModelScope 或手动下载）体验不如 Whisper 顺畅；主要面向中文，多语言场景弱于 Whisper。

---

## 三、选型理由

**本次选用 OpenAI Whisper（base 模型）**，理由如下：

1. **安装最简单**：一条 `pip install openai-whisper` 命令即可，对新手友好。  
2. **中文效果足够好**：任务二的配音脚本为标准普通话，base 模型即可准确识别。  
3. **文档与社区完善**：问题易于检索，遇到报错可快速找到解决方案。  
4. **MIT 许可证**：可自由用于学习与商业项目。

若未来需要**实时识别**（如直播字幕），推荐切换至 Vosk；若以**中文精度**为第一优先，推荐 FunASR。

---

## 四、实现说明

代码文件：`whisper_asr.py`  
依赖文件：`requirements.txt`  
实验记录：`experiment_log.md`

### 运行方式

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 对音频文件识别
python whisper_asr.py --audio your_audio.mp3

# 3. 实时麦克风识别（可选）
python whisper_asr.py --mic
```

详细说明见 `README.md`。
