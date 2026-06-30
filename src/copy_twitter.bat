@echo off

for /d %%d in (*) do (
    if /i not "%%d"=="txt_files_folder" (
        if /i not "%%d"=="txt_account_file_folder" (
            if /i not "%%d"=="find_giveaway" (
                if /i not "%%d"=="check_for_win_bot" (
                    if /i not "%%d"=="__pycache__" (
                        copy /Y "twitter.py" "%%d\"
                        copy /Y "global_variable.py" "%%d\"
                    )
                )
            )
        )
    )
)