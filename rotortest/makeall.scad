/* TODO

- FIXED by increasing size of hole for the slider and descreasing height of lock. 
  can't be assembled now the sliders have the solenoid pins on them. do something with the slider holders?

- comb is still just a guess, needs sizing
- extra slider holders would be good at the ends to deal with the acetyl bending
- springs for the sliders

*/
//main bits
//export_slider_holder=true;
//build_slider_num=1;
//build_comb=true;
//build_slider_holders=true;
//build_stepper=true;
//build_base=true;
//build_lid=true;
lid_camera_hole=true;
export_side=true;
//build_sides=true; 
//build_comb=true;
//export_base = true;
//build_pin_slider=true;
//build_stepper_mount=true;
//export_stepper_mount = true;
//optional extras
//build_solenoids=true;
//build_sliders=true; 
//build_rotors=true;
//build_rotor_rod=true;
//build_pins=true;
//build_slider_rods=true;
include <globals.scad>;
include <stepper.scad>;
include <sliders.scad>;
include <solenoids.scad>;
include <base.scad>;
include <rotors.scad>;
include <pins.scad>;


/*print some variables*/
echo("solenoid_min_y_spacing");
echo(solenoid_min_y_spacing);

/*************************************************************
sliders and slider rods
*/
if(build_sliders)
{
    //render() //why?
//    translate([0,slider_move_length/2,slider_move_height/2])
    translate([0,slider_y,slider_z])
      sliders();
}
if(export_sliders)
{
   projection()sliders(true);
}

if(build_slider_rods)
{
    made_slider_rods();
}
module made_slider_rods()
{
  translate([-solenoid_width/2-edge_margin-0.5*edge_margin,edge_margin,slider_z])
    slider_rods();
}

/*************************************************************
rotors
*/

if(build_rotors)
{
    //rotors 
    translate([0,rotor_rod_y,rotor_rod_z])
      rotors();
}
if(build_rotor_rod)
  made_rotor_rod();
module made_rotor_rod()
{
    //rod
    translate([0,rotor_rod_y,rotor_rod_z])
      translate([-solenoid_width/2-edge_margin-0.5*edge_margin,0,0])
        rotor_rod();
}
/*************************************************************
pins
*/
if(build_pins)
    made_pins();
module made_pins()
{
  translate([0,rotor_rod_y,rotor_rod_z+rotor_diameter/2+pin_length/2])
    pins();
}
module made_camera_hole()
{
  translate([thickness,rotor_rod_y,base_height-thickness])
   cube([side_separation-4*thickness,comb_length-4*thickness,thickness*4],center=true);
 }
  

/*************************************************************
solenoid
*/
if(build_solenoids)
    solenoids()solenoid();

/*************************************************************
base
*/
if(build_base)
    made_base();
if(export_base)
    projection()made_base();

module made_base()
{
  difference()
  {
    translate([base_width/2-solenoid_width/2-edge_margin,base_y,base_z])
      base();
    solenoids()solenoid_hole();
    made_slider_holder(1,false);
    made_slider_holder(2,false);
   made_side(1);
   made_side(2);
   made_stepper_mount();
  }
}

/*************************************************************
lid
*/
if(build_lid)
    made_lid();
if(export_lid)
    projection()made_lid();
module made_lid()
{
  difference()
  {
//    translate([base_width/2-solenoid_width/2-edge_margin,base_y,base_z])
    translate([base_width/2-solenoid_width/2-edge_margin,base_y,base_z+base_height-thickness])
      base();
   made_slider_holder(1,false);
   made_slider_holder(2,false);
   made_side(1);
   made_side(2);
   if(lid_camera_hole)
   {
    made_camera_hole();
   }
   else
   {
     made_pins();
   }
   made_stepper();
  }

}

/*************************************************************
sides
*/
if(build_sides)
{
    made_side(1,true);
    made_side(2,true);
}
if(export_side)
    projection()rotate([0,90,0])made_side(1,true);

module made_side(num,boolean)
{
  difference()
  {
    if(num==1)
    {
        translate([base_x+side_separation-thickness,base_y,base_z+base_height/2-thickness/2])
          side();
    }
    if(num==2)
    {
        translate([base_x,base_y,base_z+base_height/2-thickness/2])
          side();
    }
    if(boolean)
    {
    made_slider_holder(1,false);
    made_slider_holder(2,false);
    made_slider_rods();
    made_rotor_rod();
    /*
    union()
    {
    translate([pin_slider_x,pin_slider_y,pin_slider_z])
      pin_slider();
    translate([pin_slider_x,pin_slider_y,pin_slider_z+pin_slider_move_height])
      pin_slider();
    }
    */
    }
  }
}

/*************************************************************
pin slider
*/
if(build_pin_slider)
    made_pin_slider();
if(export_pin_slider)
    projection()made_pin_slider();

pin_slider_x=base_x+pin_slider_width/2-thickness/2-thickness;
pin_slider_y=rotor_rod_y;
pin_slider_z=rotor_rod_z+pin_length/2;
module made_pin_slider()
{
  color("gray")
  difference()
  {
    translate([pin_slider_x,pin_slider_y,pin_slider_z])
      pin_slider();
      made_pins();
  }
}

/*************************************************************
comb
*/
if(build_comb)
    //render()
    made_comb();
if(export_comb)
    projection()made_comb();
module made_comb()
{
  color("blue")
    translate([comb_width/2-min_spacing-rotor_thickness,rotor_rod_y,rotor_rod_z+spindle_radius*2])
      comb();
}
/*************************************************************
slider holders
*/
if(export_slider_holder)
{
    projection()
        rotate([90,0,0])
            made_slider_holder(build_slider_num,true);
}
else if(build_slider_holders)
{
//    render() //why?
    made_slider_holder(1,true);
 //   render() //why?
    made_slider_holder(2,true);
}

//pass second argument=true to create slider holder with all the holes
module made_slider_holder(num,boolean)
{
 difference()
  {
    if(num==1)
    {
        //most +ve y slider_holder
        translate([-solenoid_width/2-edge_margin+side_separation/2,rotor_rod_y+comb_length/2-thickness/2,base_z+base_height/2-thickness/2])
          rotate([90,0,0])
            slider_holder();
    }
    else if(num==2)
    {
        //close to origin slider_holder
        translate([-solenoid_width/2-edge_margin+side_separation/2,rotor_rod_y-comb_length/2+thickness/2,base_z+base_height/2-thickness/2])
          rotate([90,0,0])
            slider_holder();
    }
    if(boolean)
    {
        solenoids()solenoid_hole();
        made_comb();
        translate([0,solenoid_total_y/2-solenoid_min_y_spacing,slider_z])
          sliders_boolean();
          //add some room to get the sliders in
        translate([0,solenoid_total_y/2-solenoid_min_y_spacing,slider_z+slider_lock_height*1.3])
          sliders_boolean();
    }
  }
}

/*************************************************************
stepper
*/

if(export_stepper_mount)
    projection()rotate([0,90,0])made_stepper_mount();
if(build_stepper_mount)
{
//    made_stepper();
    made_stepper_mount();
}
module made_stepper()
{
translate([side_separation+stepper_shaft_length,rotor_rod_y,rotor_rod_z])
    rotate([90,0,-90])
      stepper();
}
module made_stepper_mount()
{
//difference()
//{
  translate([side_separation,base_y,base_z+base_height/2-thickness/2])
      rotate([90,0,-90])
        stepper_mount();
//      made_stepper();
 //     }
}
