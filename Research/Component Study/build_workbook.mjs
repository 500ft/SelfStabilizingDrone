import fs from "node:fs/promises";
import { Workbook, SpreadsheetFile } from "@oai/artifact-tool";

const out = "Research/Component Study/Drone_Component_and_Propulsion_Study.xlsx";
const previewDir = "/private/tmp/drone-component-study-previews";
const wb = Workbook.create();

const navy = "#17324D", blue = "#2E75B6", pale = "#D9EAF7", green = "#D9EAD3";
const amber = "#FFF2CC", red = "#F4CCCC", gray = "#E7E6E6", white = "#FFFFFF";

function title(sheet, range, text, subtitle) {
  sheet.mergeCells(range);
  const r = sheet.getRange(range);
  r.values = [[text]];
  r.format.fill = navy;
  r.format.font = { bold: true, color: white, size: 18 };
  r.format.rowHeight = 32;
  if (subtitle) {
    const row = Number(range.match(/\d+/)[0]) + 1;
    sheet.mergeCells(`A${row}:H${row}`);
    sheet.getRange(`A${row}:H${row}`).values = [[subtitle]];
    sheet.getRange(`A${row}:H${row}`).format.font = { italic: true, color: "#555555" };
  }
  sheet.showGridLines = false;
}

function styleHeader(range) {
  range.format.fill = blue;
  range.format.font = { bold: true, color: white };
  range.format.wrapText = true;
  range.format.rowHeight = 34;
  range.format.borders = { preset: "all", style: "thin", color: "#B7C9D6" };
}

function styleBody(range) {
  range.format.wrapText = true;
  range.format.borders = { preset: "all", style: "thin", color: "#D9E2F3" };
  range.format.verticalAlignment = "top";
}

