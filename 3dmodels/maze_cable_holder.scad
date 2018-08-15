difference () {
    cylinder(h=15,d=40);
    translate([0,0,-0.1])cylinder(h=15.2,d=26);
    rotate([0,0,-150.5]) translate([0,-4,-0.1])cube([25,8,15.2]);
}
translate([-15,-20,0])cube([30,7,15]);
translate([-25,-20,0])cube([50,4,15]);