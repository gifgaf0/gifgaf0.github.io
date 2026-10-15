# Reproduce the HYBRID-AKE symbolic analysis.
# Requires: tamarin-prover 1.12.0 and maude 3.5.1 on PATH (and MAUDE_LIB set).
#   Tamarin: https://github.com/tamarin-prover/tamarin-prover/releases/tag/1.12.0
#   Maude:   https://github.com/maude-lang/Maude/releases/tag/Maude3.5.1
MODEL = hybrid_ake.spthy

.PHONY: prove check
prove:
	tamarin-prover --prove $(MODEL)

check:
	tamarin-prover $(MODEL)   # well-formedness only, no proof
