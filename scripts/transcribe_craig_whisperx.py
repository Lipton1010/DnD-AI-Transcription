import argparse
import gc
import json
import re
from pathlib import Path

import torch
import whisperx


AUDIO_EXTS = {".wav", ".flac", ".mp3", ".m4a", ".ogg", ".opus"}


def clean_speaker_name(path: Path) -> str:
    name = path.stem
    name = re.sub(r"^\d+[_\-\s]*", "", name)
    name = name.replace("_", " ").replace("-", " ")
    return " ".join(name.split()).strip() or path.stem


def fmt_time(seconds: float) -> str:
    seconds = max(0, float(seconds))
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def merge_neighboring_segments(segments, max_gap=1.25):
    merged = []

    for seg in sorted(segments, key=lambda x: (x["start"], x["end"], x["speaker"])):
        text = seg.get("text", "").strip()
        if not text:
            continue

        if (
            merged
            and merged[-1]["speaker"] == seg["speaker"]
            and seg["start"] - merged[-1]["end"] <= max_gap
        ):
            merged[-1]["text"] += " " + text
            merged[-1]["end"] = max(merged[-1]["end"], seg["end"])
        else:
            merged.append({
                "speaker": seg["speaker"],
                "start": seg["start"],
                "end": seg["end"],
                "text": text,
                "source_file": seg["source_file"],
            })

    return merged


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", default="large-v3")
    parser.add_argument("--language", default="en")
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--compute_type", default="float16")
    parser.add_argument("--no_align", action="store_true")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    per_track_dir = output_dir / "per_track"
    per_track_dir.mkdir(parents=True, exist_ok=True)

    audio_files = sorted(
        p for p in input_dir.iterdir()
        if p.is_file() and p.suffix.lower() in AUDIO_EXTS
    )

    if not audio_files:
        raise SystemExit(f"No audio files found in {input_dir}")

    device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"Device: {device}")
    if device == "cuda":
        print(f"GPU: {torch.cuda.get_device_name(0)}")

    print(f"Loading WhisperX model: {args.model}")
    model = whisperx.load_model(
        args.model,
        device,
        compute_type=args.compute_type,
        language=args.language,
    )

    all_segments = []
    align_cache = {}

    for audio_path in audio_files:
        speaker = clean_speaker_name(audio_path)
        print(f"\n=== Transcribing: {audio_path.name} as [{speaker}] ===")

        audio = whisperx.load_audio(str(audio_path))

        result = model.transcribe(
            audio,
            batch_size=args.batch_size,
            language=args.language,
        )

        detected_language = result.get("language", args.language)

        if not args.no_align:
            if detected_language not in align_cache:
                print(f"Loading alignment model for language: {detected_language}")
                align_cache[detected_language] = whisperx.load_align_model(
                    language_code=detected_language,
                    device=device,
                )

            model_a, metadata = align_cache[detected_language]

            result = whisperx.align(
                result["segments"],
                model_a,
                metadata,
                audio,
                device,
                return_char_alignments=False,
            )

        track_segments = []

        for seg in result.get("segments", []):
            text = seg.get("text", "").strip()
            if not text:
                continue

            start = float(seg.get("start", 0.0))
            end = float(seg.get("end", start))

            entry = {
                "speaker": speaker,
                "start": start,
                "end": end,
                "text": text,
                "source_file": audio_path.name,
                "words": seg.get("words", []),
            }

            track_segments.append(entry)
            all_segments.append(entry)

        safe_speaker = re.sub(r"[^A-Za-z0-9_\- ]+", "", speaker).replace(" ", "_")
        track_json = per_track_dir / f"{safe_speaker}.json"
        track_txt = per_track_dir / f"{safe_speaker}.txt"

        track_json.write_text(
            json.dumps(track_segments, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        with track_txt.open("w", encoding="utf-8") as f:
            for seg in track_segments:
                f.write(
                    f"[{fmt_time(seg['start'])} - {fmt_time(seg['end'])}] "
                    f"{speaker}: {seg['text']}\n"
                )

        print(f"Saved: {track_json}")
        print(f"Saved: {track_txt}")

        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    all_segments_sorted = sorted(all_segments, key=lambda x: (x["start"], x["end"], x["speaker"]))
    merged_segments = merge_neighboring_segments(all_segments_sorted)

    merged_json = output_dir / "merged_transcript.json"
    merged_txt = output_dir / "merged_transcript.txt"
    merged_md = output_dir / "merged_transcript.md"

    merged_json.write_text(
        json.dumps(merged_segments, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    with merged_txt.open("w", encoding="utf-8") as f:
        for seg in merged_segments:
            f.write(
                f"[{fmt_time(seg['start'])} - {fmt_time(seg['end'])}] "
                f"{seg['speaker']}: {seg['text']}\n"
            )

    with merged_md.open("w", encoding="utf-8") as f:
        f.write("# Merged D&D Session Transcript\n\n")
        for seg in merged_segments:
            f.write(
                f"**[{fmt_time(seg['start'])}] {seg['speaker']}:** "
                f"{seg['text']}\n\n"
            )

    print("\nDONE")
    print(f"Merged JSON: {merged_json}")
    print(f"Merged TXT:  {merged_txt}")
    print(f"Merged MD:   {merged_md}")


if __name__ == "__main__":
    main()