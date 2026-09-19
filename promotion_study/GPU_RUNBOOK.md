# GPU EXECUTION RUNBOOK — AJSE

Pinned execution commit: `e2e4883cfdde3dd57eeea24b3ab73b66d003aad1`
Primary hardware: one NVIDIA A100-SXM4-80GB per job.

Do not execute from a moving branch head. Check out the pinned commit above.

## Environment

```bash
git clone --branch promotion-ajse-llm-repro https://github.com/adeebnoor/ridi.git ajse-study
cd ajse-study
git checkout e2e4883cfdde3dd57eeea24b3ab73b66d003aad1
python -m pip install --upgrade pip
python -m pip install --index-url https://download.pytorch.org/whl/cu128 torch==2.11.0
grep -v '^torch==' promotion_study/requirements.txt > /tmp/ajse-req.txt
python -m pip install -r /tmp/ajse-req.txt
```

## Pre-output checks

```bash
python promotion_study/freeze_inputs.py
python -m py_compile promotion_study/run_execution_repro.py
python -m py_compile promotion_study/analyse_execution_repro.py
nvidia-smi
```

The run must stop if the frozen sample or tokenizer-specific companion-plan SHA differs.

## Primary model jobs

Run each model in a fresh job/container on one A100-SXM4-80GB:

```bash
cd promotion_study
python run_execution_repro.py --model qwen25_7b --out /tmp/ajse-qwen --emit-zip-base64
```

```bash
cd promotion_study
python run_execution_repro.py --model mistral7b_v03 --out /tmp/ajse-mistral --emit-zip-base64
```

Archive the complete raw JSONL and execution manifest from each job before looking at aggregate outcomes.

## Locked analysis

After both raw JSONLs are recovered:

```bash
python analyse_execution_repro.py   qwen25_7b_raw.jsonl mistral7b_v03_raw.jsonl   --out AJSE_AGGREGATE.json
```

Primary contrast after Amendment 1 is **B vs C at fixed batch size 8**. Never substitute A vs C as primary because it looks larger.

## Stop conditions

Stop and document before endpoint inspection if:
- GPU is not A100-SXM4-80GB;
- any frozen source/sample/plan hash fails;
- a pinned model cannot load unquantized BF16;
- the exact declared software stack cannot execute.

Do not repair an outcome after seeing it. Any technical repair must be committed publicly before resuming model generation.
