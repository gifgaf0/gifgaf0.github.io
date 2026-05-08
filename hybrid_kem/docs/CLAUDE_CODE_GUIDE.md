# Using Claude Code on the Hybrid PQC Testbed

A short guide for running Claude Code in parallel with our chat sessions.

## Setup (one-time)

1. Install Claude Code:
   ```bash
   curl -fsSL https://claude.ai/install.sh | sh
   ```
   Or per the docs at https://docs.claude.com/en/docs/claude-code

2. From the testbed directory:
   ```bash
   cd hybrid_kem
   claude
   ```

3. First time, give it the project context:
   ```
   Read SPEC.md, README.md, and the existing files in the parent project
   (especially sqt_slwe__1_.py, sqt_prime_core__1_.py, sedenion_Fp.py).
   You're building a research testbed. Epistemic discipline matters:
   distinguish verified, structural, and conjectural claims.
   ```

## Working pattern

The pattern that works:

1. **In our chat (here)**: design, decide, write specs.
2. **In Claude Code**: implement against the spec, run tests, report.
3. **Back here**: review what came back, refine, next spec.

Each task gets a brief in `docs/CLAUDE_CODE_BRIEF_NN_*.md`. You hand
the brief to Claude Code:

```
Read docs/CLAUDE_CODE_BRIEF_01_ENTROPY.md and execute it.
When done, stop and write IMPLEMENTATION_NOTES.md.
```

## What Claude Code is good at

- Writing well-structured code from a clear spec
- Running tests and iterating on failures
- Boring-but-important infrastructure (parsing, validation, error handling)
- Researching APIs and library usage
- Refactoring and adding tests to existing code

## What it's less good at

- Anything where the goal is fuzzy
- Crypto primitives where a tiny mistake = catastrophic failure (review carefully!)
- Decisions about scope or architecture (those happen here)
- Understanding the framework's epistemic discipline without explicit reminders

## Critical: review the crypto code

Even with good specs and good tests, **you (or I) must review every line
of cryptographic code** before trusting it. Common subtle errors:

- Incorrect endianness
- Off-by-one in domain separation strings
- Wrong KDF labels
- Missing constant-time operations on secrets
- Reseeded DRBG without mixing the old state correctly
- Cache exposing entropy across requests

Claude Code passing tests is necessary but not sufficient.
Test vectors catch many bugs. Code review catches the rest.

## Pen-testing mindset translation

Your pen-testing experience translates as follows:

| Pen-test concept | Crypto-test analog |
|---|---|
| "What if the input is malformed?" | Negative test: feed garbage, must reject cleanly |
| "What if I send it twice?" | Replay test: same ct twice → same ss (correctness); but session protocols must reject |
| "What if the network drops?" | Cache fallback test, partial-write recovery |
| "What if I observe timing?" | Side-channel concern (out of scope for this testbed) |
| "What if I control one component?" | Threat model exercise: which component compromises break what |
| "What does the error message reveal?" | No error message should distinguish "wrong key" from "invalid format" — implicit rejection |

Use `pytest -v` and `pytest --cov` heavily. Coverage gaps are
where bugs hide.

## Communicating between Claude (here) and Claude Code

Claude Code commits to git as it works. The pattern:

1. After a Claude Code session, you can paste the diff/summary here.
2. I review the architecture, flag concerns, suggest follow-ups.
3. Next brief gets written here, executed there.

If something surprises you in what Claude Code did, paste it here.
If it ignored a spec requirement, paste it here.
If it found a real issue with the spec, that's also paste-here-worthy.

## On running tests yourself

You don't need to write tests, but running them is useful:

```bash
# Full suite
pytest -v

# One module
pytest tests/test_entropy.py -v

# Coverage report
pytest --cov=entropy --cov-report=term-missing

# Just the slow integration tests
pytest -m integration

# Catch flaky tests (run multiple times)
pytest --count=10 tests/test_entropy.py
```

If anything fails, paste the failure here — the message + a few lines
of context — and we'll diagnose.

## Don't worry about

- Performance optimization (later)
- Real QRNG hardware integration (later)
- Production deployment concerns (out of scope)
- Whether SLWE is "really" secure (out of scope for engineering)

## The flow we're aiming for

```
Day 1: Brief 01 (entropy) → Claude Code → review → notes
Day 2: Brief 02 (KEM standard) → Claude Code → review
Day 3: Brief 03 (combiner + slwe stub) → Claude Code → review
Day 4: Brief 04 (full integration) → Claude Code → review
Day 5: Brief 05 (tests + benchmarks) → Claude Code → review
```

Roughly. Reality will be messier. That's fine.
