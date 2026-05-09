from google import genai
from PIL import Image
import sys
import config
from google.genai import errors

error_msg = 'No comments found please open a appropiate comment window. exiting ..'

def spell_corrector(text):
    global corrected_text
    
    try:

        print("→ Requesting model correction ...")
        if config.remove_comment_limiting == True:

            response = config.client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=[
                config.norestrict_prompt,
                text,
                ]
            )
            corrected_text = response.text
        elif config.remove_comment_limiting == False:
            response = config.client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=[
                config.prompt,
                text,
                ]
            )
            corrected_text = response.text
        else:
            print('Dont play around ..')
            sys.exit()

    except errors.ClientError as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            print(" ━━━━━━━━━━━━━━ API Limit reached ━━━━━━━━━━━━━━")
            sys.exit()
        else:
            print("API Error:", e)
            sys.exit()



    print("→ Model text recieved succesfully!")
    print("━━━━━━━━━━━━━━ Corrected Text ━━━━━━━━━━━━━━")
    from etc import reply_handler
    if corrected_text == error_msg and config.remove_comment_limiting == False:
        print(error_msg)
        print('-'*30)
        sys.exit()
    else:
        print(corrected_text)
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        reply_handler()

    return corrected_text



def reply_call():
    print("━━━━━━━━━━━━━━━━━━━━━ LOGS ━━━━━━━━━━━━━━━━━━━━")
    print("→ requesting model replies ...")
    print("→ using saved channel prompt ...")
    response_reply = config.client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=[
            config.type_prompt,
            config.reply_prompt,
            corrected_text,
        ]
    )
    replies_comment = response_reply.text
    print("→ model replies recieved succesfully ...")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Model Replies : ")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(replies_comment)
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    return replies_comment
