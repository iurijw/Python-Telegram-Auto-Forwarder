from telethon import TelegramClient, events
from typing import List, Tuple
from datetime import datetime
from rich.console import Console


class PyAutoForward(TelegramClient):
    # Class with customs methods from Telethon package.
    
    def __init__(self, api_id: int, api_hash: str):
        super(PyAutoForward, self).__init__('Tdb', api_id, api_hash)
        self.start()
        self.console = Console()

    # Return a list of tuples containing names and ids for each conversation.
    def list_conversations_info(self, include_users: bool = False):
        return_list: List[Tuple] = []

        async def get_conversations():
            async for conversation in self.iter_dialogs():
                try:
                    conversation_data = await self.get_entity(conversation.name)
                    if include_users:
                        return_list.append(
                            (
                                str(conversation.name),
                                int(conversation_data.id)
                            )
                        )
                    else:
                        if conversation.is_channel or conversation.is_group:
                            return_list.append(
                                (
                                    str(conversation.name),
                                    int(conversation_data.id)
                                )
                            )
                except ValueError:
                    pass

        self.loop.run_until_complete(get_conversations())

        return return_list

    def start_forwarding(self, data: dict, error_log: bool = False):
        # Bot main method to listen and forward messages
        self.console.rule('[bold][green] Telegram Auto Forwarder Started')

        @self.on(events.NewMessage)
        async def handle(event):
            try:
                if int(event.message.peer_id.channel_id) in data['ids_origin']:
                    banned_key: bool = False
                    for word in str(event.message.message).lower().split():
                        if word in [str(key_word).lower() for key_word in data['banned_keywords']]:
                            banned_key: bool = True
                    if not banned_key:
                        try:
                            for group in data['link_destinations']:
                                await self.forward_messages(str(group), event.message)
                                self.console.log(f'Forwarded message from id '
                                                 f'{int(event.message.peer_id.channel_id)} to [yellow]{group}[/yellow]')
                        except Exception as err:
                            if error_log:
                                self.console.log(f'Error ignored: {str(err)}')
                    elif banned_key:
                        self.console.log(f'Ignoring message with banned word '
                                         f'from ID {event.message.peer_id.channel_id}')
            except AttributeError as error:
                if error_log:
                    print(f'[{datetime.now()}] Error ignored: {str(error)}')

        self.run_until_disconnected()
