#!/usr/bin/env python3
"""Generate the top-level three-tier parts PDF for the guarded micro-UAV.

Produces ``Drone_Parts_Three_Tiers.pdf`` at the repository root, summarizing the
cheapest (Value), most-expensive (Capability ceiling), and most-efficient
(Mission-optimal) parts lists, plus the mechanical/geometry data needed to begin
CAD and FEA. Run from anywhere:

    python3 "Research/Component Study/unrestricted-tier-study-2026/generate_parts_pdf.py"

Source of truth: Design Report/BOM.csv and the unrestricted-tier-study DECISION.md.
Prices/masses are catalog snapshots or engineering allowances (2026-06-22) and
remain planning evidence until delivered parts are weighed and bench-tested.
"""
from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
OUT = REPO_ROOT / "Drone_Parts_Three_Tiers.pdf"

NAVY = colors.HexColor("#1f2d44")
ACCENT = colors.HexColor("#2b6cb0")
LIGHT = colors.HexColor("#eef2f7")
RISK = colors.HexColor("#fde2e1")

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=styles["Heading1"], textColor=NAVY, spaceAfter=6)
H2 = ParagraphStyle("H2", parent=styles["Heading2"], textColor=ACCENT, spaceBefore=10, spaceAfter=4)
BODY = ParagraphStyle("BODY", parent=styles["BodyText"], fontSize=9, leading=12)
SMALL = ParagraphStyle("SMALL", parent=styles["BodyText"], fontSize=7.5, leading=9.5)
CELL = ParagraphStyle("CELL", parent=styles["BodyText"], fontSize=7.5, leading=9)
CELLB = ParagraphStyle("CELLB", parent=CELL, fontName="Helvetica-Bold")
TITLE = ParagraphStyle("TITLE", parent=styles["Title"], textColor=NAVY, alignment=TA_CENTER)
SUB = ParagraphStyle("SUB", parent=styles["BodyText"], alignment=TA_CENTER, textColor=colors.grey, fontSize=10)


def p(text, style=CELL):
    return Paragraph(text, style)


def header_style(extra=None):
    base = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c5ced8")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]
    if extra:
        base += extra
    return TableStyle(base)


story = []

# ---- Title page ------------------------------------------------------------
story += [
    Spacer(1, 1.2 * inch),
    Paragraph("Guarded Micro-UAV", TITLE),
    Paragraph("Three-Tier Parts Reference for CAD &amp; FEA", TITLE),
    Spacer(1, 0.2 * inch),
    Paragraph("Cheapest (Value) &bull; Most Expensive (Capability Ceiling) &bull; Most Efficient (Mission-Optimal)", SUB),
    Spacer(1, 0.5 * inch),
    Paragraph(
        "Snapshot 2026-06-22. Prices and masses are catalog values or engineering allowances and "
        "remain <b>planning evidence</b> until delivered parts are weighed and bench-tested. "
        "Do not freeze maximum mass, guard geometry, or load cases from this sheet alone &mdash; "
        "the values marked BENCH_REQUIRED must be measured.",
        ParagraphStyle("disc", parent=BODY, alignment=TA_CENTER, textColor=colors.grey),
    ),
    Spacer(1, 0.3 * inch),
    Paragraph(
        "Generated from <font face='Courier'>Design Report/BOM.csv</font> and "
        "<font face='Courier'>unrestricted-tier-study-2026/DECISION.md</font>.",
        ParagraphStyle("src", parent=SMALL, alignment=TA_CENTER),
    ),
    PageBreak(),
]

# ---- Side-by-side tier comparison -----------------------------------------
story.append(Paragraph("1. Tier Comparison by Subsystem", H1))
story.append(Paragraph(
    "Pick one column to model. The Value column is the current locked Stage 1 build (and FEA baseline). "
    "The Mission-optimal column is the recommended target <i>after</i> the propulsion thrust gate passes. "
    "The Capability-ceiling column is a reference only &mdash; it is not hand-throwable and breaks the indoor release experiment.",
    BODY))
story.append(Spacer(1, 6))

