import time
import PIL.Image
import pyautogui
import mimetypes
import base64
import json
import PIL
import scipy
import scipy.stats
import io
import wx

app = wx.App(False)
WIDTH, HEIGHT = wx.GetDisplaySize()

def scx(input):
    return int(input / 1920 * WIDTH)

def scy(input):
    return int(input / 1080 * HEIGHT)

def check_skip_tag(num, reference=None):
    if not reference:
        if num == 1:
            reference = pyautogui.screenshot(region=(561, 812, 76, 68))
        if num == 2:
            reference = pyautogui.screenshot(region=(914, 873, 78, 67))
    histo1 = reference.convert("RGB").histogram()
    og_histo = PIL.Image.open('tarot_icon.png' if num == 1 else 'tarot_icon_2.png').convert("RGB").histogram()

    corr = scipy.stats.pearsonr(histo1, og_histo)
    print(corr.statistic)
    if num == 1:
        return corr.statistic > 0.93
    if num == 2:
        return corr.statistic > 0.96

def click_skip(num):
    if num == 1:
        pyautogui.moveTo(730, 840)
    elif num == 2:
        pyautogui.moveTo(1051, 840)
    pyautogui.click()

def reset():
    pyautogui.keyDown('r')
    time.sleep(0.4)
    while True:
        reference = pyautogui.screenshot(region=(1300, 540, 160, 230))
        histo1 = reference.convert("RGB").histogram()
        og_histo = PIL.Image.open('green.png').convert("RGB").histogram()

        corr = scipy.stats.pearsonr(histo1, og_histo)
        print('RESET: ', corr.statistic)
        if corr.statistic < 0.9:
            pyautogui.keyUp('r')
            break

def soul_card():
    images = [pyautogui.screenshot(region=(i * 180 + 600, 660, 175, 240)) for i in range(5)]
    histos = [reference.convert("RGB").histogram() for reference in images]
    og_histo = PIL.Image.open('soul.png').convert("RGB").histogram()

    for i, histo in enumerate(histos):
        corr = scipy.stats.pearsonr(histo, og_histo)
        if corr.statistic > 0.50:
            return True


counter = 0
while True:
    counter += 1

    if check_skip_tag(1):
        click_skip(1)
        time.sleep(2)
        img = pyautogui.screenshot(region=(600, 630, 884, 261))
        img.save(f'pack{counter}.png')
        if soul_card():
            quit()
    elif check_skip_tag(2):
        click_skip(1)
        time.sleep(0.4)
        click_skip(2)
        time.sleep(2)
        img = pyautogui.screenshot(region=(600, 630, 884, 261))
        img.save(f'pack{counter}.png')
        if soul_card():
            quit()
    else:
        reset()