const components = [
  ["Flight Controller","Holybro Kakute H7 Mini","FC","5.5","31 x 30 x 6","2-6S","STM32H743 480 MHz; ICM-42688-P; SPA06; 6 UART; 128 Mbit flash","ArduPilot supported; strong logging/autonomy baseline","$58.99","Datasheet","Recommended baseline","https://holybro.com/products/kakute-h7-mini"],
  ["Flight Controller","Matek H743-MINI","FC","7.0","36 x 28 x 6.5","2-8S","STM32H743; dual IMU; DPS310; microSD; CAN; 5.5 UART","ArduPilot target; strongest redundancy, slightly heavier","Verify","Datasheet","Strong alternative","https://www.mateksys.com/?portfolio=h743-mini"],
  ["Flight Controller/AIO","BETAFPV F4 2-3S 20A AIO V1","FC + 4-in-1 ESC","5.58-5.92","26 x 26","2-3S","STM32F405; ICM42688P/42605; barometer; 16 MB; 20A continuous","Very low system mass; firmware/autonomy compatibility must be verified","$54.99","Datasheet","Mass-leading candidate","https://betafpv.com/products/f4-2-3s-20a-aio-fc-v1"],
  ["Flight Controller/AIO","BETAFPV F405 2-4S AIO V3","FC + 4-in-1 ESC","Verify","26 x 26","2-4S","F405 AIO; 12A/20A variants","Attractive packaging; exact variant and firmware support need verification","Verify","Partial datasheet","Research candidate","https://betafpv.com/products/f405-20a-aio-2-4s-brushless-flight-controllerblheli_s-v3"],
  ["Flight Controller/AIO","Happymodel X12 Lite","FC + 4-in-1 ESC + ELRS","Verify","Whoop AIO","2S","F411; ICM42688P; 12A ESC; ELRS","High integration; F411 resources and autonomy support are limiting","Verify","Reference platform","Prototype-only candidate","https://www.happymodel.cn/index.php/2023/03/21/bassline-digital-hd-2s-toothpick-fpv-drone-built-in-walksnail-or-hdzero-vtx/"],
  ["Flight Platform","Crazyflie 2.1 Brushless","Integrated platform","32-37","Platform","1S","STM32F405; BMI088; BMP388; 5A ESCs; radio","Excellent research ecosystem; limited payload/thrust for custom guarded frame","Verify","Datasheet","Benchmark / research option","https://www.bitcraze.io/products/crazyflie-2-1-brushless/"],
  ["Flight Controller","SpeedyBee F405 Wing Mini","Fixed-wing FC","5.5","Compact","2-6S","F405; fixed-wing I/O","Low mass but wrong control/output architecture for this quad","Verify","Datasheet","Not recommended","https://www.speedybee.com/speedybee-f405-wing-mini-fixed-wing-flight-controller/"],
  ["Motor","Happymodel EX1103 11000KV","Motor","3.8 each","11 x 3 stator","1-2S","Official 2S/2023R curve: 121.9 g at 9.2 A max","Best documented 2S candidate; curve supports auditable model","Verify","Bench curve","Recommended baseline","https://www.happymodel.cn/index.php/2022/09/05/bassline-spare-part-ex1103-kv11000-brushless-motor/"],
  ["Motor","BETAFPV 1103 11000KV","Motor","3.3 each","1103","2S","Recommended 40 mm 4-blade or 3020 2-blade","Very light; thrust curve must be bench-tested","$39.99/set","Datasheet","Strong lightweight candidate","https://betafpv.com/products/1103-brushless-motors"],
  ["Motor","BETAFPV 1103 8000KV","Motor","3.8 each","1103","3S","Lower KV 3S variant","Higher voltage alternative; guard/prop and risk implications","$39.99/set","Datasheet","Alternative architecture","https://betafpv.com/products/1103-brushless-motors"],
  ["Motor","BETAFPV 1103 15000KV","Motor","3.7 each","1103","1S","High-KV 1S variant","Simpler battery but likely lower recovery authority at project mass","$39.99/set","Datasheet","Benchmark only","https://betafpv.com/products/1103-brushless-motors"],
  ["Motor","Flywoo ROBO 1202.5 11500KV","Motor","3.8 each","12 x 2.5 stator","1-2S","1.5 mm shaft","Compact alternative; requires measured curve","$12.99 each","Datasheet","Research candidate","https://flywoo.net/products/flywoo-robo-1202.5-11500kv-fpv-motor-gold-purple-new-version-"],
  ["Motor","Crazyflie 08028 10000KV","Motor","2.3 each","08028","1S","Up to 30 g thrust with 55 mm prop","Mass-leading but insufficient for a 140-180 g custom vehicle","Verify","Datasheet","Benchmark only","https://store.bitcraze.io/products/crazyflie-2-1-brushless-08028-10000kv-brushless-motor"],
  ["Motor","BETAFPV Aquila20 1103 10500KV","Motor","3.5 each","1103","2S","Paired with 2218 props and 1100 mAh pack","Useful endurance benchmark; thrust curve unavailable","Verify","Datasheet/reference platform","Endurance candidate","https://betafpv.com/collections/1102-1104-motors/products/1103-brushless-motors-aquila20"],
  ["Motor","BETAFPV LAVA 1104 7200KV","Motor","5.3 each","1104","3S","Max 10.2 A; >230 g claimed thrust with 2218 prop","High authority, but raises speed/current/mass risk","Verify","Datasheet","High-power alternative","https://betafpv.com/collections/1102-1104-motors/products/lava-series-1104-brushless-motors"],
  ["Motor","Happymodel EX1103 6000/7000/8000/12000KV","Motor","Verify","1103","2-4S","Broad voltage/KV family","Useful for later voltage trade; curve must match exact variant","Verify","Datasheet","Research family","https://www.happymodel.cn/index.php/2019/06/04/happymodel-ex1103-kv6000-8000-12000-2-4s-brushless-motor/"],
  ["Motor","Happymodel EX1103S 7000KV","Motor","3.8 each","1103","3S class","Larva-X upgrade motor","Potential 3S candidate; bench data required","Verify","Datasheet","Research candidate","https://www.happymodel.cn/index.php/2019/10/24/happymodel-ex1103s-kv7000-motors-upgrade-for-larva-x/"],
  ["Propeller","Gemfan 2015-2","2-blade prop","0.5 each","2.0 in x 1.5 pitch","Motor dependent","PC; 1/1.5 mm shaft","Low mass/drag; used by Meteor85 2S reference","Verify","Datasheet","Recommended low-load prop","https://www.gemfanhobby.com/2015-pc-2-blade.html"],
  ["Propeller","Gemfan 2023S-3","3-blade prop","0.7 each","50.8 mm x 2.0 pitch","Motor dependent","PC; 1.5 mm shaft","Balanced 2-inch tri-blade option","Verify","Datasheet","Strong candidate","https://www.gemfanhobby.com/2023s-hurricane-pc-3-blade.html"],
  ["Propeller","Gemfan 2023-3","3-blade prop","0.88 each","52.17 mm x 2.3 pitch","Motor dependent","1.5 mm T-mount","Used with EX1103 reference curve/platform","Verify","Datasheet","Recommended baseline","https://www.gemfanhobby.com/2023-hurricane-pc-3-blade.html"],
  ["Propeller","Gemfan 2218-3","3-blade prop","0.58 each","55.9 mm x 1.8 pitch","Motor dependent","1.5 mm shaft; 2.32 g/set","Used on Aquila/Pavo; more disk area","Verify","Datasheet","Endurance/duct candidate","https://betafpv.com/products/gemfan-2218-3-blade-propellers-1-5mm-shaft"],
  ["Propeller","Gemfan 2036-4","4-blade prop","0.84 each","52 mm x 3.6 pitch","Motor dependent","3-hole mount","High load/authority; current and efficiency penalty","Verify","Datasheet","High-load candidate","https://www.gemfanhobby.com/2036-hulkie-pc-4-blade-3-holes"],
  ["Propeller","Gemfan D2.5-3 ducted","3-blade duct prop","1.2 each","63.5 mm x 2.4 pitch","Motor dependent","Recommended 1404 motor","Outside current 1103 baseline; useful larger protected concept","Verify","Datasheet","Deferred larger concept","https://www.gemfanhobby.com/d25-ducted-pc-3-blade.html"],
  ["Propeller","Crazyflie optimized 55 mm","2-blade prop","Verify","55 mm / 35 mm pitch","1S platform","Optimized for Crazyflie brushless platform","Low-thrust benchmark only","Verify","Reference platform","Benchmark only","https://www.bitcraze.io/products/crazyflie-2-1-brushless/"],
  ["Battery","BETAFPV LAVA 450 mAh 2S LiHV","Pouch pack","26.1","63 x 15.5 x 13.5","2S 7.6 V","3.42 Wh; 75C; XT30","Good baseline balance of mass and current capability","Verify","Retailer datasheet","Recommended baseline","https://www.fpv24.com/en/betafpv/betafpv-lava-lipo-battery-lihv-450mah-2s-2-pieces"],
  ["Battery","GNB 650 mAh 2S LiHV","Pouch pack","36","11 mm profile","2S 7.6 V","120C","More endurance/current; mass pushes recovery burden","Verify","Retailer datasheet","Strong endurance candidate","https://www.myfpvstore.com/batteries/gaoneng-gnb-lihv-2s-7-6v-650mah-120c-hv-lipo-battery-xt30/"],
  ["Battery","Tattu 650 mAh 2S LiPo","Pouch pack","43","57 x 31 x 12","2S 7.4 V","75C; XT30","Robust current rating but heavy for baseline","Verify","Retailer datasheet","Heavy endurance candidate","https://www.nextfpv.com/products/tattu-650mah-2s-75c-lipo-battery-pack"],
  ["Battery","Crazyflie 350 mAh 1S","Pouch pack","9.1","Small","1S 3.7 V","30C","Very light; insufficient voltage/energy for baseline mass","Verify","Datasheet","Benchmark only","https://store.bitcraze.io/products/350mah-lipo-battery"],
  ["Battery","Crazyflie 250 mAh 1S","Pouch pack","7.1","Small","1S 3.7 V","Research platform battery","Lightest benchmark; insufficient baseline capability","Verify","Datasheet","Benchmark only","https://www.bitcraze.io/documentation/hardware/250mah_battery/250mah_battery-datasheet.pdf"],
  ["Battery","Aquila20 1100 mAh 2S LiHV","Smart pouch pack","54.5","Platform-specific","2S 7.6 V","8.74 Wh; 15C","Proves long endurance at ~122-127 g platform mass; too heavy/risky for recovery baseline","Verify","Datasheet/reference platform","Endurance benchmark","https://betafpv.com/collections/all-drone/products/aquila20-brushless-whoop-quadcopter"],
  ["Battery","BETAFPV 450 mAh 2S 45C","Pouch pack","Verify","Verify","2S","45C","Potential lower-cost baseline; mass must be measured","Verify","Datasheet","Research candidate","https://betafpv.com/products/450mah-2s-45c-lipo-battery-2pcs"],
  ["Battery","BETAFPV LAVA 550 mAh 2S 75C","Pouch pack","~29.5 estimated","Verify","2S 7.6 V","75C","Attractive middle ground; weight must be verified before selection","Verify","Retailer/estimate","High-priority research candidate","https://www.rotorama.com/product/betafpv-lava-550mah-2s-75c-2ks"],
  ["Vision","OpenMV Cam RT1062","Vision processor + camera","15-20 estimated","Compact","5 V input","600 MHz Cortex-M7; OV5640 5MP; Wi-Fi/BLE","Strong embedded vision; estimated mass and high cost need verification","~$150","Datasheet + estimate","High-capability candidate","https://openmv.io/products/openmv-cam-rt"],
  ["Vision","OpenMV Cam H7 Plus","Vision processor + camera","17","45 x 36 x 29","3.3 V active","STM32H743; OV5640; 25-50 fps QVGA; 230-240 mA","Documented mass; availability and packaging are concerns","$130","Datasheet","Benchmark / alternative","https://openmv.io/collections/cams/products/openmv-cam-h7-plus"],
  ["Vision","Seeed XIAO ESP32S3 Sense","Vision processor + camera","Verify","Very compact","5 V/3.3 V","ESP32-S3 camera board","Low-mass potential; marker performance/latency must be tested","Verify","Documentation","Recommended low-cost prototype","https://wiki.seeedstudio.com/xiao_esp32s3_camera_usage/"],
  ["Vision","Espressif ESP32-S3-EYE","Vision processor + camera","Verify","Compact module","5 V","2MP camera; 8 MB PSRAM/flash; accelerometer","Good development board; packaging mass must be measured","Verify","Documentation","Prototype candidate","https://documentation.espressif.com/esp-who/master/docs/en/get-started/ESP32-S3-EYE_Getting_Started_Guide.md"],
  ["Vision","Raspberry Pi Zero 2 W","Companion computer","12 board only","65 x 30","5 V","Quad Cortex-A53 1 GHz; 512 MB; CSI; Wi-Fi/BLE","Powerful but peripherals/camera/power add substantial mass and current","$15 board","Datasheet","Deferred high-compute option","https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/"],
  ["Positioning","Bitcraze Flow Deck v2","Optical flow + ToF","1.6","21 x 28 x 4","Platform dependent","PMW3901 + VL53L1X; ToF up to 4 m","Excellent indoor position aid if integration is feasible","Verify","Datasheet","Strong sensor candidate","https://www.bitcraze.io/products/flow-deck-v2/"],
  ["Receiver","BETAFPV ELRS Lite","ELRS receiver","0.46-0.47","11 x 10 x 3","5 V","Integrated ceramic antenna","Lowest mass manual override link","$8.99","Datasheet","Recommended baseline","https://betafpv.com/products/elrs-lite-receiver"],
  ["Receiver","RadioMaster RP1 V2","ELRS receiver","2.2 incl. antenna","13 x 11 x 3","5 V","UFL / T antenna","More robust antenna arrangement at mass penalty","$18.99","Datasheet","Strong alternative","https://www.radiomasterrc.com/products/rp1-expresslrs-2-4ghz-nano-receiver"],
  ["Receiver","RadioMaster XR1","ELRS receiver","1.0 excl. antenna","20 x 13 x 3","5 V","100 mW telemetry","Useful telemetry capability; larger than Lite receiver","$11.99","Datasheet","Alternative","https://radiomasterrc.com/products/xr1-nano-multi-frequency-expresslrs-receiver"]
];

