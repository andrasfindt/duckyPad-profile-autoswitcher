import json
import socket
import urllib.request

dpp_fw_url = 'https://api.github.com/repos/dekuNukem/duckyPad-Pro/contents/firmware?ref=master'
dp20_fw_url = 'https://api.github.com/repos/dekuNukem/duckyPad/contents/firmware?ref=master'
pc_app_release_url = "https://api.github.com/repos/dekuNukem/duckyPad-profile-autoswitcher/releases/latest"

def is_internet_available():
    try:
        socket.create_connection(("www.google.com", 80), timeout=1)
        return True
    except OSError:
        pass
    return False

def versiontuple(v):
    return tuple(map(int, (v.strip('v').split("."))))

"""
0 no update
1 has update
2 unknown
"""
def get_pc_app_update_status(this_version):
	if is_internet_available() is False:
		return 2
	try:
		result_dict = json.loads(urllib.request.urlopen(pc_app_release_url).read())
		this_version = versiontuple(this_version)
		remote_version = versiontuple(result_dict['tag_name'])
		return int(remote_version > this_version)
	except Exception as e:
		print('get_pc_app_update_status:', e)
		return 2
"""
0 no update
1 has update
2 unknown
"""
def get_firmware_update_status_dpp(current_version):
	try:
		file_list = json.loads(urllib.request.urlopen(dpp_fw_url).read())
		dfu_list = [x['name'] for x in file_list if 'name' in x and 'type' in x and x['type'] == 'file']
		dfu_list = [d.replace('DPP_FW_', '').replace('.bin', '').split('_')[0] for d in dfu_list if d.startswith('DPP_FW_') and d.endswith('.bin')]
		dfu_list.sort(key=lambda s: list(map(int, s.split('.'))))
		this_version = versiontuple(current_version)
		remote_version = versiontuple(dfu_list[-1])
		print('this:', this_version, '\nremote:', remote_version)
		return int(remote_version > this_version)
	except Exception as e:
		print('get_firmware_update_status:', e)
		return 2


def get_firmware_update_status_dp20(current_version):
	try:
		file_list = json.loads(urllib.request.urlopen(dp20_fw_url).read())
		dfu_list = [x['name'] for x in file_list if 'name' in x and 'type' in x and x['type'] == 'file']
		dfu_list = [d.replace('duckypad_v', '').replace('.dfu', '') for d in dfu_list if d.startswith('duckypad_v') and d.endswith('.dfu')]
		dfu_list.sort(key=lambda s: list(map(int, s.split('.'))))
		this_version = versiontuple(current_version)
		remote_version = versiontuple(dfu_list[-1])
		# print('this:', this_version, '\nremote:', remote_version)
		return int(remote_version > this_version)
	except Exception as e:
		print('get_firmware_update_status:', e)
		return 2

def get_firmware_update_status(current_version, is_dpp):
	print('is_dpp', is_dpp)
	if is_dpp:
		return get_firmware_update_status_dpp(current_version)
	return get_firmware_update_status_dp20(current_version)
