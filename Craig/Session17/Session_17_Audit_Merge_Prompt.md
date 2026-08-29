# Session 17 Audit & Merge Prompt — Webster Fell's Final Gambit

Use this prompt in new threads with your audit-pass models, pasting in both draft .md files and the WhisperX transcript (plus review_flags.txt if you ran it).

---

## PROMPT

You are auditing two independently-written session recaps of the same D&D session — one produced by Claude Sonnet 5, one produced by ChatGPT — against the original WhisperX transcript, which is the ground-truth source. Your job is to produce a single, corrected master recap, not a comparison document.

This campaign is **"Webster Fell's Final Gambit"**. The DM's handle is **Lipton**.

**Active party roster:** Drebah, Father Ashton, Glade, Sgt. Andaal Dare, Vorn.

**"Xorn" is a legitimate campaign name, not a transcription error.** He is the joke level-20 version of Vorn from a one-off playtest, and the table still references him. If the transcript or either draft mentions Xorn, keep him as Xorn — do not normalize him to Vorn and do not strip him for being absent from the roster above.

**Session 17 attendance note:** all five active PCs — Drebah, Father Ashton, Glade, Sgt. Andaal Dare, and Vorn — were present this session. All five belong in the Roll of Honor. If either draft omits one of them from the Roll of Honor, that's an error to correct against the transcript.

**Aughie is not part of this campaign.** He has been permanently removed. If either draft references Aughie in any way — roster, continuity flag, open thread, anything — strip it out entirely. This is not a discrepancy to resolve by checking the transcript; it's a hard exclusion regardless of what either draft says.

**Tommi is not part of this campaign as of this session.** She has left permanently. If either draft references Tommi in any way — roster, Roll of Honor, continuity flag, open thread, anything — strip it out entirely. This is not a discrepancy to resolve by checking the transcript; it's a hard exclusion regardless of what either draft says.

## Process

1. Read both draft recaps in full, then read the complete WhisperX transcript (and `review_flags.txt` if provided — treat flagged segments with extra scrutiny).
2. Wherever the two drafts agree, and that agreement is consistent with the transcript, keep it as-is.
3. Wherever the two drafts disagree — on names, dialogue, sequence of events, who did what, dice results, item details, or any other factual point — resolve the disagreement by checking the WhisperX transcript directly. The transcript is the source of truth, not either draft.
4. Wherever the transcript is itself ambiguous, garbled, or a segment is flagged in `review_flags.txt` with no clear resolution, do not guess or silently pick one draft's version. Flag it inline using: `[UNCLEAR: best supported reading — reason]`.
5. Wherever both drafts agree with each other but *disagree* with the transcript, still defer to the transcript — independent agreement between two AI drafts is not itself evidence of accuracy.
6. Check both drafts for anything present in one but missing from the other (a scene, a line, a mechanical detail). If the transcript supports the content that's missing from one draft, include it in the master.
7. Do not introduce any new content, phrasing, or interpretation that isn't grounded in the transcript or reasonably present in at least one of the two drafts.

## Output Requirements

Produce **one single master recap as a Word document (.docx)**, following this exact structure (matching the established campaign format). If your environment only outputs plain text or Markdown, structure it with clear headers, tables, and blockquotes exactly as specified below so it converts cleanly to .docx — but the deliverable Paul needs is a Word document, not a markdown file.

1. **Title** — `Webster Fell's Final Gambit: Session 17 Recap`, with one evocative italicized subtitle and one italicized tagline underneath.
2. **Session at a Glance** — 2x2 table: STARTED / ENDED, IMMEDIATE OBJECTIVE / CLOCK.
3. **TL;DR** — blockquote bullet list of major beats in sequence.
4. **The Short Version** — 3–4 paragraph prose summary.
5. **The Full Story** — detailed chronological narrative in bolded named sub-sections.
6. **Roll of Honor** — one blockquote entry per active PC present this session.
7. **The Haul** — two-column table (Item/Change | Status at Session End), including any Inspiration awarded and why.
8. **Lore, Clues, and Open Threads** — bulleted list; mark genuinely still-open continuity threads with `[Continuity flag]`. Do not include anything related to Aughie or Tommi.
9. **Where We Left Off** — 2–3 paragraphs setting up the party's exact position for next session.
10. **Closing lines** — two short bolded punchy lines: net state-of-play, and the immediate stakes going into the next session.

## Final Checklist Before Output

Before finalizing, verify:
- [ ] All five active PCs (Drebah, Father Ashton, Glade, Sgt. Andaal Dare, Vorn) appear in the Roll of Honor
- [ ] Aughie does not appear anywhere in the document
- [ ] Tommi does not appear anywhere in the document
- [ ] Every disagreement between the two drafts was resolved against the transcript, not by preference or averaging
- [ ] Any transcript ambiguity is flagged with `[UNCLEAR: ...]` rather than silently resolved
- [ ] All dice results, damage numbers, and mechanical outcomes match the transcript exactly
- [ ] Character/place names match the established roster and campaign spellings

Output only the final master recap document as a .docx file — no meta-commentary, no discrepancy log, no notes about your process.

## Inputs

**[DRAFT 1 — Claude version]**
[paste Claude .md draft here]

**[DRAFT 2 — ChatGPT version]**
[paste ChatGPT .md draft here]

**[WHISPERX TRANSCRIPT]**
[paste full Session 17 transcript here]

**[REVIEW FLAGS — if applicable]**
[paste review_flags.txt contents here, or state "none run"]