const refs = [
  ["Crazyflie 2.1 Brushless","34 g with legs; 37 g guards","08028 10000KV","55 mm optimized","1S 350 mAh, 9.1 g","~10 min","Up to 30 g/motor; 40 g payload","Research ecosystem and low-mass benchmark","https://www.bitcraze.io/products/crazyflie-2-1-brushless/"],
  ["Happymodel Bassline 2S","Verify","EX1103 11000KV","2023 tri-blade","2S","Verify","Official motor curve reaches 121.9 g/motor","Primary propulsion-performance analog","https://www.happymodel.cn/index.php/2023/03/21/bassline-digital-hd-2s-toothpick-fpv-drone-built-in-walksnail-or-hdzero-vtx/"],
  ["BETAFPV Meteor85 2S","Verify","1103 11000KV","Gemfan 2015 2-blade","2S 300 mAh","~3 min","Protected 2S whoop","Low-mass removable-pack analog","https://betafpv.com/products/beta85-pro2-whoop-quadcopter-2s"],
  ["BETAFPV Aquila20","122-127 g takeoff","1103 10500KV","Gemfan 2218","2S 1100 mAh, 54.5 g","~10 min","Large battery at modest mass","Endurance analog; slower protected platform","https://betafpv.com/collections/all-drone/products/aquila20-brushless-whoop-quadcopter"],
  ["BETAFPV Pavo20 Pro II","65.2 g PNP","1104 7200KV","Gemfan 2218","3S 550-class","~6.5 min","Higher-power 3S protected platform","High-authority alternative analog","https://betafpv.com/collections/pavo-whoops/products/pavo20-pro-ii-brushless-whoop-quadcopter"],
  ["Happymodel Mobula8 O3","82.5 g O3 version","EX1103 11000KV","2-inch tri-blade","2S","Verify","Protected 2S digital platform","Payload/mass analog","https://www.happymodel.cn/index.php/2023/08/03/happymodel-mobula8-o3-and-o3-lite-tbs-version/"],
  ["BETAFPV Meteor85 (newer)","Verify","1103 11000KV","Gemfan 2015","2S","Verify","Current protected 2S reference","Confirms common motor/prop pairing","https://betafpv.com/collections/best-sellers/products/meteor85-brushless-whoop-quadcopter-2022"]
];

