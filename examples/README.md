# Minimal example

`r0.csv` and `r1.csv` contain the same ten candidate identities under two operational representations. Scores differ slightly and some local ordering changes.

Run:

```bash
ridi-audit compare --r0 examples/r0.csv --r1 examples/r1.csv --k 3 5
ridi-audit control --r0 examples/r0.csv --r1 examples/r1.csv --k 5 --eta 0.001
```

The example is synthetic and demonstrates file format and command behavior only.

