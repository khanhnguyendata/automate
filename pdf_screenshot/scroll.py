import pyautogui, time, os, shutil
from PIL import Image


def crop_screenshot(filename, left, top, right, bottom):
    """
    Crop an image based on the specified trim on each side
    :param filename: path of the image
    :param left: pixels cropped from left
    :param top: pixels cropped from top
    :param right: pixels cropped from right
    :param bottom: pixels cropped from bottom
    :return: pillow Image object containing the cropped image
    """
    screenshot = Image.open(filename)
    width, height = screenshot.size
    cropped = screenshot.crop((0 + left, 0 + top, width - right, height - bottom))

    return cropped


def join_screenshot(page):
    """
    Crop and join the separate screenshots taken from the PDF page
    :param page: page number of the PDF page where the screenshots were made
    :return: pillow Image object containing the image of the cropped page screenshots vertically joined together
    """
    cropped_top = crop_screenshot('{}.png'.format(page * 3), 41, 37, 29, 49)
    top_width, top_height = cropped_top.size
    cropped_middle = crop_screenshot('{}.png'.format(page * 3 + 1), 41, 25, 29, 49)
    middle_width, middle_height = cropped_middle.size
    cropped_bottom = crop_screenshot('{}.png'.format(page * 3 + 2), 41, 25, 29, 60)
    bottom_width, bottom_height = cropped_bottom.size

    joined = Image.new('RGBA', (top_width, top_height + middle_height + bottom_height - 680))
    joined.paste(cropped_top, (0, 0))
    joined.paste(cropped_middle, (0, top_height - 205))
    joined.paste(cropped_bottom, (0, top_height + middle_height - 680))

    return joined


def join_all(folder, page_count):
    """
    Join all PDF screenshots (3 shots per page)
    :param folder: folder where screenshots are to be stored
    :param page_count: number of pages in the PDF
    :return: separate screenshots, as well as joined screenshots, for each page in the folder
    """
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)
    os.chdir(folder)

    time.sleep(5)
    i = 0
    for page in range(page_count):
        # On each page, take 3 screenshots (top, middle, bottom)
        # Move to the next page, scroll up to top of page, and continue with the 3 screenshots for that page, etc.
        for position in range(3):
            screenshot = pyautogui.screenshot()
            screenshot.save('{}.png'.format(i))
            i += 1
            pyautogui.scroll(-800)
        pyautogui.press('pagedown')
        pyautogui.scroll(2000)

    for page in range(page_count):
        joined_screenshot = join_screenshot(page)
        joined_screenshot.save('joined{}.png'.format(page))


def main():
    join_all('hubbard', 20)


if __name__ == '__main__':
    main()