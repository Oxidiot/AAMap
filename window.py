import tkinter as tk
from tkinter import *
import sys
import queue
import threading
import time
import win32clipboard
from map import Map

class Window:
    def build_window(self):
        
        self.root = tk.Tk()
        self.root.config(bg="#fee5b5")
        self.root.title("AA Map")
        self.root.geometry("300x300")
        self.root.protocol("WM_DELETE_WINDOW", lambda: [print('Exiting from window close'), sys.exit(0)])
        self.start()

        self.root.mainloop()

    def start(self):
        self.f3c_queue = queue.Queue()
        self.clipboard_reader = threading.Thread(target = self.monitor_clipboard, args = (0.25, self.f3c_queue.put), daemon=True)
        self.clipboard_reader.start()
        self.world_map = Map()

        self.updater_thread = threading.Thread(target = self.update_data_loop, args = (0.25, self.f3c_queue, self.world_map), daemon=True)
        self.updater_thread.start()
    
    def update_data_loop(self, interval:float, queue:queue, map):
        while True:
            time.sleep(interval)
            while not queue.empty():
                try:
                    map.add_position(queue.get_nowait())
                except queue.Empty:
                    break
            print (map.coord_array)

    def monitor_clipboard(self, interval:float, callback):
        # return
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
                print(clipboard_current)