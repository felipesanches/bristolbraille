import nose
import test_capture
import test_arduino
import pdb
import time

#start with all blacks up
sequences = [ #black is true, white is false
  [False,False,False],
  [True,False,False],
  [True,True,False],
  [True,True,True],
  [False,True,True],
  [True,False,True],
  [False,True,False],
  [False,False,True],
  ]

def test_setup():
  test_arduino.test_feed()
  test_capture.test_create_module()

#@nose.with_setup(setup)
def test_move_and_capture():
  for sequence in sequences:
    yield check_sequence, sequence

def check_sequence(sequence):
  test_capture.test_capture_frame()
  test_arduino.test_move_motor(['f13'])
  time.sleep(5)
  test_capture.test_capture_output(sequence)
