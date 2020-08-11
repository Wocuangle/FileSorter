import os
import sys
import tkinter.filedialog
import tkinter as tk
from PIL import ImageTk, Image
import math
import random
import os
from functools import partial

# supported file types
supported_types = ["png", "jpg", "gif", "jpeg"]
# full path to file
file_path = []
# name of file with extension
file_name = []
# absolute directory file is in
file_dir = []
# file's name without extension
file_name_noext = []
# file's extension
file_ext = []
# immediate directory names
dir_names = []

# gets all files in folder
# add break to not include subdirectories

root_path = ""
#root_path = '/home/sackowee/Pictures/'
#if root_path[-1] != os.path.sep:
#    root_path = root_path + os.path.sep
#    print("NOOO")


num = 0

def img_update():
    global file_path, file_name, file_dir, file_name_noext, file_ext, dir_names
    file_path = []
    file_name = []
    file_dir = []
    file_name_noext = []
    file_ext = []

    for (dirpath, dirnames, filenames) in os.walk( root_path ):
        file_path.extend(os.path.join(dirpath, filename) for filename in filenames)
        file_name.extend(os.path.join(filename) for filename in filenames)
        file_dir.extend(os.path.join(dirpath) for filename in filenames)

        dir_names = dirnames
        break

    dir_names.sort()

    # gets file name without extension and its extension into separate variables
    # if file has no extension, file_ext value is set to "NO_EXT"
    for item in file_name:
        if '.' in item:
            split_vals = item.rsplit('.', 1)
            file_name_noext.append(split_vals[0])
            file_ext.append(split_vals[1])
        else:
            file_name_noext.append(file_name)
            file_ext.append("NO_EXT")

def img_resizer(side_max):
    #gets image from path
    orig = Image.open(file_path[num])

    # gets width and height for resizing
    width, height = orig.size
    
    if width > side_max and width > height:
        ratio = height/width
        width = side_max
        height = math.floor(width * ratio)
    elif height > side_max and height > width:
        ratio = width/height
        height = side_max
        width = math.floor(height * ratio)
    elif width == height and width > side_max:
        width, height = side_max, side_max

    #creates image with new dimensions
    resized = orig.resize((width,height),Image.ANTIALIAS)

    # returns pil image
    return resized

def randimg():
    global num
    img_update()
    file_exists = False
    for i in file_ext:
        if i in supported_types:
            file_exists = True
            break
    if file_exists:
        while (True):
            num = random.randint(0, len(file_name) - 1)
            if file_ext[num] in supported_types:
                break

        resized = img_resizer(350)

        img = ImageTk.PhotoImage(resized)

        panel.configure(image=img)
        panel.image = img

        rename_ext.configure(text="." + file_ext[num])
        rename_ext.text = "." + file_ext[num]

        # clears the textbox
        rename_tbox.delete(0, tk.END)
        # places a default value in the textbox
        rename_tbox.insert(0, file_name_noext[num])
    else:
        info_text_change("No more compatible files to sort!", 1)

def rename():
    global file_name, file_path, file_name_noext
    new_name = rename_val.get() + "." + file_ext[num]
    try:
        os.rename(file_path[num], file_dir[num] + new_name)
        info_text_change("The file name was changed to: " + new_name, 0)
        
        file_name[num] = rename_val.get() + "." + file_ext[num]
        file_path[num] = file_dir[num] + file_name[num]
        file_name_noext[num] = rename_val.get()
    except Exception as e:
        info_text_change("File name change unsuccessful :(", 1)
        print(e)

def info_text_change(msg, type):
    if type == 0:
        info_text.configure(fg="green")
        info_text.fg = "green"
    if type == 1:
        info_text.configure(fg="red")
        info_text.fg = "red"
    info_text.configure(text=msg)
    info_text.text = msg

def info_text_clear():
    info_text.configure(text=" ")
    info_text.text = " "

