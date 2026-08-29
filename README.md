# AI Transcription for Tabletop Sessions

A small pipeline for turning multi-track voice recordings (e.g. the per-speaker
FLAC/WAV files a Discord bot like [Craig](https://craig.chat/) produces) into
a clean, speaker-labeled transcript using [WhisperX](https://github.com/m-bain/whisperX).

Built for D&D/TTRPG session recap workflows, but there's nothing D&D-specific
in the code — it works for any recording where each speaker already has their
own separate audio track (podcasts, interviews, multi-mic meetings, etc.).

Because each speaker is already isolated in their own file, there's no need
for diarization — the script just labels every line with the track's speaker
name and merges all tracks into one chronological transcript.

## What's included

- **`transcribe_craig_whisperx.py`** — the main pipeline. Transcribes every
  audio file in a folder with WhisperX, labels each segment with the speaker
  (derived from the filename), and writes both per-speaker and merged
  transcripts (JSON, TXT, and Markdown).
- **`flag_hallucinations.py`** — a non-destructive review aid. Scans the
  per-track JSON output for segments that look like Whisper hallucinations
  (e.g. a stray "Thank you." generated over silence) using word-level
  alignment confidence, and writes a `review_flags.txt` you check by hand.
  It never deletes or modifies your transcripts.
- **`fix_speaker_name.py`** — renames a speaker across every output file in a
  session's `out/` folder in one pass (transcripts + per-track filenames).
  Takes a timestamped backup of the folder before touching anything.

## Requirements

- Python 3.10+
- A [WhisperX](https://github.com/m-bain/whisperX) environment (`pip install whisperx`), which pulls in `torch` and `faster-whisper`
- A working `ffmpeg` on your `PATH`
- An NVIDIA GPU is strongly recommended — CPU works but transcription is much slower

```bash
pip install whisperx torch
```

Follow WhisperX's own install instructions for GPU/CUDA setup — the correct
`torch` build depends on your CUDA version.

### Windows + conda note

If you run this from a conda environment, use `conda activate` rather than
`conda run`. `conda run` prepends the environment's own `Library\bin` to
`PATH` ahead of everything else, which can shadow a working system `ffmpeg`
with a broken bundled one and crash `whisperx.load_audio` immediately. If
that happens, activate the environment normally, or invoke `python.exe`
directly with your working `ffmpeg` prepended on `PATH`.

## Folder convention

The scripts don't require any particular top-level layout, but this is the
convention they're written around — one folder per session, with a
raw/converted/output split:

```
Session01/
  raw/     # original recordings from Craig (FLAC), one file per speaker
  wav/     # converted to WAV if your recordings need it (WhisperX also reads FLAC directly)
  out/     # transcription output goes here
```

Audio filenames become speaker labels: leading track numbers are stripped and
underscores/dashes become spaces, so `1_Alice.flac` becomes speaker `Alice`.

## Usage

### 1. Transcribe a session

```bash
python transcribe_craig_whisperx.py --input "Session01/raw" --output "Session01/out"
```

Options:

| Flag | Default | Description |
|---|---|---|
| `--input` | *(required)* | Folder containing one audio file per speaker (`.wav`, `.flac`, `.mp3`, `.m4a`, `.ogg`, `.opus`) |
| `--output` | *(required)* | Folder to write results into |
| `--model` | `large-v3` | Whisper model size (`tiny`, `base`, `small`, `medium`, `large-v3`, ...) |
| `--language` | `en` | Language code |
| `--batch_size` | `32` | Lower this if you run out of GPU memory |
| `--compute_type` | `float16` | Use `int8` on CPU or lower-memory GPUs |
| `--no_align` | off | Skip word-level alignment (faster, but hallucination flagging needs alignment scores) |

Output, written to `--output`:

```
out/
  per_track/
    Alice.json   # per-speaker segments with word-level timing/confidence
    Alice.txt
    ...
  merged_transcript.json
  merged_transcript.txt
  merged_transcript.md   # human-readable, chronological across all speakers
```

### 2. Flag likely hallucinations for review

```bash
python flag_hallucinations.py --out "Session01/out"
```

Writes `Session01/out/review_flags.txt` listing short, low-confidence
segments worth double-checking against the audio. Nothing is deleted — this
is a checklist for a human pass, not an automatic filter. Tune the
thresholds at the top of the script if it's flagging too much or too little.

### 3. Fix a mislabeled speaker

If a track was named wrong and the wrong name ended up baked into every
generated file:

```bash
python fix_speaker_name.py --out "Session01/out" --old WrongName --new CorrectName
```

Replaces the name across every `.md`/`.txt`/`.json` file in `out/` and
renames the matching `per_track` files. Takes a timestamped backup of the
whole `out/` folder first (`--no-backup` to skip, `--no-rename-files` to
leave filenames alone).

## License

No license file is currently included — treat this as source-available for
reference. Open an issue if you'd like to use it under a specific license.
