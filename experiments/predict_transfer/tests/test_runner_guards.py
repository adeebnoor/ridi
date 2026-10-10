"""Synthetic guard tests only. No real answers or model weights."""
import ast, copy, importlib.util, json, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('runner',ROOT/'run_predict.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)

class Guards(unittest.TestCase):
    def test_retry_preserves_counts(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td)
            out,status=r.begin_attempt(base,'qwen3-4b','nq',1,'same')
            with self.assertRaises(r.ProtocolError):r.begin_attempt(base,'qwen3-4b','nq',1,'same')
            with self.assertRaises(r.ProtocolError):r.begin_attempt(base,'qwen3-4b','nq',2,'same')
            r.finish_failure(out,status,MemoryError())
            with self.assertRaises(r.ProtocolError):r.begin_attempt(base,'qwen3-4b','nq',2,'different')
            out2,status2=r.begin_attempt(base,'qwen3-4b','nq',2,'same')
            r.finish_failure(out2,status2,RuntimeError('CUDA out of memory'))
            out3,status3=r.begin_attempt(base,'qwen3-4b','nq',3,'same')
            r.finish_failure(out3,status3,MemoryError())
            with self.assertRaises(r.ProtocolError):r.begin_attempt(base,'qwen3-4b','nq',4,'same')
    def test_success_and_blocked_never_retry(self):
        for state in ['succeeded','blocked']:
            with tempfile.TemporaryDirectory() as td:
                out,s=r.begin_attempt(Path(td),'qwen3-8b','fever',1,'same')
                s['status']=state;s['failure_kind']='protocol_or_code';r.atomic_json(out/'attempt_status.json',s)
                with self.assertRaises(r.ProtocolError):r.begin_attempt(Path(td),'qwen3-8b','fever',2,'same')
    def test_draw_in_configuration_hash(self):
        a=r.configuration_sha256({'files':{}},{'key':'qwen3-4b'},'nq','A')
        b=r.configuration_sha256({'files':{}},{'key':'qwen3-4b'},'nq','B')
        self.assertNotEqual(a,b)
    def test_hardware_gate(self):
        with self.assertRaises(r.ProtocolError):r.verify_gpu_memory([80*(1<<30)],2)
        with self.assertRaises(r.ProtocolError):r.verify_gpu_memory([40*(1<<30)]*2,2)
        r.verify_gpu_memory([80*(1<<30)]*2,2)
    def test_failure_classes(self):
        self.assertFalse(r.technical_failure(r.ProtocolError('mismatch')))
        self.assertFalse(r.technical_failure(ValueError('code defect')))
        self.assertTrue(r.technical_failure(r.InfrastructureInterrupted()))
    def test_generation_requires_publication(self):
        self.assertFalse((ROOT/'LOCK.json').exists())
        with self.assertRaises(SystemExit):r.verify_lock()
        with self.assertRaises(r.ProtocolError):r.verify_publication_receipt({})
    def test_zip_traversal_rejected(self):
        import io,zipfile
        b=io.BytesIO()
        with zipfile.ZipFile(b,'w') as z:z.writestr('../outside','bad')
        b.seek(0)
        with tempfile.TemporaryDirectory() as td,zipfile.ZipFile(b) as z:
            with self.assertRaises(r.ProtocolError):r.safe_extract(z,Path(td))

if __name__=='__main__': unittest.main()
