#!/bin/bash

for d in */; do
    dir="${d%/}"

    if [[ "$dir" != "txt_files_folder" &&
          "$dir" != "txt_account_file_folder" &&
          "$dir" != "find_giveaway" &&
          "$dir" != "__pycache__" ]]; then
        cp -f "twitter.py" "$dir/"
    fi
done