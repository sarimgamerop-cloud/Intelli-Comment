# BASE
from pyautogui import click , screenshot
import subprocess , os , platform , logging , re, sys
from pathlib import Path
from config import *
import cv2
import pytesseract
from textblob import TextBlob
import textwrap
sys.stdout.reconfigure(encoding='utf-8')

# Another check (Important will not work without it :/ )
if tesseract_path and os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    if tesseract_path:
        print(f"Warning: tesseract not found at {tesseract_path}; ensure it's installed or in PATH")
    else:
        print("Warning: tesseract_path not set in config; ensure tesseract is installed and on PATH")


# Taking a screenshot 
def take_shot(x,y,w,h,img_name):
    shot = screenshot(region=(x, y, w, h))
    assets_dir = project_root / "assets"
    assets_dir.mkdir(exist_ok=True)
    # Dont forget to add the name argument
    shot.save(str(assets_dir / f"{img_name}.png"))
    log.info("Screen Shot Captured")
    print("╭──────────────────────────────╮")
    print("│    Screenshot Captured ✓     │")
    print("╰──────────────────────────────╯")

def text_fetch(img):
    global text

    gray_img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    mean_val = cv2.mean(gray_img)[0]
    if mean_val < 127:
        gray_img = cv2.bitwise_not(gray_img)

    # existing threshold stays same
    _, clean_img = cv2.threshold(
    gray_img, 150, 255,
    cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    
    text = pytesseract.image_to_string(clean_img, config="--psm 4")
    
    print("━━━━━━━━━━━━━━ LOGS ━━━━━━━━━━━━━━")
    print("→ Collecting raw OCR text...")

    text = text.replace("\n", " ")

    words = text.split()
    print("→ Raw text collected successfully!")

    if show_raw_ocr_text == True:
        clean_text = str(text)
        clean_text = re.sub(r"[^\x20-\x7E\n]", "", clean_text)
        clean_text = re.sub(r"\s+", " ", clean_text).strip()

        width = 50

        wrapped = textwrap.wrap(clean_text, width=width)

        title = "RAW OCR TEXT"
        sub = "Extracted Output"

        print("┌" + "─" * (width + 2) + "┐")
        print("│" + title.center(width + 2) + "│")
        print("│" + sub.center(width + 2) + "│")
        print("├" + "─" * (width + 2) + "┤")

        for line in wrapped:
            print("│ " + line.ljust(width) + " │")

        print("└" + "─" * (width + 2) + "┘")
        
    return text