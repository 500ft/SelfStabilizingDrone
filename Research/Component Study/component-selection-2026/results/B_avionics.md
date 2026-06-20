# Stream B — Avionics core (flight controller, ESC/AIO, ELRS RX)

Key architecture tradeoff: if the companion board does ALL autonomy and the FC only holds attitude → an AIO (Happymodel X12 / BetaFPV 12A, ~5g, ELRS+ESC onboard) is mass-optimal. If the FC must run MAVLink-driven position-hold / autonomous recovery → need an H7 board (Kakute H7 Mini / Matek H743-Mini) + companion link, costing ~5.5–7g and ~$60.

## Flight controllers (top 10)
| rank | part_model | key_specs | mass_g | price_usd | pros | cons | primary_source | confidence | rationale |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Holybro Kakute H7 Mini | H743 480MHz; ICM-42688-P; SPA06 baro; 6 UART; BEC 5V/2A; 20x20 | 5.5 | ~65 | ArduPilot+PX4 both official; 6 UART for MAVLink companion; baro | Pricey; overkill on Betaflight | holybro.com; docs.px4.io | confirmed | Only 20x20/5.5g board first-class on BOTH ArduPilot+PX4 — exactly what autonomous recovery needs |
| 2 | Matek H743-Mini v3 | H743; dual gyro (ICM42688P+ICM42605); DPS310; 5.5 UART; 20x20 | ~7 | ~60 | Most mature ArduPilot; dual-gyro redundancy | PX4 experimental; heavier | mateksys.com; ardupilot.org | confirmed | Near-equal to #1; dual gyro is a real robustness win |
| 3 | Matek H743-Slim v3 | H743; dual gyro; DPS310; 7 UART; 2-8S; 30.5x30.5 | 7 | ~65 | 7 UART (companion+GPS+ELRS+telem); robust ArduPilot | 30.5x30.5 footprint large for 2" | getfpv.com | confirmed | Most companion-friendly; footprint is the only knock |
| 4 | Matek F405-MiniTE | F405; ICM42605; OSD; 6 UART; 20x20/30x30 | 5 | ~35 | Lightest board that still runs ArduPilot; cheap | F4 limits; no baro | mateksys; getfpv.com | confirmed | Lightest ArduPilot-capable; accept F4 limits + ext baro |
| 5 | SpeedyBee F405 Mini | F405; ICM42688P; baro+OSD; 6 UART; BT; 20x20 | 9.6 | ~30 | Cheap, BT tuning, baro, INAV/ArduPilot | Heaviest 20x20 here | speedybee.com; getfpv.com | confirmed | Best value F4 w/ baro; 9.6g hurts |
| 6 | Flywoo GOKU GN405 Nano | F405; ICM42688P; baro; 6 UART; 16x16; TCXO ELRS option | ~4-5 | ~40 | Tiny, integrated ELRS option, light | 16x16 std; Betaflight/INAV only, no ArduPilot | flywoo.net | inferred | Great for Betaflight stabilize-only; not autonomy platform |
| 7 | BetaFPV Toothpick/Whoop F4 1-2S 12A AIO ELRS | F411; 12A 4-in-1 BLHeli_S; ELRS option; 3 UART; 1-2S | ~5 | ~40 | True AIO ~5g; ideal 2S/1103; minimal wiring | F411 Betaflight-only; 3 UART tight | wrekd.com; betafpv.com | confirmed | Mass-optimal single-board for Betaflight self-level; no autonomy |
| 8 | Happymodel X12 AIO 5-in-1 ELRS | F4; 12A 4-in-1; OpenVTX; ELRS onboard; 1-2S; 30x30 | 5.1 | ~40 | All-in-one incl VTX+ELRS at 5.1g; lowest wiring | F4 SPI Betaflight-only; few UART | happymodel.cn; getfpv.com | confirmed | Most integrated/lightest for pure-stabilize; no autonomy headroom |
| 9 | SpeedyBee F405 Mini stack FC | F405; ICM42688P; baro; 4-6 UART; 20x20 | ~6-9 | ~30 | Cheap pre-matched 20x20 stack; INAV/ArduPilot | Heavier; ArduPilot less common target | getfpv.com | inferred | Convenient stack; redundant with #5 |
| 10 | Matek F405-STD | F405; baro on some; 5-6 UART; ArduPilot MatekF405 | ~6 | ~30 | Proven ArduPilot F4 lineage | Older/heavier than MiniTE | ardupilot.org | inferred | MiniTE supersedes it |

Firmware capability: ArduPilot+PX4 → #1,#2,#3. ArduPilot(F4) → #4,#5,#10. Betaflight-only (stabilize, no autonomous recovery) → #6,#7,#8.

