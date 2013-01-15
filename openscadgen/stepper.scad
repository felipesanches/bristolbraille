include <globals.scad>;
bolt_radius=1.55;
stepper_shaft_radius=5/2;
stepper_bush_radius=22.1/2;
stepper_bush_length=4;
bolt_distance=30.7/2;

module stepper()
{
    color("blue")
    {
        cube([stepper_width,stepper_length,stepper_height],center=true);
        translate([0,0,stepper_length/2+stepper_shaft_length/2])
            cylinder(r=stepper_shaft_radius,h=stepper_shaft_length,center=true);
        translate([0,0,stepper_length/2+stepper_bush_length/2])
            cylinder(r=stepper_bush_radius,h=stepper_bush_length,center=true);
        translate([bolt_distance,bolt_distance,stepper_length/2])
          cylinder(r=bolt_radius,h=10);
        translate([bolt_distance,-bolt_distance,stepper_length/2])
          cylinder(r=bolt_radius,h=10);
        translate([-bolt_distance,bolt_distance,stepper_length/2])
          cylinder(r=bolt_radius,h=10);
        translate([-bolt_distance,-bolt_distance,stepper_length/2])
          cylinder(r=bolt_radius,h=10);
    }
}

module stepper_mount()
{
    difference()
    {
        cube([stepper_length,stepper_width+2*thickness,thickness],center=true);    
        translate([0,stepper_width/2+thickness/2,0])
            cube([stepper_width/3,thickness,thickness],center=true);    
        translate([0,-stepper_width/2-thickness/2,0])
            cube([stepper_width/3,thickness,thickness],center=true);    
        translate([0,0,-stepper_height/2-thickness/2])
        stepper();

    }

}