def move_file(d_name):
    global file_path, file_name, file_dir, file_name_noext, file_ext
    try:
        os.rename(file_path[num], root_path + d_name + os.path.sep + file_name[num])
    except Exception as e:
        print(e)
    else:
        del file_path[num], file_name[num], file_dir[num], file_name_noext[num], file_ext[num]
        randimg()
    print(d_name + os.path.sep)

def make_dir():
    global dir_win
    new_dir = newdir_val.get()
    dir_win.destroy()
    try:
        path = root_path + new_dir
        os.mkdir(path)
    except OSError:
        info_text_change("Failed to create directory: " + new_dir, 1)
    else:
        info_text_change("Successfully created directory: " + new_dir, 0)
        img_update()
        dir_update()

def rand_butt_click():
    info_text_clear()
    randimg()

def make_dir_window():
    global newdir_val
    global dir_win
    global newdir_val

    newdir_val = tk.StringVar()

    dir_win = tk.Toplevel()
    dir_win.geometry("400x100")
    dir_win.title("Create New Directory")
    dir_win.resizable(width=False, height=False)

    margin = tk.Frame(dir_win, height=20)
    margin.pack()
    top_fr = tk.Frame(dir_win)
    top_fr.pack()
    bot_fr = tk.Frame(dir_win)
    bot_fr.pack()
    
    dir_label = tk.Label(top_fr, text="Give a new folder name: ")
    dir_label.pack(side="top")
    dir_textbox = tk.Entry(bot_fr, textvariable = newdir_val)
    dir_textbox.pack(side='left')
    dir_button = tk.Button(bot_fr, text="Create", command=make_dir)
    dir_button.pack(side='left')

def dir_update():
    # creates a button for all directories in the root folder
    global dir_buttons, dir_frame, dir_header
    i = 0
    while i < len(dir_buttons):
        dir_buttons[i].destroy()
        del dir_buttons[i]
    
    i = 0
    for dirs in dir_names:
        if i%3 == 0:
            dir_buttons.append(tk.Button(dir_frame_col1, text=dir_names[i], width=14, command=partial(move_file, dir_names[i])))
        elif i%3 == 1:
            dir_buttons.append(tk.Button(dir_frame_col2, text=dir_names[i], width=14, command=partial(move_file, dir_names[i])))
        elif i%3 == 2:
            dir_buttons.append(tk.Button(dir_frame_col3, text=dir_names[i], width=14, command=partial(move_file, dir_names[i])))
        
        dir_buttons[i].pack(pady = 1, padx = 1)
        i += 1

# brings up the directory selection dialog box and takes care of handling
def choose_directory():
    global root_path
    dir_select.attributes('-topmost', False)
    chosen_dir = tk.filedialog.askdirectory()
    # if nothing selected, program exits
    if not chosen_dir:
        sys.exit()
    # if a directory was chosen, the main window is created
    else:
        root_path = chosen_dir + os.path.sep
        dir_select.destroy()
        main_window()

# first window that pops up
# tells the user to select a directory to use the program
def dir_select_window():
    global dir_select
    dir_select = tk.Toplevel()
    dir_select.attributes('-topmost', True)
    dir_select.focus_force()
    dir_select.geometry("400x100")
    dir_select.title("Directory Selection")
    dir_select.resizable(width=False, height=False)

    margin = tk.Frame(dir_select, height=20)
    margin.pack()
    top_fr = tk.Frame(dir_select)
    top_fr.pack()
    bot_fr = tk.Frame(dir_select)
    bot_fr.pack()
    
    dir_label = tk.Label(top_fr, text="Pick a directory to sort through: ")
    dir_label.pack(side="top")
    dir_button = tk.Button(bot_fr, text="Select directory...", command=choose_directory)
    dir_button.pack(side='left')

