# Engineering calculations and simulation

All results in this chapter are **calculations, estimates or simulations**. None is a physical test. Each one names
the tool or formula that reproduces it.

## Speed

Top speed from the gearmotor and wheel (equation 3):

$$v_{max} = \pi \cdot 0.124 \cdot \frac{59}{60} = 0.383\ \text{m/s} \approx 0.38\ \text{m/s}$$

The cleaning speed is limited to 0.15 m/s (SR-004) and the MCU trips an overspeed stop at 0.40 m/s measured by the
encoders (SR-013). At 0.15 m/s the robot travels one wheel circumference (0.39 m) in 2.6 s. **Calculation.**

## Braking on oil

Worst case: the robot runs at top speed on an oiled floor with friction coefficient $\mu = 0.1$ (equation 11):

$$d = \frac{0.38^2}{2 \times 0.1 \times 9.81} = 0.074\ \text{m}$$

| Speed | μ = 0.1 (oil) | μ = 0.3 (wet) | μ = 0.6 (dry) |
|---|--:|--:|--:|
| 0.15 m/s (cleaning) | 11.5 mm | 3.8 mm | 1.9 mm |
| 0.38 m/s (top) | 73.6 mm | 24.5 mm | 12.3 mm |

The test requirement (SR-005) allows 0.10 m, so the margin over the worst calculated case is 26 mm. A LiDAR stop zone
of 30 cm leaves a wide margin for detection latency: at 0.38 m/s, even 300 ms of detection delay (T_stale) adds only
11.4 cm. **Calculation** (constant deceleration, motor braking assumed to reach the friction limit; to be measured,
SC-005).

## Energy and runtime

Usable energy (equation 9): $E_{use} = 0.5 \times 12 \times 24 = 144$ Wh. With the 160 W average load (Section 4.10):

$$t = \frac{144\ \text{Wh}}{160\ \text{W}} = 0.90\ \text{h} \approx 54\text{–}55\ \text{min}$$

`tools/wcca.py` reports 54 min at 160 W. Per cleaning cycle in the simulated cell (25.6 min) the energy is 68 Wh, so
one charge gives ≈ 2.1 cycles. Energy from the grid per cycle ≈ 0.15 kWh including charger losses (estimate), or
≈ 135 kWh/yr for 900 cycles. **Estimate.**

## Coverage rate

Theoretical rate (equation 5): $0.40\ \text{m} \times 0.15\ \text{m/s} = 216$ m²/h. Turns, overlap and transits reduce
it; the M3 target (100 m²/h) leaves room for a 54 % loss. **Calculation.**

## Coverage simulation

The team simulated one full cleaning cycle in a representative machining cell with a boustrophedon coverage path and
breadth-first-search transits between cells.

![Boustrophedon coverage of a 12 × 8 m machining cell with three machines. Blue = cleaning lanes, red dashed = transit, shaded = area covered. Simulation.](img/coverage_simulation.png)

| Parameter (assumption) | Value |
|---|---|
| Cell | 12 × 8 m with three machines; 74.5 m² free floor |
| Cleaning width | 0.40 m, 5 cm overlap |
| Speed | 0.15 m/s cleaning |
| Turn time | 6 s per turn |
| Average load | 160 W; 144 Wh usable |

| Result | Value | Target |
|---|---|---|
| Coverage of free floor | **96 %** | — |
| Cycle time | **25.6 min** | Fits a 30-min shift change |
| Coverage rate | **167 m²/h** | M3 ≥ 100 m²/h ✔ |
| Energy per cycle | **68 Wh** | ≈ 2.1 cycles per charge |

**Simulation, not a physical test.** The simulator does not model wheel slip, obstacles that move, LiDAR dropouts on
reflective metal or suction failures. Lesson 9 says the simulator must later reproduce field failures, otherwise it
lies; the planned `sim/sensors/` and `sim/replay/` folders exist for that (Chapter 11).

## Wheel torque and drive load (deduced, to be verified)

Loaded mass is not yet measured. With an estimated 35 kg loaded robot (deduced: frame, battery ≈ 7.5 kg, 20 L tank
partly full, modules) and rolling resistance coefficient $C_{rr} \approx 0.02$ on concrete, the rolling force is
$F = C_{rr} m g \approx 7$ N, i.e. 0.43 N·m per wheel at $r = 0.062$ m. Accelerating at 0.3 m/s² adds 10.5 N
(0.33 N·m per wheel). The JGB37-3530 torque at 59 rpm must be checked against these values with a full tank; until
then the test fill is limited (Design of Models, M2 notes). **Deduced estimate, to verify.**

## Structural safety factors

Target design factors (Shigley, equation 10): $n \ge 2$ on the full loaded mass, $n \ge 3$ at mounts that take
bumps; compactor 100 kgf on a 150 kgf actuator ($n = 1.5$). The structural checks are done per part when the CAD is
drawn from measured parts (rule 8: measure real parts before modeling).

## Worst-case circuit analysis (WCCA)

`tools/wcca.py risk/wcca.yaml` evaluates every interface at the extremes of supply and tolerance (EVA) and
statistically (RSS). Inputs: battery 10.5–14.7 V (discharged to charging), MCU VDD 3.2–3.4 V (to verify against the
UNO Q documentation).

| Interface | Inputs | Worst case | Status |
|---|---|---|:-:|
| Battery-sense divider → ADC | 33 kΩ / 8.2 kΩ, 1 % | Vout 2.057–2.973 V (nominal 2.548, RSS max 2.959) vs 3.10 V limit → **4.1 % margin** | ⚠ tighten |
| Bumper switch → MCU logic | Pull-up to 3.3 V; VIH 2.31 V, VIL 0.99 V | 0.89 V margin high and low | ✔ |
| HX711 DOUT → MCU logic | HX711 at 3.3 V | 0.59 V margin high and low | ✔ |
| Drive branch | 3 A nominal, 12 A peak, 15 A fuse, 14 AWG (15 A) | Fuse ≤ wire ampacity | ✔ |
| Collection branch | 10 A nominal, 25 A peak, 20 A fuse, 12 AWG (20 A) | Fuse ≤ wire ampacity | ✔ |
| Separation branch | 2 A nominal, 8 A peak, 10 A fuse, 16 AWG (10 A) | Fuse ≤ wire ampacity | ✔ |
| Logic branch | 1.5 A nominal, 3 A peak, 5 A fuse, 18 AWG (7 A) | Fuse ≤ wire ampacity | ✔ |
| Runtime | 144 Wh usable, 160 W | 54 min | ✔ |

**Action.** The battery-sense divider margin (4.1 %) is too thin: retune the divider (e.g. a larger bottom resistor
ratio) and re-run with measured parts. The analysis uses datasheet tolerances; UNO Q supply limits are still to
verify, then the WCCA is re-run with measured parts.

## Economic calculations

The full economic evaluation (investment, benefits, operating costs, payback, NPV, scenarios and sensitivity) is in
Chapter 14; it is reproduced by `python tools/econ.py`.
