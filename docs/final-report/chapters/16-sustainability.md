# Sustainability and Sustainable Development Goals

Rule: map only direct contributions (no SDG-washing), give every claim a number, unit, source and status, and include
negative impacts with mitigations. Reference: UN 2030 Agenda [76].

## SDG mapping

| SDG | Target | Contribution | Indicator we can measure |
|---|---|---|---|
| 3 Good health and well-being | 3.9 Deaths and illness from hazardous chemicals and pollution | Less worker contact with metalworking fluids | Manual handling hours avoided; kg absorbent avoided |
| 8 Decent work and economic growth | 8.8 Safe and secure working environments | Removes slip hazards at shift change | Slip incidents before/after (pilot) |
| 9 Industry, innovation and infrastructure | 9.4 Resource-efficient, clean technologies | Local, low-cost automation | Cost vs commercial alternatives |
| 12 Responsible consumption and production | 12.4 Sound management of chemicals and wastes · 12.5 Reduce waste generation | Segregation at source; chips to recycling; no third stream | t/yr hazardous waste avoided; t/yr chips recycled |

## Quantified environmental benefit (per robot, reference case, estimates)

| Indicator | Calculation | Value |
|---|---|--:|
| Mixed hazardous waste avoided | (1,350 kg chips + 792 kg oil + 450 kg absorbent) per year no longer mixed | ≈ 2.6 t/yr |
| Chips sent to scrap recycling | 1,350 kg − 5 % fines | ≈ 1.3 t/yr |
| Oil-soaked absorbent avoided | 0.5 kg × 900 cycles | 450 kg/yr |
| Raw materials conserved by recycled steel | per ton: ≈ 2,500 lb iron ore, 1,400 lb coal, 120 lb limestone [57] → × 1.28 t | ≈ 3,200 lb ore, 1,800 lb coal, 150 lb limestone per year (deduced) |
| Grid energy used by the robot | 0.15 kWh × 900 cycles | ≈ 135 kWh/yr |

The CO₂ of the 135 kWh/yr must be computed with the current official CFE/SEN emission factor (to look up; not
hard-coded).

## Footprint of the robot itself and mitigations

| Negative impact | Mitigation |
|---|---|
| Lead-acid battery (2 replacements/yr) | Return for recycling under NOM-052/LGPGIR; LiFePO4 upgrade (fewer replacements) |
| PETG printed parts | Minimal infill compatible with n ≥ 2; failed prints reused as test coupons |
| Electricity | Charge off-peak; measure real kWh/cycle |
| End of life | Modules on a T-slot frame → disassembly and reuse; electronics to e-waste recycling |
| Possible job displacement (social) | Retraining as operators; reassignment of freed hours (Chapter 14) |
| Noise | Operates only in the empty shift-change window; to be measured (NOM-011) |
