#!/usr/bin/env python
import time
import os
import pickle
import cv, cv2
import argparse

class Target:


    def __init__(self):
        self.match={}
        self.first_frame_name = "firstframe.png"
        self.font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 0.5, 1, 0, 2, 8)
        self.statefile = 'match_data.pkl'
        try:
          pkl_file = open(self.statefile, 'rb')
          self.match = pickle.load(pkl_file)
          self.matching = True; 
        except:
          self.matching = False; 
          self.match["threshold"]=10
          self.match["hue"]=50

        self.capture = cv2.VideoCapture(0) #.CaptureFromCAM(0)
        self.window_names = {
          "first" : "first frame",
          "live" : "live",
          "difference" : "difference",
          };
        cv.NamedWindow(self.window_names["first"])
        cv.NamedWindow(self.window_names["difference"])
#        cv.NamedWindow(self.window_names["live"])
        cv.CreateTrackbar("thresh", self.window_names["difference"], self.match["threshold"], 50, self.update_threshold)
        cv.CreateTrackbar("hue", self.window_names["difference"], self.match["hue"], 255, self.update_hue)
        cv.SetMouseCallback(self.window_names["difference"], self.diff_mouse)
      #  cv.SetMouseCallback(self.window_names["first"], self.first_mouse)
#        cv.SetMouseCallback(self.window_names["live"], self.live_mouse)
        try:
          self.first_frame = cv.LoadImageM(self.first_frame_name) #, cv.CV_LOAD_IMAGE_GRAYSCALE)
        except IOError:
          print "no first frame found, taking new pic"
          self.get_first_frame()

    def update_threshold(self,threshold):
      self.match["threshold"]=threshold
#      self.get_first_frame()

    def update_hue(self,hue):
      self.match["hue"]=hue
    
    def get_first_frame(self):
        #get first frame
        print "getting first frame"

        flag, im_array = self.capture.read()
        frame = cv.fromarray(im_array)
        frame_size = cv.GetSize(frame)
        first_frame = cv.CreateImage(frame_size, cv.IPL_DEPTH_8U, 3)
        #convert colour space, src, dst
        cv.CvtColor(frame, first_frame, cv.CV_BGR2HSV)
#        cv.Smooth(first_frame, first_frame, cv.CV_GAUSSIAN, 3, 0)


        self.first_frame = first_frame
        #save it
        cv.SaveImage(self.first_frame_name, first_frame)

    def first_mouse(self,event, x, y, flags,user_data):
      if event == cv.CV_EVENT_LBUTTONDOWN:
        s = cv.Get2D(self.first_frame,y,x) #colour of circle
        self.match["hue"] = s[0]

        #print "B: %f G: %f R: %f\n" % (s[0],s[1],s[2])
        
    def diff_mouse(self,event, x, y, flags,user_data):
      if event == cv.CV_EVENT_RBUTTONDOWN:
        s = cv.Get2D(self.hsv_frame,y,x) #colour of circle
        self.match["hue"] = s[0]
        cv.SetTrackbarPos("hue", self.window_names["difference"], self.match["hue"])
      if event == cv.CV_EVENT_LBUTTONDOWN:
        self.match["top_corner"] = (x,y)
      if event == cv.CV_EVENT_LBUTTONUP:
        #check area is big enough
        if x > self.match["top_corner"][0] and y > self.match["top_corner"][1]:
          self.matching = True;
          self.match["dots"] = []
          self.match["bottom_corner"] = (x,y)

          match_width = abs(self.match["top_corner"][0] - self.match["bottom_corner"][0])
          match_height = abs(self.match["top_corner"][1] - self.match["bottom_corner"][1])
          print "matching to %d %d" % (match_width,match_height)

          #we have 3 dots and 2 spaces = 5
          self.match["dot_width"] = int(match_width / 5)
          self.match["dot_height"]= match_height

          first_dot = ( self.match["top_corner"][0], self.match["top_corner"][1] )
          for dot_num in range(3):
            dot = (first_dot[0]+dot_num*2*self.match["dot_width"],first_dot[1])
            self.match["dots"].append(dot)
          print self.match
          output = open(self.statefile, 'wb')
          # Pickle dictionary using protocol 0.
          pickle.dump(self.match, output)
          output.close()

    def run(self):
          #frame = cv.QueryFrame(self.capture)
          flag, im_array = self.capture.read()
          frame = cv.fromarray(im_array)
          if frame == None:
            print "no frame"
            return
          hsv_frame = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 3)
          cv.CvtColor(frame, hsv_frame, cv.CV_BGR2HSV)
          #cv.Threshold(grey_frame, grey_frame, self.threshold, 255, cv.CV_THRESH_BINARY)
          cv.Smooth(hsv_frame, hsv_frame, cv.CV_GAUSSIAN, 3, 0)
          self.hsv_frame = hsv_frame
          
         # difference = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 3)
         # cv.AbsDiff(hsv_frame, self.first_frame, difference)
         # self.difference = difference

          if self.matching:
            dot_num = 0
            dot_value=[]
            temp = cv.CloneImage(hsv_frame)
            for dot in self.match["dots"]:
              src_region = cv.GetSubRect(temp, (dot[0], dot[1], self.match["dot_width"], self.match["dot_height"]) )
              dot_value.append(cv.Avg(src_region)[0])
              cv.Rectangle(hsv_frame, dot,(dot[0]+self.match["dot_width"],dot[1]+self.match["dot_height"]), cv.CV_RGB(255, 0, 255), 2, 7)
              #print "dot %d avg %3.1f" % (dot_num, cv.Avg(src_region)[0])
              """
              for point in points:
                if abs(point[0]-dot[0]) < self.match_dist and abs(point[1]-dot[1]) < self.match_dist:
                  print "match on dot %d" % dot_num
              """
              #print "%3.0f" % ( dot_value[dot_num] ) #'1' if dot_value[dot_num] > 100 else '0' ),
              dot_num += 1
            
            self.dot_match = []
            match_str = ""
            for dot in dot_value:
                dot_match =  True if abs(dot-self.match["hue"]) < self.match["threshold"] else False
                self.dot_match.append(dot_match)
                match_str += "True  " if dot_match else "False "

            if args.single:
              print match_str
          #show images
            cv.PutText(hsv_frame,"%d" % self.match["hue"],(10,20),self.font, (255,255,255))
            cv.PutText(hsv_frame,"%s" % match_str,(10,40),self.font, (255,255,255))
            cv.PutText(hsv_frame,"%d %d %d" % (dot_value[0],dot_value[1],dot_value[2]),(10,60),self.font, (255,255,255))
#          cv.ShowImage(self.window_names["first"], self.first_frame)
#          cv.ShowImage(self.window_names["live"], frame)
          cv.ShowImage(self.window_names["difference"], hsv_frame)

          c = cv.WaitKey(10)

    def finish_cv(self):
      cv.DestroyAllWindows()
      self.capture.release()




if __name__=="__main__":
  argparser = argparse.ArgumentParser()

  group = argparser.add_mutually_exclusive_group(required=True)
  group.add_argument('--live',
      action='store_const', const=True, dest='live', default=False,
      help="run the live video")
  group.add_argument('--single',
      action='store_const', const=True, dest='single', default=False,
      help="take one shot")
      
  args = argparser.parse_args()

  t = Target()
  if args.live:
    while(True):
      t.run()

  if args.single:
    t.run()

  t.finish_cv()

