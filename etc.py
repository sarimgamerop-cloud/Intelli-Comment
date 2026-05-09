import config
import sys
from api_handler import corrected_text , reply_call

def reply_handler():
    print(" Do you want to generate replies ? ")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    generate_replies = input("Y or N : ")
    if generate_replies == "Y":
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        if config.type_prompt == "":
            print("Please generate your channel type prompt (Only first time): ")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            # save value into the shared config module so other modules see it
            config.type_prompt = input("Type Here : ")
            config.data["type_prompt"] = config.type_prompt
            config.save_config()
            print("-"*10,"Logs","-"*10)
            print("Channel prompt saved succesfully ...")
        # import here to avoid circular import at module import time
        from api_handler import reply_call
        reply_call()
    else:
        sys.exit()

    return config.type_prompt