def main_window():
    global root_path, window, top_frame, bottom_frame, info_frame, img_frame, rename_frame, button_frame, dir_margin, dir_header, dir_frame, create_folder_frame, dir_frame_col1, dir_frame_col2, dir_frame_col3, info_text, panel, rename_butt, rand_butt, rename_val, rename_tbox, rename_ext, newdir_val, dir_buttons, create_folder_butt, resized, img, dir_win

    # updates the lists that allows the program to work
    img_update()

    # program's focus switched to the main window after the user selects a directory
    window.focus_force()

    # top and bottom frames for window organization
    top_frame = tk.Frame(window)
    top_frame.pack()
    bottom_frame = tk.Frame(window)
    bottom_frame.pack(side='bottom')

    # displays notifications on the top of the window to notify the user if an operation succeeded or failed (errors)
    info_frame = tk.Frame(top_frame)
    info_frame.pack(pady=7)
    # displays images
    img_frame = tk.Frame(top_frame, borderwidth=2, relief='solid')
    img_frame.pack(pady=7)

    # frame for textbox for renaming a file
    rename_frame = tk.Frame(bottom_frame)
    rename_frame.pack(pady=4)
    # buttons for file-related operations other than moving files to a different folder
    button_frame = tk.Frame(bottom_frame)
    button_frame.pack(pady=4)
    # separator
    dir_margin = tk.Frame(bottom_frame, height=15)
    dir_margin.pack()
    # directory section's header
    dir_header = tk.Label(bottom_frame, text="Move to folder:")
    dir_header.pack()
    # container for directory's button columns
    dir_frame = tk.Frame(bottom_frame)
    dir_frame.pack(pady=7)
    # container for new folder/directory button
    create_folder_frame = tk.Frame(bottom_frame)
    create_folder_frame.pack(pady=7)

    # columns where directory buttons will be placed
    dir_frame_col1 = tk.Frame(dir_frame)
    dir_frame_col2 = tk.Frame(dir_frame)
    dir_frame_col3 = tk.Frame(dir_frame)
    dir_frame_col1.pack(side="left")
    dir_frame_col2.pack(side="left")
    dir_frame_col3.pack(side="left")

    # sets the notification text's default height, lets the text wrap, and sets the text to blank
    info_text = tk.Label(info_frame, text=" ", wraplength=440, height=2)
    info_text.pack()

    # label where the image is displayed
    panel = tk.Label(img_frame, height = 350, width = 350)
    panel.pack(side='bottom', fill="both", expand="yes")

    # button for rename operation
    rename_butt = tk.Button(button_frame, text="Rename", command=rename)
    rename_butt.pack(side= 'left')
    # button for random file operation
    rand_butt = tk.Button(button_frame, text="Random file", command=rand_butt_click)
    rand_butt.pack(side= 'left')

    # textbox for renaming the current file
    rename_val = tk.StringVar()
    rename_tbox = tk.Entry(rename_frame, width = 30, textvariable = rename_val)
    rename_tbox.pack(side = 'left', padx=3)
    # displays the file's extension beside the textbox
    rename_ext = tk.Label(rename_frame, text="." + file_ext[num])
    rename_ext.pack(side = 'left')

    dir_buttons = []
    i = 0

    # creates buttons for all directories in the root folder
    dir_update()

    newdir_val = tk.StringVar()
    create_folder_butt = tk.Button(create_folder_frame, text="Create new folder...", command=make_dir_window)
    create_folder_butt.pack(side='bottom')

    # clears the textbox
    rename_tbox.delete(0, tk.END)
    # places a default value in the textbox
    rename_tbox.insert(0, file_name_noext[num])

    resized = ''
    img = ''
    randimg()

    dir_win = 0

    img_update()

# used to keep the parts of the main window global so the functions can access them
window = top_frame = bottom_frame = info_frame = img_frame = rename_frame = button_frame = dir_margin = dir_header = dir_frame = create_folder_frame = dir_frame_col1 = dir_frame_col2 = dir_frame_col3 = info_text = panel = rename_butt = rand_butt = rename_val = rename_tbox = rename_ext = newdir_val = create_folder_butt = resized = img = dir_win = 0

#creates tkinter window with options
window = tk.Tk()
window.title("Picture!")
window.geometry("450x850")
window.resizable(width=False, height=True)
#window.configure(background='grey')

dir_buttons = []

dir_select = ""
dir_select_window()

window.mainloop()