# Power Integrity Signoff on a 7nm Design — Ansys RedHawk-SC

Hands-on power integrity (PI) signoff methodology applied to a ~1M-instance block on the ASAP7 7nm academic PDK, using Ansys RedHawk-SC — the industry-standard tool also used in production PI signoff at major foundries and IP vendors. Completed as part of DTU's *Big-Data Driven Power Integrity Signoff in ICs* coursework.

This repo documents the methodology, findings, and scripting work — not raw tool output (license/infrastructure details have been excluded).

## What this covers

Power integrity signoff isn't one check — it's a stack of interdependent analyses that all have to pass before a design can tape out:

- **Static IR-drop analysis** — voltage drop across the power grid under worst-case average load
- **Grid robustness** — shorts, opens, and disconnected nodes in the power/ground network
- **Shortest Path Resistance (SPR) & Bump Quality Metric (BQM)** — identifying poorly-connected cells and unbalanced current loading at the package interface
- **Electromigration (EM)** — current-density reliability checks against Black's equation, for both metal and via layers
- **Power breakdown** — by domain, frequency, and cell class
- **Scripted report extraction** — pulling structured insight out of multi-thousand-line tool reports with `awk`/`grep`/Python rather than manual inspection

## Design under test

| Parameter | Value |
|---|---|
| Technology | ASAP7 7nm academic PDK |
| Instance count | ~1,011,133 (999,170 leaf cells) |
| Supply | VDD 0.7V nominal |
| Clock | Single domain, 714.3 MHz |
| Macros | Multiple SRAM_16_2048 blocks |
| Packaging | Flip-chip, C4 bump array |

## Key findings

**Grid robustness:** found 6 VDD–VSS shorts on the M1 layer, 1,419 disconnected power-grid nodes, and 3,413 instances with Supply Pin Resistance (SPR) above 500Ω — extracted via a one-line `grep | awk` filter rather than manual report scanning. In a production flow, all three categories are signoff-blocking issues requiring PDN rework before tapeout.

**IR-drop:** worst-case static IR-drop was ~4.9mV (0.7% of nominal 0.7V) — well within typical signoff margins (commonly 5–10%), and concentrated almost entirely in clock-tree inverter cells. This is a textbook signature: clock cells sit deep in the design, switch every cycle at full toggle rate, and are physically furthest from the bump-fed power straps — so they're consistently the first cells to show IR-drop stress, regardless of design.

**SPR/BQM correlation:** mapping SPR and BQM heatmaps together showed an inverse spatial relationship — cells with the worst SPR clustered in regions far from the highest-current bumps, confirming the power delivery network was leaning on a small subset of bumps in one quadrant rather than distributing load evenly.

**Electromigration:** all metal and via layers passed DC EM checks, with worst-case usage at 23.71% of the Black's-equation current-density budget on M5 (76% headroom) and 0.15% on the worst via layer — a comfortably EM-clean design under DC conditions.

**Power breakdown:** total power 156mW, dominated by sequential logic (44.8%) and clock distribution (30.8%), with leakage at under 2% of total — consistent with a design operating well above threshold at nominal voltage.

## Scripts

- [`scripts/spr_violation_filter.sh`](scripts/spr_violation_filter.sh) — filters an SPR report for instances exceeding a resistance threshold
- [`scripts/extract_top_bottom_voltage.py`](scripts/extract_top_bottom_voltage.py) — parses an instance-voltage report and returns the N best/worst-supplied cells, merged against power data

## Tools

Ansys RedHawk-SC 2025 R2.3 · UNIX/bash · Python · ASAP7 7nm PDK

---
*Academic coursework project. Tool output and proprietary infrastructure details intentionally excluded; this repo documents methodology and original scripting only.*
