#!/usr/bin/env python3

"""
Sourcecode Map
-some text
-modules
-global vars
-global objects
-core function
-main function
-argument function
-other functions
-run

Prefix description
| Prefix | Meaning | Description |
| a_ | argument | e.g.: argument of function |
| c_ | class | class |
| e_ | external file | e.g.: local file, network file |
| f_ | function | function |
| g_ | global var | global variable |
| m_ | master | master object |
| o_ | object | object with attributes |
| s_ | sequence | e.g.: array, list, tuple or dictionary |
| t_ | task | multitasking object |
| v_ | local variable | local var, also name object  |
| _ | local variable (hidden) | local var, but do not touch |
| w_ | window | window object |
"""

def f_author():
    print(
        """
    This program is written 2023 by Sonic2k under GNU GPL v2.0.
    You can buy a Coffee for Sonic2k at ko-fi.com/sonic2k"""
    )
    f_set_exit()


def f_info():
    print(
        """
    A Timer for the Desktop.
    It has a GUI and generates a sound, if expired."""
    )
    f_set_exit()


def f_help():
    f_author()
    print("\n" + g_app_name)
    f_info()
    print(
        """
    The idea of the Timer was for cooking at first, while working on the PC.
    But after some testing I was surprised, how much more use cases it has.
    Feel free to find out for yourself.
    
    The Usage is quite easy and straight forward. It also serves the goal of intuitive handling.
    First you adjust the Timer time with the slider. Then you press Start. That's it :)
    
    With Start, Stop and Reset, you can start, stop and reset the Timer.
    The Volume slider has no function yet. I found out, it is not necessary.
    It will become removed or used for another function.

    Pro tip:
    You can change some extra settings by editing the config file."""
    )
    #  f_options()
    f_set_exit()


def f_options():
    print(
        """
    Options:
    --author zeigt den author
    --help oder -h zeigt die hilfe
    --about zeigt die lizenz
    --options zeigt die optionen"""
    )
    f_set_exit()


def f_about():
    f_author()
    print(
        """
    The licenses for most software are designed to take away your
    freedom to share and change it. By contrast, the GNU General Public
    License is intended to guarantee your freedom to share and change free
    software--to make sure the software is free for all its users.
                                     - from the Preamble of GNU GPLv2

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; version 2
    of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>."""
    )
    f_set_exit()


# Modules
import tkinter as tk
import customtkinter as ctk
import time
import pysine
import threading
import configparser
import sys
import os
import io


# Global Vars
g_app_name = "Desk-Timer"
g_app_version = "1.11 beta"
g_default_min = 10
g_default_vol = 60
g_update_min = g_default_min
g_update_vol = g_default_vol
g_default_sound = 1
g_default_repeat = 1
g_timer_cache = 0
g_timer_stop = False
g_max_lps = 60  # set max loops per second
g_debug = False  # set True for debug
g_exit = False  # Trigger Exit


# Global Objects
global m_app  # Master Object
global o_slider_time
global o_slider_vol
global o_label_set_time
global o_button_start
global o_button_reset


# Global Threads
global t_main
global t_timer


#################
# Core Function #
#################
def f_core():
    # Call Threads
    global t_main
    global t_timer

    # Load Configuation
    f_config_load()

    # Handle Argumets
    f_args()

    # Exit when Exit is called
    if g_exit:
        f_exit()

    # Open Main
    t_main = threading.Thread(target=f_main)
    t_main.start()

    # Exit when Exit is called
    if g_exit:
        f_exit()


