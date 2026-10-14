---
name: application-craft
description: Draft and check application materials — resume tailoring and cover letters for job applications, and submission packages for academic journals (format compliance, editor cover letter, reference formatting). Use when the user asks to tailor a resume to a job posting, write or improve a cover letter, check whether a resume matches a job description, format a manuscript to a journal's author guidelines, or draft a cover letter to an editor. Tailors and formats the applicant's real experience and real research — it does not invent credentials and does not help evade plagiarism or similarity detection.
---

# application-craft

Two high-friction application workflows, done honestly:

- **Job applications** — align a resume to a specific posting (not keyword-stuff), and write a cover letter that argues fit instead of restating the resume.
- **Academic submissions** — get a manuscript into a target journal's required shape, and write the cover letter to the editor.

The through-line: this skill *organizes and sharpens what is true*. It will not fabricate experience, invent publications, or help a manuscript dodge similarity/plagiarism checks.

## When to use this skill

- "Tailor my resume to this job posting."
- "Write a cover letter for this role."
- "Does my resume match this JD? What am I missing?"
- "Format this paper for *<journal>*'s author guidelines."
- "Draft a cover letter to the editor for my submission."

## Hard limits (read first)

- **Tailoring ≠ fabrication.** Rephrase and prioritize real experience. If a required qualification is genuinely missing, the skill says so — it does not invent it.
- **No plagiarism-check evasion.** This skill will not paraphrase sources to lower a similarity score, will not "rewrite to beat 查重/Similarity", and will not generate text the author didn't produce. Formatting and cover letters only. If asked for the former, decline and explain.
- **No ghostwritten research.** For papers it helps with *format, structure, and packaging*, not with fabricating results or drafting content the author can't stand behind.
- **Not a guarantee.** Applicant tracking systems vary; journal rules change. Verify against the actual posting / current author guidelines.

## Workflow A — job application

1. **Gather**: the resume text and the full job description (both as files or pasted).
2. **Scan**: `python3 scripts/ats_check.py --resume resume.txt --jd jd.txt --out ats-report.md`
   - Reports the JD's key terms, which appear in the resume, which don't, plus structure red flags (missing contact/sections, length, weak bullet starts).
3. **Rewrite, not stuff**: for each *true* experience, reorder and reword bullets so the relevant terms surface naturally. Never add a skill the applicant doesn't have.
4. **Cover letter**: use `templates/cover-letter.md`. One concrete argument for fit, one proof, one ask. No restating the resume.
5. See `references/job-application-playbook.md`.

## Workflow B — academic submission

1. **Target the journal**: read its current author guidelines.
2. **Check format**: run against `references/journal-submission-checklist.md` — abstract word limit, section order, reference style, figure/table rules, required statements (data availability, conflicts, funding, ethics).
3. **Cover letter to the editor**: use `templates/research-cover-letter.md`.
4. Never "rephrase to reduce similarity score".

## Files

- `scripts/ats_check.py` — resume↔JD keyword + structure check (stdlib only)
- `templates/cover-letter.md`
- `templates/research-cover-letter.md`
- `references/job-application-playbook.md`
- `references/journal-submission-checklist.md`
