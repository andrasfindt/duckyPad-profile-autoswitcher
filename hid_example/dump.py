"""
duckyPad HID example: HID read AND write

For more details, see:

https://github.com/dekuNukem/duckyPad-profile-autoswitcher/blob/master/HID_details.md

"""

import hid
import time

PC_TO_DUCKYPAD_HID_BUF_SIZE = 64
DUCKYPAD_TO_PC_HID_BUF_SIZE = 64

h = hid.device()

def millis():
	return time.time_ns() // 1000000;

pgm_start = millis()

duckypad_pid = 0xd11c
duckypad_pro_pid = 0xd11d
valid_pid_list = [duckypad_pro_pid, duckypad_pid]

def get_duckypad_path_uncached():
    path_dict = {}
    for device_dict in hid.enumerate():
        if device_dict['vendor_id'] == 0x0483 and device_dict['product_id'] in valid_pid_list:
            path_dict[device_dict['usage']] = device_dict['path']
    if len(path_dict) == 0:
        return None
    if 58 in path_dict:
        return path_dict[58]
    return list(path_dict.values())[0]

last_dp_path = None
def get_duckypad_path(start_fresh=False):
    global last_dp_path
    if start_fresh:
        last_dp_path = None
    if last_dp_path is None:
        last_dp_path = get_duckypad_path_uncached()
    return last_dp_path

# wait up to 0.5 seconds for response
def hid_read():
	read_start = time.time()
	while time.time() - read_start <= 1:
		result = h.read(DUCKYPAD_TO_PC_HID_BUF_SIZE)
		if len(result) > 0:
			return result
		time.sleep(0.01)
	return []

pc_to_duckypad_buf = [0] * PC_TO_DUCKYPAD_HID_BUF_SIZE
pc_to_duckypad_buf[0] = 5	# HID Usage ID, always 5
pc_to_duckypad_buf[1] = 0	# Sequence Number
pc_to_duckypad_buf[2] = 0	# Command type


duckypad_path = get_duckypad_path()
if duckypad_path is None:
	raise OSError('duckyPad Not Found!')
h.open_path(duckypad_path)
h.set_nonblocking(1)

for x in range(10):
	# print("\n\nSending to duckyPad:\n", pc_to_duckypad_buf)
	h.write(pc_to_duckypad_buf)
	duckypad_to_pc_buf = hid_read()
	# print("\nduckyPad response:\n", duckypad_to_pc_buf)
	print(x, millis() - pgm_start)

h.close()