import dearpygui.dearpygui as dpg
import os

dpg.create_context()

# this is ugly code but since this is a simple gui / program I do not care about preformance / modularity
def callback(sender, app_data):
    new_name = "test"
    folder_path = app_data["file_path_name"]
    split = folder_path.split("\\")
    old_name = split[-1]
    print("old name: ", old_name)
    print(split)
    print("Folder path: ", folder_path)
    file_list = []
    for file in os.listdir(folder_path):
        if file.endswith(".ioc"):
            file_list.append(file)
            print(file)
            with open(folder_path + "\\" + file, "r") as f:
                filedata = f.read()
            filedata = filedata.replace(old_name, new_name)
            with open(folder_path + "\\" + file, "w") as f:
                f.write(filedata)
            os.rename( folder_path + "\\" + file, folder_path + "\\" + file.replace(old_name, new_name))
    new_folder_path = folder_path.replace(old_name, new_name)
    if len(file_list) > 0:
        print(folder_path)
        print(new_folder_path)
        os.rename(folder_path, new_folder_path)
    

    


dpg.add_file_dialog(directory_selector=True, show=False, callback=callback, tag="file_dialog_id", height=300, width=600)

with dpg.window(label="Tutorial",tag = "main_window" , width=800, height=300):
    dpg.add_text("To use press the button, select the folder of the project you want to rename, input the new desiered name")
    dpg.add_button(label="Directory Selector", callback=lambda: dpg.show_item("file_dialog_id"))
    
dpg.set_primary_window("main_window", True)
dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()