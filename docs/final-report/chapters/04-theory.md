# Theoretical framework

This chapter summarizes the theory behind each subsystem and the design methods used. Each topic is tied to the
design decision it supports.

| Subsystem | Theory | Design consequence |
|---|---|---|
| Whole project | VDI 2206 V-model, systematic design | Requirements → architecture → domains → integration → verification |
| Mobility | Differential-drive kinematics | 0.38 m/s top speed, in-place turns in aisles |
| Localization | Odometry error, inertial sensing, probabilistic SLAM | Encoders + IMU + LiDAR; localize against a saved map |
| Coverage | Coverage path planning (boustrophedon) | M3 target of 100 m²/h; coverage simulation |
| Collection | Pneumatic conveying, pickup velocity | Suction rig first; option B as contingency |
| Separation | Screening, magnetic separation | Mesh basket + neodymium bar magnets close to the flow |
| Waste recovery | Metalworking-fluid recovery, chip briquetting | Two streams; compaction drains oil back to the tank |
| Actuation and power | DC-motor equations, lead-acid battery limits | Current as stall measure; 50 % DoD → 144 Wh |
| Control | Embedded real-time vs. general-purpose computing | MCU/Linux split by timing requirement |
| Structure | Design factor (Shigley) | n ≥ 2 general, n ≥ 3 at bump mounts |
| Safety | ISO 3691-4 driverless trucks, braking physics, IP code | Speed limit, hardware e-stop, bumpers, IP54 bay |

## Mechatronic design methodology

The project follows the V-model for mechatronic systems in VDI 2206, which goes from requirements to a system
architecture, develops each domain (mechanical, electrical, software) in parallel and integrates them through staged
verification [22]. The conceptual-design tools come from systematic engineering design: the black box and function
structure abstract the product as flows of material, energy and signals, and the morphological matrix combines
alternative working principles for each function into concepts [18]. Requirement weighting, concept screening and
the product architecture follow Ulrich, Eppinger and Yang [17]. The quality matrix uses the 0/1/3/9 relationship scale
of the house of quality [19], the component comparison borrows the pairwise logic of the analytic hierarchy process
[20], and the goal tree follows the logical-framework approach [21].

## Differential-drive locomotion

A differential-drive robot has two independently driven wheels on a common axle and a passive caster. With wheel
radius $r$, track width $b$ and wheel speeds $\omega_R$ and $\omega_L$, the forward and angular velocities of the body
are [23]:

$$v = \frac{r(\omega_R + \omega_L)}{2}, \qquad \omega = \frac{r(\omega_R - \omega_L)}{b} \tag{1}$$

and the pose $(x, y, \theta)$ evolves as

$$\dot x = v\cos\theta, \qquad \dot y = v\sin\theta, \qquad \dot\theta = \omega \tag{2}$$

Equal and opposite wheel speeds turn the robot in place, which is what lets it work in narrow aisles. With the
selected 59 rpm gearmotors and 124 mm wheels, the maximum speed is

$$v_{max} = \pi \cdot d \cdot \frac{n}{60} = \pi \cdot 0.124\ \text{m} \cdot \frac{59}{60}\ \text{s}^{-1} \approx 0.38\ \text{m/s} \tag{3}$$

(calculation); the cleaning speed is limited to 0.15 m/s in firmware.

## Odometry, inertial sensing and traction on oily floors

Integrating equation (2) with encoder counts gives wheel odometry, whose error grows without bound. Borenstein and
Feng separate systematic errors (unequal wheel diameters, uncertain track width) from non-systematic ones (uneven
floors, wheel slip) and show how to calibrate the former [24]. On an oily floor, slip is the dominant non-systematic
error: liquid contaminants lower the available friction coefficient between a contact surface and the floor [3]. The
robot therefore fuses encoders with an IMU (BNO055), whose gyroscope measures the turn rate $\dot\theta$ independently
of the wheels, and corrects the remaining drift with LiDAR scan matching. The BNO055 runs in IMU mode, without the
magnetometer, because steel machines and motors distort the magnetic field (ADR-0005). Traction also sets the maximum
braking deceleration ($a \le \mu g$), which is why speed is limited and rubber wheels were chosen.

## Mapping and localization (SLAM)

Probabilistic robotics models the robot's pose and map as a belief updated by motion and sensor models [25]. In SLAM
the robot estimates both at once; Cadena et al. describe the modern factor-graph formulation and its robustness
challenges [8]. For a 2D LiDAR such as the RPLIDAR A1M8, occupancy-grid methods are standard: GMapping uses a
Rao-Blackwellized particle filter [26], Cartographer combines local scan matching with submaps and real-time loop
closure [27], and SLAM Toolbox provides graph-based mapping, localization in a saved map and map merging for long-term
use [28]. The project needs exactly these functions: **map the area once, save it, and localize against it on every
shift change.** The team's previous robot showed that localizing against a known map beats building the map on the
fly (lesson 8, Chapter 17).

