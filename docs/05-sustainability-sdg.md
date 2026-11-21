# 05 · Sustainability and SDG impact

## SDG mapping (direct contribution only; avoid SDG-washing)

| SDG | Target | Contribution | Indicator we can measure |
|---|---|---|---|
| 3 Good health and well-being | 3.9 (deaths/illness from hazardous chemicals and pollution) | Less worker contact with metalworking fluids | Manual handling hours avoided; kg absorbent avoided |
| 8 Decent work and economic growth | 8.8 (safe working environments) | Removes slip hazards at shift change | Slip incidents before/after (pilot) |
| 9 Industry, innovation and infrastructure | 9.4 (resource-efficient, clean technologies) | Local, low-cost automation | Cost vs commercial alternatives |
| 12 Responsible consumption and production | 12.4 (sound management of chemicals and wastes), 12.5 (reduce waste generation) | Segregation at source; chips to recycling; no third stream | t/yr hazardous waste avoided; t/yr chips recycled |

Per robot (reference case, estimates): ≈ 2.6 t/yr mixed hazardous waste avoided; ≈ 1.3 t/yr chips to scrap recycling;
450 kg/yr oil-soaked absorbent avoided. Each ton of recycled steel conserves ≈ 2,500 lb iron ore, 1,400 lb coal,
120 lb limestone (AISI 2025).

## Environmental footprint of the robot itself (to quantify)

- Lead-acid battery: return for recycling; consider LiFePO4 upgrade (fewer replacements).
- PETG parts: print with minimal infill compatible with n ≥ 2; reuse failed prints as test coupons.
- Energy: ≈ 0.15 kWh/cycle from grid → ≈ 135 kWh/yr; multiply by the current CFE/SEN emission factor (look up the
  latest official value; do not hard-code).
- End of life: modules on T-slot frame → disassembly and reuse.

## Method

Use `docs/templates/sdg-assessment.md`. Every claim carries a number, unit, source and status (estimate /
simulation / measured). Include negative impacts (battery, plastics, possible job displacement) and mitigations.
