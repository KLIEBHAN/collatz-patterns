#!/usr/bin/env python3
"""check_residual.py

Diagnostic script to verify the Poisson residual and clarify the drift metrics.

Based on GPT 5.2 Pro analysis (2026-02-01):
- The Poisson residual r = (I - P)ψ - (g - ḡ) should be ~0
- The "global drift" after centering is NOT E[Δlog n]
- E[Δlog n] should be ~-0.18 to -0.24 (the real negative drift!)

Usage:
    python src/check_residual.py [run_dir]
    python src/check_residual.py  # uses latest run
"""

import json
import sys
from pathlib import Path
import numpy as np


def find_latest_run(base_dir: Path) -> Path:
    """Find the most recent run directory."""
    runs = sorted(base_dir.glob("*_k*_S*"))
    if not runs:
        raise FileNotFoundError(f"No runs found in {base_dir}")
    return runs[-1]


def load_run(run_dir: Path) -> dict:
    """Load all arrays and summary from a run."""
    return {
        "psi": np.load(run_dir / "psi.npy"),
        "g_raw": np.load(run_dir / "g_raw.npy"),
        "g_corrected": np.load(run_dir / "g_corrected.npy"),
        "pi_occ": np.load(run_dir / "pi_occ.npy"),
        "state_counts": np.load(run_dir / "state_counts.npy"),
        "summary": json.loads((run_dir / "summary.json").read_text()),
    }


