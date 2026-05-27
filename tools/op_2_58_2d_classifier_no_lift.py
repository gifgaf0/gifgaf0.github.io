"""op_2_58_2d_classifier_no_lift.py — signed-lift-disabled variant (Brief 08, F1).

The production classifier (op_2_58_2d_classifier.FanoLineClassifier) signed-lifts
a candidate's mod-q residues into (-q/2, q/2] before the Euclidean projection
(`_lift`). This module provides a subclass that DISABLES that lift at its single
entry point, so a residue near q (e.g. 910 at q = 911) arrives at the projection
as +910 rather than its signed equivalent (−1).

Production behaviour is preserved: the production module is not edited, and
constructing this class with `disable_signed_lift=False` reproduces the
production classifier exactly. The default disables the lift (the F1 test mode).

`_lift` is the sole place the production classifier centres candidates
(`fano_ratios`/`pair_ratios` both call it; `classify` calls those), so
overriding it disables the lift at all entry points — there is no sibling
code path that silently re-applies it. The F1 driver's instrumentation
confirms this empirically.
"""

from __future__ import annotations

import numpy as np

from op_2_58_2d_classifier import TOY_P, FanoLineClassifier


class NoLiftFanoLineClassifier(FanoLineClassifier):
    def __init__(self, p: int = TOY_P, disable_signed_lift: bool = True):
        self.disable_signed_lift = disable_signed_lift
        super().__init__(p)

    def _lift(self, v) -> np.ndarray:
        if not self.disable_signed_lift:
            # Production behaviour: centre to (-p/2, p/2].
            return super()._lift(v)
        # Signed-lift DISABLED: positive residues in [0, p). 910 stays +910.
        p = self.p
        arr = np.asarray(v)
        return np.array([int(c) % p for c in arr], dtype=float)
