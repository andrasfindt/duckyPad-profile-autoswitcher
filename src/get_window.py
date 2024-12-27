import time
import platform

this_os = platform.system()

if this_os == 'Windows':
    import ctypes
    import ctwin32
    import ctwin32.ntdll
    import ctwin32.user
    import pygetwindow as gw
elif this_os == 'Darwin':
    from AppKit import NSWorkspace
    import Quartz
elif this_os == 'Linux':
    from ewmh import EWMH
    import psutil
    import Xlib
    NET_WM_NAME = Xlib.display.Display().intern_atom('_NET_WM_NAME')

def get_active_window():
    if this_os == 'Windows':
        return win_get_active_window()
    elif this_os == 'Darwin':
        return darwin_get_active_window()
    elif this_os == 'Linux':
        return linux_get_active_window()
    raise f'Platform {this_os} not supported'

def get_list_of_all_windows():
    if this_os == 'Windows':
        return win_get_list_of_all_windows()
    elif this_os == 'Darwin':
        return darwin_get_list_of_all_windows()
    elif this_os == 'Linux':
        return linux_get_list_of_all_windows()
    raise f'Platform {this_os} not supported'

def linux_get_list_of_all_windows():
    ret = set()
    ewmh = EWMH()
    for window in ewmh.getClientList():
        try:
            win_pid = ewmh.getWmPid(window)
        except TypeError:
            win_pid = False
        if win_pid:
            app = psutil.Process(win_pid).name()
        else:
            app = 'Unknown'
        wm_name = window.get_wm_name()
        if not wm_name:
            wm_name = window.get_full_property(NET_WM_NAME, 0).value
        if not wm_name:
            wm_name = f'class:{window.get_wm_class()[0]}'
        if isinstance(wm_name, bytes):
            wm_name = wm_name.decode('utf-8')
        ret.add((app, wm_name))
    return ret

def linux_get_active_window():
    ret = set()
    ewmh = EWMH()
    active_window = ewmh.getActiveWindow()
    if not active_window:
        return '', ''
    try:
        win_pid = ewmh.getWmPid(active_window)
    except TypeError:
        win_pid = False
    except Xlib.error.XResourceError:
        return '', ''
    wm_name = active_window.get_wm_name()
    if not wm_name:
        wm_name = active_window.get_full_property(NET_WM_NAME, 0).value
    if not wm_name:
        wm_name = f'class:{active_window.get_wm_class()[0]}'
    if isinstance(wm_name, bytes):
        wm_name = wm_name.decode('utf-8')
    if win_pid:
        active_app = psutil.Process(win_pid).name()
    else:
        return '', wm_name
    return (active_app, wm_name)

def darwin_get_active_window():
    windows = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListExcludeDesktopElements | Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
    for window in windows:
        if window[Quartz.kCGWindowLayer] == 0:
            return window[Quartz.kCGWindowOwnerName], window.get(Quartz.kCGWindowName, 'unknown')
    return '', ''

def darwin_get_list_of_all_windows():
    apps = []
    windows = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListExcludeDesktopElements | Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)

    for window in windows:
        apps.append((window[Quartz.kCGWindowOwnerName],
                    window.get(Quartz.kCGWindowName, 'unknown')))
    apps = list(set(apps))
    apps = sorted(apps, key=lambda x: x[0])
    return apps

def win_get_app_name(hwnd):
    """Get application name given hwnd."""
    try:
        _, pid = ctwin32.user.GetWindowThreadProcessId(hwnd)
        spii = ctwin32.ntdll.SYSTEM_PROCESS_ID_INFORMATION()
        buffer = ctypes.create_unicode_buffer(0x1000)
        spii.ProcessId = pid
        spii.ImageName.MaximumLength = len(buffer)
        spii.ImageName.Buffer = ctypes.addressof(buffer)
        ctwin32.ntdll.NtQuerySystemInformation(ctwin32.SystemProcessIdInformation, ctypes.byref(spii), ctypes.sizeof(spii), None)
        name = str(spii.ImageName)
        dot = name.rfind('.')
        slash = name.rfind('\\')
        exe = name[slash+1:dot]
    except:
        return 'unknown'
    else:
        return exe

def win_get_list_of_all_windows():
    ret = set()
    for item in gw.getAllWindows():
        ret.add((win_get_app_name(item._hWnd), item.title))
    ret = sorted(list(ret), key=lambda x: x[0])
    return ret

def win_get_active_window():
    active_window = gw.getActiveWindow()
    if active_window is None:
        return '', ''
    return (win_get_app_name(active_window._hWnd), active_window.title)

if __name__ == "__main__":

    # list of tuples of str: (app_name, window_title)
    all_win = get_list_of_all_windows()
    print("\n----- All Windows -----\n")
    for item in all_win:
        print(item)


    print("\n----- Current Window -----\n")
    current_win = get_active_window()
    print(current_win)