from pathlib import Path
import importlib.util
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]

def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod

sel = load("protocol_selection", "tools/protocol_selection.py")
chk = load("eligibility_check", "tools/eligibility_check.py")
bun = load("make_raw_bundle", "tools/make_raw_bundle.py")


def base_row(case_id="CASE_A"):
    return {
        "case_id": case_id,
        "source_a_sha256": "a"*64,
        "offline_endpoint_a_sha256": "1"*64,
        "source_ref_a": "ref:a",
        "source_b_sha256": "b"*64,
        "offline_endpoint_b_sha256": "2"*64,
        "source_ref_b": "ref:b",
        "evaluation_definition_id": "eval:v1",
        "evaluation_definition_sha256": "e"*64,
        "original_support_requirement_status": "AUTHORITATIVE_1",
        "offline_endpoint_present": "TRUE",
        "m1_representable": "TRUE",
        "a1_preexisting_authority_available": "TRUE",
        "i1_compatible": "TRUE",
        "no_consequential_execution": "TRUE",
        "prior_public_exposure": "FALSE",
        "outcome_independent_eligibility_attestation": "TRUE",
        "eligibility_rationale": "eligible by frozen pre-selection facts",
    }


class ProtocolInfraTests(unittest.TestCase):
    def test_seed_commitment_is_deterministic(self):
        seed = "0" * 64
        self.assertEqual(sel.seed_commitment("ADEEB", seed), sel.seed_commitment("ADEEB", seed))
        self.assertNotEqual(sel.seed_commitment("ADEEB", seed), sel.seed_commitment("KRZYSZTOF", seed))

    def test_combined_order_is_fixed(self):
        a = "1" * 64
        k = "2" * 64
        pool = "3" * 64
        self.assertNotEqual(sel.combined_hash(a, k, pool), sel.combined_hash(k, a, pool))

    def test_unknown_support_requirement_is_rejected(self):
        row = base_row()
        row["original_support_requirement_status"] = "UNKNOWN"
        audit, pool = chk.evaluate([row], "f"*64)
        self.assertEqual(audit[0]["eligibility_status"], "REJECT")
        self.assertIn("ORIGINAL_SUPPORT_REQUIREMENT_UNKNOWN", audit[0]["reason_codes"])
        self.assertEqual(pool, [])

    def test_authoritative_gt1_is_rejected(self):
        row = base_row()
        row["original_support_requirement_status"] = "AUTHORITATIVE_GT1"
        audit, pool = chk.evaluate([row], "f"*64)
        self.assertEqual(audit[0]["eligibility_status"], "REJECT")
        self.assertIn("AUTHORITATIVE_SUPPORT_REQUIREMENT_GT1", audit[0]["reason_codes"])
        self.assertEqual(pool, [])

    def test_reversed_pair_is_duplicate(self):
        first = base_row("CASE_A")
        second = base_row("CASE_B")
        second["source_a_sha256"], second["source_b_sha256"] = first["source_b_sha256"], first["source_a_sha256"]
        second["offline_endpoint_a_sha256"], second["offline_endpoint_b_sha256"] = first["offline_endpoint_b_sha256"], first["offline_endpoint_a_sha256"]
        second["source_ref_a"], second["source_ref_b"] = first["source_ref_b"], first["source_ref_a"]
        audit, pool = chk.evaluate([first, second], "f"*64)
        statuses = {r["case_id"]: (r["eligibility_status"], r["reason_codes"]) for r in audit}
        self.assertEqual(statuses["CASE_A"][0], "ACCEPT")
        self.assertEqual(statuses["CASE_B"][0], "REJECT")
        self.assertIn("DUPLICATE_PAIR_REGISTRATION", statuses["CASE_B"][1])
        self.assertEqual(len(pool), 1)

    def test_shared_one_arm_is_not_duplicate(self):
        first = base_row("CASE_A")
        second = base_row("CASE_B")
        second["source_b_sha256"] = "c"*64
        second["offline_endpoint_b_sha256"] = "3"*64
        second["source_ref_b"] = "ref:c"
        audit, pool = chk.evaluate([first, second], "f"*64)
        self.assertEqual([r["eligibility_status"] for r in audit], ["ACCEPT", "ACCEPT"])
        self.assertEqual(len(pool), 2)
        self.assertNotEqual(pool[0]["pair_fingerprint"], pool[1]["pair_fingerprint"])

    def test_pair_metadata_conflict_rejects_both(self):
        first = base_row("CASE_A")
        second = base_row("CASE_B")
        second["source_a_sha256"], second["source_b_sha256"] = first["source_b_sha256"], first["source_a_sha256"]
        second["offline_endpoint_a_sha256"], second["offline_endpoint_b_sha256"] = first["offline_endpoint_b_sha256"], first["offline_endpoint_a_sha256"]
        second["source_ref_a"], second["source_ref_b"] = first["source_ref_b"], first["source_ref_a"]
        second["prior_public_exposure"] = "TRUE"
        audit, pool = chk.evaluate([first, second], "f"*64)
        self.assertTrue(all(r["eligibility_status"] == "REJECT" for r in audit))
        self.assertTrue(all("DUPLICATE_PAIR_METADATA_CONFLICT" in r["reason_codes"] for r in audit))
        self.assertEqual(pool, [])

    def test_pool_requires_fixed_eval_hash_and_fingerprint(self):
        row = base_row()
        audit, pool = chk.evaluate([row], "f"*64)
        self.assertEqual(audit[0]["eligibility_status"], "ACCEPT")
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "eligible_pool.tsv"
            lines = ["\t".join(sel.POOL_COLUMNS)]
            lines.append("\t".join(pool[0][c] for c in sel.POOL_COLUMNS))
            p.write_bytes(("\n".join(lines) + "\n").encode())
            ids, sha = sel.parse_pool(p)
            self.assertEqual(ids, ["CASE_A"])
            self.assertEqual(len(sha), 64)

    def test_registry_schema_lf_sorted_ascii(self):
        r1 = base_row("CASE_A")
        r2 = base_row("CASE_B")
        r2["source_b_sha256"] = "c"*64
        r2["offline_endpoint_b_sha256"] = "3"*64
        r2["source_ref_b"] = "ref:c"
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "candidate_registry.tsv"
            lines = ["\t".join(chk.REGISTRY_COLUMNS)]
            for row in (r1, r2):
                lines.append("\t".join(row[c] for c in chk.REGISTRY_COLUMNS))
            p.write_bytes(("\n".join(lines) + "\n").encode())
            rows, sha = chk.parse_registry(p)
            self.assertEqual([r["case_id"] for r in rows], ["CASE_A", "CASE_B"])
            self.assertEqual(len(sha), 64)

    def test_selection_is_reproducible(self):
        ids = ["CASE_A", "CASE_B", "CASE_C"]
        c = "4" * 64
        a, scores1 = sel.select_case(ids, c)
        b, scores2 = sel.select_case(ids, c)
        self.assertEqual(a, b)
        self.assertEqual(scores1, scores2)

    def test_raw_bundle_is_byte_deterministic(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "src"
            root.mkdir()
            (root / "a.txt").write_bytes(b"alpha\n")
            sub = root / "logs"
            sub.mkdir()
            (sub / "b.json").write_bytes(b'{"ok":true}\n')
            z1 = Path(d) / "one.zip"
            z2 = Path(d) / "two.zip"
            bun.make_zip(root, z1)
            bun.make_zip(root, z2)
            self.assertEqual(z1.read_bytes(), z2.read_bytes())
            with zipfile.ZipFile(z1) as z:
                self.assertIn("SHA256_MANIFEST.tsv", z.namelist())


if __name__ == "__main__":
    unittest.main()
