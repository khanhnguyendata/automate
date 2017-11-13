import pyautogui


try:
    while True:
        x, y = pyautogui.position()
        position_str = 'x: {:<4}, y: {:<4}'.format(x, y)
        print(position_str, end='')
        print('\b' * len(position_str), end='', flush=True)
except KeyboardInterrupt:
    print('\nDone')
