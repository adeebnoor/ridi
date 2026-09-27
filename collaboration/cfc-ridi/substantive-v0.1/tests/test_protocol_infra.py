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

m = load("protocol_selection", "tools/protocol_selection.py")
b = load("make_raw_bundle", "tools/make_raw_bundle.py")


class ProtocolInfraTests(unittest.TestCase):
    def test_seed_commitment_is_deterministic(self):
        seed = "0" * 64
        self.assertEqual(m.seed_commitment("ADEEB", seed), m.seed_commitment("ADEEB", seed))
        self.assertNotEqual(m.seed_commitment("ADEEB", seed), m.seed_commitment("KRZYSZTOF", seed))

    def test_combined_order_is_fixed(self):
        a = "1" * 64
        k = "2" * 64
        pool = "3" * 64
        self.assertNotEqual(m.combined_hash(a, k, pool), m.combined_hash(k, a, pool))

    def test_pool_requires_schema_lf_sorted_ascii(self):
        header = "\t".join(m.POOL_COLUMNS) + "\n"
        row_a = "\t".join([
            "CASE_A", "a"*64, "b"*64, "ref:a", "ref:b", "eval:v1",
            "TRUE", "1", "FALSE", "eligible"
        ]) + "\n"
        row_b = "\t".join([
            "CASE_B", "c"*64, "d"*64, "ref:c", "ref:d", "eval:v1",
            "TRUE", "NONE_SPECIFIED", "UNKNOWN", "eligible"
        ]) + "\n"
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "eligible_pool.tsv"
            p.write_bytes((header + row_a + row_b).encode())
            ids, sha = m.parse_pool(p)
            self.assertEqual(ids, ["CASE_A", "CASE_B"])
            self.assertEqual(len(sha), 64)

    def test_pool_rejects_original_support_requirement_gt_one(self):
        row = {
            "case_id": "CASE_A",
            "source_a_sha256": "a"*64,
            "source_b_sha256": "b"*64,
            "source_ref_a": "a",
            "source_ref_b": "b",
            "evaluation_definition_id": "e",
            "offline_endpoint_present": "TRUE",
            "original_support_requirement": "2",
            "prior_public_exposure": "FALSE",
            "eligibility_rationale": "x",
        }
        with self.assertRaises(ValueError):
            m.validate_pool_rows([row])

    def test_selection_is_reproducible(self):
        ids = ["CASE_A", "CASE_B", "CASE_C"]
        c = "4" * 64
        a, scores1 = m.select_case(ids, c)
        b2, scores2 = m.select_case(ids, c)
        self.assertEqual(a, b2)
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
            b.make_zip(root, z1)
            b.make_zip(root, z2)
            self.assertEqual(z1.read_bytes(), z2.read_bytes())
            with zipfile.ZipFile(z1) as z:
                self.assertIn("SHA256_MANIFEST.tsv", z.namelist())


if __name__ == "__main__":
    unittest.main()
