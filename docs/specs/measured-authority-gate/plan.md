# EST-REC-007 — Execution Plan

1. Receive and inspect Wave-1 hardware; do not purchase Wave 2.
2. Sign the propulsion-bench safety checklist and complete props-off telemetry,
   current-limit, fuse, and kill-switch checks.
3. Calibrate load, voltage, current, RPM/time, and arm-length measurements.
4. Test all six motors at 8.4, 7.6, and 7.0 V; repeat the frozen throttle and
   collective grid while recording temperature and supply state.
5. Derive `tau_rp(T)` with uncertainty and run
   `Analysis/measured_authority_gate.py` on the 7.0 V samples.
6. If the authority gate is PASS, inject measured distributions into the fixed
   Monte Carlo and run 250/1,000/250 trials at 1/2/3 rad/s.
7. Record PASS, FAIL, or INCONCLUSIVE before proposing follow-on work.
8. On August 3, freeze the portfolio page as a measured verdict only if the
   calibrated dataset exists; otherwise publish “measurement pending.”
