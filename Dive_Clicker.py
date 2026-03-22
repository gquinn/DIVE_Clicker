#
# Auto clicks in the game at https://alexfink.github.io/dive/
#

from datetime import datetime
import random
import os

OPTIONS_FILE = "options.txt"

SCORE_IMAGE_SIZE = 200

    
def copyright_message():
    print("""\n\n\nDIVE_Clicker.py  Copyright 2026  Gary Quinn

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See <https://www.gnu.org/licenses/>.\n\n""")


#
# This function is for testing purposes only.
#
def test_function_get_score_positions() -> None:

    input("\n\nHover the cursor over the score and press the enter key")
    sx,sy = pyautogui.position()

    input("\n\nHover the cursor over the high score and press the enter key")
    hx,hy = pyautogui.position()

    print(f"score pos {sx},{sy}   high score pos {hx},{hy}     diff {hx-sx},{hy-sy}")


#
# Dynamically install the requested python modules.
#
def install_modules(module_list : list) -> None:

    for module in module_list:
        print(f"Trying {module}")
        try:
            __import__(module)
            print(f"Successfully imported {module}")
        except:
            print(f"Trying to Install required module: {module}\n")
            os.system(f'python -m pip install {module}')
            __import__(module)
            print(f"Successfully imported {module}")


#
# Save a screenshot to "prove" the score that was obtained.
#
def get_score(filename : str) -> None:

    image = pyautogui.screenshot()
    image.save(filename)


#
# Play through a single game of DIVE
#
def send_keys(keys : str, score_panel_x : int, score_panel_y : int) -> None:

    arrow_key_dict = {"W":"up",
                      "A":"left",
                      "D":"right",
                      "S":"down"}

    no_change_count = 0
    start_score_colour = pyautogui.screenshot().getpixel((score_panel_x, score_panel_y))

    pyautogui.click(score_panel_x, score_panel_y)
    
    pyautogui.keyDown("f5")
    pyautogui.keyUp("f5")

    while no_change_count < 3*len(keys):
        for key in keys:

            pyautogui.keyDown(arrow_key_dict[key])
            pyautogui.keyUp(arrow_key_dict[key])
            current_colour = pyautogui.screenshot().getpixel((score_panel_x, score_panel_y))
            
            if start_score_colour != current_colour:
                start_score_colour = current_colour
                no_change_count = 0
            else:
                no_change_count += 1

            print(f"{key}, {arrow_key_dict[key]:6}, {str(start_score_colour):15} -> {str(current_colour):15}, {no_change_count:3} ({score_panel_x},{score_panel_y})")


#
# Generate a string of random moves
#
def get_random_moves() -> str:

    valid_keys = "WASD"
    return ''.join(random.choice(valid_keys) for i in range(random.randint(4, 12)))


def read_options() -> dict:

    key_dict = {}

    count = 1
    
    with open(OPTIONS_FILE, "r") as fi:
        for line in fi:
            if len(line) >= 2:
                key_dict[str(count)] = line.strip()
                count += 1

    return key_dict


def append_user_choice_to_options_file(options : str) -> None:

    if len(options) > 0:
        with open(OPTIONS_FILE, "a") as fo:
            fo.write(f"\n{options}")
                    

def process_user_input(key_dict : dict, option : str, x : int, y : int, hx : int, hy : int) -> bool:

    if option in key_dict:
        user_choice = key_dict[option]

    else:
        user_choice = [key for key in option if key in "wasdWASD"]
        user_choice = ''.join(user_choice)
        user_choice = user_choice.upper()

        if user_choice not in key_dict.values():
            append_user_choice_to_options_file(user_choice)
            key_dict[str(len(key_dict)+1)] = user_choice


    print(f"Chosen {option} {user_choice}")

    if len(user_choice) == 0:
        print("Nothing to do.\n")
        return False

    
    print(f"\n\nUsing {user_choice}")

    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"Current date & time : {current_datetime}\n")
    
    high_score_colour = pyautogui.screenshot().getpixel((hx, hy))
    
    send_keys(user_choice, x, y) # Play a single game

    # Take a screen shot if the high score has changed
    new_high_score_colour = pyautogui.screenshot().getpixel((hx, hy))
    if high_score_colour != new_high_score_colour:
        get_score(f"DIVE_highscore_{current_datetime}_{user_choice}.png")

    return True


def get_user_input(key_dict : dict):

    repeat_count = 1

    print("\n\nPress ENTER to Exit\nType a selection of WASD characters, OR...\n0 Random selection of WASD key presses")
    for key in key_dict:
        print(key, key_dict[key])
        
    option = input(f"\n--> ")

    print(f"Chosen <{option}>")

    if len(option) == 0:
        print("Nothing to do.\n")
        return False, False, False, 0

    command = option.split(".")[0]

    try:
        count = option.split(".")[1]
        repeat_count = int(count)

        print(command, count, repeat_count)

    except:
        repeat_count = 1

    if command == "0":
        command = get_random_moves()

    input("\n\nHover the cursor over the score and press the enter key : ")
    x,y = pyautogui.position()

    input("\n\nHover the cursor over the high score and press the enter key : ")
    hx,hy = pyautogui.position()

    return command, x, y, hx, hy, repeat_count


def main() -> None:

    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    get_score(f"DIVE_highscore_{current_datetime}_start_of_new_session.png")


    key_dict = read_options()

    run_again = True
    while run_again:

        option, x, y, hx, hy, repeat_count = get_user_input(key_dict)

        if repeat_count == 0:
            return

        for i in range(repeat_count):
            print(f"\n\nRun {i+1} of {repeat_count}")
            run_again = process_user_input(key_dict, option, x, y, hx, hy)
            if not run_again:
                return



if __name__ == "__main__":
    
    install_modules(["pyautogui"])

    import pyautogui

    copyright_message()

    #test_function_get_score_positions()
    
    main()

    print("\n\nBye Bye For Now :-)\n\n")

    
