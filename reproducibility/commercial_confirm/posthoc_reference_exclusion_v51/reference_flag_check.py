#!/usr/bin/env python3
"""Check (v53) that the 174 Natural Questions items retained in scores_commercial.csv are exactly the questions that the
frozen reference file marks has_reference = false, and exactly the questions absent from the open-weight score table.
Usage (run from 03_Source_Data):  python commercial_confirm/posthoc_reference_exclusion_v51/reference_flag_check.py <holdout_1500_gold.jsonl>
The reference file is part of the frozen RIDI-CONFIRM inputs and is not distributed in this package; its SHA-256 is recorded below and in the registered addendum.
No model call; changes no frozen file."""
import csv, hashlib, json, sys
gold_path = sys.argv[1]
g = [json.loads(l) for l in open(gold_path, encoding='utf8')]
no_ref = {(r['dataset'], r['qid']) for r in g if not r['has_reference']}
empty = {(r['dataset'], r['qid']) for r in g if not r.get('gold')}
allq = {(r['dataset'], r['qid']) for r in g}
ow = {(r['dataset'], r['qid']) for r in csv.DictReader(open('holdout/scores_W_AND_H3_D_REAL.csv', encoding='utf8'))}
cells = [r for r in csv.DictReader(open('commercial_confirm/scores_commercial.csv', encoding='utf8')) if (r['dataset'], r['qid']) in no_ref]
out = {
 'gold_file_sha256': hashlib.sha256(open(gold_path, 'rb').read()).hexdigest(),
 'questions_in_gold_file': len(g),
 'has_reference_false': len(no_ref), 'datasets_of_has_reference_false': sorted({d for d, _ in no_ref}),
 'has_reference_false_equals_empty_gold': no_ref == empty,
 'questions_absent_from_open_weight_table': len(allq - ow),
 'absent_set_equals_has_reference_false_set': (allq - ow) == no_ref,
 'commercial_cells_for_these_questions': len(cells),
 'commercial_cells_scored_correct': sum(int(r['correct']) for r in cells),
 'qids_has_reference_false': sorted(q for _, q in no_ref)}
print(json.dumps(out, indent=1))
