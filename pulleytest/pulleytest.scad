include <globals.scad>;
include <stepper.scad>;
include <pulley.scad>;
include <solenoids.scad>;
include <makerbeam.scad>;

module bearing(r1,r2,h)
{
    color("blue")
    difference()
    {
        cylinder(r=r1,h=h,center=true);
      //  cylinder(r=r2,h=h*2,center=true);
    }
}

pulley_z = stepper_height/2+stepper_shaft_length/2;
mount_z = stepper_height/2+thickness/2;

module made_extras()
{
stepper();
translate([0,0,pulley_z])
  pulley(pulley_r);
translate([0,0,pulley_z])
belt();
translate([base_length/2-stepper_width/2,base_height/2-makerbeam_w/2,stepper_height/2-makerbeam_w/2]) rotate([0,90,0])makerbeam(200);
translate([base_length/2-stepper_width/2,-base_height/2+makerbeam_w/2,stepper_height/2-makerbeam_w/2]) rotate([0,90,0])makerbeam(200);

}

*projection() translate([belt_length,0,0]) sliding_pulley(project=true);
*projection() translate([belt_length/2,0,0]) pulley_clutch(project=true);
*projection()stepper_mounting();
projection() horn(project=true);
module stepper_mounting()
{
  difference()
  {
    translate([0,0,mount_z])
      stepper_mount();
    stepper();
  }
}

module belt()
{
  color("brown")
  difference()
  {
    hull()
    {
      cylinder(r=pulley_r+0.5,h=belt_width,center=true);
      translate([belt_length,0,0])
      cylinder(r=pulley_r+0.5,h=belt_width,center=true);
    }
    hull()
    {
      cylinder(r=pulley_r,h=belt_width*2,center=true);
      translate([belt_length,0,0])
      cylinder(r=pulley_r,h=belt_width*2,center=true);
    }
  }
}
    
module pulley_clutch(project=false)
{
  //smaller pulley, no rim
  smaller_r = pulley_r-0.5;
  difference()
  {
  sliding_pulley(rim=false,radius=smaller_r,project=project);
  translate([horn_w/2-sbearing_r1,roller_y-horn_w/2+sbearing_r1/2,pulley_z-sbearing_h])
    translate([horn_w/2-sbearing_r1,horn_w/2-sbearing_r1,0])
      cylinder(r=sbearing_r2,h=40,center=true);
  }
 if(!project)
 {
 horn();

  //solenoid
  
  translate([-stepper_width,-base_height/2+solenoid_length/2,mount_z+solenoid_length/2-thickness/2]) rotate([90,0,90]) 
    solenoid();
  }

}

  //horn
  module horn(project=false)
  {
  //roller

  color("grey")
  translate([horn_w/2-sbearing_r1,roller_y-horn_w/2+sbearing_r1/2,pulley_z-sbearing_h])
  {
    difference()
    {
      cube([horn_w,horn_w,thickness],center=true);
      translate([-horn_w/2+sbearing_r1,horn_w/2-sbearing_r1/2,0])
        cylinder(r=sbearing_r2,h=10,center=true);
      translate([-horn_w/2+sbearing_r1,-horn_w/2+sbearing_r1,0])
        cylinder(r=sbearing_r2,h=10,center=true);
    }
    if(!project)
    {
      //pivot
      translate([horn_w/2-sbearing_r1,horn_w/2-sbearing_r1,0])
        cylinder(r=sbearing_r2,h=20,center=true);
      //bearing
      translate([-horn_w/2+sbearing_r1,horn_w/2-sbearing_r1/2,sbearing_h])
        bearing(sbearing_r1,sbearing_r2,sbearing_h);
    }
  }
}

module sliding_pulley(radius=pulley_r,rim=true,project=false)
{
  translate([0,0,mount_z])
  {
    difference()
    {
      stepper_mount();
      bearing(bearing_diameter/2,shaft_diameter/2,bearing_height);
    }
    if(!project)
      bearing(bearing_diameter/2,shaft_diameter/2,bearing_height);
  }

  if(!project)
  translate([0,0,pulley_z])
  {
    pulley(radius,rim);
    cylinder(r=shaft_diameter/2,h=20,center=true);
  }
}