#################
# Main Function #
#################
def f_main():
    # import Global Objects
    global m_app
    global o_slider_time
    global o_slider_vol
    global o_label_set_time
    global o_button_start
    global o_button_reset

    # Set max lps
    time.sleep(1./g_max_lps)

    # Main Program
    ctk.set_appearance_mode("light")  # Modes: system (default), light, dark
    ctk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

    # Master Object
    m_app = ctk.CTk()
    m_app.geometry("402x490")
    m_app.title(f"S2k {g_app_name} {g_app_version}")

    # Menu
    m_menu = tk.Menu(m_app)
    m_app.configure(menu=m_menu)
    s_menu_fontsize = ("", 18)

    o_menu = tk.Menu(m_menu, tearoff=0)
    m_menu.add_cascade(label="Menu", menu=o_menu, font=s_menu_fontsize)
    o_menu.add_command(label="Save Settings", command=f_config_save, font=s_menu_fontsize)
    o_menu.add_command(label="Info", command=f_window_info, font=s_menu_fontsize)
    o_menu.add_command(label="Help", command=f_window_help, font=s_menu_fontsize)
    o_menu.add_command(label="About", command=f_window_about, font=s_menu_fontsize)
    o_menu.add_separator()
    o_menu.add_command(label="Exit", command=f_on_closing, font=s_menu_fontsize)

    # Label Top
    o_label_top = ctk.CTkLabel(master=m_app, width=120, height=25, text=g_app_name, font=("Arial", 24, "bold"))
    o_label_top.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    # Label Time
    o_label_time = ctk.CTkLabel(master=m_app, text="Minutes")
    o_label_time.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

    # Slider Time
    o_slider_time = ctk.CTkSlider(master=m_app, from_=0, to=120, command=f_slider_time_event, number_of_steps=120, width=360)
    o_slider_time.place(relx=0.5, rely=0.2, anchor=tk.CENTER)
    o_slider_time.set(g_default_min)

    # Label Set Time
    o_label_set_time = ctk.CTkLabel(master=m_app, width=120, height=25, text=f"{int(o_slider_time.get())}:00", fg_color=("gray75", "white"), corner_radius=8)
    o_label_set_time.place(relx=0.5, rely=0.34, anchor=tk.CENTER)

    # Label Vol
    o_label_vol = ctk.CTkLabel(master=m_app, text="Volume")
    o_label_vol.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Slider Vol
    o_slider_vol = ctk.CTkSlider(master=m_app, from_=0, to=100, command=f_slider_vol_event, number_of_steps=100)
    o_slider_vol.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
    o_slider_vol.set(g_default_vol)

    # Button Start
    o_button_start = ctk.CTkButton(master=m_app, text="Start", command=f_button_start)
    o_button_start.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    # Button Stop
    o_button_stop = ctk.CTkButton(master=m_app, text="Stop", command=f_button_stop)
    o_button_stop.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    # Button Reset
    o_button_reset = ctk.CTkButton(master=m_app, text="Reset", command=f_button_reset)
    o_button_reset.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    m_app.protocol("WM_DELETE_WINDOW", f_on_closing)

    m_app.mainloop()
    f_set_exit()

def f_window_help():
    w_show_help = ctk.CTkToplevel()
    w_show_help.geometry("640x480")
    w_show_help.configure(fg_color="gray")
    w_show_help.title(f"{g_app_name} Help")
    w_show_help.attributes('-topmost', True)

    _buffer = io.StringIO()
    sys.stdout = _buffer
    f_help()
    v_text_output = _buffer.getvalue()
    sys.stdout = sys.__stdout__

    v_help_text = str(v_text_output)
    o_show_help_label = ctk.CTkLabel(w_show_help, fg_color="lightgray", padx=20, pady=20, corner_radius=8, anchor=tk.CENTER, text=v_help_text)
    o_show_help_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def f_window_about():
    w_show_about = ctk.CTkToplevel()
    w_show_about.geometry("640x480")
    w_show_about.configure(fg_color="gray")
    w_show_about.title(f"{g_app_name} Help")
    w_show_about.attributes('-topmost', True)

    _buffer = io.StringIO()
    sys.stdout = _buffer
    f_about()
    v_text_output = _buffer.getvalue()
    sys.stdout = sys.__stdout__

    v_about_text = str(v_text_output)
    o_show_about_label = ctk.CTkLabel(w_show_about, fg_color="lightgray", padx=20, pady=20, corner_radius=8, anchor=tk.CENTER, text=v_about_text)
    o_show_about_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


def f_window_info():
    w_show_info = ctk.CTkToplevel()
    w_show_info.geometry("640x180")
    w_show_info.configure(fg_color="gray")
    w_show_info.title(f"{g_app_name} Help")
    w_show_info.attributes('-topmost', True)

    _buffer = io.StringIO()
    sys.stdout = _buffer
    f_info()
    v_text_output = _buffer.getvalue()
    sys.stdout = sys.__stdout__

    v_info_text = str(v_text_output)
    o_show_info_label = ctk.CTkLabel(w_show_info, fg_color="lightgray", padx=20, pady=20, corner_radius=8, anchor=tk.CENTER, text=v_info_text)
    o_show_info_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


# Handle Arguments
def f_args():
    l_args = sys.argv
    global g_debug
    if g_debug:
        print(f"\nArgumets list: {l_args}")
    if len(l_args) == 1:
        return
    match l_args[1]:
        case "--help":
            f_help()
        case "--info":
            f_info()
        case "--about":
            f_about()
        case "--author":
            f_author()
        case "--options":
            f_options()
        case "--debug":
            g_debug = True
        case "-h":
            f_help()
        case _:
            return


###################
# Other Functions #
###################


def f_set_exit():
    global g_exit
    g_exit = True


def f_exit():
    print("")
    os._exit(0)


def f_button_start():
    if g_debug:
        print("Start button pressed")
    global t_timer
    global g_timer_stop

    g_timer_stop = False

    f_lock_gui_objects()

    # Initialize Timer
    t_timer = threading.Thread(target=f_timer, args=("start",))
    t_timer.start()


def f_button_stop():
    if g_debug:
        print("Stop button pressed")
    global g_timer_stop

    g_timer_stop = True


def f_button_reset():
    if g_debug:
        print("Reset button pressed")
    global g_timer_cache

    g_timer_cache = 0
    o_label_set_time.configure(text=f"{int(g_update_min)}:00")


def f_slider_time_event(a_value):
    global g_update_min
    global g_timer_cache

    if g_debug:
        print(f"Slider Time: {a_value}")
    o_label_set_time.configure(text=f"{int(a_value)}:00")
    g_update_min = a_value
    g_timer_cache = 0