## ESC / AIO 4-in-1 (top 10) — 1103@11000KV on 2S draws modest current; DON'T over-spec amps, optimize mass
| rank | part_model | key_specs | mass_g | price_usd | pros | cons | primary_source | confidence | rationale |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Integrated 12A AIO (BetaFPV/X12) | 1-2S, 12A 4-in-1, BLHeli_S/Bluejay (in FC) | (in FC) | (in FC) | Right class; zero ESC wiring; lowest system mass | Fixed to its FC; BLHeli_S | betafpv.com; happymodel.cn | confirmed | ESC mass disappears into FC — system-mass winner |
| 2 | HGLRC Forward FD13A 4-in-1 | 2-4S, 13A/20A burst, BLHeli_S, 16x16 | 3.2 | ~20 | Tiny/light, matched current, cheap | 16x16; no BEC | getfpv.com | confirmed | Mass-optimal standalone if FC/ESC separated |
| 3 | HGLRC 28A 2-4S 4-in-1 20x20 | 2-4S, 28A/35A burst, BLHeli_S, 20x20 | 4.2 | ~22 | True 20x20 to match H7/F4 FCs; light | Mild over-spec | getfpv.com | confirmed | Best 20x20 standalone match for H7 stack |
| 4 | Holybro Tekko32 F4 Mini 45A AM32 | 2-6S, 45A, AM32, 20x20 | ~(stack) | ~35 | Native Kakute H7 stack partner; AM32 telem | Over-spec for 2S/1103; adds mass | holybro.com | confirmed | Convenient Holybro stack but 45A overkill |
| 5 | Holybro Tekko32 F4 Mini 50A AM32 | 2-6S, 50A, AM32, 20x20 | 15.6 | ~40 | AM32, bulletproof | 15.6g FAR too heavy; wrong spec | holybro.com | confirmed | DO NOT use here — mass+current both wrong |
| 6 | SpeedyBee BLS 35A Mini V2 20x20 | 3-6S, 35A/45A, BLHeli_S, current sensor | 7.2 | ~25 | Cheap, current sensor | 3-6S min (verify 2S); over-spec | speedybee.com | confirmed | Better for 3-4S 2.5"; verify 2S |
| 7 | Aikon AK32PIN 35A 6S 20x20 | 2-6S, 35A/45A, BLHeli_32, current sensor | 10 | ~30 | BLHeli_32 full telem; 2S-capable | 10g + over-spec | getfpv.com | confirmed | If you want BLHeli_32 telem on 20x20 |
| 8 | HGLRC 13A 2-3S 4-in-1 (BB2) | 2-3S, 13A/20A, BLHeli_S, 20x20 | 3 | ~18 | Lightest standalone; exact class; cheap | 2-3S only; no BEC/telem | rotorev.com | confirmed | Tied-lightest, perfectly matched to 2S/1103 |
| 9 | T-Motor F15A/F25A 2-4S 4-in-1 | 2-4S, 15-25A, BLHeli_S, 20x20 | ~4-6 | ~25-30 | Quality FETs, right class | Availability varies | T-Motor | inferred | Verify exact SKU specs |
| 10 | HGLRC Forward 45A BLHeli_32 2-6S 20x20 | 2-6S, 45A, BLHeli_32 | ~6-7 | ~30 | BLHeli_32, 2S-capable | Over-spec, heavier | getfpv.com | confirmed | Only if BLHeli_32 wanted |

## ELRS receivers (top 7)
| rank | part_model | key_specs | mass_g | price_usd | pros | cons | primary_source | confidence | rationale |
|---|---|---|---|---|---|---|---|---|---|
| 1 | BetaFPV ELRS Lite RX | SX1280, ESP8285, flat ceramic ant, no PA/LNA | 0.46 | ~12 | Lightest viable; flat ant easy to mount; ~1km@50mW | No PA/LNA; single ant | betafpv.com | confirmed | Effectively free mass; LOS range rarely the limit |
| 2 | Happymodel EP2 | SX1280, ESP8285, TCXO, SMD ceramic ant, 500Hz | 0.44 | ~10 | Lightest; TCXO thermal stability | Ceramic ant directional; no diversity | happymodel.cn; getfpv.com | confirmed | TCXO is a genuine link-lock plus |
| 3 | Happymodel EP1 | SX1280, TCXO, omni dipole T antenna, 500Hz | 0.42 (no ant) | ~10 | Omni dipole best pattern for agile micro | External antenna to route | happymodel.cn | confirmed | Best omni pattern for tumbling/maneuvering craft |
| 4 | BetaFPV ELRS Nano | SX1280 + PA/LNA (100mW telem), dipole T ant | ~1.8 (w/ant) | ~17 | Best range+telem of single-ant set | ~1.8g | betafpv.com; getfpv.com | confirmed | Step up for companion-link telemetry margin |
| 5 | RadioMaster RP1 V2 | SX1280, UFL ant socket, WiFi config | 2.2 (w/ant) | ~13 | Swappable UFL antenna; WiFi | UFL adds mass | radiomasterrc.com | confirmed | Antenna flexibility |
| 6 | RadioMaster RP2 V2 | SX1280, built-in ceramic ant, WiFi | 0.55 | ~13 | Sub-gram, integrated, WiFi config | Ceramic lower gain | pyrodrone.com | confirmed | RadioMaster-ecosystem alt to Lite/EP2 |
| 7 | RadioMaster RP3 V2 (diversity) | SX1280 + PA/LNA 100mW, antenna diversity 2x T, 500/1000Hz | 4.6 (w/ant) | ~20 | Antenna diversity = fewer dropouts when frame shadows ant | 4.6g heavy; 2 antennas | radiomasterrc.com | confirmed | Reliability play for guarded frame; mass is the price |

## Open questions
- SpeedyBee BLS 35A / Aikon AK32 2S operation: verify low-voltage 2S behavior/startup.
- T-Motor F-series 4-in-1: exact current/mass per SKU unconfirmed.
- Flywoo GN405 is 16x16 not 20x20; no official ArduPilot/PX4.
- PX4 on Matek H743-Mini is experimental; Kakute H7 Mini safer if PX4 mandatory.
- Confirm companion-board current draw vs FC 5V/2A BEC; hungry SBC may need own regulator.
- Real 2S/1103@11000KV peak current unmeasured — "12-20A class plenty" is inference; bench-measure before final ESC sizing.
- All prices inferred from street pricing.
