from braille import Target
import os

t = None

def test_camera():
  if not os.path.exists("/dev/video0"):
    assert False


def test_create_module():
  global t
  t = Target()
  if not t:
    assert False

def test_capture_frame():
  global t
  t.run()

def test_capture_output(pattern=None):
  global t
  if not len(t.dot_match) == 3:
    assert False
  if pattern:
    if not pattern == t.dot_match:
      assert False

def test_finish():
  global t
  t.finish_cv()
