from pathlib import Path
import importlib.util
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("protocol_selection", ROOT / "tools" / "protocol_selection.py")
m = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(m)


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

    def test_pool_requires_lf_sorted_ascii(self):
        good = (
            "case_id\tsource_a_sha256\n"
            "CASE_A\t" + "a" * 64 + "\n"
            "CASE_B\t" + "b" * 64 + "\n"
        ).encode()
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "eligible_pool.tsv"
            p.write_bytes(good)
            ids, sha = m.parse_pool(p)
            self.assertEqual(ids, ["CASE_A", "CASE_B"])
            self.assertEqual(len(sha), 64)

    def test_selection_is_reproducible(self):
        ids = ["CASE_A", "CASE_B", "CASE_C"]
        c = "4" * 64
        a, scores1 = m.select_case(ids, c)
        b, scores2 = m.select_case(ids, c)
        self.assertEqual(a, b)
        self.assertEqual(scores1, scores2)


if __name__ == "__main__":
    unittest.main()