const arch = [
  ["Removable central pouch","0","0.80","Low","Excellent","Good","Low","Minimum inertia if centered; easiest recovery baseline","Recommended V1"],
  ["Semi-integrated protected central bay","4","0.78","Medium","Good","Good with venting","Medium","Still near CG; added enclosure mass","Recommended later iteration"],
  ["Split 2 x 1S cells in opposing arms, series wired","12","0.72","High","Poor","Uneven cooling/monitoring risk","High","Raises roll/pitch inertia and slows attitude arrest","Research only; not V1"],
  ["Four distributed/structural frame cells","18","0.68","Very high","Very poor","Highest thermal/impact complexity","Very high","Largest inertia penalty; uncertain load paths and cell abuse","Deferred research concept"]
];

const scenarios = [
  ["Baseline documented","EX1103 11000KV","2023-3","LAVA 450 2S","Removable central pouch",82.75,3.8,3.52,26.1,0,450,75,7.6,121.9,9.2,9.5,0.80,"Official motor curve; hover current estimated from curve"],
  ["Middle-capacity candidate","EX1103 11000KV","2023-3","LAVA 550 2S","Removable central pouch",82.75,3.8,3.52,29.5,0,550,75,7.6,121.9,9.2,9.8,0.80,"Battery mass estimated; verify"],
  ["Endurance/current candidate","EX1103 11000KV","2023-3","GNB 650 2S","Removable central pouch",82.75,3.8,3.52,36,0,650,120,7.6,121.9,9.2,10.2,0.80,"Heavier but strong current headroom"],
  ["Heavy endurance","EX1103 11000KV","2023-3","Tattu 650 2S","Removable central pouch",82.75,3.8,3.52,43,0,650,75,7.4,121.9,9.2,10.5,0.80,"Heavy; recovery penalty"],
  ["Central integrated bay","EX1103 11000KV","2023-3","LAVA 550 2S","Semi-integrated protected central bay",82.75,3.8,3.52,29.5,4,550,75,7.6,121.9,9.2,10.1,0.78,"Moderate integration penalty"],
  ["Split-arm battery concept","EX1103 11000KV","2023-3","2 x 1S 450 equivalent","Split 2 x 1S cells in opposing arms, series wired",82.75,3.8,3.52,26.1,12,450,75,7.6,121.9,9.2,10.8,0.72,"Mass/inertia/wiring penalties; research only"],
  ["Structural battery concept","EX1103 11000KV","2023-3","Custom embedded 2S 550","Four distributed/structural frame cells",82.75,3.8,3.52,29.5,18,550,50,7.6,121.9,9.2,11.5,0.68,"Highest uncertainty and safety risk"],
  ["Lowest motor mass","BETAFPV 1103 11000KV","Gemfan 2015-2","LAVA 450 2S","Removable central pouch",82.75,3.3,2.0,26.1,0,450,75,7.6,105,8.5,8.8,0.80,"Thrust/current estimated from similar 1103 platform"],
  ["1202.5 alternative","Flywoo ROBO 1202.5 11500KV","2023S-3","LAVA 450 2S","Removable central pouch",82.75,3.8,2.8,26.1,0,450,75,7.6,110,8.8,9.1,0.80,"Estimated; bench curve required"],
  ["Research-platform minimum","Crazyflie 08028 10000KV","55 mm optimized","1S 350","Removable central pouch",82.75,2.3,1.5,9.1,0,350,30,3.7,30,3.0,5.5,0.80,"Cannot meet 2:1 at project base mass"],
  ["Aquila endurance analog","Aquila 1103 10500KV","2218-3","Aquila 1100 2S","Removable central pouch",82.75,3.5,2.32,54.5,0,1100,15,7.6,105,8.0,10.5,0.80,"Thrust/current estimated; low-C pack limits peaks"],
  ["High-authority 3S","LAVA 1104 7200KV","2218-3","3S 550","Removable central pouch",82.75,5.3,2.32,45,0,550,75,11.4,230,10.2,11.5,0.80,"Outside baseline; high speed and impact energy"]
];

