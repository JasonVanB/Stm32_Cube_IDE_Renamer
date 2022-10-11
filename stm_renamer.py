import dearpygui.dearpygui as dpg
import os

# function to show pop up window, 
#   message is determined by message 
#   yes_no is a boolean to determine if the pop up window should have a yes/no option or just an ok option
#   yes_callback is the function to call when the yes button is pressed
#   no_callback is the function to call when the no button is pressed
#   yes_callback_data is the data to pass to the yes_callback function
#   no_callback_data is the data to pass to the no_callback function
def show_pop_up_window(message, yes_no, yes_callback=None, no_callback=None, yes_callback_data=None, no_callback_data=None):
    dpg.configure_item("popup_window", show = True)
    dpg.set_value("popup_window_text", message)
    dpg.configure_item("popup_window_text", indent = ((dpg.get_item_width("popup_window")/2) - (len(message) * 6)/2))

    if yes_no:
        dpg.configure_item("popup_window_yes_no", show=True)
        dpg.configure_item("popup_window_yes_no_spacer", width=dpg.get_item_width("popup_window")/2 - 150)
        dpg.configure_item("popup_window_ok", show=False)
        dpg.configure_item("popup_window_yes", callback=yes_callback)
        dpg.configure_item("popup_window_no", callback=no_callback)
        dpg.configure_item("popup_window_yes", user_data=yes_callback_data)
        dpg.configure_item("popup_window_no", user_data=no_callback_data)
    else:
        dpg.configure_item("popup_window_yes_no", show=False)
        dpg.configure_item("popup_window_ok", show=True)
        dpg.configure_item("popup_window_ok_spacer", width=dpg.get_item_width("popup_window")/2 - 75)

# function to get the folder path from the user, shows a pop up window that lets you select a folder
# the function then calls show_pop_up_window to show a pop up window that ask the user to confirm renameeing of the project
# if error occurs, show_pop_up_window is called with the error message
# this function has no error checking for the file io for searching the slected directory
def get_folder(sender, app_data):
    new_name = dpg.get_value("new_name_input")
    folder_path = app_data["file_path_name"]
    old_name = folder_path.split("\\")[-1]

    if new_name == "":
        show_pop_up_window("Please enter a new name", False)
        return

    if new_name == old_name:
        show_pop_up_window("New name is the same as the old name", False)
        return
        
    # if there is one or more ioc files, error out may want to add additional functionality for this
    # to allow renaming mutiple ioc files at once if needed
    file_list = []
    for file in os.listdir(folder_path):
        if file.endswith(".ioc"):
            file_list.append(file)

    if len(file_list) == 1:

        ioc_file = folder_path + "\\" + file_list[0]

        popup_string = "Are you sure you want to rename " + old_name + " to " + new_name + "?\n\nThis will rename the following files: \n " + ioc_file + "\n " + folder_path + "\n\n" + "Please note this program does not check for invalid characters in the new name." + "\n\n" + "IT IS RECOMMENDED THAT YOU CLOSE CUBE IDE WHEN DOING THIS"
        
        show_pop_up_window(popup_string, True, get_folder_popup_yes, get_folder_popup_no, (new_name, folder_path, old_name, ioc_file), None)

    elif len(file_list) == 0:
        show_pop_up_window("No ioc file found in folder", False)
    else:
        show_pop_up_window("Multiple ioc files found in folder", False)

# callback function for the yes button in the pop up window when it is called from get_folder
# this function has no exception handling for the file io, but does properly close the relevant files in the event of an error
def get_folder_popup_yes(sender, app_data, user_data):
    dpg.configure_item("popup_window", show = False)

    new_name = user_data[0]
    folder_path = user_data[1]
    old_name = user_data[2]
    ioc_file = user_data[3]

    # read ioc file into memory
    with open(ioc_file, "r") as f:
        filedata = f.read()

    # replace old name with new name in file data in memory
    filedata = filedata.replace(old_name, new_name)

     # open ioc file again and write updated data to it
    with open(ioc_file, "w") as f:
        f.write(filedata)

    # rename ioc file
    os.rename(ioc_file, folder_path + "\\" + new_name + ".ioc")

    # rename parent folder
    new_folder_path = folder_path.replace(old_name, new_name)
    os.rename(folder_path, new_folder_path)

    show_pop_up_window("Renamed " + old_name + " to " + new_name, False)

# callback function for the no button in the pop up window when it is called from get_folder
def get_folder_popup_no(sender, app_data):
    dpg.configure_item("popup_window", show = False)


if __name__ == "__main__": 

    dpg.create_context()

    # file selection window, is hiddent untill the directory selector button is pressed
    dpg.add_file_dialog(directory_selector=True, show=False, callback=get_folder, tag="file_dialog_id", height=300, width=600)

    # primary window of the gui
    with dpg.window(tag = "main_window" ,width=800, height=300):
        dpg.add_text("To use, input the name you want to change the project to and press the button to select the folder, you will have to reimport the project into cube ide after renaming", wrap=0)
        
        # input for new name and directory selector button
        with dpg.group(horizontal=True):
            new_name_input = dpg.add_input_text(tag = "new_name_input", hint="Type New Name Here")
            dpg.add_button(label="Directory Selector", callback=lambda: dpg.show_item("file_dialog_id"), width=150)

            # general purpose popup window used for confirmation, status, and error messages
            with dpg.window(tag="popup_window", width=600, height=300, modal=True, no_close=True, no_resize=True, show=False):

                # text is changed depending on the function that calls the popup window
                dpg.add_text("test", tag="popup_window_text", wrap=0)

                # yes no buttons are shown if the popup window is called with yes_no = True
                with dpg.group(horizontal=True):
                    dpg.add_spacer(width = 300, tag = "popup_window_ok_spacer")
                    dpg.add_button(label="OK", tag= "popup_window_ok" ,callback=lambda: dpg.hide_item("popup_window"), width=150)
                
                # ok button is shown if the popup window is called with yes_no = False
                with dpg.group(horizontal=True, tag="popup_window_yes_no"):
                    # default callbacks will be changed
                    dpg.add_spacer(width=300, tag="popup_window_yes_no_spacer")
                    dpg.add_button(label="Yes", tag= "popup_window_yes" ,callback=lambda: dpg.hide_item("popup_window"), width=150)
                    dpg.add_button(label="No", tag = "popup_window_no" ,callback=lambda: dpg.hide_item("popup_window"), width=150)
        

        
    dpg.set_primary_window("main_window", True)
    dpg.create_viewport(title='Cube ide project renamer ver 1.0.0', width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()