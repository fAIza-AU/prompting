# Prompt Evaluation Harness

A small evaluation system that tests an LLM-powered article summarizer against a fixed set of real articles, scores each output automatically, and proves whether a prompt change actually improves the model's behavior — instead of relying on eyeballing outputs.

## Why this exists

Anyone can call an LLM API and get a response back. The harder, more useful skill is knowing whether that response is actually *good* — reliably, across different inputs, not just on the one example you happened to test. This project treats prompt engineering as something you test and iterate on with evidence, not something you guess at.

The system under test is `ask_llm()`, a Groq-powered article summarizer originally built as a separate project. This harness evaluates it.

## How it works

**Test set** (`test_cases.json`) — 6 real articles, deliberately varied: short factual news, long technical explainers, a numbers-dense funding story, a two-sided dispute, and a pop-culture opinion piece. Each case defines what a good summary must do: required facts (`must_include`), a word limit (`must_not_exceed_words`), and notes on what a summary could get wrong.

**Rule-based scoring** — for every case, the harness runs the article through the summarizer, then checks:
- Word count against the case's limit
- Whether each required fact appears in the output (exact text match)

**LLM-as-judge** — a second, separate model call reads the summary and the required facts, and answers a strict YES/NO on whether the summary correctly captures them. This exists because exact text matching breaks down when a model phrases the same fact differently — see Findings below.

**Iteration loop** — run the harness, read the failures, adjust the prompt, re-run, compare. Results are below.

## Results

| Version | Pass rate (word limit) | What changed |
|---|---|---|
| v1 | 0 / 6 | Original prompt: "summarize clearly and concisely" — no word limit or format instruction. Model returned bulleted, headed summaries, 100–300+ words each. |
| v2 | 3 / 6 | Added an explicit word limit and "no bullet points" to the system prompt, dynamically per case. |
| v3 | 5 / 6 | Tightened the instruction to state the limit as a hard constraint. |

The one remaining failure (`case_01`) has the tightest limit in the test set (60 words) on an article with five distinct facts packed into it (funding amount, valuation, revenue run rate, growth rate, three named clients). The model consistently chooses to keep all the facts and slightly exceed the limit rather than drop one to comply exactly. This is a real, reproducible trade-off, not a bug.

## Findings

- **A vague length instruction ("concisely") is not an instruction the model can act on.** It needs an explicit number to actually comply.
- **Exact-text matching is brittle against LLM output.** The same fact can come back as "$5 billion," "$5B," or "$5 bn" across different runs of the *same* prompt on the *same* input — LLMs are non-deterministic by default. Rule-based `must_include` checks flagged these as failures even though a human reader would consider the fact present. This is what motivated the LLM-as-judge layer, which correctly recognized these as equivalent.
- **Hidden Unicode characters cause silent false failures.** Model output sometimes uses non-standard space characters (e.g. `\u202f`, a narrow no-break space) that look identical to a normal space but don't match in exact string comparison. Fixed with a `.replace()` cleanup step before scoring.
- **Tight word limits on fact-dense articles are a genuine tension**, not something a single prompt tweak fully resolves — the model will trade length compliance for factual completeness when forced to choose.

## What I'd do next

- Extend the LLM-judge to also check for hallucination (does the summary state anything *not* in the source), not just fact presence
- Grow the test set beyond 6 cases for broader coverage
- Test whether a lower `temperature` setting improves length compliance without hurting content quality

## Project files

- `test_cases.json` — the 6 test cases and their pass criteria
- `bb.py` — the summarizer under test (`ask_llm()`)
- `eval_1.py` — the harness: runs the test set, scores rule-based checks, calls the judge
- `judge.py` - act as professional grader using (`judge_llm()`)