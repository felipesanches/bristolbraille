include <globals.scad>;

module solenoid()
{
  color("lightblue")
  {
  cube([solenoid_width,solenoid_length,solenoid_height],center=true);
  translate([0,0,solenoid_height/2+solenoid_plunger_length/2])
    cylinder(r=solenoid_plunger_radius,h=solenoid_plunger_length,center=true);
  }
}
