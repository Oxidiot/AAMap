import tkinter as tk
from tkinter import *
import sys
import queue
import threading
import time
import win32clipboard
from map import Map

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

class Window:
    def build_window(self):

        self.root = tk.Tk()
        self.root.config(bg="#fee5b5")
        self.root.title("AA Map")
        self.root.geometry("600x400")
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

        self.draw_plot()

        figure = plt.gcf()
        canvas = FigureCanvasTkAgg(figure = figure, master = self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

        reset_button = Button(master=self.root, command = lambda: self.restart(self.world_map), text= "reset")
        reset_button.place(x=20,y=20, width=40, height=20)

        # plt.scatter(25, 25, s=30)

        # self.graph = Figure(figsize = (100, 100), dpi = 10)
        # # self.plot = self.graph.add_subplot(111)
        # # self.plot.plot([10], 10)
        # self.canvas = FigureCanvasTkAgg(self.graph, master=self.root)
        # self.canvas.draw()
        # self.canvas.get_tk_widget().pack()
        # plt.scatter(50, 50, s = 3000)
        # self.canvas.draw()

    def draw_plot(self):

        plt.axis("equal")
        plt.grid(visible = True, axis = "both", color = "#b2b2b2", snap = True, zorder = 1)
        plt.xticks(ticks = [i*1024 for i in range(-40, 40)])
        plt.yticks(ticks = [i*1024 for i in range(-40, 40)])

        plt.scatter(2500, 2500, s=0)
        plt.scatter(-2500, -2500, s=0)

        plt.draw()

    def restart(self, map):
        pass
        map.clear_array()
        plt.clf()
        self.draw_plot()
        # self.start()


    def update_data_loop(self, interval:float, queue:queue, map):
        while True:
            time.sleep(interval)
            while not queue.empty():
                # map.add_position(queue.get_nowait())
                try:
                    map.add_position(queue.get_nowait())
                except queue.Empty:
                    break

            print (map.get_coord_array())

            try:
                print(map.get_curr_coords())
                # plt.scatter(map.get_curr_x(), map.get_curr_z(), s=30)

                if map.get_curr_x() > map.zenith:
                    map.zenith = map.get_curr_x()
                if map.get_curr_z() > map.zenith:
                    map.zenith = map.get_curr_z()

                plt.arrow(map.get_last_x(), map.get_last_z(), map.get_dx(), map.get_dz(), color = map.get_color(), zorder = 2)
                plt.scatter(map.zenith, map.zenith, s=0)
                plt.scatter(-(map.zenith), -(map.zenith), s=0)
                plt.draw()

            except IndexError:
                pass

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
            if clipboard_current[:8] == "/execute" and clipboard_current[26:29] != "end":
                
                
                
                clipboard_last = clipboard_current
                callback(clipboard_current)
                print(clipboard_current)

                

# /execute in minecraft:overworld run tp @s 453.30 74.00 829.30 420.94 -31.15   
# ^ example fc3