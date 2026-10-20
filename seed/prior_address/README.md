# Prior address

`research_raw.json` is the unedited return of the four literature agents run on October 18, 2026,
before any experiment: `citations` (SEED.md §9), `claims` (§2–§8), `targets-numeric` (E1, E6, E8)
and `targets-algebraic` (E2–E5). Each item records its source URL and whether the number was read
in the source (`read_directly`).

Access: publisher sites, arXiv.org and INSPIRE were blocked by the sandbox's proxy. Full texts came
from the public arXiv mirror at `https://storage.googleapis.com/arxiv-dataset/arxiv/` and PDG numbers
from the PDG 2026 SQLite file in the `pdg` Python package. Everything else rests on search-engine
extracts, as each item says. The corrections that matter for SEED.md are summarized in `../PLAN.md` §3.

Some "own computation" values in the targets were scratch checks made by the literature agents.
They are not literature targets and are not used as such in `../PLAN.md`.
