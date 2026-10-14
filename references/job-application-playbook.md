# Job-application playbook

How to use `ats_check.py` output well, and the rules of honest tailoring.

## The one rule

Tailoring means **choosing what to surface and how to phrase it** — from experience that actually happened. If a required qualification is genuinely absent, that's information. Address it in the cover letter or accept the role isn't a fit. Do not invent it.

## Reading the coverage report

- **High-coverage terms** → already in your resume. Make sure they're in *prominent* spots (top bullets, skills line), not buried.
- **Missing terms, genuinely held** → reword an existing bullet so the term appears naturally. "Worked on the payments backend" → "Built and scaled the payments backend (Stripe integration)".
- **Missing terms, not held** → do not add. Decide: skip, or address honestly in ¶3 of the cover letter.

## Bullets that get read

Format: **strong verb + what + scale/outcome**.

- Weak: "Responsible for managing the database."
- Strong: "Cut p99 query latency 40% by indexing the events table and moving hot reads to a cache."

Numbers turn claims into evidence. One metric per bullet where it's honest.

## Structure checklist

- Contact line at top (email, phone, one profile link).
- Reverse-chronological experience; most relevant role first if the chronology allows a summary section.
- A skills line that mirrors the JD's *language* (their words, your truth).
- One page unless senior/academic.

## Before you send

- [ ] Runs through `ats_check.py` without missing contact/section red flags.
- [ ] Every bullet maps to something you actually did.
- [ ] No skill listed that you can't discuss for two minutes.
- [ ] Cover letter's ¶1 references the specific company/role.
- [ ] File name is `Firstname_Lastname_Resume.pdf`, not `resume_final_v3.pdf`.
