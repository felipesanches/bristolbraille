include <globals.scad>;
module makerbeam(l)
{
  color("grey")
    cube([makerbeam_w,makerbeam_w,l],center=true); }
