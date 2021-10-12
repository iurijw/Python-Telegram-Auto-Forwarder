from modules.pyautofward import PyAutoForward
from modules.config import Config
from rich import print
from rich.prompt import Prompt
import os


def main():
    verify_config()


def start_bot():
    # User confirmation to start the bot
    prompt = Prompt()
    continue_var = prompt.ask('Start?', choices=['Y', 'N'])

    if continue_var == 'Y':
        return True
    else:
        quit()


def verify_config():
    # Function to verify existence of config in path

    # Instance config object
    config = Config()

    if 'config.json' in [str(arc).replace("<DirEntry '", '').replace("'>", '')
                         for arc in os.scandir()]:

        data: dict = config.get_json_config_data()

        if data['api_id'] == 0 and data['api_hash'] == '':
            define_vars()

        print("To change the settings, edit the 'config.json' file in the same path of the program\n"
              "This is your actual config:\n")
        print(data)
        print('')

        client = PyAutoForward(
            api_id=data['api_id'],
            api_hash=data['api_hash']
        )

        if start_bot():
            client.start_forwarding(data)

    else:
        # If config not exist it will create
        config.create_json_config()
        define_vars()


def define_vars():
    # Function to define config variables

    # Instance config object
    config = Config()

    # User Data Input for Telegram Api
    api_id = int(input('Insert api-id: ').replace(' ', ''))
    api_hash = input('Insert api-hash: ').replace(' ', '')

    # Add API config
    config.define_config_var(
        api_id=api_id,
        api_hash=api_hash
    )
    data = config.get_json_config_data()

    # Instance main object and print conversation information
    client = PyAutoForward(
        api_id=data['api_id'],
        api_hash=data['api_hash']
    )
    print('\nListing conversations information...\n')
    groups = client.list_conversations_info()
    for group in groups:
        print(f'Name: {group[0]} / Id: {group[1]}')

    # User input ID's and Links
    ids_origin = tuple(int(id_var) for id_var in input("\nInsert Id's from origin groups, split by ',': ").split(','))
    link_destinations = tuple(link for link in input("Insert 't.me/*' from destinations, split by ',': ").split(','))
    banned_keywords = tuple(word for word in input("Insert banned-keywords, split by ',': ").split(','))

    # Add bot config
    config.define_config_var(
        ids_origin=ids_origin,
        link_destinations=link_destinations,
        banned_keywords=banned_keywords
    )

    if start_bot():
        data = config.get_json_config_data()
        client.start_forwarding(data=data)


if __name__ == '__main__':
    main()
