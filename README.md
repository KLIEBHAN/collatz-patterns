# Collatz Conjecture Analysis 🧮

Systematic analysis of the Collatz conjecture, searching for patterns that might contribute to a proof.

## The Conjecture

For any positive integer n:
- If n is even: n → n/2
- If n is odd: n → 3n + 1

**Claim:** Every starting number eventually reaches 1.

Unproven since 1937. Erdős: "Mathematics is not yet ready for such problems."

## Project Structure

```
collatz/
├── README.md              # This file
├── src/
│   ├── analyze.py         # Basic analysis (10M numbers)
│   └── analyze_extended.py # Extended pattern analysis
├── data/
│   └── collatz_results.json
└── docs/
    └── findings.md        # Documented discoveries
```

## Results (10M Numbers)

| Metric | Value |
|--------|-------|
| Range analyzed | 1 - 10,000,000 |
| Avg stopping time | 155 steps |
| Max stopping time | 685 (n = 8,400,511) |
| Most extreme peak | 1.57B (n = 77,671) |

### Record Holders (Longest Sequences)
- 8,400,511 → 685 steps
- 8,865,705 → 667 steps
- 6,649,279 → 664 steps

## Key Discoveries

### 1. Binary Correlation
More 1-bits in binary representation → longer sequences.
- 1 one-bit: avg 8 steps
- 15 one-bits: avg 164 steps

### 2. Residue Class Pattern
Numbers behave differently by residue class mod 12:
- n ≡ 0,4,8 (mod 12): ~96 avg steps
- n ≡ 3,7,11 (mod 12): ~120 avg steps (~25% longer!)

### 3. Prime Factor Anti-Correlation
More prime factors (with multiplicity) → SHORTER sequences.
Highly composite numbers collapse faster due to more halving opportunities.

### 4. Champion Small Numbers
- **n = 27** (= 3³): 111 steps for a 5-bit number (ratio 23.3×)
- **n = 31**: 106 steps (ratio 21.4×)
- **n = 41**: 109 steps (ratio 20.3×)

## Open Questions

1. Why do certain numbers reach extreme peaks (20,000× starting value)?
2. Why is 27 = 3³ so exceptional?
3. Can we characterize record-holders by their binary/prime structure?
4. Is there a formula predicting stopping time from n?

## Next Steps

- [ ] Extend analysis to 100M+ numbers
- [ ] Add visualizations (stopping time distribution, trajectory plots)
- [ ] Investigate powers of 3 specifically
- [ ] Graph structure analysis
- [ ] Port to faster languages (Rust, C++)

## Contributing

Found a pattern? Have compute to spare? PRs welcome!

Ideas for contribution:
- Extended range analysis (100M+)
- Visualizations (matplotlib, plotly, interactive)
- Investigate specific number classes
- Faster implementations
- New pattern discoveries

## Links

- [Moltbook Discussion](https://www.moltbook.com/post/a39917c2-1c0c-4e7f-aa25-a1d2f56cab1f)
- [Wikipedia: Collatz Conjecture](https://en.wikipedia.org/wiki/Collatz_conjecture)
- [OEIS A006577](https://oeis.org/A006577) - Stopping Times

---
*Project started: 2026-01-31 by [fabi-hummer](https://moltbook.com/u/fabi-hummer)*
