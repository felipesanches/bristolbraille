include <globals.scad>;
use <cam.scad>;
/*
todo:
  -guide needs to fit slider really accurately to ensure non-wobbly rise
  bit is cutting slightly wide, reduce bit width to 1.9mm
  +cam is too hard to turn, increase slope time from 40 to 50
cam_r = 10;
min_cam_r = 5;
*/

slider_width = 50;
slider_height = 30;
slot_dist = 30;
slot_length=5;
base_height = 40;
display = true;
cam_y = (base_height-slider_height)/2;
if(display)
{
  translate([0,cam_y,thickness*1.5])
    color("blue")
      draw_cam(center_r=spindle_radius);

  made_slider();
  made_backplate();
  made_guide();
  //translate([0,cam_y,-thickness]) color("grey") backplate();
}

//projection()draw_cam(center_r=spindle_radius);
//projection()made_slider();
//projection()made_backplate();
//projection()made_guide();
module bolts(r=spindle_radius)
{
  translate([-slot_dist/2,0,0])
    cylinder(r=r,h=thickness*4,center=true);
  translate([+slot_dist/2,0,0])
    cylinder(r=r,h=thickness*4,center=true);
  //cam
  translate([0,0,0])
    cylinder(r=r,h=thickness*4,center=true);
}

module side_bolts()
{
  translate([-slider_width/2-5,0,0])
    cylinder(r=spindle_radius+0.1,h=thickness*4,center=true);
  translate([+slider_width/2+5,0,0])
    cylinder(r=spindle_radius+0.1,h=thickness*4,center=true);
}
module made_guide()
{
  translate([0,0,thickness])
    guide();
}
module guide()
{
  color("grey")
    difference()
    {
      backplate();
       translate([0,cam_y,0])
        slider_plate(2*thickness);
      side_bolts();
    }
}
module made_slider(diff=false)
{
 color("green")
   translate([0,cam_y,thickness+0.1])slider(diff);
}
module made_backplate()
{
  difference()
  {
    backplate();
    made_slider(diff=true);
    side_bolts(spindle_radius+0.1);
  }
}
module backplate()
{
  cube([slider_width*1.5,base_height,thickness],center=true);
}
module slot(length=5)
{
  hull()
  {
  translate([0,length,0])
    cylinder(r=spindle_radius,h=2*thickness,center=true);
  cylinder(r=spindle_radius,h=2*thickness,center=true);
  }
}
module slider(diff=false)
{
  follower_y = min_cam_r+spindle_radius;
  if(diff)
  {
    translate([0,0,0])
      bolts(spindle_radius+0.1);
  }
  difference()
  {
    slider_plate(thickness);
    translate([-slot_dist/2,-slot_length,0])
      slot();
    translate([+slot_dist/2,-slot_length,0])
      slot();
    translate([0,-slot_length,0])
      slot();
    translate([0,follower_y,0])
      bolts();
  }
  
}

module slider_plate(thickness)
{
    cube([slider_width,slider_height,thickness],center=true);
}