// Component candidates
const cs = wb.worksheets.add("Component Candidates");
title(cs, "A1:L1", "Drone Component Candidate Register", "Source-linked catalog research; 'Verify' and 'estimated' entries must be confirmed before selection.");
const ch = ["Category","Product","Function","Mass (g)","Dimensions","Voltage","Key specifications","Engineering assessment","Price","Evidence basis","Current disposition","Source URL"];
cs.getRange("A4:L4").values = [ch]; styleHeader(cs.getRange("A4:L4"));
cs.getRange(`A5:L${4+components.length}`).values = components; styleBody(cs.getRange(`A5:L${4+components.length}`));
cs.tables.add(`A4:L${4+components.length}`, true, "ComponentCandidatesTable").style = "TableStyleMedium2";
cs.freezePanes.freezeRows(4);
[120,190,120,90,120,100,260,280,90,120,150,320].forEach((w,i)=>cs.getRangeByIndexes(0,i,components.length+4,1).format.columnWidthPx=w);

// Reference drones
const rs = wb.worksheets.add("Reference Drones");
title(rs, "A1:I1", "Comparable Small-Drone Benchmarks", "Observed combinations ground the estimated propulsion cases; they are not direct proof for this custom vehicle.");
const rh = ["Platform","Flying mass","Motor","Propeller","Battery","Reported flight time","Relevant performance","Use in study","Source URL"];
rs.getRange("A4:I4").values=[rh]; styleHeader(rs.getRange("A4:I4"));
rs.getRange(`A5:I${4+refs.length}`).values=refs; styleBody(rs.getRange(`A5:I${4+refs.length}`));
rs.tables.add(`A4:I${4+refs.length}`,true,"ReferenceDronesTable").style="TableStyleMedium2";
rs.freezePanes.freezeRows(4);
[170,120,160,150,170,120,220,240,320].forEach((w,i)=>rs.getRangeByIndexes(0,i,refs.length+4,1).format.columnWidthPx=w);

// Architectures
const bs = wb.worksheets.add("Battery Architectures");
title(bs,"A1:I1","Frame-Integrated Battery Architecture Study","Integration penalties are planning estimates and must be replaced by CAD, cell-abuse, thermal, and serviceability evidence.");
const bh=["Architecture","Net integration penalty (g)","Usable energy fraction","Design complexity","Serviceability","Thermal behavior","Impact/fire risk","Recovery/inertia effect","Recommendation"];
bs.getRange("A4:I4").values=[bh]; styleHeader(bs.getRange("A4:I4"));
bs.getRange(`A5:I${4+arch.length}`).values=arch; styleBody(bs.getRange(`A5:I${4+arch.length}`));
bs.tables.add(`A4:I${4+arch.length}`,true,"BatteryArchitectureTable").style="TableStyleMedium2";
bs.getRange("B5:C8").format.fill=amber;
bs.getRange("A10:I10").merge(); bs.getRange("A10").values=[["Core conclusion: embedding cells away from the CG may improve packaging but increases inertia, slows attitude arrest, complicates charging/balancing, and makes crash-damaged cells harder to isolate. Keep the V1 pack removable and centered."]];
bs.getRange("A10:I10").format.fill=red; bs.getRange("A10:I10").format.font={bold:true}; bs.getRange("A10:I10").format.wrapText=true; bs.getRange("A10:I10").format.rowHeight=52;
[230,150,140,130,130,180,160,260,180].forEach((w,i)=>bs.getRangeByIndexes(0,i,12,1).format.columnWidthPx=w);

