# GPU EXECUTION RUNBOOK — JKSUCIS

Pinned execution commit: `1a92ec909426154c439ed0e4f5254d2f662ae760`
Primary hardware: one NVIDIA A100-SXM4-80GB per model job.

## Environment

```bash
git clone --branch promotion-jksucis-evaluator https://github.com/adeebnoor/ridi.git jks-study
cd jks-study
git checkout 1a92ec909426154c439ed0e4f5254d2f662ae760
python -m pip install --upgrade pip
python -m pip install --index-url https://download.pytorch.org/whl/cu128 torch==2.11.0
grep -v '^torch==' promotion_study/requirements.txt > /tmp/jks-req.txt
python -m pip install -r /tmp/jks-req.txt
```

## Pre-output checks

```bash
cd promotion_study
python freeze_inputs.py
python test_evaluators.py
python -m py_compile run_evaluator_study.py
python -m py_compile analyse_evaluator_study.py
nvidia-smi
```

## Model jobs

Each model/item is generated once at batch size 1. All E1-E5 evaluators consume the same saved raw output.

```bash
python run_evaluator_study.py --model qwen25_3b --out /tmp/jks-qwen --emit-zip-base64
```

```bash
python run_evaluator_study.py --model phi35_mini --out /tmp/jks-phi --emit-zip-base64
```

```bash
python run_evaluator_study.py --model smollm2_17b --out /tmp/jks-smol --emit-zip-base64
```

Recover and hash all three raw JSONLs before aggregate analysis.

## Locked analysis

```bash
python analyse_evaluator_study.py   qwen25_3b_raw.jsonl phi35_mini_raw.jsonl smollm2_17b_raw.jsonl   --out JKSUCIS_AGGREGATE.json
```

Primary after Amendment 1:
1. evaluator-specification-sensitive ordering rate using the E1-E5 pairwise difference interval;
2. strict reversal rate as the stronger subtype.

E1-vs-E2 is mandatory but secondary/special-case. Do not promote whichever evaluator pair produces the largest effect.

## Stop conditions

Stop and publicly document before endpoint inspection if hardware, model revision, frozen panel, evaluator tests or unquantized BF16 execution differs from the lock.
