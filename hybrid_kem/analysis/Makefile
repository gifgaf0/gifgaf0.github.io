# Reproduce the HYBRID-AKE symbolic analysis.
# Requires: tamarin-prover 1.12.0 and maude 3.5.1 on PATH (and MAUDE_LIB set).
#   Tamarin: https://github.com/tamarin-prover/tamarin-prover/releases/tag/1.12.0
#   Maude:   https://github.com/maude-lang/Maude/releases/tag/Maude3.5.1

.PHONY: prove prove-ext check
prove:
	tamarin-prover --prove hybrid_ake.spthy

prove-ext:
	tamarin-prover --prove hybrid_ake_ext.spthy

check:
	tamarin-prover hybrid_ake.spthy
	tamarin-prover hybrid_ake_ext.spthy