comp_header = ["Subsystem", "Cheapest (Value)", "Most Expensive (Ceiling)", "Most Efficient (Optimal)"]
comp_rows = [
    ["Frame &amp; guards", "Custom 2\" nylon frame", "Custom 23\" guarded industrial quad", "GEPRC GEP-CL35 V2 (142 mm, 3.5\")"],
    ["Flight controller", "Kakute H7 Mini v1.5", "Pixhawk 6X Pro + PM02D", "Pixhawk 6C Mini + PM02 V3"],
    ["ESC / distribution", "HGLRC XJB BS13A 2-3S", "4x A6-M FOC/CAN arms", "Tekko32 F4 Mini 50A AM32"],
    ["Motors", "4x Happymodel EX1103 11000KV", "4x T-Motor A6-M KV280", "4x GEPRC SPEEDX2 2105.5 2650KV"],
    ["Propellers", "Gemfan Hurricane 2023-3", "MF2311P-M 23\"", "Gemfan D90-3 ducted"],
    ["Battery", "GNB 2S 550 mAh 100C", "Large 6S (sized post-test)", "6S 1050-1300 mAh high-rate"],
    ["Companion compute", "Arduino Nicla Vision (MCU)", "Jetson AGX Orin Industrial 64 GB", "Raspberry Pi Zero 2 W"],
    ["Vision / camera", "Nicla onboard GC2145", "Luxonis OAK 4 D Pro W", "Luxonis OAK-D Lite"],
    ["Flow / range", "Matek 3901-L0X (MSP)", "ARK Flow + LightWare SF45/B", "ARK Flow (DroneCAN)"],
    ["Manual control RX", "BetaFPV ELRS Lite", "CubePilot Herelink 1.1", "RadioMaster RP3 V2 diversity"],
    ["Telemetry / logs", "CRSF + onboard log", "Herelink + Microhard P900", "SiK V3 100 mW pair + microSD"],
    ["Perception power", "FC rail (if measured safe)", "Custom isolated DC/DC", "Separate 5 V regulator"],
    ["Flying-HW cost", "~$333", ">$6,200 (>$9,000 complete)", "~$1,030"],
    ["Vehicle scale", "~129.8 g nominal", "Multi-kilogram", "~0.55-0.70 kg (bench-frozen)"],
    ["Build decision", "First build &amp; control case", "Reference only - do not build", "Recommended after thrust gate"],
]
data = [[p(c, CELLB) for c in comp_header]]
for r in comp_rows:
    data.append([p(r[0], CELLB), p(r[1]), p(r[2]), p(r[3])])
t = Table(data, colWidths=[1.15 * inch, 1.7 * inch, 1.95 * inch, 1.9 * inch], repeatRows=1)
style_extra = [
    ("BACKGROUND", (0, 13), (-1, 14), colors.HexColor("#dfe8f3")),
    ("BACKGROUND", (0, 15), (-1, 15), colors.HexColor("#e6f0e6")),
    ("FONTNAME", (0, 13), (-1, 15), "Helvetica-Bold"),
]
t.setStyle(header_style(style_extra))
story.append(t)
story.append(PageBreak())


# ---- Detailed Value (cheapest) BOM ----------------------------------------
def bom_table(header, rows, colw, risk_rows=()):
    data = [[p(h, CELLB) for h in header]]
    for r in rows:
        data.append([p(str(c)) for c in r])
    tbl = Table(data, colWidths=colw, repeatRows=1)
    extra = [("BACKGROUND", (0, i + 1), (-1, i + 1), RISK) for i in risk_rows]
    tbl.setStyle(header_style(extra))
    return tbl


story.append(Paragraph("2. Cheapest &mdash; Value Build (locked Stage 1, FEA baseline)", H1))
story.append(Paragraph(
    "~$333 flying hardware, ~129.8 g nominal. Rows shaded red are EOL/legacy and must be re-confirmed or "
    "substituted before ordering (see Open Questions OQ-007, OQ-008).", BODY))
story.append(Spacer(1, 6))
value_header = ["Subsystem", "Part", "Qty", "Mass nom (g)", "Cost nom ($)", "Notes"]
value_rows = [
    ["Flight control", "Holybro Kakute H7 Mini v1.5", "1", "5.5", "65", "v1.5 effectively unavailable since ~mid-2025"],
    ["ESC", "HGLRC XJB BS13A 2-3S 4-in-1", "1", "3.0", "18", "20x20; legacy, mostly sold in flytower"],
    ["Motors", "Happymodel EX1103 11000KV", "4", "15.2 ea", "36", "121.9 gf @ 9.2 A vendor pt; bench @ 7.0 V"],
    ["Propellers", "Gemfan Hurricane 2023-3", "1 set", "3.5", "6", "1.5 mm T-mount, 4x 0.88 g"],
    ["Battery", "GNB 2S 550 mAh 100C LiHV XT30", "1", "29.0", "14", "7.6 V LiHV; sag BENCH_REQUIRED"],
    ["Control link", "BetaFPV ELRS Lite RX", "1", "0.46", "12", "5 V ELRS/CRSF on SERIAL6"],
    ["Status", "VIFLY Finder Mini + WS2812", "1 set", "3.3", "18", "self-powered buzzer + LED"],
    ["Vision", "Arduino Nicla Vision ABX00051", "1", "19.8", "90", "MCU+cam+IMU+ToF; rolling shutter"],
    ["Positioning", "Matek 3901-L0X flow + lidar", "1", "2.0", "26", "EOL; flow+range over 1 MSP UART"],
    ["Electrical", "XT30 + 22/26 AWG + JST-SH", "1 set", "5.5", "8", "weigh completed harness"],
    ["Mechanical", "Printed nylon frame + guards + M2", "1 set", "42.5", "40", "CAD/FEA/push test required"],
]
story.append(bom_table(value_header, value_rows,
                       [0.8 * inch, 1.8 * inch, 0.4 * inch, 0.75 * inch, 0.7 * inch, 2.05 * inch],
                       risk_rows=(0, 1, 8)))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "Support (non-flying): ToolkitRC M6AC charger ~$60, PVC+net cage ~$40, tethered release rig ~$20, "
    "DIY 1-2 kg thrust stand ~$100. All-in project ~$350-650.", SMALL))
