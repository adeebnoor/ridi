#!/usr/bin/env python3
import importlib.util
from pathlib import Path
from decimal import Decimal
p=Path(__file__).with_name('analyze_table16b.py')
spec=importlib.util.spec_from_file_location('m',p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
assert m.ccn('12345')=='012345'
assert m.ccn('12345.0')=='012345'
assert m.dec('1.0023')==Decimal('1.0023')
f={(2024,'000001'):Decimal('0.9990'),(2025,'000001'):Decimal('1.0010'),(2024,'000002'):Decimal('1.0100'),(2025,'000002'):Decimal('1.0100')}
s=m.summarize_factor_changes({'000001','000002'},2024,2025,f)
assert s['n_complete']==2 and s['factor_changed']==1 and s['exact_factor_unchanged']==1
assert s['cross_below1_to_ge1']==1 and s['cross_ge1_to_below1']==0
print('PASS synthetic tests')
