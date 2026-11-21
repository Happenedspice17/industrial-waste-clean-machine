// Wheel hub adapter: JGB37-3530 motor D-shaft -> 12 mm hex wheel (Talon 124 mm). Module M2.
// All interface dimensions MUST be measured on the real parts before printing (lesson 15).
include <../lib/common.scad>

/* [Shaft (measure with caliper)] */
shaft_d = 6.0;          // TODO measure: JGB37 output shaft diameter
shaft_flat = 2.5;       // TODO measure: axis-to-flat distance (D-cut)
shaft_engage = 12;      // length of shaft inside the hub
bore_tol = 0.15;        // radial clearance, tune with a test coupon

/* [Wheel interface (measure)] */
hex_af = 12.0;          // TODO measure: wheel hex socket across flats
hex_len = 10;           // TODO measure: wheel hub depth
hex_tol = 0.15;

/* [Flange and set screw] */
flange_d = 22;
flange_h = 3;
set_screw_m = 3;        // radial set screw on the shaft flat, captive nut
retain_screw_m = 3;     // axial screw holding the wheel (0 = none)

total_h = flange_h + max(hex_len, shaft_engage);

difference() {
  union() {
    cylinder(d = flange_d, h = flange_h, $fn = fn());
    translate([0, 0, flange_h]) hex_prism(hex_af - hex_tol, total_h - flange_h);
  }
  // D-bore from the motor side
  translate([0, 0, -0.01]) d_bore(shaft_d + 2 * bore_tol, shaft_flat + bore_tol, shaft_engage + 0.02);
  // set screw (radial, +X) acting on the shaft flat, with captive nut inserted from the motor side
  set_z = shaft_engage / 2 + 0.5;
  nut_x = shaft_flat + bore_tol + 1.2;
  translate([0, 0, set_z]) rotate([0, 90, 0]) cylinder(d = clearance(set_screw_m), h = hex_af, $fn = fn());
  translate([nut_x, 0, set_z]) rotate([0, 90, 0]) rotate([0, 0, 30])
    hex_prism(nut_af(set_screw_m) + 0.2, nut_h(set_screw_m) + 0.2);
  translate([nut_x, -(nut_af(set_screw_m) + 0.2) / 2, -0.01])
    cube([nut_h(set_screw_m) + 0.2, nut_af(set_screw_m) + 0.2, set_z + 0.01]);
  // axial wheel-retention screw from the wheel side
  if (retain_screw_m > 0)
    translate([0, 0, shaft_engage + 0.6]) clearance_hole(retain_screw_m, total_h);
}