// Propulsion model
const ps=wb.worksheets.add("Propulsion Study");
title(ps,"A1:AA1","Motor–Propeller–Battery Estimate Study","Formula-driven planning comparison. Only EX1103/2023 values use a published motor bench curve; all estimated cases require thrust-stand verification.");
const ph=["Scenario","Motor","Propeller","Battery","Battery architecture","Base mass excl. motor/prop/batt (g)","Motor mass each (g)","Prop set mass (g)","Battery mass (g)","Integration penalty (g)","Total flying mass (g)","Capacity (mAh)","C rating","Nominal V","Energy (Wh)","Usable fraction","Usable energy (Wh)","Max thrust / motor (g)","Total max thrust (g)","Static T/W","Max current / motor (A)","Max system current (A)","Battery continuous current (A)","Discharge check","Estimated hover current (A)","Estimated flight time (min)","Notes"];
ps.getRange("A4:AA4").values=[ph]; styleHeader(ps.getRange("A4:AA4"));
const inputRows=scenarios.map(s=>[
  ...s.slice(0,10), "", s[10], s[11], s[12], "", s[16], "", s[13],
  "", "", s[14], "", "", "", s[15], "", s[17]
]);
ps.getRange(`A5:AA${4+scenarios.length}`).values=inputRows;
for(let r=5;r<5+scenarios.length;r++){
  ps.getRange(`K${r}`).formulas=[[`=F${r}+4*G${r}+H${r}+I${r}+J${r}`]];
  ps.getRange(`O${r}`).formulas=[[`=L${r}/1000*N${r}`]];
  ps.getRange(`Q${r}`).formulas=[[`=O${r}*P${r}`]];
  ps.getRange(`S${r}`).formulas=[[`=4*R${r}`]];
  ps.getRange(`T${r}`).formulas=[[`=S${r}/K${r}`]];
  ps.getRange(`V${r}`).formulas=[[`=4*U${r}+0.5`]];
  ps.getRange(`W${r}`).formulas=[[`=L${r}/1000*M${r}`]];
  ps.getRange(`X${r}`).formulas=[[`=IF(W${r}>=V${r},"PASS","FAIL")`]];
  ps.getRange(`Z${r}`).formulas=[[`=60*(L${r}/1000)*P${r}/Y${r}`]];
}
styleBody(ps.getRange(`A5:AA${4+scenarios.length}`));
ps.getRange(`F5:J${4+scenarios.length}`).format.fill=amber;
ps.getRange(`L5:N${4+scenarios.length}`).format.fill=amber;
ps.getRange(`P5:P${4+scenarios.length}`).format.fill=amber;
ps.getRange(`R5:R${4+scenarios.length}`).format.fill=amber;
ps.getRange(`U5:U${4+scenarios.length}`).format.fill=amber;
ps.getRange(`Y5:Y${4+scenarios.length}`).format.fill=amber;
ps.getRange(`K5:Z${4+scenarios.length}`).format.numberFormat="0.00";
ps.getRange(`X5:X${4+scenarios.length}`).conditionalFormats.add("containsText",{text:"FAIL",format:{fill:red,font:{bold:true,color:"#9C0006"}}});
ps.getRange(`T5:T${4+scenarios.length}`).conditionalFormats.add("cellIs",{operator:"lessThan",formula:2,format:{fill:red,font:{bold:true}}});
ps.tables.add(`A4:AA${4+scenarios.length}`,true,"PropulsionStudyTable").style="TableStyleMedium2";
ps.freezePanes.freezeRows(4); ps.freezePanes.freezeColumns(5);
[170,170,130,150,220,120,105,105,105,115,110,100,80,90,90,100,105,110,105,90,110,115,120,110,120,130,250].forEach((w,i)=>ps.getRangeByIndexes(0,i,scenarios.length+4,1).format.columnWidthPx=w);

