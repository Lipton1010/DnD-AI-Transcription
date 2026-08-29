"""
flag_hallucinations.py

Non-destructive review aid for WhisperX D&D transcripts.

Reads the per_track/*.json files produced by transcribe_craig_whisperx.py and
flags segments that look like Whisper hallucinations (e.g. a stray "Thank you."
generated over near-silence) WITHOUT deleting anything.

The signal used is word-level alignment confidence, which whisperx.align()
already attaches to each word as "score". Real spoken phrases align with high
confidence; phrases hallucinated over silence usually align poorly. Combining
that with segment length and word-timing density gives a reliable "check this"
list that a human can verify against the audio.

Output: a single review_flags.txt written into the session out/ folder, listing
every flagged segment with its speaker, timestamp, text, and the reason(s) it
was flagged. NOTHING is removed from your transcripts.

USAGE
    python flag_hallucinations.py --out "D:\\AI_Transcription\\Craig\\Session11\\out"

You can re-run this on any past session by pointing --out at that session's
out\\ folder. It only reads per_track\\*.json and writes review_flags.txt.
"""

import argparse
import json
from pathlib import Path


# ---------------------------------------------------------------------------
# Tunable thresholds. Adjust these to make flagging stricter or looser.
# The goal is to catch hallucinations while flagging as few REAL lines as
# possible. When in doubt the script errs toward flagging (you review by hand),
# never toward deleting.
# ---------------------------------------------------------------------------

# A segment is only ever considered "suspicious" if it is short. Long segments
# are almost never hallucinations, so we leave them alone regardless of score.
MAX_WORDS_TO_CONSIDER = 6

# Mean word-confidence below this is treated as low confidence.
# WhisperX alignment scores roughly span 0.0-1.0; genuine clear speech usually
# sits high, hallucinations over silence usually sit low. 0.40 is a cautious
# starting point. Lower it to flag fewer segments, raise it to flag more.
LOW_CONFIDENCE_MEAN = 0.40

# Phrases Whisper commonly hallucinates over silence. Matching one of these is
# treated as a *weak* corroborating signal ONLY -- it raises suspicion but is
# never sufficient on its own, precisely because a player may really say these.
# Matching text here does NOT get a segment flagged unless confidence is also
# low or timing is degenerate. Nothing here is ever auto-deleted.
COMMON_HALLUCINATION_PHRASES = {
    "thank you.",
    "thank you",
    "thanks for watching.",
    "thanks for watching",
    "thank you for watching.",
    "thank you for watching",
    "thanks for watching!",
    "please subscribe.",
    "bye.",
    "bye bye.",
    "you",
    ".",
    "thank you very much.",
    "okay.",
    "so.",
}


def mean_word_score(words):
    """Average alignment confidence across words that have a numeric score.

    Returns None when no word carries a score (alignment may omit scores for
    some words, e.g. numerals or out-of-dictionary tokens). A None result is
    itself mildly suspicious for a short segment and is surfaced as such.
    """
    scores = [
        w["score"]
        for w in words
        if isinstance(w, dict) and isinstance(w.get("score"), (int, float))
    ]
    if not scores:
        return None
    return sum(scores) / len(scores)


def words_have_no_timing(words):
    """True when a short segment's words lack start/end timing entirely.

    Hallucinated chunks frequently come back with missing or zero-width word
    timings because there is no actual audio to align to. Real speech has
    spread-out word timings.
    """
    timed = [
        w for w in words
        if isinstance(w, dict)
        and isinstance(w.get("start"), (int, float))
        and isinstance(w.get("end"), (int, float))
    ]
    return len(timed) == 0


