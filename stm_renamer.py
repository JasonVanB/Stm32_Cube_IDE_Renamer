from asyncio.windows_events import NULL
import dearpygui.dearpygui as dpg
import os
import time

pop_up_yes = NULL

dpg.create_context()

# this is ugly code but since this is a simple gui / program I do not care about preformance / modularity
def get_folder(sender, app_data):
    new_name = dpg.get_value("new_name_input")
    folder_path = app_data["file_path_name"]
    old_name = folder_path.split("\\")[-1]

    # if there is one or more ioc files, error out may want to add additional functionality for this
    # to allow renaming mutiple ioc files at once if needed
    file_list = []
    for file in os.listdir(folder_path):
        if file.endswith(".ioc"):
            file_list.append(file)

    if len(file_list) == 1:

        with open(folder_path + "\\" + file_list[0], "r") as f:
            filedata = f.read()

        filedata = filedata.replace(old_name, new_name)

        with open(folder_path + "\\" + file_list[0], "w") as f:
            f.write(filedata)

        os.rename( folder_path + "\\" + file_list[0], folder_path + "\\" + file_list[0].replace(old_name, new_name))

        new_folder_path = folder_path.replace(old_name, new_name)
        os.rename(folder_path, new_folder_path)
    elif len(file_list) == 0:
        show_pop_up_window("No ioc file found in folder", False)
    else:
        show_pop_up_window("Multiple ioc files found in folder", False)

# this is a ugly implementation of a generic pop up window
# Not the biggest fan of how I handled the callback function as it requires a global variable
# and busy waiting, but it works for this simple gui if I expand this I will need to rework this 
def show_pop_up_window(display_text, bool_show):
    pop_up_yes = NULL
    dpg.configure_item("pop_up_window", show=True)

    if bool_show:
        dpg.configure_item("pop_up_window_ok", show=False)
        dpg.configure_item("pop_up_window_yes_no", show=True)
        while pop_up_yes == NULL:
            time.sleep(.1)
        return pop_up_yes

    else:
        dpg.configure_item("pop_up_window_ok", show=True)
        dpg.configure_item("pop_up_window_yes_no", show=False)
        return True

def close_pop_up_window_yes():
    dpg.set_value("pop_up_window_ok", False)
    pop_up_yes = True

def close_pop_up_window_no():
    dpg.set_value("pop_up_window_ok", False)
    pop_up_yes = False
    


dpg.add_file_dialog(directory_selector=True, show=False, callback=get_folder, tag="file_dialog_id", height=300, width=600)

with dpg.window(label="Tutorial",tag = "main_window" , width=800, height=300):
    dpg.add_text("To use, input the name you want to change the project to and press the button to select the folder")
    with dpg.group(horizontal=True):
        new_name_input = dpg.add_input_text(tag = "new_name_input")
        dpg.add_button(label="Directory Selector", callback=lambda: dpg.show_item("file_dialog_id"))

        with dpg.window(tag="pop_up_window", width=300, height=100, show=False):
            dpg.add_text("test", tag="pop_up_text")
            dpg.add_button(label="OK", tag= "pop_up_window_ok" ,callback=lambda: dpg.hide_item("pop_up_window"))
            with dpg.group(horizontal=True, tag="pop_up_window_yes_no"):
                dpg.add_button(label="Yes", callback=close_pop_up_window_yes)
                dpg.add_button(label="No", callback=close_pop_up_window_no)
    
dpg.set_primary_window("main_window", True)
dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()