story.append(PageBreak())

# ---- Mission-optimal (most efficient) -------------------------------------
story.append(Paragraph("3. Most Efficient &mdash; Mission-Optimal Build (~$1,030, ~0.55-0.70 kg)", H1))
story.append(Paragraph(
    "Recommended target after the guarded propulsion thrust gate passes. Buy the propulsion-validation subset "
    "first (one motor, prop set, 50 A ESC, 6S pack, one guard) and require &ge;350 gf/motor at minimum loaded "
    "voltage before committing the avionics.", BODY))
story.append(Spacer(1, 6))
opt_header = ["Subsystem", "Part", "Cost ($)", "Notes"]
opt_rows = [
    ["Frame &amp; guards", "GEPRC GEP-CL35 V2 3.5\"", "69.99", "142 mm, 95 mm guard ID, 133.7 g frame"],
    ["Flight controller", "Pixhawk 6C Mini + PM02 V3", "149.98", "dual isolated/heated IMU, H743"],
    ["ESC", "Holybro Tekko32 F4 Mini 50A AM32", "~69.99", "20 mm, 6S, inferred standalone price"],
    ["Motors", "4x GEPRC SPEEDX2 2105.5 2650KV", "~88", "21 g ea, 12x12 M2 mount, 2-6S"],
    ["Propellers", "Gemfan D90-3 ducted tri-blade", "incl.", "90 mm, 2.3 g, for 3.5\" ducts"],
    ["Battery", "6S 1050-1300 mAh high-rate LiPo", "~45", "final capacity bench-selected"],
    ["Companion", "Raspberry Pi Zero 2 W", "15", "MAVLink/DepthAI host"],
    ["Vision", "Luxonis OAK-D Lite", "169", "global-shutter stereo + on-device NN"],
    ["Flow / range", "ARK Flow (DroneCAN)", "250", "5 g, PAW3902 + ToF + IMU on CAN"],
    ["Control link", "RadioMaster RP3 V2 diversity", "19.99", "TCXO, dual-antenna ELRS"],
    ["Telemetry", "Holybro SiK V3 100 mW pair", "58.99", "independent MAVLink + onboard log"],
    ["Perception power", "Separate 5 V regulator", "20.99", "isolates OAK/Pi transients from FC"],
    ["Mounts / wiring / status", "allowance", "~68", "adapter plate, isolated avionics deck"],
]
story.append(bom_table(opt_header, opt_rows,
                       [1.3 * inch, 2.2 * inch, 0.7 * inch, 2.3 * inch]))
story.append(Spacer(1, 4))
story.append(Paragraph(
    "The GEP frame does not natively accept the Pixhawk 6C Mini footprint &mdash; a stiff adapter plate and "
    "isolated avionics deck are an FEA item. Excludes the optional $1,075 Tyto thrust stand (support gear).", SMALL))
story.append(PageBreak())

# ---- Capability ceiling (most expensive) ----------------------------------
story.append(Paragraph("4. Most Expensive &mdash; Capability Ceiling (reference only)", H1))
story.append(Paragraph(
    "Highest rational COTS capability, independent of cost: &gt;$6,200 airborne subtotal, likely &gt;$9,000 complete. "
    "<b>Do not build for the release mission</b> &mdash; multi-kilogram scale makes hand release unsafe and changes "
    "the project into an industrial UAV program. Listed so the design space is bounded.", BODY))
