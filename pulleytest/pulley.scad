include <globals.scad>;
module pulley(radius,rim=true)
{
  rim_w=1;
  cylinder(r=radius,h=belt_width,center=true);
  if( rim )
  {
  translate([0,0,belt_width/2+rim_w/2])
    cylinder(r=radius+rim_w,h=1,center=true);
  translate([0,0,-belt_width/2-rim_w/2])
    cylinder(r=radius+rim_w,h=1,center=true);
    }
}

