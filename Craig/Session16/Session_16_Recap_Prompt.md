# Session Recap Generation Prompt — Webster Fell's Final Gambit

Use this prompt verbatim (swap in the Session 16 transcript) in **Claude Sonnet 5, set to max effort** for one first-pass draft, and separately in **ChatGPT** for the second opinion. Output must be a single Markdown (.md) file in both cases — the drafts get converted to a final .docx later, during the audit/merge pass.

---

## PROMPT

You are helping produce a session recap document for a Dungeons & Dragons campaign called **"Webster Fell's Final Gambit"**. The DM's handle is **Lipton**.

You will be given a WhisperX transcript of Session 16, generated from Craig multitrack Discord recordings. The transcript may contain transcription artifacts: mis-heard words, mis-transcribed speaker names, dropped words in fast dialogue, or short garbled segments (some of these may be flagged in an accompanying `review_flags.txt` — treat flagged segments with extra scrutiny, but do not assume they're wrong; verify against context).

**Active party roster** (use these names exactly, correcting any transcription variants you encounter — e.g. "Tommy" should read as "Tommi"):
- Drebah
- Father Ashton
- Glade
- Sgt. Andaal Dare
- Tommi
- Vorn

**"Xorn" is a real name in this campaign, not an error.** He is the joke level-20 version of Vorn from a one-off playtest, and the table still references him. Never "correct" Xorn to Vorn, and don't drop him for being absent from the roster above. WhisperX tends to mangle him as "Zorn" or "Zero" — read either as Xorn where the context is clearly about the playtest character.

Session 16 attendance note: Drebah's player was not present for this session, so Drebah does not appear in the transcript. Do not include Drebah in the Roll of Honor for this session. If the transcript establishes an in-fiction reason for the absence, reflect that briefly wherever relevant. Do not invent a reason if none is given — a simple factual note is sufficient.

Do not include Aughie anywhere in the recap — not in the roster, Roll of Honor, active-party context, Lore/Open Threads, or anywhere else. Aughie has been permanently removed from the campaign. Do not create or carry forward any continuity note, flag, or explanation regarding Aughie's absence — that thread is closed and should not be referenced at all, even in passing.

## Accuracy Requirements (read carefully)

- **Capture all real dialogue and events.** Do not compress or omit actual game content for the sake of brevity — this recap is a record, not just an advertisement for the session.
- **Never fabricate or embellish.** Every claim, quote, roll, and outcome must be traceable to the transcript. If something is ambiguous or inaudible, note it rather than guessing at specifics.
- **Do not silently "fix" uncertain content.** If a name, number, or line of dialogue is unclear in the transcript, flag it inline using this convention: `[UNCLEAR: best guess — reason]`. Do not delete or paper over uncertain material — flag it and move on. Accuracy over automation.
- **Quotes should be verbatim** from the transcript where used as callouts (e.g. in TL;DR, Roll of Honor, or chapter narration), not paraphrased dialogue dressed up as a quote.
- **Preserve actual dice results, damage numbers, DCs, and mechanical outcomes** exactly as stated in the transcript.

## Required Document Structure

Match this structure and tone exactly (in-universe, novelistic recap voice with a wry/dramatic flair, similar to prior session recaps for this campaign):

1. **Title** — `Webster Fell's Final Gambit: Session 16 Recap`, followed by one evocative italicized subtitle line and one more italicized tagline/summary line underneath.
2. **Session at a Glance** — a 2x2 table: STARTED / ENDED (top row), IMMEDIATE OBJECTIVE / CLOCK (bottom row).
3. **TL;DR** — a bulleted list (blockquote style) of the session's major beats in sequence, punchy and specific, each bullet a self-contained moment.
4. **The Short Version** — 3–4 paragraphs prose summary of the whole session, hitting every major plot beat in order.
5. **The Full Story** — the detailed narrative, broken into named sub-sections (bolded headers) for each major scene/sequence of the session, in chronological order. This is the most detailed section — don't skimp here.
6. **Roll of Honor** — one blockquote entry per active PC present this session, summarizing their standout moments and character beats for the session.
7. **The Haul** — a two-column table (Item/Change | Status at Session End) covering items gained/lost, NPCs affected, and any Inspiration awarded with the reason.
8. **Lore, Clues, and Open Threads** — bulleted list of worldbuilding reveals, mysteries, and dangling plot threads. Mark any unresolved threads carried over from prior sessions as `[Continuity flag]` at the start of the bullet.
9. **Where We Left Off** — 2–3 paragraphs setting up exactly where the party stands as the session ends, framed for a reader picking up next session.
10. **Closing lines** — two short punchy bolded lines: one summarizing the session's net state-of-play, one teasing what's immediately at stake going into next session.

## Output Format

- Output as a single **Markdown (.md) file**, not a docx.
- Use `#`/`##` headers appropriately, tables in standard Markdown table syntax, and `>` blockquotes for the TL;DR and Roll of Honor sections as shown in prior recaps.
- Do not include any meta-commentary, notes to the user, or explanation of your process in the output file itself — just the recap document.
- If you need to flag uncertainty per the accuracy requirements above, keep those flags inline in the document using the `[UNCLEAR: ...]` convention so they're visible during the audit pass.

## Input

[PASTE SESSION 16 WHISPERX TRANSCRIPT HERE — and review_flags.txt contents if applicable]