def f_slider_vol_event(a_value):
    global g_update_vol

    if g_debug:
        print(f"Slider Volume: {a_value}")
    g_update_vol = a_value


def f_lock_gui_objects():
    # import Global Objects
    global o_slider_time
    global o_button_start
    global o_button_reset

    # Lock Gui Objects
    o_slider_time.configure(state="disabled")
    o_button_start.configure(state="disabled")
    o_button_reset.configure(state="disabled")


def f_unlock_gui_objects():
    # import Global Objects
    global o_slider_time
    global o_button_start
    global o_button_reset

    # Unlock Gui Objects
    o_slider_time.configure(state="normal")
    o_button_start.configure(state="normal")
    o_button_reset.configure(state="normal")


def f_timer(a_command):
    # Local Vars
    v_time = 0
    v_mins = 0
    v_secs = 0
    _count = 0

    # import Global Objects
    global o_label_set_time

    # import Global Vars
    global g_timer_cache

    # Start the Timer
    if a_command == "start":
        if g_debug:
            print("command is: Start")
        v_time = int(g_update_min * 60)
    if a_command == "start" and g_timer_cache != 0:
        v_time = g_timer_cache
    for _count in range(v_time, -1, -1):
        if g_debug:
            print(f"Seconds: {_count}")
        v_secs = _count % 60
        v_mins = int(_count / 60)
        if g_debug:
            print(f"{v_mins}:{v_secs:02}")
        o_label_set_time.configure(text=f"{v_mins}:{v_secs:02}")
        time.sleep(1)
        if g_timer_stop:
            g_timer_cache = _count
            break
    if g_debug:
        print("done")

    f_unlock_gui_objects()

    if _count == 0:
        f_playsound(g_default_sound, g_default_repeat)


def f_playsound(a_sound, a_repeat):
    for _count in range(a_repeat):
        if a_sound == 1:  # Pre Alarm Sound, original repeat 1x
            pysine.sine(frequency=1000.0, duration=0.200)
            pysine.sine(frequency=2000.0, duration=0.200)
            pysine.sine(frequency=4000.0, duration=0.200)
            pysine.sine(frequency=4500.0, duration=0.200)
            time.sleep(1./4)  # ~250ms

        if a_sound == 2:  # Alarm Sound, original repeat 30x
            pysine.sine(frequency=500.0, duration=0.200)
            pysine.sine(frequency=1000.0, duration=0.200)
            pysine.sine(frequency=1500.0, duration=0.200)
            pysine.sine(frequency=2000.0, duration=0.200)
            time.sleep(1./4)  # ~250ms

        if a_sound == 3:  # Timer Sound, original repeat 3x
            pysine.sine(frequency=1000.0, duration=0.100)
            pysine.sine(frequency=2000.0, duration=0.100)
            pysine.sine(frequency=4000.0, duration=0.100)
            pysine.sine(frequency=5000.0, duration=0.100)
            time.sleep(1./3)  # ~300ms

        if a_sound == 4:  # Single Beep, original repeat 1x
            pysine.sine(frequency=00.0, duration=0.300)
            pysine.sine(frequency=00.0, duration=0.300)
            pysine.sine(frequency=00.0, duration=0.200)
            pysine.sine(frequency=6000.0, duration=0.200)
            time.sleep(1./50)  # ~20ms


def f_config_save():
    o_config = configparser.ConfigParser()
    o_config["app_info"] = {
        "app_name" : g_app_name,
        "app_version" : g_app_version,
        "sounds_available" : 4,
    }
    o_config["user_settings"] = {
        "default_min" : g_update_min,
        "default_vol" : g_update_vol,
        "default_sound" : g_default_sound,
        "default_repeat" : g_default_repeat
    }

    with open("settings.cfg", "w") as e_settings:
        o_config.write(e_settings)

def f_config_load():
    global g_default_min
    global g_default_vol
    global g_update_min
    global g_update_vol
    global g_default_sound
    global g_default_repeat
    global g_debug
    v_debug = False

    o_config = configparser.ConfigParser()

    try:
        o_config.read("settings.cfg")
        o_config_data = o_config["user_settings"]
        g_default_min = float(o_config_data["default_min"])
        g_default_vol = float(o_config_data["default_vol"])
        g_update_min = g_default_min
        g_update_vol = g_default_vol
        g_default_sound = int(o_config_data["default_sound"])
        g_default_repeat = int(o_config_data["default_repeat"])
    except:  # do nothing and just skip, if anything with config fails
        return

    try:
        v_debug = int(o_config_data["debug"])  # hidden option
        if v_debug == 1:  # this is necessary because configparser
            g_debug = True  # returns "debug = False" always as True
    except:  # do nothing and just skip, if anything with debug flag fails
        return


def f_on_closing():
    if tk.messagebox.askokcancel("Quit", f"Close {g_app_name}?"):
        f_set_exit()
        f_core()


# Run
if __name__ == "__main__":
    f_core()
