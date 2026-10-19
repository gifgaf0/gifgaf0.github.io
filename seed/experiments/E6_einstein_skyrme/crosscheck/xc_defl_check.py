#!/usr/bin/env python3
"""Deflection per unit alpha computed two ways from the flat profile:
 (iso)  (2/b) int [m + m_T](b cosh t)/cosh^2 t dt
 (schw) 1/2 int d/db [h00 + h_zz] dz,  h00 = 2(1-sigma)/alpha + 2 m/r, h_zz = (2 m/r)(z/r)^2  (Schwarzschild coords)
"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xc_iso as X
from xc_firstorder import flat, profiles, cumint  # noqa (re-runs firstorder prints)