// Assumptions
const as=wb.worksheets.add("Assumptions & Sources");
title(as,"A1:H1","Model Assumptions, Equations, and Limitations","Yellow values are planning inputs. The workbook is a selection-screening tool, not a substitute for bench testing.");
const assumptions=[
 ["Parameter","Best / nominal / value","Worst / range","Units","Basis","Conservative direction","Use","Source / note"],
 ["Current project nominal mass","140.75","","g","Repository mass budget","Higher is worse","Derives non-propulsion base mass","Engineering Data/estimates.csv"],
 ["Nominal motors in current budget","23","","g/set","Repository mass budget","Higher is worse","Removed from baseline","Engineering Data/estimates.csv"],
 ["Nominal props in current budget","2.5","","g/set","Repository mass budget","Higher is worse","Removed from baseline","Engineering Data/estimates.csv"],
 ["Nominal battery in current budget","32.5","","g","Repository mass budget","Higher is worse","Removed from baseline","Engineering Data/estimates.csv"],
 ["Base aircraft excluding motors/props/battery","82.75","","g","Calculated","Higher is worse","Scenario base mass","140.75 - 23 - 2.5 - 32.5"],
 ["Static thrust-to-weight requirement","2.0","","ratio","Fixed requirement","Lower is worse","Initial propulsion screen","Engineering Plan"],
 ["Avionics current allowance","0.5","","A","Estimated","Higher is worse","Maximum system current","Replace with measurement"],
 ["Removable battery usable fraction","0.80","","fraction","Estimated","Lower is worse","Flight-time estimate","Planning assumption"],
 ["Semi-integrated usable fraction","0.78","","fraction","Estimated","Lower is worse","Flight-time estimate","Thermal/service allowance"],
 ["Split-arm usable fraction","0.72","","fraction","Estimated","Lower is worse","Flight-time estimate","Balancing/wiring/thermal allowance"],
 ["Structural battery usable fraction","0.68","","fraction","Estimated","Lower is worse","Flight-time estimate","Highest uncertainty/risk"],
 ["Total mass equation","Base + 4*m_motor + m_prop_set + m_battery + integration penalty","","","Calculated","","Propulsion Study","Formula"],
 ["Battery energy equation","capacity_Ah * nominal_voltage","","Wh","Calculated","","Propulsion Study","Formula"],
 ["Estimated flight time","60 * capacity_Ah * usable_fraction / hover_current","","min","Calculated","","Propulsion Study","Does not include reserve/aging beyond usable fraction"],
 ["Battery continuous current","capacity_Ah * C_rating","","A","Calculated","","Discharge screen","C ratings may be optimistic"],
 ["Critical limitation","Recovery torque, motor transient response, thermal performance, and estimator behavior are not proven by static catalog data.","","","Engineering judgment","","Selection gate","Measure on thrust stand and controlled test rig"]
];
as.getRange(`A4:H${3+assumptions.length}`).values=assumptions; styleHeader(as.getRange("A4:H4")); styleBody(as.getRange(`A5:H${3+assumptions.length}`));
as.getRange("B5:B20").format.fill=amber;
[220,260,160,90,140,160,190,330].forEach((w,i)=>as.getRangeByIndexes(0,i,assumptions.length+3,1).format.columnWidthPx=w);

// Dashboard
const ds=wb.worksheets.add("Dashboard");
title(ds,"A1:H1","Guarded Micro-UAV Component & Propulsion Study","Initial source-backed selection screen | Component research + frame-integrated battery trade study");
ds.getRange("A4:B4").values=[["Study metric","Value"]]; styleHeader(ds.getRange("A4:B4"));
ds.getRange("A5:A11").values=[["Component candidates"],["Propulsion scenarios"],["Reference drones"],["Baseline base mass (g)"],["Required static T/W"],["Baseline scenario T/W"],["Baseline est. flight time (min)"]];
ds.getRange("B5:B11").formulas=[[`=COUNTA('Component Candidates'!B5:B100)`],[`=COUNTA('Propulsion Study'!A5:A100)`],[`=COUNTA('Reference Drones'!A5:A100)`],[`='Assumptions & Sources'!B9`],[`='Assumptions & Sources'!B10`],[`='Propulsion Study'!T5`],[`='Propulsion Study'!Z5`]];
styleBody(ds.getRange("A5:B11")); ds.getRange("B5:B11").format.numberFormat="0.00";
ds.getRange("D4:H4").merge(); ds.getRange("D4").values=[["Engineering recommendations"]]; styleHeader(ds.getRange("D4:H4"));
const recs=[
 ["D5:H5","Start bench testing with EX1103 11000KV + 2023-3 + removable 2S 550-650 mAh pack. The modeled 450 mAh 75C pack clears static T/W but fails the catalog full-load discharge screen."],
 ["D6:H6","Use a removable, centrally located pack for V1. Frame-integrated cells add uncertain mass, increase rotational inertia when distributed, and create charging, thermal, impact, and replacement hazards."],
 ["D7:H7","Prioritize AIO versus H7 FC trade testing: the AIO can save meaningful mass, but H7-class ArduPilot support/logging may be required for recovery research."],
 ["D8:H8","Do not select from estimated thrust cases until the exact motor-prop-voltage combination has measured thrust, current, RPM, transient response, and temperature data."],
 ["D9:H9","Static T/W is only a screen. Final selection must close recovery torque, motor-start latency, battery sag, gyro/estimator envelope, guard clearance, and thermal limits."]
];
for(const [range,text] of recs){ds.mergeCells(range); ds.getRange(range).values=[[text]]; ds.getRange(range).format.wrapText=true; ds.getRange(range).format.fill=pale; ds.getRange(range).format.rowHeight=50; ds.getRange(range).format.borders={preset:"all",style:"thin",color:"#B7C9D6"};}
ds.getRange("A14:C14").values=[["Scenario","Static T/W","Est. flight time (min)"]]; styleHeader(ds.getRange("A14:C14"));
for(let r=0;r<scenarios.length;r++){
  const rr=15+r, src=5+r;
  ds.getRange(`A${rr}`).formulas=[[`='Propulsion Study'!A${src}`]];
  ds.getRange(`B${rr}`).formulas=[[`='Propulsion Study'!T${src}`]];
  ds.getRange(`C${rr}`).formulas=[[`='Propulsion Study'!Z${src}`]];
}
styleBody(ds.getRange(`A15:C${14+scenarios.length}`)); ds.getRange(`B15:C${14+scenarios.length}`).format.numberFormat="0.00";
const chart1=ds.charts.add("bar",ds.getRange(`A14:B${14+scenarios.length}`)); chart1.setPosition("E12","L27"); chart1.title="Static Thrust-to-Weight by Scenario"; chart1.hasLegend=false; chart1.yAxis={numberFormatCode:"0.0x"};
const chart2=ds.charts.add("bar",ds.getRange(`A14:A${14+scenarios.length}`)); chart2.setData(ds.getRange(`A14:A${14+scenarios.length}`)); // reset below with helper range
chart2.setData(ds.getRange(`A14:C${14+scenarios.length}`)); chart2.setPosition("M12","T27"); chart2.title="Estimated Flight Time and T/W"; chart2.hasLegend=true;
[210,130,160,30,170,170,170,170,30,100,100,100,100,100,100,100,100,100,100,100].forEach((w,i)=>ds.getRangeByIndexes(0,i,30,1).format.columnWidthPx=w);
ds.getRange("A30:H30").merge(); ds.getRange("A30").values=[["Decision status: a removable central 2S pack is the defensible V1 architecture. Frame-integrated batteries remain a later research track after propulsion, mass properties, thermal behavior, crash protection, charging/balancing, and recovery dynamics are experimentally characterized."]];
ds.getRange("A30:H30").format.fill=red; ds.getRange("A30:H30").format.font={bold:true}; ds.getRange("A30:H30").format.wrapText=true; ds.getRange("A30:H30").format.rowHeight=58;

