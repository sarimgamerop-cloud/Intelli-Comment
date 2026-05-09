import logging , platform , os
from google import genai
import argparse
import argparse, json
from pathlib import Path

## All main configuration variables to set : ##
## Note ##
"""All resolutions will have different length and width etc so read the
   Documents on the Github for more information or download premade 
   configuration for different monitor resolutions """

# configuring path
CONFIG = Path("config.json")

# defining arguments optionally but --api_key is important
parser = argparse.ArgumentParser()
parser.add_argument("--api_key")
parser.add_argument("--debug", action="store_true")
parser.add_argument("--no_limit", action="store_true")
parser.add_argument("--delete_key", action="store_true")
args = parser.parse_args()

# load or create config
data = CONFIG.exists() and json.loads(CONFIG.read_text()) or {
    "api_key": "",
    "debug": False,
    "no_limit": False,
    "type_prompt": ""
}

if "type_prompt" not in data:
    data["type_prompt"] = ""

# updates
if args.api_key is not None:
    data["api_key"] = args.api_key

if args.delete_key:
    data["api_key"] = ""

if args.debug:
    data["debug"] = True

if args.no_limit:
    data["no_limit"] = True


def save_config():
    CONFIG.write_text(json.dumps(data, indent=2))

# save permanently
save_config()

# use values
key = data["api_key"]
show_raw_ocr_text = data["debug"]
remove_comment_limiting = data["no_limit"]


# root of the project put at default
project_root = Path(__file__).parent
# logger to see whats wrong only for debugging
log = logging.getLogger(__name__)
# name of the image file to be saved in /assets (optional)
name = "cap"
# path for where to save the image , dont recommend changing it.
image_path = "assets/cap.png"
# Initialize the API key *(see documentation)
client = genai.Client(api_key=key)
# Comment detector


# Checks the platform ( Copied from TypeBroker :p )
if platform.system() == "Windows":
    tesseract_path = os.path.join(
        os.environ["LOCALAPPDATA"],
        "Programs",
        "Tesseract-OCR",
        "tesseract.exe"
    )
elif platform.system() == "Linux":
    tesseract_path = "/usr/bin/tesseract"
else:
    tesseract_path = None

# Prompt to give to the model. modification may not give expected results, be cautious.
prompt = """
You are an OCR text structuring engine for YouTube comments.

You will receive messy OCR output from a YouTube comment section.

Your job:
1. Extract only valid comments.
2. Identify each comment using the username starting with @.
3. Keep the username EXACT (do not modify it).
4. Attach the correct comment text under each username.
5. Remove all UI noise such as:
   - Reply / replies
   - “Add a comment”
   - view counts (e.g. 654, 195)
   - timestamps (e.g. "2 weeks ago")
   - “Read more”
   - random symbols or broken OCR artifacts
6. Preserve original meaning of text.
7. Keep comments in correct order.
8. If "Add a Comment" text is not found output this line : "No comments found please open a appropiate comment window. exiting .."

STRICT OUTPUT FORMAT:

@username
comment text

@username
comment text

RULES:
- Do NOT add explanations.
- Do NOT summarize.
- Do NOT rewrite meaning.
- Only clean OCR noise and structure text.
- If a comment is long, keep it as a single paragraph under username.

INPUT:
"""

norestrict_prompt = """
You are an OCR text structuring engine for YouTube comments.

You will receive messy OCR output from a YouTube comment section.

Your job:
1. Extract only valid comments.
2. Identify each comment using the username starting with @.
3. Keep the username EXACT (do not modify it).
4. Attach the correct comment text under each username.
5. Remove all UI noise such as:
   - Reply / replies
   - “Add a comment”
   - view counts (e.g. 654, 195)
   - timestamps (e.g. "2 weeks ago")
   - “Read more”
   - random symbols or broken OCR artifacts
6. Preserve original meaning of text.
7. Keep comments in correct order.

STRICT OUTPUT FORMAT:

@username
comment text

@username
comment text

RULES:
- Do NOT add explanations.
- Do NOT summarize.
- Do NOT rewrite meaning.
- Only clean OCR noise and structure text.
- If a comment is long, keep it as a single paragraph under username.

INPUT:
"""


# Channel Type Prompt (very important because i can make mistakes.)

type_prompt = data.get("type_prompt", "")

# Reply Prompt (Dont change strictly)

reply_prompt = """
You are generating YouTube comment replies.

INPUT:
A list of comments in this format:

@username
comment text

TASK:
Generate ONE short reply for EACH comment.

RULES:
- Reply directly to the comment.
- Keep replies SHORT (1–2 lines max).
- Use a casual, human, gaming tone.
- Do NOT analyze the comments.
- Do NOT explain anything.
- Do NOT give suggestions or ideas.
- Do NOT write paragraphs.

STYLE:
- Natural YouTube replies
- Can include light humor, agreement, or reaction
- Can include emojis (optional)

OUTPUT FORMAT:

@username
reply

@username
reply

Only return replies. Nothing else.
"""