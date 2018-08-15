h0 = 5;
h1 = 10;
difference() {
  union(){
    translate([-20,-20,0])cube([40,40,h0]);
    translate([-17,-17,0])cube([34,34,h1]);
  }
  translate([-12.7,-12.7,h0-1])cube([25.4,25.4,h1]);
}
for(i=[0:3]) rotate([0,0,i*90]) translate([0,-12.7-0.01,0]) t_slot_C(h1);
translate([0,0,h0-1]) cylinder(h=h0,d=5.1,$fn=40);
module v_slot_C(height1) {
x1=4.5;
x2=3.1;
x3=5.4;
x4=2.9;
y1=1.9;
y2=3.5;
y3=6;

linear_extrude(height = height1, convexity = 10, slices = 20, scale = 1.0)
polygon(points=[[-x1,0],[-x2,y1],[-x3,y1],[-x3,y2],[-x4,y3],[x4,y3],[x3,y2], [x3,y1],[x2,y1],[x1,0]],convexity=10);
}



module t_slot_C(height1) {

    d1 = 1.1;
    x1=7.4 - d1/2;
    y1=2.5+d1/2;

    d2 = 3;
    y2=8.1-d2/2;
    x2=x1-(y2-y1)-(d2-d1)/sqrt(2);


    x3 = 6;
    d3 = y1-d1/2;

    hull(){
     translate([-x1,y1,height1/2]) cylinder(h=height1,d=d1,$fn=40,center=true);
     translate([x1,y1,height1/2]) cylinder(h=height1,d=d1,$fn=40,center=true);
     translate([-x2,y2,height1/2]) cylinder(h=height1,d=d2,$fn=40,center=true);
     translate([x2,y2,height1/2]) cylinder(h=height1,d=d2,$fn=40,center=true);
    }

    translate([-x3/2,0,0])cube([x3,y1,height1]);

    difference(){
        translate([-x3/2-d3/2,d3/2,0])cube([x3+d3,d3/2,height1]);
        translate([-x3/2-d3/2,d3/2,height1/2]) cylinder(h=height1+.1,d=d3,$fn=20,center=true);
        translate([x3/2+d3/2,d3/2,height1/2]) cylinder(h=height1+.1,d=d3,$fn=20,center=true);
    }
}

