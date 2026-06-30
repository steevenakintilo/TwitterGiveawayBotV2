from utility_function import reset_file
import os
for file in os.listdir():
    if ".txt" in file and file != "giveaway_won.txt":
        reset_file(file)
        print(f"Reseting {file} file")

print("Txt files reset done")