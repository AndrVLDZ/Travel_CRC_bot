import db
import qiwi
from aiogram import F, Router
from aiogram.types import Message
from aiogram.methods.delete_message import DeleteMessage

router = Router()


@router.message()
async def converter(message: Message) -> DeleteMessage:
    user_id = message.from_user.id
    if not await db.check_user_id(user_id):
        await message.answer(
            "Send `/start` command first!",
            parse_mode="Markdown"
            )
    else:
        # user input
        value: str = message.text.replace(',','.')
        # getting user settings
        round = await db.get_round_state(user_id)
        
        # calling and validating the converter function
        res = await qiwi.converter(user_id, value, round)
        if not res:
            await message.answer(
                "Set different currencies!",
                parse_mode="Markdown"
            )
        else: 
            curr_from, curr_to = await db.get_currency_pair(user_id)
            if curr_from != curr_to: 
                await message.answer(
                    f"**`{value}` {curr_to}  ==  `{res}` {curr_from}**",
                    parse_mode="Markdown"
                )


    # removing user input for better readability of converter responses
    return DeleteMessage(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
