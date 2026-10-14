"""Test suite for application-craft. Zero dependencies — runs with either:

    python3 -m unittest discover -s tests
    pytest tests/
"""
import importlib.util
import os
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
EX = os.path.join(REPO, "examples")

_spec = importlib.util.spec_from_file_location("ac_ats", os.path.join(REPO, "scripts", "ats_check.py"))
ats = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ats)


def write(tmp, name, content):
    path = os.path.join(tmp, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path


RESUME = """Jane Doe
jane@example.com · +1 555 010 0000 · github.com/janedoe

EXPERIENCE
- Built and scaled the distributed systems behind payments, cutting p99 latency 40%
- Led migration from a monolith to services

EDUCATION
BSc Computer Science

SKILLS
Python, PostgreSQL, Docker
"""

JD = """Senior Backend Engineer — payments platform

Requirements
- Strong Python programming.
- Experience with distributed systems.
- Deep distributed systems knowledge.
- Experience with Kubernetes. Hands-on Kubernetes required.
- Backend experience: 5+ years shipping production services.
"""


class KeywordTests(unittest.TestCase):
    def test_extracts_repeated_terms(self):
        kws = dict(ats.extract_keywords(JD, top=20))
        self.assertIn("kubernetes", kws)          # appears twice
        self.assertIn("distributed systems", kws)  # repeated bigram

    def test_single_mention_is_not_a_keyword(self):
        # "python" appears once, below the frequency threshold
        kws = dict(ats.extract_keywords(JD, top=40))
        self.assertNotIn("python", kws)

    def test_bigrams_within_line(self):
        kws = dict(ats.extract_keywords(JD, top=30))
        self.assertTrue(any(" " in k for k in kws), "expected at least one bigram")

    def test_plural_matches_singular(self):
        resume_set = {ats.singular(w) for w in ats.tokens("Built APIs and services")}
        self.assertTrue(ats.present("api", resume_set))


class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def test_matched_and_missing_partition(self):
        r = write(self.tmp, "r.txt", RESUME)
        j = write(self.tmp, "j.txt", JD)
        resume_set = {ats.singular(w) for w in ats.tokens(ats.read(r))}
        kws = [k for k, _ in ats.extract_keywords(ats.read(j), 30)]
        matched = [k for k in kws if ats.present(k, resume_set)]
        missing = [k for k in kws if not ats.present(k, resume_set)]
        self.assertTrue(matched)                                  # resume covers some JD terms
        self.assertIn("kubernetes", missing)                      # and lacks others
        self.assertEqual(set(matched) & set(missing), set())      # no term in both
        self.assertEqual(len(matched) + len(missing), len(kws))   # every keyword accounted for


class StructureTests(unittest.TestCase):
    def test_flags_missing_contact(self):
        notes = ats.structure_checks("EXPERIENCE\n- did a thing\nEDUCATION\nBSc\nSKILLS\nPython")
        self.assertTrue(any("email" in n.lower() for n in notes))
        self.assertTrue(any("link" in n.lower() for n in notes))

    def test_flags_missing_section(self):
        notes = ats.structure_checks("jane@example.com\n+1 555 010 0000\nhttps://x.dev\nSKILLS\nPython")
        self.assertTrue(any("'experience'" in n for n in notes))

    def test_clean_resume_has_few_notes(self):
        notes = ats.structure_checks(RESUME)
        self.assertFalse(any("email" in n.lower() for n in notes))
        self.assertFalse(any("phone" in n.lower() for n in notes))

    def test_length_reported(self):
        notes = ats.structure_checks(RESUME)
        self.assertTrue(any("Length" in n for n in notes))


class BulletTests(unittest.TestCase):
    def test_counts_strong_bullets(self):
        total, strong = ats.bullet_check(RESUME)
        self.assertEqual(total, 2)
        self.assertEqual(strong, 2)   # "Built" and "Led" are strong verbs

    def test_weak_bullet_not_counted(self):
        total, strong = ats.bullet_check("- Responsible for the database\n- Built a thing")
        self.assertEqual(total, 2)
        self.assertEqual(strong, 1)

    def test_no_bullets(self):
        self.assertEqual(ats.bullet_check("just prose, no bullets"), (0, 0))


class EndToEndTests(unittest.TestCase):
    def test_runs_on_examples(self):
        out = os.path.join(tempfile.mkdtemp(), "report.md")
        rc = ats.main(["--resume", os.path.join(EX, "resume.example.txt"),
                       "--jd", os.path.join(EX, "jd.example.txt"),
                       "--out", out])
        self.assertEqual(rc, 0)
        with open(out, encoding="utf-8") as f:
            report = f.read()
        self.assertIn("Keyword coverage", report)
        self.assertIn("How to act on this", report)
        self.assertIn("Guidance only", report)


if __name__ == "__main__":
    unittest.main(verbosity=2)
