#!/usr/bin/env python3
from evaluators import EVALUATORS
def check(text,expect):
    got={k:f(text,"mc",["A","B","C","D"],["alpha","beta","gamma","delta"]) for k,f in EVALUATORS.items()}
    assert got==expect,(text,got,expect)
check("Reasoning.\nFINAL: C",{"E1":"C","E2":"C","E3":"C","E4":"C","E5":"C"})
check("I think option A first, but after checking, answer is B.\nFINAL: B",{"E1":"B","E2":"A","E3":"B","E4":"B","E5":"B"})
check("Reasoning only.\nFINAL: gamma",{"E1":None,"E2":None,"E3":None,"E4":None,"E5":"C"})
b={k:f("No, because evidence says otherwise.\nFINAL: yes","bool",["yes","no"],["yes","no"]) for k,f in EVALUATORS.items()}
assert b["E1"]=="yes" and b["E2"]=="no" and b["E3"]=="yes" and b["E4"]=="yes" and b["E5"]=="yes",b
print("EVALUATOR_TESTS_PASS")
