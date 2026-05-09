# Base for the CODE : 
from identifier import text_fetch, take_shot
from config import *
from api_handler import spell_corrector
import ctypes , sys
ctypes.windll.user32.SetProcessDPIAware()
sys.stdout.reconfigure(encoding='utf-8')

# taking a screenshoot and saving it in the assets folder
take_shot(808, 201, 373, 752, name)

# capture OCR output into a local variable
text = text_fetch(image_path)

# model tasks functions
spell_corrector(text)








