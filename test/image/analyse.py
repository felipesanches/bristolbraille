from PIL import Image
import colorsys

def get_main_color(img):
    colors = img.getcolors(10000) #put a higher value if there are many colors in your image
    max_occurence, most_present = 0, 0
    try:
        for c in colors:
            if c[0] > max_occurence:
                (max_occurence, most_present) = c
        return most_present
    except TypeError:
        raise Exception("Too many colors in the image")


def get_region(img,region):
  (x,y)=im.size
  region_w=x/3
  #3 bands
  box = (region_w*region,y/2,region_w*region+region_w,y)
  region = im.crop(box)
  #region.save("region.jpg")
  return region

im = Image.open("captured/100.JPG")
for i in range(3):
  region = get_region(im,i)
  r,g,b = get_main_color(region)
  h,s,v= colorsys.rgb_to_hsv(r/float(255),g/float(255),b/float(255))
  print h
  if h > 0.18:
    print 1,
  else :
    print 0,
#  print "%f,%f,%f" % (h*255,s*255,v*255)
  """
  mode = "RGB"
  out=Image.new(mode, (200,200), main_colour)
  out.save("%icolor.jpg" % i)
  """
"""
print region.size
main_colour= get_main_color(region)
"""
"""
source = im.split()

R, G, B = 0, 1, 2

# select regions where g is less than 100
mask = source[G].point(lambda i: i > 100 and 255)
"""