def assess_segment(seg):
    """Decide whether a single segment should be flagged for human review.

    Returns a list of human-readable reason strings. An empty list means the
    segment looks fine and will NOT appear in the review file.
    """
    text = seg.get("text", "").strip()
    words = seg.get("words", []) or []
    word_count = len(text.split())

    # Long segments are left alone. Hallucinations are short by nature, and we
    # do not want to bury the reviewer in false positives.
    if word_count > MAX_WORDS_TO_CONSIDER:
        return []

    reasons = []

    mean_score = mean_word_score(words)
    is_known_phrase = text.lower() in COMMON_HALLUCINATION_PHRASES

    # Primary signal: low alignment confidence on a short segment.
    if mean_score is not None and mean_score < LOW_CONFIDENCE_MEAN:
        reasons.append(f"low confidence (mean word score {mean_score:.2f})")

    # Secondary signal: no usable word timing on a short segment.
    if words and words_have_no_timing(words):
        reasons.append("no word-level timing")

    # If alignment produced no scores at all on a short segment, note it -- mild
    # on its own, but worth a glance, especially paired with a known phrase.
    if mean_score is None:
        reasons.append("no confidence scores from alignment")

    # Corroborating signal: matches a phrase Whisper habitually hallucinates.
    # Only meaningful alongside one of the above; on its own we DON'T flag,
    # because real dialogue includes these words.
    if is_known_phrase and reasons:
        reasons.append("matches a common hallucination phrase")
    elif is_known_phrase and not reasons:
        # Known phrase but confidence/timing look fine -> most likely REAL
        # speech. We deliberately do not flag, to avoid hiding real lines.
        return []

    return reasons


def fmt_time(seconds):
    seconds = max(0, float(seconds))
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def main():
    parser = argparse.ArgumentParser(
        description="Flag (never delete) likely Whisper hallucinations for human review."
    )
    parser.add_argument(
        "--out",
        required=True,
        help=r'Session out\ folder, e.g. D:\AI_Transcription\Craig\Session11\out',
    )
    args = parser.parse_args()

    out_dir = Path(args.out)
    per_track_dir = out_dir / "per_track"

    if not per_track_dir.is_dir():
        raise SystemExit(f"No per_track folder found in {out_dir}")

    track_files = sorted(per_track_dir.glob("*.json"))
    if not track_files:
        raise SystemExit(f"No per_track/*.json files found in {per_track_dir}")

    flagged = []  # (start, speaker, end, text, reasons, source_json)
    total_segments = 0

    for tf in track_files:
        try:
            segments = json.loads(tf.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            print(f"  WARNING: could not read {tf.name}: {e}")
            continue

        for seg in segments:
            total_segments += 1
            reasons = assess_segment(seg)
            if reasons:
                flagged.append((
                    float(seg.get("start", 0.0)),
                    seg.get("speaker", "?"),
                    float(seg.get("end", 0.0)),
                    seg.get("text", "").strip(),
                    reasons,
                    tf.name,
                ))

    flagged.sort(key=lambda x: x[0])  # chronological by start time

    review_path = out_dir / "review_flags.txt"
    with review_path.open("w", encoding="utf-8") as f:
        f.write("WhisperX hallucination review flags\n")
        f.write("=" * 60 + "\n")
        f.write(
            "These segments are flagged for a human to verify against the audio.\n"
            "NOTHING has been removed from your transcripts. If a flagged line is\n"
            "real dialogue, ignore it. If it is a hallucination, delete it by hand\n"
            "in merged_transcript.* and/or the relevant per_track file.\n\n"
        )
        f.write(f"Scanned {total_segments} segments across {len(track_files)} tracks.\n")
        f.write(f"Flagged {len(flagged)} segment(s) for review.\n\n")
        f.write(
            f"(Thresholds: <= {MAX_WORDS_TO_CONSIDER} words AND mean word score "
            f"< {LOW_CONFIDENCE_MEAN}, or degenerate timing. Tune at top of script.)\n"
        )
        f.write("-" * 60 + "\n\n")

        if not flagged:
            f.write("No segments flagged. Nothing to review.\n")
        else:
            for start, speaker, end, text, reasons, src in flagged:
                f.write(f"[{fmt_time(start)} - {fmt_time(end)}] {speaker}\n")
                f.write(f'    text   : "{text}"\n')
                f.write(f"    reason : {'; '.join(reasons)}\n")
                f.write(f"    source : per_track/{src}\n\n")

    print(f"\nScanned {total_segments} segments across {len(track_files)} tracks.")
    print(f"Flagged {len(flagged)} segment(s) for review.")
    print(f"Wrote: {review_path}")
    print("\nNothing was deleted. Open review_flags.txt and verify each entry by hand.")


if __name__ == "__main__":
    main()
