#!/usr/bin/python
import math

#define the movement we want from the cam
slope = 50
control_points = [[0,5],[slope,10],[359-slope,10],[359,5]]
#how many degrees to increment each time, smaller number makes the cam smoother
deg_inc = 1 

points = []
last_point = None
#interpolate the control points
for point in control_points:
  if last_point:
    print "interpolate between ", last_point, " and ", point
    inc = float(point[1] - last_point[1]) / (point[0] - last_point[0]-deg_inc) / deg_inc
    for deg in range(last_point[0],point[0],deg_inc):
      new_point = [deg,last_point[1]+(deg-last_point[0])*inc]
      points.append(new_point)
  last_point = point

#then calculate the x,y for polygon
poly_points = []
for point in points:
  x = math.sin(math.radians(point[0]))*point[1]
  y = math.cos(math.radians(point[0]))*point[1]
  poly_points.append([x,y])
  #print "%3d, x %2.2f y %2.2f" % (point[0], x, y)

#finally, format for openscad
f = open("cam.scad",'w')
f.write( """$fs=1;
draw_cam();
module draw_cam(thickness=2,center_r=2)
{
  difference()
  {
    linear_extrude(height=thickness) 
      polygon([""" )
for point in poly_points:
  f.write( "[%2.2f,%2.2f],\n" % (point[0], point[1]) )
f.write("""]);
    cylinder(r=center_r,h=3*thickness,center=true);
  }
}""")
f.close