## Fiducial-marker localization (bench tool)

To test pose estimation before the LiDAR stack exists, the team uses AprilTag fiducial markers [65], [66]. A camera
with intrinsic matrix $K$ observes the four corners of a square tag of known size; the camera pose follows from the
perspective-n-point problem. For a single planar square, infinitesimal plane-based pose estimation (IPPE) gives two
candidate solutions [67], which is why a single small or oblique tag can produce a mirror-image pose. The project's
app constrains the problem to the plane of the floor: with the mount height $z_c$ and pitch $\varphi$ fixed, only
$(x, y, \psi)$ remain, which are solved by Gauss–Newton minimization of the reprojection error

$$E(x, y, \psi) = \sum_{k} \left\| \mathbf{u}_k - \pi\!\left(K, R(\psi,\varphi), \mathbf{t}(x,y,z_c), \mathbf{X}_k\right) \right\|^2 \tag{4}$$

over all corners $\mathbf{X}_k$ of all known tags (Chapter 11).

## Coverage path planning

Cleaning requires visiting every point of the free area, not just reaching a goal. Choset classifies coverage
methods into heuristic, approximate (grid-based) and exact cellular decompositions such as the boustrophedon
decomposition, which splits the area into cells covered by back-and-forth passes [29]. Galceran and Carreras survey
these methods and their performance metrics: coverage completeness, path length, overlap and number of turns [30].
Le et al. show that turns dominate the energy use of a differential-drive cleaner [7]. The theoretical coverage rate
is the product of cleaning width $w$ and speed $v$:

$$\dot A = w \cdot v = 0.40\ \text{m} \times 0.15\ \text{m/s} = 0.06\ \text{m}^2/\text{s} \approx 216\ \text{m}^2/\text{h} \tag{5}$$

which turns, overlaps and transits reduce in practice; this is the basis of the M3 target of 100 m²/h (calculation).

## Vacuum collection and pneumatic pickup

The wet/dry collector works by lowering the pressure inside a sealed volume (separation chamber and tank) so that air
entering the nozzle drags the liquid and particles with it; the waste drops out in the chamber and only air reaches
the motor. The useful air power is

$$P_{air} = \Delta p \cdot Q \tag{6}$$

the product of the pressure difference and the volumetric flow, and it is a fraction of the motor's electrical power.
A particle is lifted and carried only if the local air velocity exceeds its pickup velocity, which increases with
particle density and size [31]. Steel ($\rho \approx 7{,}850$ kg/m³) is several times denser than common dust and
debris, so dense, long chips are the hardest load for a small 80 W unit. **This is the main technical risk of the
project**; if the suction tests fail for chips, the brush will throw the chips into a front hopper and the vacuum will
handle only the liquid (ADR-0004).

## Solid–liquid separation: screening and magnetic capture

Screening separates particles by size: the mesh aperture defines the cut size, and particles larger than the aperture
are retained while the liquid passes [32]. Magnetic separation then exploits differences in magnetic susceptibility.
The force on a particle of volume $V$ and susceptibility difference $\Delta\chi$ in a field $\mathbf{B}$ is [33], [9]:

$$\mathbf{F}_m = \frac{V\,\Delta\chi}{\mu_0}\,(\mathbf{B}\cdot\nabla)\mathbf{B} \tag{7}$$

so capture requires both a strong field and a strong field gradient, which the edges of neodymium bar magnets provide
at short range. Ferrous chips (steel, cast iron) are strongly ferromagnetic and are held; aluminum and brass are not,
so non-ferrous chips are retained only if they are larger than the mesh aperture. The magnets must therefore sit
where the flow passes close to them.

## Recovery of metalworking fluids and chip compaction

Metalworking fluids lose value and become harder to treat when mixed with water, solids or other fluids [10]. Lee et
al. review recovery technologies and show that chips and cutting fluid are best recovered as separate streams: oil is
filtered and reconditioned, and chips are de-oiled and compacted (briquetted) to reduce volume and residual oil
before remelting [11]. The on-board compactor applies this principle at small scale: pressing the chips drains
entrained oil back to the tank and reduces the volume of the solid stream. NIOSH and OSHA document the health effects
that justify minimizing manual contact with these fluids [5], [4].

## Actuation, power and energy budget

The drive, brush and compactor use brushed DC motors controlled by PWM through H-bridges (BTS7960). In steady state,
the armature and torque equations

$$V = R_a I + k_e\,\omega, \qquad T = k_t\,I \tag{8}$$

