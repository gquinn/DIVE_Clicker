#
# Auto clicks in the game at https://alexfink.github.io/dive/
#

from datetime import datetime
import random
import sys
import os


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

    arrow_key_dict = {"L":"left",
                      "U":"up",
                      "R":"right",
                      "D":"down"}

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

    valid_keys = "UDLR"
    return ''.join(random.choice(valid_keys) for i in range(random.randint(4, 12)))
    
def main():

    key_dict = {"1":"LURD",
                "2":"LURU",
                "3":"LR",
                "4":"UD",
                "5":"LRLRLRLRUDUDUDUD",
                "6":"LURULURULDRDLRDR",
                "7":"LRLRULRLRD",
                "8":"LRLRDU"}

    score_image_size = 200

    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"Current date & time : {current_datetime}\n\n")

    while True:

        print("ENTER: Exit\n0: Random\nSelection of LRUD: use those, OR...")
        for key in key_dict:
            print(key, key_dict[key])
            
        version = input(f"\n--> ")

        if len(version) == 0:
            return

        if version == "0":
            version = get_random_moves()

        print("\n\nHover the cursor over the score and press the enter key")

        input()

        x,y = pyautogui.position()

        if version in key_dict:

            user_choice = key_dict[version]

            #print(f"Using {key_dict[version]}")
            
            #get_score(f"DIVE_score_at_start_{key_dict[version]}_{current_datetime}.png", x, y, score_image_size, score_image_size)
            #send_keys(key_dict[version], x, y)
            #get_score(f"DIVE_score_at_end_{key_dict[version]}_{current_datetime}.png", x, y, score_image_size, score_image_size)
            
        else:
            user_choice = [key for key in version if key in "lrudLRUD"]
            user_choice = ''.join(user_choice)
            user_choice = user_choice.upper()


        if len(user_choice) == 0:
            return

        print(f"Using {user_choice}")
         
        get_score(f"DIVE_{current_datetime}_score_at_start_{user_choice}.png", x, y, score_image_size, score_image_size)
        send_keys(user_choice, x, y) # Send the user's choice
        get_score(f"DIVE_{current_datetime}_score_at_end_{user_choice}.png", x, y, score_image_size, score_image_size)


if __name__ == "__main__":
    
    install_modules(["pyautogui"])

    import pyautogui
    
    main()

    print("\n\nBBFN\n\n")

    
