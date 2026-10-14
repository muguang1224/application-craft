#!/usr/bin/env python3
"""ats_check — compare a resume against a job description.

Extracts the key terms from a job description, reports which appear in the
resume and which don't, and flags structural problems (missing contact info,
missing sections, length, weak bullet starts). Guidance, not a guarantee —
real ATS software varies. Standard library only.

Usage:
    python3 ats_check.py --resume resume.txt --jd jd.txt --out ats-report.md
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter

STOP = set("""
a an and or the to of in on at for with as by from is are be been being this that these those
you your we our they their he she it its i me my will would should could can may might must
do does did have has had not no nor so if then than too very just also into over under about
who whom which what when where why how all any both each few more most other some such only own
same s t don now new use used using work working role position job candidate ideal you'll we're
experience experiences year years team teams strong ability able excellent good great plus etc
responsibilities requirements qualifications preferred required must-have nice across within
including include includes well like help support build building develop developing
""".split())

STRONG_VERBS = set("""
led lead leads built build builds build designed design designs architected developed develop
develops shipped ship ships launched launch launches created create creates drove drive drives
owned own owns managed manage manages delivered deliver delivers improved improve improves
reduced reduce reduces increased increase increases scaled scale scales implemented implement
implemented migrated migrate migrates automated automate automates optimized optimize optimizes
spearheaded founded established grew grow grows wrote write writes authored designed
""".split())


def read(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def singular(w: str) -> str:
    if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
        return w[:-1]
    return w


def tokens(text: str) -> list[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.\-]*", text.lower())
    return [w for w in words if len(w) > 2 and not w.isdigit()]


def extract_keywords(jd: str, top: int = 30) -> list[tuple[str, int]]:
    toks = tokens(jd)
    uni = Counter(w for w in toks if w not in STOP)
    score: Counter = Counter({w: c for w, c in uni.items() if c >= 2})
    # bigrams within a line only (avoid "engineer payments" across a line break)
    bi = Counter()
    for ln in jd.splitlines():
        lw = [w for w in tokens(ln) if w not in STOP]
        for a, b in zip(lw, lw[1:]):
            bi[f"{a} {b}"] += 1
    for phrase, c in bi.items():
        if c >= 2:
            score[phrase] = c + 1  # slight boost to multiword signals
    return score.most_common(top)


def present(phrase: str, resume_set: set[str]) -> bool:
    return all(singular(w) in resume_set for w in phrase.split())


def structure_checks(resume: str) -> list[str]:
    notes = []
    low = resume.lower()
    if not re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", resume):
        notes.append("No email address found — recruiters need a contact line.")
    if not re.search(r"(\+?\d[\d\s().-]{7,}\d)", resume):
        notes.append("No phone number found (optional, but common).")
    if not re.search(r"(linkedin\.com|github\.com|gitlab\.com|https?://)", low):
        notes.append("No profile/portfolio link (LinkedIn, GitHub, site).")
    for section in ("experience", "education", "skill", "project"):
        if section not in low:
            notes.append(f"No obvious '{section}' section.")
    words = len(resume.split())
    pages = words / 500
    if words > 0:
        notes.append(f"Length: ~{words} words (~{pages:.1f} pages at 500 wpp).")
    if words > 1200:
        notes.append("Long for a resume — trim unless it's a CV/academic context.")
    return notes


def bullet_check(resume: str) -> tuple[int, int]:
    bullets = [ln.strip() for ln in resume.splitlines()
               if re.match(r"^\s*[-•*·]\s+", ln)]
    strong = 0
    for b in bullets:
        body = re.sub(r"^[-•*·]\s+", "", b).strip()
        if not body:
            continue
        first = re.sub(r"[^a-zA-Z]", "", body.split()[0]).lower()
        if singular(first) in STRONG_VERBS:
            strong += 1
    return len(bullets), strong


def render(resume, jd, keywords, matched, missing, notes, bullets, strong) -> str:
    rate = (100 * len(matched) / len(keywords)) if keywords else 0
    out = ["# Resume ↔ job-description check", ""]
    out.append(f"Keyword coverage: **{len(matched)}/{len(keywords)} ({rate:.0f}%)**")
    out.append("")
    out.append("> Guidance only — real ATS software varies. Tailor by reordering "
               "and rewording *real* experience; never add a skill you don't have.")
    out.append("")
    out.append("## Terms the JD emphasizes — in your resume")
    out.append("")
    out.append(", ".join(f"`{k}`" for k, _ in matched) or "_none_")
    out.append("")
    out.append("## Terms the JD emphasizes — missing")
    out.append("")
    out.append(", ".join(f"`{k}`" for k, _ in missing) or "_none — good coverage_")
    out.append("")
    out.append("## Structure")
    out.append("")
    for n in notes:
        out.append(f"- {n}")
    if bullets:
        pct = 100 * strong / bullets
        out.append(f"- Bullets: {bullets}, {strong} ({pct:.0f}%) start with a strong action verb.")
    else:
        out.append("- No bullet lines detected — resumes read best as concise bullets.")
    out.append("")
    out.append("## How to act on this")
    out.append("")
    out.append("1. For real experience that overlaps a missing term, reword the bullet so the term appears naturally.")
    out.append("2. A missing term you genuinely lack is *information*, not a gap to fake — decide whether to address it in the cover letter.")
    out.append("3. Lead bullets with a strong verb + a number. See `templates/cover-letter.md`.")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Compare a resume to a job description.")
    ap.add_argument("--resume", required=True)
    ap.add_argument("--jd", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--top", type=int, default=30)
    args = ap.parse_args(argv)

    resume = read(args.resume)
    jd = read(args.jd)
    keywords = extract_keywords(jd, args.top)
    resume_set = {singular(w) for w in tokens(resume)}
    matched = [(k, c) for k, c in keywords if present(k, resume_set)]
    missing = [(k, c) for k, c in keywords if not present(k, resume_set)]
    notes = structure_checks(resume)
    bullets, strong = bullet_check(resume)

    report = render(resume, jd, keywords, matched, missing, notes, bullets, strong)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"coverage {len(matched)}/{len(keywords)} -> {args.out}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
