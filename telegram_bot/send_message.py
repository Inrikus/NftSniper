from telethon import TelegramClient
from data import config 


async def send_telegram_message(union_data: dict) -> None:
    async with TelegramClient('anon', config.API_ID, config.API_HASH) as client:
        
        message_text = "Mechs: "
        message_text += "@Shpingaletos\n"
        for title_id, data in union_data.items():
            message_text += f"Title ID: {title_id}\n"
            message_text += f"Link: {data['Link']}\n"
            message_text += f"GRADE: {data['GRADE']}\n"
            message_text += f"Weapons: {data['Weapons']}\n"
            message_text += f"Price: {data['Price']}\n\n"

        await client.send_message(config.CHAT_ID, message_text)