story.append(Spacer(1, 6))
ceil_header = ["Subsystem", "Part", "Cost ($)"]
ceil_rows = [
    ["Flight controller", "Pixhawk 6X Pro Standard v2B + PM02D", "797.99"],
    ["Companion", "NVIDIA Jetson AGX Orin Industrial 64 GB", "2,899"],
    ["Vision", "Luxonis OAK 4 D Pro W", "1,049"],
    ["Propulsion", "4x T-Motor A6-M 6S FOC modules + 23\" props", "~400+/arm"],
    ["Flow / range", "ARK Flow + LightWare SF45/B scanning lidar", "—"],
    ["Control / telemetry", "CubePilot Herelink 1.1 + Microhard P900 pair", "449 (P900 pair)"],
    ["Test gear", "Tyto Robotics Series 1585 thrust-stand bundle", "1,075"],
    ["Frame", "Custom carbon/composite guarded industrial quad", "custom"],
]
story.append(bom_table(ceil_header, ceil_rows, [1.6 * inch, 3.4 * inch, 1.5 * inch]))
story.append(PageBreak())

# ---- FEA / CAD data --------------------------------------------------------
story.append(Paragraph("5. Mechanical &amp; Geometry Data for CAD / FEA", H1))
story.append(Paragraph(
    "Use these for the structural model and load cases. Guard deflection and stress are the governing FEA "
    "outputs; all are BENCH_REQUIRED to confirm.", BODY))

story.append(Paragraph("Masses (point/distributed loads)", H2))
mass_rows = [
    ["Value frame + guards + M2 (allowance)", "best 35.0 / nom 42.5 / worst 50.0 g"],
    ["Value flying mass (Sigma)", "best 117.96 / nom 129.76 / worst 149.5 g"],
    ["Value unmodeled-HW allowance", "5.0 g"],
    ["Value proposed frozen max (NOT frozen)", "155.0 g; abort threshold 225 g"],
    ["EX1103 motor (Value)", "15.2 g each (x4 as corner point loads)"],
    ["GEP-CL35 V2 frame (Optimal)", "133.7 g bare frame"],
    ["SPEEDX2 2105.5 motor (Optimal)", "21 g each"],
    ["D90-3 prop (Optimal)", "2.3 g each"],
    ["Optimal vehicle target", "~0.55-0.70 kg, bench-frozen"],
]
story.append(bom_table(["Item", "Mass"], mass_rows, [3.4 * inch, 3.1 * inch]))

story.append(Paragraph("Mounting geometry", H2))
geo_rows = [
    ["Value FC/ESC stack", "20 x 20 mm pattern"],
    ["Optimal frame", "142 mm motor-to-motor, 95 mm guard inside diameter, 3.5\" props"],
    ["Optimal FC holes", "25.5 x 25.5 mm"],
    ["Optimal motor holes", "12 x 12 mm (M2), matches SPEEDX2 2105.5"],
    ["Optimal battery mount", "integrated XT60, 6S current"],
    ["6C Mini adapter", "frame does NOT natively fit 6C Mini; stiff adapter plate + isolated avionics deck required"],
]
story.append(bom_table(["Feature", "Spec"], geo_rows, [2.0 * inch, 4.5 * inch]))

story.append(Paragraph("Load cases &amp; acceptance gates (structural)", H2))
load_rows = [
    ["Guard lateral deflection", "&le; 1.0 mm at the defined proof load"],
    ["Guard permanent set", "none after release-envelope drop test"],
    ["Prop-to-guard clearance", "no contact under load (verify duct interaction)"],
    ["Thrust-to-weight (Value)", "&ge; 112.5 gf/motor @ 7.0 V for full 225 g reserve"],
    ["Thrust-to-weight (Optimal)", "T/W &ge; 2.0 at min loaded voltage; &ge; 350 gf/motor @ 700 g screen"],
    ["Thrust rise (10-90%)", "&le; 100 ms"],
    ["Battery sag at acceptance step", "&le; 10%"],
]
story.append(bom_table(["Load case / gate", "Acceptance criterion"], load_rows, [2.4 * inch, 4.1 * inch]))
story.append(Spacer(1, 8))
story.append(Paragraph(
    "Modeling note: guards alter propeller thrust and transient response; model the guard-to-frame joint as the "
    "critical region. Freeze the maximum flying mass only after the complete CAD mass model exists and receipt "
    "masses are measured (Open Question OQ-002).", SMALL))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.grey)
    canvas.drawString(0.75 * inch, 0.5 * inch,
                      "Guarded Micro-UAV - Three-Tier Parts Reference - snapshot 2026-06-22 - planning evidence, not bench-verified")
    canvas.drawRightString(letter[0] - 0.75 * inch, 0.5 * inch, "Page %d" % doc.page)
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(OUT), pagesize=letter,
    leftMargin=0.75 * inch, rightMargin=0.75 * inch,
    topMargin=0.7 * inch, bottomMargin=0.7 * inch,
    title="Guarded Micro-UAV - Three-Tier Parts Reference",
    author="SelfStabilizingDrone",
)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("wrote", OUT)
