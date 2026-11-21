// Shared modules. Units: mm.
fn_preview = 24;
fn_render = 96;
function fn() = $preview ? fn_preview : fn_render;

// Regular hexagonal prism given distance across flats.
module hex_prism(across_flats, h) {
  cylinder(d = across_flats / cos(30), h = h, $fn = 6);
}

// D-shaped bore: diameter d with a flat at distance `flat_to_center` from the axis.
module d_bore(d, flat_to_center, h) {
  intersection() {
    cylinder(d = d, h = h, $fn = fn());
    translate([-d, -d / 2 - 1, 0]) cube([d / 2 + flat_to_center + d, d + 2, h]);
  }
}

// Clearance hole along Z (ISO medium fit).
function clearance(m) = m == 3 ? 3.4 : m == 4 ? 4.5 : m == 5 ? 5.5 : m + 0.5;
module clearance_hole(m, h) { cylinder(d = clearance(m), h = h, $fn = fn()); }

// Captive hex nut pocket with insertion slot along +X.
function nut_af(m) = m == 3 ? 5.5 : m == 4 ? 7.0 : m == 5 ? 8.0 : 1.8 * m;
function nut_h(m) = m == 3 ? 2.4 : m == 4 ? 3.2 : m == 5 ? 4.0 : 0.8 * m;
module nut_trap(m, slot_len = 10, tol = 0.2) {
  af = nut_af(m) + tol;
  h = nut_h(m) + tol;
  hex_prism(af, h);
  translate([0, -af / 2, 0]) cube([slot_len, af, h]);
}
