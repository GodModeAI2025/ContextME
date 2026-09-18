"""Deterministic tests. No model calls, internet, credentials or real user data."""
from __future__ import annotations
import copy
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from contextme import Store, ContextError, canonical, material, load_json, timestamp, now
from install import install

AT = "2026-09-17T12:00:00Z"
OLD = "2026-08-01T12:00:00Z"
DEMO = json.loads((ROOT / "examples/demo-batch.json").read_text(encoding="utf-8"))


def batch(value="high", origin="explicit", confidence=1., date="2026-09-01T12:00:00Z", sid="s1", subject="topic", predicate="priority", context="work", activity="reference"):
    return {"schema_version": 1,
            "entities": [{"id": subject, "kind": "topic", "name": "Thema", "aliases": ["Topic"]}],
            "sources": [{"id": sid, "kind": "statement" if origin == "explicit" else "note", "author": "user", "observed_at": date, "activity": activity}],
            "claims": [{"subject": subject, "predicate": predicate, "value": value, "context": context,
                        "origin": origin, "confidence": confidence, "sources": [sid], "evidence": "Test-only evidence."}]}


def signal_batch(count=1, activity="create", date="2026-09-01T12:00:00Z", actor="user"):
    b = {"schema_version": 1, "entities": [{"id": "topic", "kind": "topic", "name": "Thema"}], "sources": [], "signals": []}
    for i in range(count):
        sid = f"s{i}"
        b["sources"].append({"id": sid, "kind": "note", "author": actor, "activity": activity, "observed_at": date})
        b["signals"].append({"subject": "topic", "context": "work", "source": sid, "confidence": 1., "strength": 1.})
    return b


class ContextTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "vault"
        self.s = Store(self.root)
        self.s.init()
    def tearDown(self):
        self.tmp.cleanup()
    def score(self, scope="work", at=AT):
        return next(r for r in self.s.snapshot(at, scope)["relevance"] if r["subject"] == "topic")

    def test_init_is_idempotent(self):
        original = self.s.read()
        self.s.init()
        self.assertEqual(original, self.s.read())
    def test_demo_roundtrip_and_integrity(self):
        self.s.ingest(DEMO)
        self.assertTrue(self.s.doctor()["ok"])
        self.assertEqual(self.s.doctor()["claims"], 19)
    def test_mobile_private_and_work_are_independent(self):
        self.s.ingest(DEMO)
        r = {(r["subject"], r["context"]): r for r in self.s.snapshot(AT)["relevance"]}
        self.assertEqual(r[("mobile", "work")]["level"], "low")
        self.assertEqual(r[("mobile", "private")]["level"], "high")
        self.assertEqual(r[("ai", "work")]["level"], "high")
    def test_old_role_is_historical_not_deleted(self):
        self.s.ingest(DEMO)
        r = next(r for r in self.s.snapshot(AT)["relevance"] if r["subject"] == "role-mobile")
        self.assertEqual(r["freshness"], "historical")
        self.assertIn("role-mobile", self.s.project(self.s.read())["entities"])
    def test_work_export_excludes_private_project(self):
        self.s.ingest(DEMO)
        serialized = canonical(self.s.snapshot(AT, "work"))
        self.assertNotIn("podcast-project", serialized)
        self.assertNotIn('"context":"private"', serialized)
    def test_duplicate_ingestion_does_not_reinforce_or_advance_revision(self):
        b = signal_batch()
        self.s.ingest(b)
        original = self.s.read()
        score = self.score()["score"]
        self.s.ingest(b)
        self.assertEqual(original, self.s.read())
        self.assertEqual(score, self.score()["score"])
    def test_dry_run_is_not_a_write(self):
        original = self.s.read()
        self.s.ingest(batch(), dry_run=True)
        self.assertEqual(original, self.s.read())
    def test_bad_batch_is_atomic(self):
        b = batch()
        b["claims"][0]["sources"] = ["missing"]
        original = self.s.read()
        with self.assertRaises(ContextError): self.s.ingest(b)
        self.assertEqual(original, self.s.read())
    def test_document_cannot_become_explicit_instruction(self):
        b = batch(); b["sources"][0]["kind"] = "email"
        with self.assertRaises(ContextError): self.s.ingest(b)
    def test_inference_can_be_saved_without_user_confirmation(self):
        self.s.ingest(batch(origin="inferred", confidence=.85))
        c = self.s.snapshot(AT)["claims"][0]
        self.assertEqual(c["origin"], "inferred")
    def test_uncertain_inference_is_pending(self):
        self.s.ingest(batch(origin="inferred", confidence=.3))
        self.assertFalse(self.s.snapshot(AT)["claims"])
        self.assertEqual(len(self.s.reviews()["pending"]), 1)
    def test_review_accepts_pending(self):
        r = self.s.ingest(batch(origin="inferred", confidence=.3))
        self.s.review(r["pending"][0], "accept")
        self.assertEqual(len(self.s.snapshot(AT)["claims"]), 1)
    def test_review_rejects(self):
        r = self.s.ingest(batch(origin="inferred", confidence=.3))
        self.s.review(r["pending"][0], "reject")
        self.assertFalse(self.s.snapshot(AT)["claims"])
        self.assertFalse(self.s.reviews()["pending"])
    def test_explicit_beats_later_inference_and_reports_conflict(self):
        self.s.ingest(batch("high", date=OLD))
        self.s.ingest(batch("low", origin="inferred", sid="s2"))
        snap = self.s.snapshot(AT)
        self.assertEqual(snap["claims"][0]["value"], "high")
        self.assertTrue(snap["conflicts"])
    def test_explicit_correction_beats_older_import(self):
        self.s.ingest(batch("low", sid="new"))
        self.s.ingest(batch("high", date=OLD, sid="old"))
        self.assertEqual(self.s.snapshot(AT)["claims"][0]["value"], "low")
    def test_future_valid_from_is_not_current(self):
        b = batch(); b["claims"][0]["valid_from"] = "2027-01-01"
        self.s.ingest(b)
        self.assertFalse(self.s.snapshot(AT)["claims"])
    def test_ended_assertion_does_not_resurrect_predecessor(self):
        self.s.ingest(batch("old", sid="s1", date=OLD, predicate="description"))
        b = batch("new", sid="s2", predicate="description")
        b["claims"][0]["valid_to"] = "2026-09-10"
        self.s.ingest(b)
        self.assertFalse(self.s.snapshot(AT)["claims"])
    def test_future_observation_is_rejected(self):
        b = batch(date="2099-01-01")
        with self.assertRaises(ContextError): self.s.ingest(b)
    def test_unknown_source_date_does_not_fake_recency(self):
        self.s.ingest(signal_batch(date=None))
        r = self.score()
        self.assertEqual(r["score"], 0)
        self.assertEqual(r["activity"]["unknown_date_signals"], 1)
    def test_passive_mail_is_not_interest(self):
        self.s.ingest(signal_batch(count=20, activity="passive"))
        self.assertEqual(self.score()["score"], 0)
    def test_other_people_activity_does_not_count(self):
        self.s.ingest(signal_batch(actor="other"))
        self.assertEqual(self.score()["score"], 0)
    def test_user_can_read_other_authored_material(self):
        b = signal_batch(activity="read", actor="other")
        b["sources"][0]["actor"] = "user"
        self.s.ingest(b)
        self.assertGreater(self.score()["score"], 0)
    def test_daily_cap_limits_bulk_import(self):
        self.s.ingest(signal_batch(count=100))
        r = self.score(at="2026-09-01T12:00:00Z")
        self.assertEqual(r["activity"]["mass"], 2.)
        self.assertLess(r["score"], 40)
    def test_same_content_hash_is_counted_once(self):
        b = signal_batch(count=2)
        for s in b["sources"]: s["content_sha256"] = "a" * 64
        self.s.ingest(b)
        self.assertEqual(self.score()["activity"]["unique_events"], 1)
    def test_alias_matching_has_word_boundaries(self):
        self.s.ingest(DEMO)
        self.assertEqual(self.s.classify("main", at=AT)["matched_entities"], [])
        self.assertIn("ai", self.s.classify("AI", at=AT)["matched_entities"])
    def test_unknown_material_is_kept_not_discarded(self):
        self.s.ingest(DEMO)
        r = self.s.classify("Ornithologie", at=AT)
        self.assertEqual(r["action"], "keep_in_inbox")
    def test_classification_is_read_only(self):
        self.s.ingest(DEMO)
        old = self.s.read()
        self.s.classify("AI", at=AT)
        self.assertEqual(old, self.s.read())
    def test_semantic_entity_input_is_supported(self):
        self.s.ingest(DEMO)
        r = self.s.classify("Neue automatische Sprachverarbeitung", entities=["ai"], at=AT)
        self.assertEqual(r["matching_mode"], "host_semantic_entities")
        self.assertEqual(r["decision"], "multi_context")
    def test_context_outside_scope_cannot_be_requested(self):
        self.s.ingest(DEMO)
        with self.assertRaises(ContextError):
            self.s.classify("", scope="work", entities=["podcast-project"], at=AT)
    def test_activity_decays_without_erasing_history(self):
        self.s.ingest(signal_batch())
        a = self.score(at="2026-09-01T12:00:00Z")
        b = self.score(at="2027-09-01T12:00:00Z")
        self.assertGreater(a["score"], b["score"])
        self.assertEqual(a["activity"]["unique_events"], b["activity"]["unique_events"])
    def test_explicit_low_priority_overrides_old_activity(self):
        b = signal_batch(10, date=OLD)
        for i,s in enumerate(b["sources"]): s["observed_at"] = f"2026-08-{i+1:02d}T12:00:00Z"
        self.s.ingest(b)
        b = batch("low", sid="priority-now")
        b["entities"][0].pop("aliases")
        self.s.ingest(b)
        self.assertEqual(self.score()["level"], "low")
    def test_priority_pin_does_not_decay(self):
        self.s.ingest(batch("high", predicate="pinned_priority"))
        self.assertEqual(self.score(at="2030-01-01")["score"], 90.)
    def test_sensitive_claim_is_opt_in(self):
        b = batch("private medical detail", predicate="health")
        r = self.s.ingest(b)
        self.assertTrue(r["skipped_sensitive"])
        self.assertNotIn("private medical detail", canonical(self.s.read()))
    def test_sensitive_self_statement_can_be_saved_but_not_exported_by_default(self):
        b = batch("private medical detail", predicate="health")
        self.s.ingest(b, allow_sensitive=True)
        self.assertNotIn("private medical detail", canonical(self.s.snapshot(AT)))
        self.assertIn("private medical detail", canonical(self.s.snapshot(AT, include_sensitive=True)))
    def test_sensitive_inference_is_not_saved_even_with_flag(self):
        b = batch("inferred diagnosis", origin="inferred", predicate="mental_health")
        self.s.ingest(b, allow_sensitive=True)
        self.assertNotIn("inferred diagnosis", canonical(self.s.read()))
    def test_forget_purges_entity_and_generated_views(self):
        self.s.ingest(batch("UNIQUE_PRIVATE_CONTENT", predicate="description"))
        self.s.forget(entity="topic")
        self.assertNotIn("UNIQUE_PRIVATE_CONTENT", canonical(self.s.read()))
        for p in self.root.rglob("*.md"):
            self.assertNotIn("UNIQUE_PRIVATE_CONTENT", p.read_text(encoding="utf-8"))
        self.assertTrue(self.s.doctor()["ok"])
    def test_forget_source_removes_derived_claims_and_blocks_reimport(self):
        b = batch()
        self.s.ingest(b)
        self.s.forget(source="s1")
        self.assertFalse(self.s.snapshot(AT)["claims"])
        with self.assertRaises(ContextError): self.s.ingest(b)
    def test_path_traversal_is_rejected(self):
        b = batch(); b["entities"][0]["id"] = "../outside"
        with self.assertRaises(ContextError): self.s.ingest(b)
    def test_context_cycle_is_rejected(self):
        b = {"schema_version":1, "contexts":[{"id":"c1","label":"A","parent":"c2"},{"id":"c2","label":"B","parent":"c1"}]}
        with self.assertRaises(ContextError): self.s.ingest(b)
    def test_organization_subcontexts_are_scoped(self):
        b = batch(context="work:one")
        b["contexts"] = [{"id":"work:one","label":"One","parent":"work"},{"id":"work:two","label":"Two","parent":"work"}]
        self.s.ingest(b)
        self.assertTrue(self.s.snapshot(AT,"work")["claims"])
        self.assertFalse(self.s.snapshot(AT,"work:two")["claims"])
    def test_material_sha_and_no_mtime_inference(self):
        f = Path(self.tmp.name) / "note.md"; f.write_text("Test", encoding="utf-8")
        m = material(str(f))
        self.assertEqual(m["source"]["content_sha256"], hashlib.sha256(b"Test").hexdigest())
        self.assertIsNone(m["source"]["observed_at"])
        self.assertEqual(m["source"]["activity"], "reference")
    def test_email_reader_preserves_message_id_and_date(self):
        f = Path(self.tmp.name) / "note.eml"
        f.write_text("From: person@example.test\nSubject: Example\nMessage-ID: <id@example.test>\nDate: Tue, 1 Sep 2026 12:00:00 +0000\nContent-Type: text/plain; charset=utf-8\n\nHello", encoding="utf-8")
        m = material(str(f))
        self.assertEqual(m["source"]["canonical_id"], "<id@example.test>")
        self.assertIn("Hello", m["untrusted_material"])
        self.assertTrue(m["source"]["observed_at"].startswith("2026-09-01"))
    def test_html_reader_does_not_include_scripts(self):
        f = Path(self.tmp.name) / "x.html"; f.write_text("<script>BAD</script><p>Good</p>", encoding="utf-8")
        m = material(str(f))
        self.assertNotIn("BAD", m["untrusted_material"])
        self.assertIn("Good", m["untrusted_material"])
    def test_binary_reader_fails_explicitly(self):
        with self.assertRaises(ContextError): material("x.pdf")
    def test_packet_respects_character_budget(self):
        self.s.ingest(DEMO)
        p = self.s.context_packet("work", "KI", 1500, AT)
        self.assertLessEqual(len(canonical(p)), 1500)
        self.assertGreater(p["omitted"], 0)
    def test_lock_prevents_second_writer(self):
        with self.s.locked():
            with self.assertRaises(ContextError): self.s.ingest(batch())
    def test_duplicate_ids_within_batch_are_rejected(self):
        b = batch(); b["entities"].append(copy.deepcopy(b["entities"][0]))
        with self.assertRaises(ContextError): self.s.ingest(b)
    def test_invisible_control_text_is_rejected(self):
        b = batch("abc\u200bdef", predicate="description")
        with self.assertRaises(ContextError): self.s.ingest(b)
    def test_cli_can_load_workspace_and_report_doctor(self):
        p = subprocess.run([sys.executable, str(ROOT / "scripts/contextme.py"), "--workspace", str(self.root), "doctor"], capture_output=True,text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertTrue(json.loads(p.stdout)["ok"])
    def test_installer_targets_both_hosts_in_sandbox(self):
        home = Path(self.tmp.name) / "home"
        r = install("both", home)
        self.assertEqual(len(r["installed"]), 2)
        self.assertTrue((home / ".agents/skills/contextme/SKILL.md").is_file())
        self.assertTrue((home / ".claude/skills/contextme/SKILL.md").is_file())
    def test_interview_covers_all_dimensions_and_limits_questions(self):
        r = self.s.interview()
        self.assertEqual(len(r["coverage"]), 24)
        self.assertLessEqual(len(r["suggested_questions"]), 3)
    def test_pending_hypothesis_not_served_as_context_membership(self):
        self.s.ingest(batch(origin="inferred", confidence=.4))
        self.assertFalse(self.s.snapshot(AT)["entities"])
        self.assertFalse(self.s.classify("Thema", at=AT)["matched_entities"])
        self.assertTrue(self.s.project(self.s.read())["claims"])
    def test_rejected_hypothesis_not_served_as_context_membership(self):
        report = self.s.ingest(batch(origin="inferred", confidence=.8))
        self.s.review(report["accepted"][0], "reject", "Not my interest")
        self.assertFalse(self.s.snapshot(AT)["entities"])
    def test_scoped_sources_do_not_expose_mixed_source_metadata(self):
        b = batch()
        b["sources"][0]["title"] = "PRIVATE_TITLE_WITH_WORK_FRAGMENT"
        b["sources"][0]["uri"] = "file:///private/personal-note.md"
        self.s.ingest(b)
        scoped = self.s.snapshot(AT, "work")
        self.assertTrue(scoped["sources"])
        self.assertNotIn("PRIVATE_TITLE_WITH_WORK_FRAGMENT", canonical(scoped))
        self.assertNotIn("file:///private", canonical(scoped))
        self.assertIn("PRIVATE_TITLE_WITH_WORK_FRAGMENT", canonical(self.s.snapshot(AT)))
    def test_schema_version_mismatch_is_rejected(self):
        with self.assertRaises(ContextError): self.s.ingest({"schema_version": 999})


if __name__ == "__main__":
    unittest.main(verbosity=2)
