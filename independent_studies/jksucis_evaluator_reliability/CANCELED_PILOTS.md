# Incomplete scheduler-canceled pilot executions

A set of initial full-panel GPU jobs was launched after the frozen-panel lock. The compute scheduler subsequently canceled the concurrently running jobs before any model completed its required panel.

No incomplete job contributes any result to the study. No benchmark response content, cell statistic, accuracy, disagreement rate, ranking or primary endpoint from the incomplete jobs was inspected for scientific interpretation or used to modify the protocol.

The complete analyses are rerun from the same frozen panels and pinned model revisions. The canceled job IDs remain available in the Hugging Face Jobs audit history.

This note documents compute execution history only; no scientific hypothesis, sample, model, prompt, endpoint or analysis rule changes.
