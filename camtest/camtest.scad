include <globals.scad>;
use <cam.scad>;

cam_r = 10;
min_cam_r = 5;


side_width = 50;
side_height = 30;
slot_dist = 30;
slot_length=5;

//display = true;
if(display)
{
  translate([0,0,thickness])
    color("blue")
      draw_cam(center_r=spindle_radius);

  side();

  translate([0,0,-thickness]) color("grey") backplate();
}

//projection()draw_cam(center_r=spindle_radius);
//projection()side();
projection()backplate();

module backplate()
{
  difference()
  {
  cube([side_width*1.5,side_height,thickness],center=true);
  translate([-slot_dist/2,0,0])
    cylinder(r=spindle_radius,h=thickness*2,center=true);
  translate([+slot_dist/2,0,0])
    cylinder(r=spindle_radius,h=thickness*2,center=true);
  //cam
  translate([0,0,0])
    cylinder(r=spindle_radius,h=thickness*2,center=true);
  }
    
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
module side()
{
  follower_y = min_cam_r+spindle_radius;
  difference()
  {
    cube([side_width,side_height,thickness],center=true);
    translate([-slot_dist/2,-slot_length,0])
      slot();
    translate([+slot_dist/2,-slot_length,0])
      slot();
    translate([0,-slot_length,0])
      slot();
    //3 x cam follower for testing cam in different locations
    translate([-slot_dist/2,follower_y,0])
      cylinder(r=spindle_radius,h=thickness*2,center=true);
    translate([slot_dist/2,follower_y,0])
      cylinder(r=spindle_radius,h=thickness*2,center=true);
    translate([0,follower_y,0])
      cylinder(r=spindle_radius,h=thickness*2,center=true);
  }
  
}