// Checks
const ck=wb.worksheets.add("Checks");
title(ck,"A1:F1","Workbook Verification Checks","PASS means the screening workbook is internally consistent; it does not certify hardware.");
ck.getRange("A4:D4").values=[["Check","Formula / criterion","Result","Interpretation"]]; styleHeader(ck.getRange("A4:D4"));
const checks=[
 ["Candidate breadth","At least 35 candidates",`=IF(COUNTA('Component Candidates'!B5:B100)>=35,"PASS","FAIL")`,"Wide initial option set"],
 ["Scenario breadth","At least 10 scenarios",`=IF(COUNTA('Propulsion Study'!A5:A100)>=10,"PASS","FAIL")`,"Multiple architectures compared"],
 ["Baseline static T/W","Baseline >= 2.0",`=IF('Propulsion Study'!T5>=2,"PASS","FAIL")`,"Initial propulsion screen"],
 ["Baseline discharge","Baseline pack continuous current >= estimated max",`='Propulsion Study'!X5`,"Catalog C-rating screen only"],
 ["All source URLs populated","No missing source cells",`=IF(COUNTBLANK('Component Candidates'!L5:L44)=0,"PASS","FAIL")`,"Sources auditable"],
 ["Frame battery warning present","Architecture sheet populated",`=IF(COUNTA('Battery Architectures'!A5:A8)=4,"PASS","FAIL")`,"Integration alternatives explicit"]
];
ck.getRange("A5:B10").values=checks.map(x=>x.slice(0,2)); ck.getRange("D5:D10").values=checks.map(x=>[x[3]]);
ck.getRange("C5:C10").formulas=checks.map(x=>[x[2]]);
styleBody(ck.getRange("A5:D10")); ck.getRange("C5:C10").conditionalFormats.add("containsText",{text:"FAIL",format:{fill:red,font:{bold:true}}}); ck.getRange("C5:C10").conditionalFormats.add("containsText",{text:"PASS",format:{fill:green,font:{bold:true}}});
[220,280,120,300].forEach((w,i)=>ck.getRangeByIndexes(0,i,12,1).format.columnWidthPx=w);

// Reorder dashboard first is not supported consistently; sheets remain well named.
await fs.mkdir(previewDir,{recursive:true});
for(const name of ["Dashboard","Component Candidates","Propulsion Study","Battery Architectures","Reference Drones","Assumptions & Sources","Checks"]){
  const blob=await wb.render({sheetName:name,scale:0.7});
  await fs.writeFile(`${previewDir}/${name.replaceAll(" ","_").replaceAll("&","and")}.png`,Buffer.from(await blob.arrayBuffer()));
}
const inspection=await wb.inspect({kind:"match",searchTerm:"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",options:{useRegex:true,maxResults:100},summary:"formula error scan"});
console.log(inspection.ndjson);
await fs.mkdir("Research/Component Study",{recursive:true});
const xlsx=await SpreadsheetFile.exportXlsx(wb);
await xlsx.save(out);
console.log(`Wrote ${out}`);
