import os
import yaml  # Ensure PyYAML is installed: pip install pyyaml

# Full list of usernames
uusernames = """
musak2Ug
8am_Yaklad
hamzriiiiiii
WengerEra199
iprecio9s59
Kanzo_Ba1
dannyppppppp
katakuriener1
JamesMorris10
"""


uusernames = uusernames.split("\n")

# for uz in uusernames:
#     if uz not in uuu:
#         print(uz)


# time.sleep(100000000)


usernames = []
for u in uusernames:
    if len(u) > 3:
        usernames.append(u)

def rename_folders_and_update_config(usernames):
    # Get all subfolders in the current directory
    subfolders = [f for f in os.listdir('.') if os.path.isdir(f)]
    
    # Sort to ensure the order is consistent, if needed
    subfolders.sort()

    print(len(subfolders),len(usernames))
    
    # Ensure there's a one-to-one match
    if len(subfolders) != len(usernames):
        print("Error: Number of subfolders does not match number of usernames.")
        return
    
    for i, folder in enumerate(subfolders):
        try:
            new_folder_name = usernames[i]
            
            # Skip if the target folder name already exists
            if os.path.exists(new_folder_name):
                print(f"Skipping '{new_folder_name}' as it already exists.")
                continue
            
            os.rename(folder, new_folder_name)
            print(f"Renamed '{folder}' to '{new_folder_name}'")
        except Exception as e:
            print(f"Error renaming '{folder}' to '{new_folder_name}': {e}")


import time


def list_folder(usernames):
    # Get all subfolders in the current directory
    subfolders = [f for f in os.listdir('.') if os.path.isdir(f)]
    
    # Sort to ensure the order is consistent, if needed
    subfolders.sort()
    print(len(subfolders))
    
    # Ensure there's a one-to-one match
    if len(subfolders) != len(usernames):
        print("Error: Number of subfolders does not match number of usernames.")
        return
    
    for i, folder in enumerate(subfolders):
        try:
            new_folder_name = usernames[i]
            
            # Skip if the target folder name already exists
            if os.path.exists(new_folder_name):
                print(f"Skipping '{new_folder_name}' as it already exists.")
                continue
            
            os.rename(folder, new_folder_name)
            print(f"Renamed '{folder}' to '{new_folder_name}'")
        except Exception as e:
            print(f"Error renaming '{folder}' to '{new_folder_name}': {e}")

# Run the function
#list_folder(usernames)

rename_folders_and_update_config(usernames)