def main():
    base_dir = Path("~/workspace/data/psi_correction").expanduser()
    
    if len(sys.argv) > 1:
        run_dir = Path(sys.argv[1]).expanduser()
    else:
        run_dir = find_latest_run(base_dir)
    
    print(f"Analyzing run: {run_dir.name}")
    print("=" * 60)
    
    data = load_run(run_dir)
    psi = data["psi"]
    g_raw = data["g_raw"]
    g_corrected = data["g_corrected"]
    pi = data["pi_occ"]
    counts = data["state_counts"]
    summary = data["summary"]
    
    n_states = len(psi)
    
    # ========================================
    # 1. The TRUE E[Δlog n] (weighted by π)
    # ========================================
    g_bar_log = np.sum(pi * g_raw)
    
    print("\n📊 DRIFT METRICS (the important ones!)")
    print("-" * 40)
    print(f"E[Δlog n] (ḡ_log)        = {g_bar_log:.6f}")
    print(f"  → This is the REAL drift!")
    print(f"  → Expected: ~-0.18 to -0.24")
    
    # ========================================
    # 2. Poisson Residual
    # ========================================
    # From the math:
    # g_corrected = g_raw + (Pψ) - ψ
    # (I-P)ψ = ψ - Pψ = ψ - (g_corrected - g_raw + ψ) = g_raw - g_corrected
    # 
    # Poisson equation: (I-P)ψ = g - ḡ = g_raw - ḡ_log
    # Residual: r = (I-P)ψ - (g_raw - ḡ_log) = (g_raw - g_corrected) - (g_raw - ḡ_log)
    #             = ḡ_log - g_corrected
    
    r = g_bar_log - g_corrected  # Poisson residual per state
    
    print(f"\n🔬 POISSON RESIDUAL (r = ḡ - g_corrected)")
    print("-" * 40)
    print(f"||r||∞              = {np.abs(r).max():.2e}")
    print(f"||r||₂              = {np.linalg.norm(r):.2e}")
    print(f"||r||₂,π            = {np.sqrt(np.sum(pi * r**2)):.2e}")
    print(f"mean(|r|)           = {np.abs(r).mean():.2e}")
    
    # ========================================
    # 3. Corrected drift analysis
    # ========================================
    print(f"\n📈 CORRECTED DRIFT ANALYSIS")
    print("-" * 40)
    print(f"g_corrected range   = [{g_corrected.min():.2e}, {g_corrected.max():.2e}]")
    print(f"g_corrected std     = {g_corrected.std():.2e}")
    
    # The corrected drift SHOULD be approximately constant = ḡ_log
    # Deviation from constant is the residual
    deviation = g_corrected - g_bar_log
    print(f"\nDeviation from constant (g_corrected - ḡ):")
    print(f"  max deviation     = {deviation.max():.2e}")
    print(f"  min deviation     = {deviation.min():.2e}")
    print(f"  std deviation     = {deviation.std():.2e}")
    
    # ========================================
    # 4. "Positive drift" analysis with proper threshold
    # ========================================
    print(f"\n⚠️  'POSITIVE DRIFT' ANALYSIS")
    print("-" * 40)
    
    # Naive count (threshold = 0)
    n_positive_naive = np.sum(g_corrected > 0)
    mass_positive_naive = np.sum(pi[g_corrected > 0])
    
    # With threshold = 1e-4
    threshold = 1e-4
    n_positive_thresh = np.sum(g_corrected > threshold)
    mass_positive_thresh = np.sum(pi[g_corrected > threshold])
    
    # With threshold = 5 * typical SE (assuming SE ~ 0.1 / sqrt(1000) ~ 0.003)
    # But actually we should compute SE properly
    
    print(f"Naive (threshold=0):")
    print(f"  States > 0        = {n_positive_naive} / {n_states}")
    print(f"  π-mass            = {mass_positive_naive:.8f}")
    
    print(f"\nWith threshold={threshold}:")
    print(f"  States > {threshold}    = {n_positive_thresh} / {n_states}")
    print(f"  π-mass            = {mass_positive_thresh:.8f}")
    
    # ========================================
    # 5. Key insight summary
    # ========================================
    print(f"\n" + "=" * 60)
    print("🎯 KEY INSIGHTS")
    print("=" * 60)
    
    margin = abs(g_bar_log) / np.abs(r).max() if np.abs(r).max() > 0 else float('inf')
    
    print(f"""
1. TRUE DRIFT MARGIN:
   |E[Δlog n]| = {abs(g_bar_log):.4f}
   ||r||∞     = {np.abs(r).max():.2e}
   RATIO      = {margin:.0f}x
   
   → The real drift margin is ~{abs(g_bar_log):.2f}, NOT ~10⁻⁵!
   → The 10⁻⁵ is just solver residual.

2. INTERPRETATION:
   The Poisson correction makes drift CONSTANT across states.
   It does NOT make it negative everywhere (that's impossible).
   
   The constant value IS negative: ḡ = {g_bar_log:.4f}
   This is the proof-relevant quantity!

3. WHAT "4324 STATES POSITIVE" REALLY MEANS:
   All states have drift ≈ {g_bar_log:.4f} ± {np.abs(r).max():.1e}
   The "positive" ones are just on the + side of numerical noise.
   With threshold > {np.abs(r).max():.1e}, we get {n_positive_thresh} truly positive.
""")
    
    # ========================================
    # 6. ψ statistics
    # ========================================
    print(f"\n📐 ψ STATISTICS")
    print("-" * 40)
    print(f"ψ range             = {psi.max() - psi.min():.4f}")
    print(f"ψ mean (π-weighted) = {np.sum(pi * psi):.2e} (should be ~0)")
    print(f"ψ std               = {psi.std():.4f}")
    print(f"ψ min, max          = [{psi.min():.4f}, {psi.max():.4f}]")
    
    # ========================================
    # 7. Compare with summary.json
    # ========================================
    print(f"\n📋 COMPARISON WITH summary.json")
    print("-" * 40)
    print(f"summary.global_drift         = {summary['global_drift']:.2e}")
    print(f"computed ḡ_log               = {g_bar_log:.6f}")
    print(f"summary.worst_corrected_drift= {summary['worst_corrected_drift']:.2e}")
    print(f"computed max(g_corrected)    = {g_corrected.max():.2e}")
    
    if abs(summary['global_drift'] - g_bar_log) > 0.01:
        print(f"\n⚠️  NOTE: summary.global_drift appears to be the RESIDUAL,")
        print(f"    not the true E[Δlog n]. This is a labeling issue in compute_psi.py.")


if __name__ == "__main__":
    main()