relate voltage, current, speed and torque, so current is a direct measure of load and stall [34]. This is why the
drivers' current-sense outputs are used to stop a jammed motor (stall cut after ≈ 2 s). Lead-acid batteries lose
cycle life quickly when deeply discharged, so the usable energy is limited to about 50 % of the nominal capacity [35]:

$$E_{use} \approx 0.5 \times 12\ \text{V} \times 24\ \text{Ah} = 144\ \text{Wh} \tag{9}$$

| Load | Estimated average power | Basis |
|---|---|---|
| Vacuum unit (Mikels AA-12) | 80 W | Nameplate rating |
| Brush motor (775) at partial load | ≈ 40 W | Estimate; to be measured |
| Two drive gearmotors | ≈ 30 W | Estimate at 0.15 m/s; to be measured |
| UNO Q, LiDAR, camera, sensors, HMI | ≈ 12 W | Estimate from typical module ratings |
| **Total** | **≈ 160 W → ≈ 55 min per charge** | Compactor runs are short and intermittent |

## Embedded control architecture

The Arduino UNO Q combines a Qualcomm Dragonwing QRB2210 microprocessor running Debian Linux with an STM32U585
microcontroller running Arduino sketches on Zephyr, linked by a remote-procedure-call bridge, plus on-board Wi-Fi and
Bluetooth [36]. The project uses this split: time-critical tasks (PWM, encoder speed loops, sensor sampling,
compactor sequence, watchdog) run on the MCU, and computation-heavy tasks (LiDAR mapping, routes, vision, web
interface) run on Linux. The split is made **by timing requirement, not by complexity**: whatever has a deadline
lives on the MCU, which executes each motion order autonomously and stops by itself if Linux is late (ADR-0002). The
emergency stop does not depend on either processor: it opens the coil of the main relay in hardware.

## Structural design and safety factors

Static and fatigue design follow Shigley's methodology: a part is acceptable when its design factor

$$n = \frac{S}{\sigma} \tag{10}$$

(strength over stress) meets the target [37]. The project uses $n \ge 2$ on the full loaded mass and $n \ge 3$ at
mounts that take bumps, because loads from ramps, cracks and collisions are uncertain. The same idea applies to
actuators: the compactor force is limited to 100 kgf on a 150 kgf actuator ($n = 1.5$).

## Safety of autonomous industrial vehicles

ISO 3691-4 sets safety requirements for driverless industrial trucks and their systems, including speed limits,
personnel detection, braking and emergency stops in operating zones [38]. The prototype is not a certified product,
but its safety concept follows the same logic: a hardware emergency stop, bumpers as a contact backup to the LiDAR,
limited speed, operation only when authorized and in an area cleared of people. The stopping distance under constant
deceleration limited by friction is

$$d = \frac{v^2}{2\mu g} = \frac{(0.38\ \text{m/s})^2}{2 \times 0.1 \times 9.81\ \text{m/s}^2} \approx 0.074\ \text{m} \tag{11}$$

so even on oil ($\mu = 0.1$) the robot needs at most 7.4 cm to stop from top speed (calculation), and a LiDAR stop
zone of 30 cm leaves a wide margin. IEC 60529 defines the IP code used to specify the electronics enclosure; the
target is IP54 (dust-protected and splash-resistant) for oil splash in the plant [39]. ISO 12100 gives the risk
assessment method [59], ISO 13849-1 the performance levels of safety-related control parts [60] and ISO 13850 the
emergency-stop design principles [61].

## Risk, quality and security methods

- **FMEA.** Each failure mode is scored for severity S, occurrence O and detection D (1–10); the risk priority number
  is RPN = S × O × D, and any S ≥ 9 requires an action regardless of RPN [68].
- **Special characteristics (SCCAF).** Characteristics whose variation affects safety, regulation or a key metric
  are classed YC (potential critical) or YS (potential significant) in the DFMEA and agreed as CC/SC with a control
  before build, adapted from Ford's Special Characteristics Communication and Agreement Form [64].
- **DFMA.** Boothroyd–Dewhurst design efficiency $DE = 3 N_{min} / \sum t$ compares the theoretical minimum part count
  with the estimated assembly time [69].
- **WCCA.** Worst-case circuit analysis checks interfaces at the extreme of every tolerance (extreme value analysis,
  EVA) and statistically (root sum square, RSS).
- **Threat modeling.** STRIDE (spoofing, tampering, repudiation, information disclosure, denial of service,
  elevation of privilege) is applied per data flow [70], with IEC 62443 as the industrial reference [71].
- **Ethics by design.** IEEE 7000-2021 turns stakeholder values into ethical value requirements [58].
