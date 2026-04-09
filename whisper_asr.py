"""
whisper_asr.py
==============
基于 OpenAI Whisper 的本地语音识别脚本。

支持两种模式：
  1. 文件模式：对指定音频文件进行识别（--audio 参数）
  2. 麦克风模式：实时录制并识别（--mic 参数，需安装 sounddevice + scipy）

使用示例：
  python whisper_asr.py --audio tts_output.mp3
  python whisper_asr.py --audio tts_output.mp3 --model small
  python whisper_asr.py --mic --duration 10

依赖：见 requirements.txt
"""

import argparse
import time
import os
import sys


def transcribe_file(audio_path: str, model_name: str = "base", language: str = "zh"):
    """
    对音频文件进行语音识别。

    参数：
        audio_path : 音频文件路径（支持 mp3 / wav / m4a / mp4 等 ffmpeg 支持的格式）
        model_name : Whisper 模型规模，可选 tiny / base / small / medium / large-v3
        language   : 语言代码，中文用 "zh"，英文用 "en"，None 表示自动检测
    """
    import whisper

    if not os.path.exists(audio_path):
        print(f"[错误] 找不到文件：{audio_path}")
        sys.exit(1)

    print(f"[信息] 正在加载 Whisper {model_name} 模型……（首次运行会自动下载，请耐心等待）")
    model = whisper.load_model(model_name)

    print(f"[信息] 开始识别：{audio_path}")
    t_start = time.time()

    result = model.transcribe(
        audio_path,
        language=language,          # 指定语言可提升速度和准确率
        verbose=False,              # 关闭逐段打印，统一最后输出
        fp16=False,                 # CPU 推理需关闭 fp16
        initial_prompt="以下是普通话内容，包含标点符号。",  # 提示词，帮助模型加标点
    )

    t_end = time.time()
    elapsed = t_end - t_start

    print("\n" + "=" * 60)
    print("【识别结果】")
    print("=" * 60)
    print(result["text"])
    print("=" * 60)
    print(f"[信息] 识别完成，耗时 {elapsed:.1f} 秒")

    # 将结果写入同名 .txt 文件
    out_path = os.path.splitext(audio_path)[0] + "_transcript.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(result["text"])
    print(f"[信息] 结果已保存至：{out_path}")

    # 打印分段时间戳（可选）
    print("\n【分段时间戳】")
    for seg in result.get("segments", []):
        start = seg["start"]
        end = seg["end"]
        text = seg["text"].strip()
        print(f"  [{start:6.2f}s → {end:6.2f}s]  {text}")

    return result["text"]


def transcribe_mic(duration: int = 10, model_name: str = "base", language: str = "zh"):
    """
    录制麦克风音频并识别（非流式，录完再识别）。

    参数：
        duration   : 录制时长（秒）
        model_name : Whisper 模型规模
        language   : 语言代码
    """
    try:
        import sounddevice as sd
        from scipy.io.wavfile import write as wav_write
        import numpy as np
        import whisper
    except ImportError as e:
        print(f"[错误] 缺少依赖：{e}")
        print("请执行：pip install sounddevice scipy")
        sys.exit(1)

    SAMPLE_RATE = 16000  # Whisper 需要 16kHz
    tmp_file = "mic_recording_tmp.wav"

    print(f"[信息] 开始录音，时长 {duration} 秒，请说话……")
    audio_data = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
    )
    sd.wait()  # 等待录音结束
    print("[信息] 录音完成，正在保存临时文件……")

    wav_write(tmp_file, SAMPLE_RATE, audio_data)

    print("[信息] 正在加载模型并识别……")
    model = whisper.load_model(model_name)
    t_start = time.time()

    result = model.transcribe(
        tmp_file,
        language=language,
        fp16=False,
        initial_prompt="以下是普通话内容，包含标点符号。",
    )

    t_end = time.time()

    print("\n" + "=" * 60)
    print("【实时识别结果】")
    print("=" * 60)
    print(result["text"])
    print("=" * 60)
    print(f"[信息] 识别耗时 {t_end - t_start:.1f} 秒（录音时长 {duration} 秒）")

    # 清理临时文件
    os.remove(tmp_file)
    return result["text"]


def main():
    parser = argparse.ArgumentParser(
        description="基于 OpenAI Whisper 的语音识别工具",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--audio", type=str, default=None,
        help="音频文件路径（如 tts_output.mp3）"
    )
    parser.add_argument(
        "--mic", action="store_true",
        help="使用麦克风录音并识别"
    )
    parser.add_argument(
        "--duration", type=int, default=10,
        help="麦克风录音时长（秒，默认 10）"
    )
    parser.add_argument(
        "--model", type=str, default="base",
        choices=["tiny", "base", "small", "medium", "large", "large-v3"],
        help="Whisper 模型规模（默认 base；精度更高用 small/medium）"
    )
    parser.add_argument(
        "--language", type=str, default="zh",
        help="语言代码（中文 zh，英文 en，自动检测留空）"
    )

    args = parser.parse_args()

    if args.audio:
        transcribe_file(args.audio, model_name=args.model, language=args.language)
    elif args.mic:
        transcribe_mic(duration=args.duration, model_name=args.model, language=args.language)
    else:
        print("[提示] 请指定 --audio 文件路径 或 --mic 使用麦克风")
        print("示例：")
        print("  python whisper_asr.py --audio tts_output.mp3")
        print("  python whisper_asr.py --mic --duration 15")
        parser.print_help()


if __name__ == "__main__":
    main()
