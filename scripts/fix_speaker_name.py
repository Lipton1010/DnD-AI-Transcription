"""
fix_speaker_name.py

Replace every occurrence of one speaker name with another across ALL files in a
WhisperX session out/ folder -- merged_transcript.md/.txt/.json and every file
under per_track/. One pass, all files.

Use case: a track was named wrong (e.g. the wav was "Zorn" but the speaker is
"Vorn"), so the wrong name is now baked into every generated transcript.

By default this also renames the per_track files themselves (Zorn.json ->
Vorn.json) so the filenames match the corrected speaker label.

SAFE BY DEFAULT: makes a timestamped backup copy of the whole out/ folder before
touching anything, so you can roll back if something looks off.

USAGE
    python fix_speaker_name.py --out "D:\\AI_Transcription\\Craig\\Session11\\out" --old Zorn --new Vorn

Optional flags:
    --no-backup        skip the backup copy (not recommended)
    --no-rename-files  edit file *contents* but leave per_track filenames as-is
"""

import argparse
import shutil
from datetime import datetime
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Replace a speaker name across all files in a session out/ folder."
    )
    parser.add_argument("--out", required=True, help="Session out/ folder")
    parser.add_argument("--old", required=True, help="Name to replace, e.g. Zorn")
    parser.add_argument("--new", required=True, help="Correct name, e.g. Vorn")
    parser.add_argument("--no-backup", action="store_true", help="Skip the safety backup")
    parser.add_argument(
        "--no-rename-files",
        action="store_true",
        help="Edit file contents but do not rename per_track files",
    )
    args = parser.parse_args()

    out_dir = Path(args.out)
    if not out_dir.is_dir():
        raise SystemExit(f"Folder not found: {out_dir}")

    old, new = args.old, args.new
    if old == new:
        raise SystemExit("--old and --new are the same; nothing to do.")

    # --- Safety backup of the entire out/ folder -------------------------------
    if not args.no_backup:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = out_dir.parent / f"{out_dir.name}_backup_{stamp}"
        shutil.copytree(out_dir, backup_dir)
        print(f"Backup created: {backup_dir}")

    # --- Gather the text files we know this pipeline produces -------------------
    # We only touch text-based outputs. (No binaries live in out/.)
    text_suffixes = {".md", ".txt", ".json"}
    targets = [
        p for p in out_dir.rglob("*")
        if p.is_file() and p.suffix.lower() in text_suffixes
    ]

    total_replacements = 0
    files_changed = 0

    for path in targets:
        text = path.read_text(encoding="utf-8")
        count = text.count(old)
        if count == 0:
            continue
        path.write_text(text.replace(old, new), encoding="utf-8")
        total_replacements += count
        files_changed += 1
        print(f"  {path.relative_to(out_dir)}: {count} replacement(s)")

    # --- Rename per_track files whose NAME contains the old speaker -------------
    renamed = 0
    if not args.no_rename_files:
        per_track = out_dir / "per_track"
        if per_track.is_dir():
            for path in list(per_track.iterdir()):
                if path.is_file() and old in path.name:
                    new_name = path.name.replace(old, new)
                    target = path.with_name(new_name)
                    if target.exists():
                        print(f"  SKIP rename (target exists): {path.name} -> {new_name}")
                        continue
                    path.rename(target)
                    renamed += 1
                    print(f"  renamed: {path.name} -> {new_name}")

    print()
    print(f'Replaced "{old}" -> "{new}"')
    print(f"  {total_replacements} replacement(s) across {files_changed} file(s)")
    if not args.no_rename_files:
        print(f"  {renamed} per_track file(s) renamed")
    print("Done.")


if __name__ == "__main__":
    main()
