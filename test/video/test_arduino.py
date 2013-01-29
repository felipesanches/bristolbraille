import os
import feed
import mock

def test_arduino():
  if not os.path.exists("/dev/ttyUSB0"):
    assert False

def test_feed():
  with mock.patch('sys.argv'):
    feed.args = feed.get_args()
    feed.serial_port = feed.setup_serial()

def test_move_motor(codes=['f10','f-10']):
  response = feed.send_robot_commands(codes)
  if not response.splitlines()[0] == 'ok':
    assert False

