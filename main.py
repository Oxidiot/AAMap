import queue
import threading
import win32clipboard
import time
from map import Map

def monitor_clipboard(interval:float, callback:queue):
    clipboard_last = ""
    while True:
        time.sleep(interval)
        win32clipboard.OpenClipboard()
        clipboard_current = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        if clipboard_current == clipboard_last: 
            continue
        if clipboard_current[:8] == "/execute":
            clipboard_last = clipboard_current
            callback(clipboard_current)
            # print(clipboardCurrent)

def main():
    f3c_queue = queue.Queue()
    clipboard_reader = threading.Thread(target = monitor_clipboard, args = (1, f3c_queue.put), daemon=True)
    clipboard_reader.start()
    world_map = Map()
    while True:
        time.sleep(1)
        while not f3c_queue.empty():
            try:
                world_map.add_position(f3c_queue.get_nowait())
            except queue.Empty:
                break
        print (world_map.coord_array)

if __name__ == "__main__":
    main()


# /execute in minecraft:overworld run tp @s 453.30 74.00 829.30 420.94 -31.15   
# ^ example fc3