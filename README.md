# application-craft

**An Agent Skill for application materials that stay honest — job applications and academic submissions.**

Two workflows in one package: tailor a resume and write a cover letter for a specific job, and get a manuscript into a target journal's required shape with a proper cover letter to the editor. It sharpens and formats what's *true* — it will not invent credentials, and it will not reword a manuscript to dodge a similarity/plagiarism check.

> A [Claude / Agent Skill](https://claude.com/docs): a `SKILL.md` plus scripts an agent can load and run. Drop the folder into your skills directory and ask "tailor my resume to this job" or "format this paper for <journal>."

## Quick start

```bash
python3 scripts/ats_check.py --resume resume.txt --jd job-description.txt --out ats-report.md
```

Standard library only. No install. Reads plain-text resume and job description.

The report gives you the JD's key terms, which are in the resume, which aren't, and structure red flags (missing contact line, missing sections, length, bullets that don't start with a strong verb).

## What's inside

```
SKILL.md                                 # the skill + hard limits
scripts/ats_check.py                     # resume↔JD keyword + structure check
templates/cover-letter.md                # job cover letter structure
templates/research-cover-letter.md       # editor cover letter structure
references/job-application-playbook.md   # honest-tailoring rules
references/journal-submission-checklist.md
examples/                                # sample resume + JD to try it on
```

## Hard limits

- **Tailoring ≠ fabrication.** Rephrase and prioritize real experience; never add a skill you don't have. A genuinely missing qualification is reported, not invented.
- **No plagiarism-check evasion.** No paraphrasing sources to lower a 查重/Similarity score, no generating text the author didn't write.
- **Not a guarantee.** Real ATS software varies; journal rules change. Verify against the live posting and current author guidelines.

## 中文简介

`application-craft` 是一个 Agent Skill，覆盖两条投递链路：求职（按 JD 定制简历 + 写 cover letter）与科研投稿（按目标期刊的投稿要求排版 + 写致编辑信）。`scripts/ats_check.py`（纯标准库）对简历和 JD 做关键词覆盖与结构检查。原则是**只优化和排版真实内容**——不编造经历，也不做"降重/改写骗过查重"这类事；合规的部分照做，学术不端的部分明确拒绝。

## License

MIT
