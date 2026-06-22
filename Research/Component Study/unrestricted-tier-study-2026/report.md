# Weight-Unrestricted Component Research

Generated from the validated JSON evidence register. Fields explicitly marked uncertain are omitted here and remain visible in `results/`.

## Contents

1. [Vehicle scale, frame and prop guards](#vehicle-scale-frame-and-prop-guards)
2. [Flight controller and autopilot](#flight-controller-and-autopilot)
3. [ESC and power distribution](#esc-and-power-distribution)
4. [Motors, propellers and battery](#motors-propellers-and-battery)
5. [Companion compute](#companion-compute)
6. [Cameras and perception sensors](#cameras-and-perception-sensors)
7. [Optical flow, ranging and navigation](#optical-flow-ranging-and-navigation)
8. [Control link, telemetry and logging](#control-link-telemetry-and-logging)
9. [Safety, test and support hardware](#safety-test-and-support-hardware)

## Vehicle scale, frame and prop guards

### Value Pick

Existing custom 2-inch printed-nylon guarded frame, steel M2 fasteners, positive battery strap

### Value Cost Usd

$40 engineering allowance

### Value Rationale

The locked 129.8 g architecture is already the lowest-cost credible guarded vehicle. Removing the mass ceiling creates no reason to discard a frame that closes the current mass, mounting, and safety requirements.

### Premium Pick

Custom carbon/composite guarded industrial quad sized around four T-Motor A6-M 23-inch propulsion modules

### Premium Rationale

This is the coherent airframe scale for the premium sensors and industrial compute. It can provide large payload and redundant avionics capacity, but it is not safely hand-thrown and is a poor match to the original indoor recovery experiment.

### Optimal Pick

GEPRC GEP-CL35 V2 3.5-inch guarded frame, SKU GP105886

### Optimal Cost Usd

$69.99

### Optimal Rationale

The 142 mm frame has one-piece injection guards, reinforced guard-to-frame joints, a shock-isolated camera mount, positive battery retention, and enough volume for a Pixhawk-class FC plus perception hardware. It is the smallest catalog frame with credible room for the optimal avionics stack.

### Key Specs

Value: about 42.5 g design allowance, 2-inch guards. Premium: 23-inch propulsion class and multi-kilogram vehicle. Optimal: 142 mm motor-to-motor, 95 mm guard inside diameter, 3.5-inch props, 25.5 x 25.5 mm FC holes, 12 x 12 mm motor holes, 133.7 g frame.

### Interfaces

The optimal frame does not natively accept the Pixhawk 6C Mini footprint; a stiff adapter plate and isolated avionics deck are required. Motor holes directly match the selected GEPRC 2105.5 motors. The integrated XT60 mount suits 6S current.

### Evidence

- url: https://geprc.com/product/gep-cl35-v2-frame/ | supports: $69.99 price, 133.7 g mass, geometry, injection guards, reinforced joints, battery retention, and mounting patterns
- url: https://geprc.com/product/geprc-cinelog35-v2-analog-fpv-drone/ | supports: 263.8 g catalog aircraft using this frame, 6S 1050-1300 mAh recommendation, and selected motor family
- url: https://store.tmotor.com/product/a6-m-6s-uav-modular-propulsion-kit.html | supports: Premium scale: 23-inch prop, 390 g per arm, 2-2.5 kg rated and 6 kg maximum thrust per arm

### Integration Risks

The GEP frame consumes 133.7 g before avionics and may be near the practical payload limit of a 3.5-inch cinewhoop once OAK, Pixhawk, telemetry, and a 6S pack are added. Guards alter propeller thrust and transient response. The premium frame would make release testing hazardous and changes the project into an industrial UAV program.

### Bench Gates

Freeze actual takeoff mass after assembly. Require measured T/W >=2.0 at minimum loaded voltage, no prop-to-guard contact, <=1.0 mm lateral guard deflection at the defined proof load, and no permanent deformation after the release-envelope drop test. Reject the 3.5-inch scale if the fully integrated craft cannot meet T/W or guard clearance.

### Confidence

Optimal frame geometry, price, and mass CONFIRMED by GEPRC. Adapter design and installed stiffness BENCH_REQUIRED. Premium custom frame cost and structural design ASSUMED.


## Flight controller and autopilot

### Value Pick

Holybro Kakute H7 Mini v1.5, SKU 11082, running ArduPilot

### Value Cost Usd

$58.99

### Value Rationale

It retains the six-UART resource map already proven at the desk, exposes enough DShot outputs, weighs 5.5 g, and is the least expensive H7 option in the current evidence set.

### Premium Pick

Holybro Pixhawk 6X Pro Standard v2B with PM02D, SKU 11070+18125+15011

### Premium Cost Usd

$797.99

### Premium Rationale

The industrial ADIS16470 IMU, triple-IMU architecture, dual barometers, isolation, heating, Ethernet, and Pixhawk connector standard maximize sensor quality, redundancy, and development I/O.

### Optimal Pick

Holybro Pixhawk 6C Mini Model A current revision with PM02 V3

### Optimal Cost Usd

$149.98 configured price captured 2026-06-22

### Optimal Rationale

It provides dual isolated/heated IMUs, an H743, I/O processor, 14 outputs, CAN, and standardized connectors without the cost, size, and payload penalty of the 6X Pro. For a violent release event, redundant isolated IMUs are a material upgrade over the single-IMU Kakute.

### Key Specs

Kakute: H743, 6 UART, 9 PWM, 5.5 g, 2S-6S. 6C Mini: H743, ICM-42688-P plus BMI088, MS5611, 42.4 g Model A, 14 PWM, -40 to 85 C. 6X Pro: H753, industrial ADIS16470 plus redundant IMUs, dual barometers, Ethernet.

### Interfaces

Value uses solder pads and the existing UART allocation. Optimal uses JST-GH serial ports, CAN for ARK Flow, UART for companion MAVLink and ELRS, analog PM02 V3, and microSD logs. Premium requires PM02D digital power; Holybro explicitly says the 6X does not accept analog power modules.

### Evidence

- url: https://holybro.com/collections/flight-controllers/products/kakute-h7-mini | supports: $58.99, SKU 11082, six UARTs and product availability
- url: https://docs.holybro.com/autopilot/kakute-h7-v1-v2-mini/kakute-h7-mini/overview | supports: Kakute processor, power, output and mass specifications
- url: https://holybro.com/products/pixhawk-6c-mini | supports: 6C Mini price, current 42.4 g Model A, redundant IMUs, H743, isolation and heating
- url: https://docs.holybro.com/autopilot/pixhawk-6c-mini/technical-specification | supports: 6C Mini detailed ports and electrical specifications
- url: https://holybro.com/products/pixhawk-6x-pro | supports: $797.99 Standard+PM02D configuration and compatibility warning
- url: https://docs.holybro.com/autopilot/pixhawk-6x-pro/overview | supports: ADIS16470, redundancy, isolation, heating and Ethernet

### Integration Risks

ArduPilot target support does not prove every optional port or sensor path in the exact purchased revision. The optimal frame needs a custom FC adapter. Industrial IMU saturation range is useful, but recovery success still depends on estimator tuning and vibration, not FC price alone.

### Bench Gates

Verify exact revision, ArduPilot boot, all assigned ports, microSD logging, CAN discovery, and DShot outputs before installing props. Replay or rig-test release angular rates without IMU clipping or EKF lane failure. Require no brownout at worst simultaneous peripheral load and motor step.

### Confidence

Catalog hardware and prices CONFIRMED. ArduPilot recovery behavior and estimator performance BENCH_REQUIRED. The 6C Mini optimal ranking is an engineering decision based on redundancy-to-integration tradeoff.


## ESC and power distribution

### Value Pick

HGLRC 13A 2-3S BB2 20 x 20 mm 4-in-1 ESC

### Value Cost Usd

$18 baseline acquisition estimate

### Value Rationale

It is already sized above the claimed 9.2 A motor peak and matches the locked 20 mm stack. No cheaper substitute has better project-specific evidence.

### Premium Pick

Four T-Motor A6-M integrated 6S FOC 50A CAN/PWM propulsion modules plus a high-current distribution harness

### Premium Rationale

Per-arm integrated FOC control, CAN telemetry, IPX6 construction, and matched motor/ESC/prop remove the largest compatibility uncertainty in a large professional vehicle.

### Optimal Pick

Holybro Tekko32 F4 4-in-1 Mini 50A AM32 ESC plus Holybro PM02 V3 and separate 5 V regulator for perception

### Optimal Cost Usd

$69.99 inferred standalone ESC price from the $128.98 Kakute stack minus $58.99 FC; PM02 V3 included with selected FC configuration; add $20.99 UBEC 5A if rail test requires it

### Optimal Rationale

The 20 mm AM32 ESC provides large margin over the GEPRC motor's 34.9 A published maximum, digital protocol support, and compact wiring. Separating the perception regulator prevents OAK/Pi transients from contaminating the flight-controller rail.

### Key Specs

Value: 13 A/channel, 2-3S. Optimal ESC: 50 A/channel mini class, 6S capable; selected motor publishes 34.9 A maximum. Holybro UBEC: 5 A, 3-14S. Premium A6-M: 6S, FOC 50A, PWM/CAN, 40 A stated short peak in the product table.

### Interfaces

Optimal: battery to XT60/PDB; PM02 V3 supplies FC voltage/current measurement; ESC receives four DShot signals; isolated 5 V BEC supplies OAK-D Lite and Pi with a common signal ground. Premium CAN protocol support must be validated against the exact ArduPilot ESC driver before relying on it; PWM is the fallback.

### Evidence

- url: https://holybro.com/products/kakute-h7-mini-stacks | supports: $128.98 Kakute+Tekko32 Mini stack and AM32 50A selection
- url: https://holybro.com/collections/flight-controllers/products/kakute-h7-mini | supports: $58.99 FC price used to infer ESC subtotal
- url: https://holybro.com/collections/power-modules-pdbs | supports: $20.99 UBEC 5A and power-module catalog
- url: https://store.tmotor.com/product/a6-m-6s-uav-modular-propulsion-kit.html | supports: $99.90 base module, 6S FOC, CAN/PWM, rated and maximum thrust

### Integration Risks

The Tekko standalone price is inferred, not a direct quote. AM32 bidirectional DShot and telemetry behavior must be proven with ArduPilot. The motor's published 34.9 A is at 5S despite a 6S application; the exact 6S prop current remains unknown. PM02 V3 current and connector ratings must exceed measured pack current.

### Bench Gates

At minimum loaded voltage, require per-channel RMS and peak current within ESC ratings with >=20% continuous margin, pack connector temperature rise <20 C, no desync over repeated full-step commands, valid RPM telemetry if used, and no FC/perception brownout. Measure rail ripple and p95 voltage during synchronized motor and inference load steps.

### Confidence

Value selection INFERRED from prior baseline evidence. Optimal ESC rating CONFIRMED at product-family level; exact standalone SKU/price and 6S current BENCH_REQUIRED. Premium CAN interoperability BENCH_REQUIRED.


## Motors, propellers and battery

### Value Pick

4 x Happymodel EX1103 11000KV, Gemfan Hurricane 2023-3, GNB 2S 550 mAh 100C XT30

### Value Cost Usd

$56 total baseline estimate: motors $36, props $6, battery $14

### Value Rationale

This remains the lowest-cost tested architecture candidate and has a vendor motor/prop data point. The main limitation is not nominal thrust but the absence of independent 7.0 V guarded thrust data.

### Premium Pick

4 x T-Motor A6-M KV280 integrated 6S propulsion units with MF2311P-M 23-inch props and an appropriately sized 6S high-rate pack

### Premium Rationale

The matched industrial propulsion system publishes rated and maximum thrust, integrates FOC ESCs, and has enough reserve to carry premium compute. It is intentionally a capability ceiling, not the recommended recovery platform.

### Optimal Pick

4 x GEPRC SPEEDX2 2105.5 2650KV, Gemfan D90-3 90 mm ducted tri-blades, 6S 1050-1300 mAh high-rate LiPo

### Optimal Rationale

GEPRC uses the same motor family and 6S 1050-1300 mAh pack class on the 263.8 g CineLog35 V2. The motor is designed for 3-4 inch whoops and the D90 is explicitly designed for 3.5-inch ducts. This is the strongest coherent catalog propulsion match for the selected guarded frame.

### Key Specs

Optimal motor: 21 g, 2-6S, 34.9 A and 559 W published maximum at 5S, 12 x 12 mm M2 mount. D90: 90 mm, 3-inch pitch, 2.3 g, 2203-2306 motor compatibility. Frame vendor recommends 6S 1050-1300 mAh. Premium A6-M: 390 g/arm including prop and wires, 2-2.5 kg rated thrust, 6 kg maximum.

### Interfaces

Optimal motor and frame both use 12 x 12 mm M2 mounting. D90 supports M5 and T-mount adapters; verify the exact hub hardware against the 1.5 mm motor shaft. Use XT60, 6S-rated ESC/BEC, and a battery strap plus secondary retention.

### Evidence

- url: https://geprc.com/product/geprc-speedx2-2105-5-2650kv-3450kv-motor/ | supports: $21.99, 21 g, voltage, current, power, mounting, and intended prop class
- url: https://www.gemfanhobby.com/d90-ducted-pc-3-blade-m5.html | supports: D90 geometry, 2.3 g mass, ducted application and motor compatibility
- url: https://geprc.com/product/geprc-cinelog35-v2-analog-fpv-drone/ | supports: 263.8 g reference craft, 2105.5 2650KV 6S use, and 1050-1300 mAh recommendation
- url: https://store.tmotor.com/product/a6-m-6s-uav-modular-propulsion-kit.html | supports: Premium module price and performance

### Integration Risks

No primary source found for static thrust of the exact 2105.5+D90+guard combination at minimum loaded 6S voltage. The published motor maximum is at 5S and cannot size the 6S battery or ESC by itself. Larger vehicles increase angular inertia; premium thrust does not compensate for release safety and inertia penalties.

### Bench Gates

Test the exact guarded assembly at full, nominal, and minimum loaded voltage. Require measured total static thrust >=2.0 x frozen takeoff mass using an uncertainty-adjusted lower bound; battery sag <=10% during the acceptance step; cell temperature <=60 C and connector rise <20 C; no prop/guard rub; and repeatable 10-90% thrust rise <=100 ms. Derive the final battery capacity from measured current, not C-rating alone.


## Companion compute

### Value Pick

Arduino Nicla Vision

### Value Cost Usd

$90 baseline estimate

### Value Rationale

It combines MCU, camera, IMU, and ToF in the existing 19.8 g architecture and avoids a Linux computer. It is the cheapest path already integrated into the project, provided it passes the 50 ms event-to-MAVLink gate.

### Premium Pick

NVIDIA Jetson AGX Orin Industrial 64 GB production module on an airborne carrier

### Premium Cost Usd

$2,899 suggested 1KU+ module price; carrier, storage, cooling and DC/DC excluded

### Premium Rationale

Industrial temperature range, ECC, long operating life, large memory, and up to roughly 248 TOPS support multi-camera models and extensive onboard logging. The compute is vastly beyond the recovery classifier's demonstrated need.

### Optimal Pick

Raspberry Pi Zero 2 W as MAVLink/DepthAI host, with inference executed on OAK-D Lite

### Optimal Cost Usd

$15 Pi plus $169 OAK-D Lite accounted under perception

### Optimal Rationale

The Pi handles orchestration, timestamps, logging and MAVLink while the OAK executes neural and stereo workloads on-device. This avoids the 7-25 W and thermal burden of a Jetson while replacing the Nicla rolling-shutter bottleneck.

### Key Specs

Pi Zero 2 W: quad-core 64-bit Cortex-A53 at 1 GHz, 512 MB, 65 x 30 mm, $15. Jetson AGX Orin Industrial: 64 GB, ECC, industrial temperature support, up to about 248 TOPS and 15-75 W operating range. OAK RVC2 provides 4 TOPS/1.4 AI TOPS and typically a few watts.

### Interfaces

Optimal: OAK-D Lite over USB host to Pi; Pi UART at 3.3 V to Pixhawk TELEM port using MAVLink2; separate regulated 5 V supply sized for Pi+OAK; common ground; hardware timestamps carried in logs. Companion sends bounded high-level commands only.

### Evidence

- url: https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/ | supports: $15, CPU, memory and board dimensions
- url: https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-agx-orin/ | supports: Jetson performance and power families
- url: https://developer.nvidia.com/embedded/faq | supports: $2,899 Jetson AGX Orin Industrial suggested price and 10-year industrial product lifetime
- url: https://ardupilot.org/dev/docs/mavlink-basics.html | supports: MAVLink companion addressing, command acknowledgement limitations and transport behavior

### Integration Risks

Pi Zero 2 has only 512 MB and one USB OTG path; the exact DepthAI pipeline must fit and remain deterministic. Linux scheduling can create latency tails. The Jetson industrial module requires a carrier, cooling, regulated high power, and startup management; listing price is not a complete airborne solution.

### Bench Gates

Require p95 sensor-event-to-accepted-MAVLink latency <=50 ms, p99 <=75 ms, zero missed heartbeat failsafes over a 30-minute run, synchronized timestamps within 5 ms, and no compute reset during motor load steps. Demonstrate safe FC behavior when the companion freezes, reboots, sends malformed commands, or disconnects.

### Confidence

Catalog compute specifications and prices CONFIRMED. Pi+OAK software fit and latency BENCH_REQUIRED. Jetson carrier mass, thermal solution, and complete cost are not included and remain ASSUMED.


## Cameras and perception sensors

### Value Pick

Nicla Vision onboard GC2145 camera with onboard IMU/ToF fusion

### Value Cost Usd

Included in the $90 Nicla line

### Value Rationale

It is already the lowest-parts-count vision path. Its rolling shutter and unproven effective FPS are the reasons it is not the mission-optimal path.

### Premium Pick

Luxonis OAK 4 D Pro W

### Premium Cost Usd

$1,049 wide-field variant

### Premium Rationale

OAK4 adds a Linux-capable 48-52 TOPS vision platform, stereo depth, global-shutter mono cameras, integrated storage and a modern standalone perception stack. It maximizes sensor/compute capability in one supported product.

### Optimal Pick

Luxonis OAK-D Lite with fixed-focus/global-shutter stereo mono pair; use the mono stream for motion/release cues and stereo depth for scene geometry

### Optimal Cost Usd

$169

### Optimal Rationale

It provides two global-shutter OV7251 mono cameras, stereo depth, IMU, and onboard neural inference at about 2.5-4 W. This directly addresses the Nicla rolling-shutter/FPS risk without requiring a high-power Jetson.

### Key Specs

OAK-D Lite: RVC2, 4 TOPS/1.4 AI TOPS, dual global-shutter OV7251 mono sensors, rolling-shutter IMX214 color sensor, BMI270 IMU, approximately 2.5-4 W. OAK 4 D Pro W: up to about 52 TOPS, integrated Linux-class compute, stereo depth; store listing mass 674 g.

### Interfaces

OAK-D Lite uses USB to Pi Zero 2 W and a dedicated regulated 5 V rail. The perception pipeline should use global-shutter mono frames for recovery classification; color is optional. Output only time-stamped state/confidence to the FC over MAVLink.

### Evidence

- url: https://docs.luxonis.com/hardware/products/OAK-D%20Lite | supports: OAK-D Lite cameras, global shutter, IMU, compute and power
- url: https://shop.luxonis.com/collections/oak-cameras-col | supports: $169 OAK-D Lite price
- url: https://shop.luxonis.com/products/oak-4-d-ea | supports: $949/$1,049 OAK4 variants, 674 g listing mass and current availability signal
- url: https://shop.luxonis.com/ | supports: OAK4 compute claims and product-family status

### Integration Risks

OAK-D Lite's RGB camera remains rolling shutter, so the wrong pipeline choice would preserve the original failure mode. Stereo depth can fail on textureless surfaces and at close range. OAK4 availability is early-access/new-stock and its 674 g enclosure makes it unsuitable for the optimal 3.5-inch build.

### Bench Gates

Use a rotating/release target to require >=40 effective global-shutter frames/s, p95 exposure-to-classification <=40 ms, total event-to-FC <=50 ms, >=95% release-event recall at the pre-registered false-trigger rate, and no dropped-frame burst longer than 25 ms. Validate lighting, motion blur, minimum range, and guard occlusion across the cage test envelope.

### Confidence

Sensor types, power and prices CONFIRMED by Luxonis. Recovery classification accuracy, latency and stereo behavior BENCH_REQUIRED. OAK4 stock timing may change.


## Optical flow, ranging and navigation

### Value Pick

Matek 3901-L0X optical flow plus ToF module over one MSP UART

### Value Cost Usd

$26 baseline estimate

### Value Rationale

It is the lowest-cost and lightest integrated flow/range option already mapped to ArduPilot, with both functions sharing one serial resource.

### Premium Pick

ARK Flow for nadir velocity/height plus LightWare SF45/B scanning lidar for wider obstacle and range awareness

### Premium Rationale

The pair adds redundant ranging modalities, DroneCAN integration, an onboard IMU, long-range scanning, and far more environmental observability than the release controller requires.

### Optimal Pick

ARK Electronics ARK Flow over DroneCAN

### Optimal Cost Usd

$250

### Optimal Rationale

At 5 g it provides PAW3902 low-light optical flow, AFBR ToF ranging and an ICM-42688 IMU on DroneCAN. CAN avoids consuming another serial port, offers device status, and is a cleaner Pixhawk integration than MSP UART.

### Key Specs

ARK Flow: 5 g, 5 V, maximum stated 76 mA, PAW3902, AFBR range sensor with typical reach up to 30 m, ICM-42688, Pixhawk-standard CAN connector. SF45/B: 0.2-50 m, up to 5,000 readings/s, five sweeps/s, UART/I2C, about 59 g.

### Interfaces

Optimal connects to CAN1 with a Pixhawk-standard four-pin cable and must be terminated correctly. ArduPilot configures optical flow and rangefinder as DroneCAN devices. Premium SF45/B needs a separate UART or I2C path, regulated 5 V, and a mechanically clear scan plane.

### Evidence

- url: https://arkelectron.com/product/ark-flow/ | supports: $250, 5 g, sensor set, power, range and DroneCAN interface
- url: https://docs.arkelectron.com/sensor/ark-flow-mr/ardupilot-instructions | supports: ArduPilot DroneCAN configuration for optical flow and rangefinder
- url: https://lightwarelidar.com/shop/sf45-b-50-m/ | supports: SF45/B product and 50 m class
- url: https://lightwarelidar.com/wp-content/uploads/2025/07/SF45B-Product-Guide-v3.pdf | supports: SF45/B range, rate, interfaces, mass and electrical specifications

### Integration Risks

Optical flow is surface-, illumination-, height-, and vibration-dependent. The ARK Flow range figure is typical, not guaranteed acceptance performance. CAN node IDs, bus termination, orientation and EKF source switching require explicit configuration. SF45/B adds mass and scan latency without solving the core release classifier.

### Bench Gates

Require valid flow quality and range throughout the intended height, lighting and floor-texture envelope; velocity error <=0.25 m/s RMS in the cage; range error <=5% or 5 cm, whichever is larger, in the recovery band; no CAN errors over 30 minutes; and clean EKF fallback when flow/range is blocked or invalid.


## Control link, telemetry and logging

### Value Pick

BetaFPV ELRS Lite receiver using CRSF telemetry; FC microSD logs; USB download after each trial

### Value Cost Usd

$12 receiver baseline estimate

### Value Rationale

One low-cost link supplies manual override and basic telemetry. Full-rate logs remain onboard, so a second air radio is not required for the first recovery experiments.

### Premium Pick

CubePilot Herelink 1.1 for RC/video/telemetry plus Holybro Microhard P900 V2 pair as an independent MAVLink data link

### Premium Rationale

Herelink combines control, HD video and telemetry while Microhard adds an independent high-power data path. This maximizes link redundancy and ground observability, at substantial cost, RF complexity and airborne power.

### Optimal Pick

RadioMaster RP3 V2 diversity ELRS receiver for manual override plus Holybro SiK Telemetry Radio V3 100 mW pair for MAVLink; FC microSD as the authoritative log

### Optimal Cost Usd

$19.99 RP3 plus $58.99 SiK pair = $78.98

### Optimal Rationale

The RP3 adds antenna diversity and a TCXO for the safety-critical RC path. The independent SiK link supports live Mission Planner/QGroundControl observability without coupling control loss to telemetry loss. Onboard logs avoid treating an RF link as lossless.

### Key Specs

RP3: dual-antenna diversity, up to 100 mW telemetry, ExpressLRS 2.4 GHz. SiK V3 100 mW: 23.5 g airborne unit with antenna, 5 V, 100 mA transmit, MAVLink-oriented firmware, up to 250 kbps RF data rate. Microhard P900: up to 1 W, 276 kbps, 81 g with antenna. Herelink: up to 20 km FCC, 110 ms video delay, 720p/1080p.

### Interfaces

RP3 uses CRSF on a full UART. SiK uses a separate 3.3 V UART/JST-GH telemetry port. Logs from Pixhawk microSD and companion storage must share event IDs and synchronized timestamps. Ground link loss must not alter FC stabilization behavior.

### Evidence

- url: https://www.radiomasterrc.com/products/rp3-expresslrs-2-4ghz-nano-receiver | supports: $19.99 sale price, TCXO, diversity and telemetry PA
- url: https://holybro.com/products/sik-telemetry-radio-v3 | supports: $58.99 pair, MAVLink support, link rates, mass and electrical data
- url: https://holybro.com/products/microhard-telemetry-radio-copy | supports: $449 pair, RF power, rates, mass and power
- url: https://docs.cubepilot.org/user-guides/herelink/herelink-overview | supports: Herelink range, video delay, resolution and system integration
- url: https://ardupilot.org/dev/docs/mavlink-basics.html | supports: MAVLink is not guaranteed delivery and commands require state/acknowledgement checks

### Integration Risks

2.4 GHz RC and any 2.4 GHz Wi-Fi/video source can interfere if antennas and channels are poorly planned. The SiK air unit is 23.5 g, material on a 3.5-inch craft. Herelink plus Microhard duplicates functions and increases RF, power and configuration failure modes.

### Bench Gates

Perform range and antenna-shadow tests in the complete guard/frame, verify independent RC and telemetry failsafes, require no RC packet-loss burst longer than the configured recovery tolerance, prove onboard logs survive link loss, and align FC/companion timestamps within 5 ms. Test loss and restoration of each link independently.


## Safety, test and support hardware

### Value Pick

VIFLY Finder Mini/LED, DIY 1-2 kg load-cell thrust stand, PVC/net cage, tethered release fixture and ToolkitRC-class charger

### Value Cost Usd

Approximately $168 support subtotal: $18 flying status hardware plus $150 charger/stand/cage/release allowances

### Value Rationale

These are sufficient to validate the current micro propulsion, execute tethered releases and recover logs without buying laboratory instrumentation.

### Premium Pick

Tyto Robotics Series 1585 thrust-stand bundle, instrumented guarded flight stand/release rig, redundant independent kill path, high-speed camera and isolated battery fire enclosure

### Premium Cost Usd

$1,075 for the Series 1585 bundle; custom flight rig, camera and enclosure excluded

### Premium Rationale

Calibrated thrust/torque/RPM/electrical measurement and a mechanically constrained release rig provide defensible professional evidence. For a premium multi-kilogram vehicle, an open hand-release is unacceptable.

### Optimal Pick

Tyto Series 1585 or verified equivalent for propulsion characterization, rigid netted cage, repeatable gimbaled/tethered release rig with angle encoder, independent RC kill, VIFLY finder, smoke-safe LiPo charging/storage

### Optimal Rationale

The optimal vehicle is likely 0.5-0.65 kg, beyond the current DIY 1-2 kg stand's comfortable evidence margin once guarded transients are measured. A calibrated stand and repeatable release fixture buy more decision quality than premium airborne compute.

### Key Specs

Series 1585/1580 class measures up to 5 kgf thrust and 2 N m torque. Tyto's 2026 Flight Stand successor advertises 1,000 Hz sampling. The selected 3.5-inch system needs guarded single-motor and, ideally, full-vehicle thrust characterization.

### Interfaces

Log stand thrust/current/voltage/RPM against synchronized FC and companion timestamps. Release rig must constrain translation until commanded release, measure initial attitude/rate, and allow a hard mechanical tether independent of software. Kill switch must bypass companion logic.

### Evidence

- url: https://www.tytorobotics.com/products/series-1580-test-stand-bundle | supports: $1,075 Series 1585 bundle
- url: https://www.tytorobotics.com/pages/drone-test-stands/1000 | supports: 5 kgf thrust and 2 N m torque measurement range
- url: https://www.tytorobotics.com/blogs/updates/tyto-robotics-releases-new-drone-test-stand-the-flight-stand-15-50 | supports: 2026 successor, 1,000 Hz sampling and measured quantities
- url: https://download.ardupilot.org/downloads/wiki/pdf_guides/MultiCopter_Safety.pdf | supports: ArduPilot safety modes and controlled test principles

### Integration Risks

A single-motor stand does not reproduce duct interactions or full-vehicle battery sag. The Series 1585 listing was out of stock when crawled, so an equivalent calibrated instrument may be required. Large premium propulsion exceeds this stand and requires a different facility.

### Bench Gates

Calibrate before and after each propulsion campaign; require measurement uncertainty <=3% of the acceptance threshold. No free-flight release until prop-off state-machine tests, restrained motor tests, kill-switch test, tethered recovery attempts and guard proof test all pass. Abort on any uncommanded arming, estimator reset, prop contact, battery movement or lost kill path.
