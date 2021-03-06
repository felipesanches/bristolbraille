#!/usr/bin/env python
from PIL import Image, ImageDraw
import argparse
import colorsys
import sys
import pickle
state_file = 'coords'

def get_coords():
    f=open(state_file)
    
    (left, upper, right, lower) =pickle.load(f)
    return (left,upper,right,lower)

def get_main_color(img):
    colors = img.getcolors(img.size[0]*img.size[1])
    max_occurence, most_present = 0, 0
    for c in colors:
        if c[0] > max_occurence:
            (max_occurence, most_present) = c
    return most_present


def draw_region(img, box):
    draw = ImageDraw.Draw(img)
    draw.rectangle(box, outline="red") 

def get_region_box(img,region_num):
  (x,y)=img.size

  band_w = x/args.num_regions
  region_w=x/args.num_regions*args.region_width
  region_offset = (band_w - region_w)/2

  box = (
    int(band_w*region_num+region_offset),
    0, #y/2,
    int(band_w*region_num+region_offset+region_w),
    y)
  if args.debug:
    print >> sys.stderr, box
    print >> sys.stderr, x,y
    print >> sys.stderr, region_w, region_offset, band_w, region_offset*2+region_w
  #box = (region_w*region_num,y/2,region_w*region_num+region_w,y)
  return box

def get_zoom(img,box):
  region = img.crop(box)
  return region

def get_region(img,region_num):
  region = img.crop(get_region_box(img,region_num))
  region.save("region%d.jpg" % (region_num))
  return region

def analyse():
  box=get_coords() 
  im = Image.open(args.file)
  im = get_zoom(im,box)
  im = im.rotate(-90)
  #im.save("zoom.jpg")
  """
  r,g,b = get_main_color(im)
  h,s,v= colorsys.rgb_to_hsv(r/float(255),g/float(255),b/float(255))
  print h
  return
  """
  matches = [None,None,None] 
  for i in range(args.num_regions):
    region = get_region(im,i)

    r,g,b = get_main_color(region)
    h,s,v= colorsys.rgb_to_hsv(r/float(255),g/float(255),b/float(255))
    if args.debug:
      print >> sys.stderr, "%i: %.2fh" % (i,h)
    if h > args.hue_match:
      matches[i]=True
      print 1,
    else :
      matches[i]=False
      print 0,
 
  print ""
  for i in range(args.num_regions):
    draw_region(im, get_region_box(im,i))
  im.save("regions.jpg")
  return matches

def get_args():
  argparser = argparse.ArgumentParser()

#  group = argparser.add_mutually_exclusive_group(required=True)
  argparser.add_argument('--hue-match',
      action='store', type=float, dest='hue_match', default=0.18,
      help="hue to be greater than to match")
  argparser.add_argument('--region-width',
      action='store', type=float, dest='region_width', default=0.3,
      help="percentage width")
  argparser.add_argument('--num-regions',
      action='store', type=int, dest='num_regions', default=3,
      help="number of regions")
  argparser.add_argument('--debug',
      action='store_const', const=True, dest='debug', default=False,
      help="debug")
  argparser.add_argument('--file',
      action='store', dest='file', default='capt0000.jpg',
      help="load an image")
      
  return argparser.parse_args()

if __name__=="__main__":

  args = get_args()
  analyse()
  

