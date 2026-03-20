#
# Auto clicks in the game at https://alexfink.github.io/dive/
#

from datetime import datetime
import random
import sys
import os

OPTIONS_FILE = "options.txt"

SCORE_IMAGE_SIZE = 200

    
def copyright_message():
    print("""DIVE_Clicker.py  Copyright 2026  Gary Quinn

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

along with this program.  If not, see <https://www.gnu.org/licenses/>.""")


def install_modules(module_list):

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



def get_score(filename, x, y, xsize, ysize):

    image = pyautogui.screenshot(filename, region=(x-xsize//2, y-ysize//2, int(xsize*2.1), ysize))



def send_keys(keys, score_x, score_y):

    arrow_key_dict = {"W":"up",
                      "A":"left",
                      "D":"right",
                      "S":"down"}

    no_change_count = 0
    start_colour = pyautogui.screenshot().getpixel((score_x, score_y))

    pyautogui.click(score_x, score_y)
    
    pyautogui.keyDown("f5")
    pyautogui.keyUp("f5")

    while no_change_count < 3*len(keys):
        for key in keys:

            pyautogui.keyDown(arrow_key_dict[key])
            pyautogui.keyUp(arrow_key_dict[key])
            current_colour = pyautogui.screenshot().getpixel((score_x, score_y))
            
            if start_colour != current_colour:
                start_colour = current_colour
                no_change_count = 0
            else:
                no_change_count += 1

            print(score_x, score_y, start_colour, key, arrow_key_dict[key], current_colour, no_change_count)


def get_random_moves():

    valid_keys = "WASD"
    return ''.join(random.choice(valid_keys) for i in range(random.randint(4, 12)))


def read_options():

    key_dict = {}

    count = 1
    
    with open(OPTIONS_FILE, "r") as fi:
        for line in fi:
            if len(line) >= 2:
                key_dict[str(count)] = line.strip()
                count += 1

    return key_dict


def append_user_choice_to_options_file(options):

    if len(options) > 0:
        with open(OPTIONS_FILE, "a") as fo:
            fo.write(f"\n{options}")
                    

def process_user_input(key_dict, option, x, y):

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

    print(f"Using {user_choice}")

    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"Current date & time : {current_datetime}\n\n")
    
    get_score(f"DIVE_{current_datetime}_score_at_start_{user_choice}.png", x, y, SCORE_IMAGE_SIZE, SCORE_IMAGE_SIZE)
    send_keys(user_choice, x, y) # Send the user's choice
    get_score(f"DIVE_{current_datetime}_score_at_end_{user_choice}.png", x, y, SCORE_IMAGE_SIZE, SCORE_IMAGE_SIZE)

    return True


def get_user_input(key_dict):

    repeat_count = 1

    print("ENTER: Exit\n0: Random\nSelection of LRUD: use those, OR...")
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

    print("\n\nHover the cursor over the score and press the enter key")

    input()

    x,y = pyautogui.position()

    return command, x, y, repeat_count


def main():

    key_dict = read_options()

    run_again = True
    while run_again:

        option, x, y, repeat_count = get_user_input(key_dict)

        if repeat_count == 0:
            return

        for i in range(repeat_count):
            print(f"\n\nRun {i+1} of {repeat_count}")
            run_again = process_user_input(key_dict, option, x, y)
            if not run_again:
                return



if __name__ == "__main__":
    
    install_modules(["pyautogui"])

    import pyautogui

    copyright_message()
    
    main()

    print("\n\nBye Bye For Now :-)\n\n")

    
