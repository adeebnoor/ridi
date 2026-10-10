#!/usr/bin/env python3
"""Create the scientific lock only after a verified OSF registration receipt."""
import argparse, json, re
from pathlib import Path
import run_predict as runner

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--registration-receipt', type=Path, required=True)
    a = ap.parse_args()
    dest = runner.HERE / 'LOCK.json'
    runner.require(not dest.exists(), 'LOCK already exists; refusing overwrite')
    receipt = json.loads(a.registration_receipt.read_text())
    runner.require(receipt.get('study') == runner.STUDY, 'registration study mismatch')
    runner.require(receipt.get('verified_public_registration') is True, 'public registration not verified')
    runner.require(bool(re.fullmatch(r'https://osf\.io/[a-z0-9]+/?', receipt.get('registration_url', ''))),
                   'OSF registration URL required')
    runner.require(receipt.get('registration_url', '').rstrip('/').rsplit('/',1)[-1]
                   not in {'whjbs','txwdv','ms4w8'}, 'new PREDICT registration required')
    runner.require(bool(receipt.get('registered_at_utc')), 'registration timestamp required')
    # The verified OSF download must have matched this exact registration text.
    prereg = runner.HERE/'prereg/OSF_Preregistration_RIDI-PREDICT-v1.md'
    runner.require(receipt.get('preregistration_md_sha256') == runner.sha_file(prereg),
                   'filed preregistration text differs from prepared text')
    lock = {'study': runner.STUDY, 'created_at_utc': runner.utc_now(),
            'files': {n:runner.sha_file(runner.HERE/n) for n in sorted(runner.LOCK_FILES)},
            'sealed_key_sha256':runner.SEALED_KEY_SHA,
            'registration_receipt':receipt,
            'parent_science_commit':'869abda18a17ba528ecfcddcb4461914b8b113c1'}
    # Exclusive creation preserves the no-overwrite gate.
    with dest.open('x', encoding='utf-8') as f:
        json.dump(lock,f,indent=2,sort_keys=True);f.write('\n')
    runner.verify_lock()
    print('LOCK_CREATED', runner.sha_file(dest))
    print('Publish this LOCK on GitHub and OSF, verify both, and record PUBLICATION_RECEIPT.json before generation.')

if __name__ == '__main__': main()
