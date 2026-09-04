# Frequently asked questions

## What does RIDI stand for?

RIDI is the **Reproducibility of Identity Decisions Index**. It measures how much the membership of a finite selected set changes between two aligned score states.

## Is RIDI the main scientific claim?

No. RIDI is an instrument. The broader scientific object is **allocation identity**: whether a reported audit identifies the finite entities that actually receive scarce action, attention or context. The current manuscript tests whether exact audit equivalence can coexist with allocation and downstream decision non-equivalence.

## Is RIDI just Jaccard distance?

Its set-distance primitive is Jaccard distance. The toolkit's contribution is not a claim to have invented a new set-similarity formula; it operationalizes allocation-identity auditing around finite decisions, including deterministic top-k selection, sufficient zero-turnover certification and exact identity–utility control.

## Why not use Spearman or Kendall correlation?

Global rank statistics average over the full candidate universe. Finite decisions depend on membership near a cutoff. High global agreement therefore does not certify that the same entities occupy a finite top-k set.

## Is turnover necessarily bad?

No. Turnover can be beneficial, neutral or harmful. RIDI makes membership change observable. Outcome or utility evidence must determine whether preserving identity is desirable in a particular application.

## How should eta be chosen?

Prospectively, from application-specific utility, safety, review capacity and stakeholder constraints. `eta = 0.001` means a maximum normalized updated-score utility regret of 0.1%; it is not a universal standard.

## Does non-zero RIDI prove a particular mechanism caused the change?

No. Causal attribution requires a design that freezes or calibrates competing mechanisms. Without such a design, RIDI is a diagnostic measure of realized membership change.

## Does audit equivalence imply the same AI output?

Not necessarily. In the preregistered RAG experiment, the complete relevance-grade-by-position vector and all registered retrieval metrics were held exactly fixed while metric-zero passage identities were changed. Benchmark-defined correctness diverged in a non-zero fraction of cases, establishing behavioral non-equivalence within the registered audit-equivalence class.

## Are qrel-zero passages semantically irrelevant?

No. They are called **metric-zero** because the declared benchmark audit assigns them zero relevance. Incomplete qrels mean a metric-zero passage can still contain semantically influential text.

## Is the external verification a CODECHECK certificate?

No. The EPSS workflow has been reproduced by two independent external executors, and the SciFact 275 case has a targeted blind external regeneration. The community CODECHECK request is registered, but formal checking has not begun and no certificate is claimed.
