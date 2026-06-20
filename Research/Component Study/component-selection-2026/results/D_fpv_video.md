# Stream D — FPV / Video (analog, digital, video antennas)

Headline verdict: **default to analog** for a sub-200 g 2S guarded micro. Analog nano stack ≈ 2.6 g / ~1.3 W. Digital is mass-viable only via **HDZero Whoop Lite** (~6 g, native 2S 2.8–13 V) but draws **~7 W** — a real flight-time/thermal hit on a small 2S pack. DJI O4 and Walksnail Nano V3 not viable (power/mass); Walksnail Mini 1S Lite is mass-OK but 5 V-input only (needs BEC).

## Analog FPV (top 7)
| rank | part_model | key_specs | mass_g | price_usd | pros | cons | primary_source | confidence | rationale |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Caddx Ant Lite + Foxeer Reaper Nano V2 | 1200TVL cam (3.7–18V) + 5.8G VTX 25–350mW (5V, 340mA@350mW) | ~2.6 | ~$35 | Lightest credible cam+VTX; 350mW real LOS range | VTX 5V-only → needs 5V BEC | pyrodrone.com (Caddx Ant Lite; Reaper Nano V2) | confirmed | Min mass; VTX needs 5V rail |
| 2 | BetaFPV C04 + M04 module | 1200TVL 160°, VTX 25–400mW, 5V | 4.14 (w/ ant) | ~$25 | One-piece, solder-free, 400mW | 5V supply; heavier than discrete | betafpv.com; Amazon | confirmed | Lowest-risk integration |
| 3 | RunCam Nano 3 + Reaper Nano V2 | 800TVL 2.3mm 140° + 5V VTX | ~1.9 | ~$40 | Lightest camera (1.1g), good low light | 800TVL; cam Vin unconfirmed | oscarliang.com; pyrodrone.com | confirmed/inferred | Lightest cam; verify cam Vin |
| 4 | Happymodel OVX306 OpenVTX + Caddx Ant Lite | OpenVTX 400mW + 1200TVL cam | ~3.0 | ~$33 | Open firmware, BF VTX tables, cheap | VTX mass inferred; 5V-class | pyrodrone.com | inferred | Verify VTX mass |
| 5 | Foxeer Razer Nano + Reaper Nano V2 | 1200TVL cam (4.5–25V, native 2S) + VTX | ~4.7 | ~$42 | Cam runs direct off 2S (no cam BEC) | Heavy cam (3.9g) | getfpv.com | confirmed | Only native-2S cam; costs grams |
| 6 | BetaFPV C03 + A03 400mW VTX | 1200TVL 160° cam (3–5.5V) + VTX | ~3+ | ~$35 | Solderless JST-0.8; documented | Cam ceiling 5.5V; combo mass inferred | betafpv.com | confirmed/inferred | Watch 5.5V cam ceiling |
| 7 | RunCam Nano 4 + nano VTX | 800TVL 2.1mm 155° | 2.9 (cam)+VTX | ~$45 | Wide 155° FOV, waterproof variant | Heavier than Nano 3, no res gain | shop.runcam.com | confirmed | Only for wider FOV |

## Digital FPV (top 5)
| rank | part_model | key_specs | mass_g | price_usd | pros | cons | primary_source | confidence | rationale |
|---|---|---|---|---|---|---|---|---|---|
| 1 | HDZero Whoop Lite VTX + Nano Lite cam | 2.8–13V (native 2S), ~200mW, ~7W draw, ~14ms frame | ~6 | ~$120 | Lightest production digital; native 2S; low latency | ~7W draw heavy on 2S; 200mW range | docs.hd-zero.com; getfpv.com | confirmed | Only digital fitting mass+2S |
| 2 | Walksnail Avatar HD Mini 1S Lite Kit | cam 1.8g+VTX 5.1g, 3.1–5V, ~4W, 22ms | 8.7 (kit) | ~$130 | Light, 350mW, good image | 5V-only (needs BEC); ~4W | oscarliang.com | confirmed | Mass-OK but not direct-2S |
| 3 | Walksnail Avatar HD Nano Kit V3 | 3.1–13V (native 2S), 500mW, 19–40ms | ~21 (kit) | ~$140 | Native 2S, 500mW | 21g over budget; heavy metal VTX | caddxfpv.com | confirmed | Too heavy |
| 4 | DJI O4 Air Unit (Lite) | 3.7–13.2V (native 2S), 1/2" CMOS, 20–35ms | 8.2–9.2 (unit) | ~$160 | Best image; light body; native 2S | Multi-W draw; DJI-goggle lock-in | dji.com; oscarliang.com | confirmed | Power + lock-in blockers |
| 5 | DJI O4 Air Unit Pro | 4K120 record, native 2S | >10 (unit) | ~$200 | Top image, onboard record | Heaviest/most power-hungry | getfpv.com | confirmed | Not feasible here |

## Video antennas (top 5)
| rank | part_model | key_specs | mass_g | price_usd | pros | cons | primary_source | confidence | rationale |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Lumenier Micro Dipole 5.8G (U.FL) | ~2.5dBic, U.FL, analog+HDZero | 1.0 | ~$6 | Lightest mast; U.FL matches nano VTX | Dipole (less gain than lollipop) | getfpv.com | confirmed | Best mass/perf analog/HDZero |
| 2 | HDZero Whoop Lite stock dipole | 5.8G dipole bundled | ~0.4 | incl | Tuned to VTX; near-zero mass | Fragile; HDZero band only | getfpv.com | confirmed | Lightest if HDZero |
| 3 | Foxeer Micro Lollipop 5.8G (U.FL) | 2.5dBi RHCP, U.FL | ~1.5 (U.FL); 3.1 (MMCX) | ~$8/pr | CP rejects multipath; durable | Heavier; pick U.FL not MMCX | pyrodrone.com | confirmed/inferred | CP for cleaner video |
| 4 | Walksnail stock antenna (IPEX-1) | proprietary-tuned | 0.5 | incl | Matched to VTX; ultralight | Walksnail-only | oscarliang.com | confirmed | Use bundled for Walksnail |
| 5 | Lumenier Micro Dipole (MMCX) | same as #1, MMCX | ~1 | ~$7 | For MMCX-socket VTX | Most nano VTX are U.FL | getfpv.com | confirmed/inferred | Only if VTX is MMCX |

## Open questions
- Confirm FC/AIO provides a clean 5V rail (~0.5–1A) before assuming "2S compatible" for 5V-input VTXs.
- HDZero Nano 90 cam mass/Vin unconfirmed (1.5g is the older Nano Lite).
- Happymodel OVX306 / BetaFPV A03 exact masses inferred.
- DJI O4 wattage not published (power verdict is inferred from class).
- RunCam Nano 3/4 Vin vs 5V rail unconfirmed.
- TX/RX polarization must match (Walksnail often LHCP).
- VTX power 350–500mW+ may exceed unlicensed limits depending on jurisdiction (separate from FAA 250g).
