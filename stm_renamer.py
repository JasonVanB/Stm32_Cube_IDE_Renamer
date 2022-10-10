import dearpygui.dearpygui as dpg
import os

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
        print("no ioc files found")
    else:
        print("multiple ioc files found")
        
    

    


dpg.add_file_dialog(directory_selector=True, show=False, callback=get_folder, tag="file_dialog_id", height=300, width=600)

with dpg.window(label="Tutorial",tag = "main_window" , width=800, height=300):
    dpg.add_text("To use, input the name you want to change the project to and press the button to select the folder")
    with dpg.group(horizontal=True):
        new_name_input = dpg.add_input_text(tag = "new_name_input")
        dpg.add_button(label="Directory Selector", callback=lambda: dpg.show_item("file_dialog_id"))
    
dpg.set_primary_window("main_window", True)
dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()