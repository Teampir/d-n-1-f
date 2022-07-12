import re
import time
import asyncio

from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from bot import start_uptime, Translation, VERIFY # pylint: disable=import-error
from plugins.pm_filter import ( # pylint: disable=import-error
    FIND, 
    INVITE_LINK, 
    ACTIVE_CHATS,
    recacher,
    gen_invite_links
    )
from bot.plugins.settings import( # pylint: disable=import-error
    remove_emoji
)
from database import Database # pylint: disable=import-error

db = Database()



@Client.on_message(filters.command('setting') & filters.incoming)
async def cb_settings(bot, update: CallbackQuery):
    """
    A Callback Funtion For Back Button in /settings Command
    """
    global VERIFY
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    
    if user_id not in VERIFY.get(str(chat_id)): # Check If User Is Admin
        return

    bot_status = await bot.get_me()
    bot_fname= bot_status.first_name
    
    text =f"<i>{bot_fname}'s</i> Settings Pannel.....\n"
    text+=f"\n<i>You Can Use This Menu To Change Connectivity And Know Status Of Your Every Connected Channel, Change Filter Types, Configure Filter Results And To Know Status Of Your Group...</i>"
    
    buttons = [
        [
            InlineKeyboardButton
                (
                    "Status", callback_data=f"status({chat_id})"
                )
        ],
            InlineKeyboardButton
                (
                    "Configure 🛠", callback_data=f"config({chat_id})"
                ), 
            
            InlineKeyboardButton
                (
                    "Filter Types", callback_data=f"types({chat_id})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "Close 🔐", callback_data="close"
                )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)

    await update.message.edit_text(
        text, 
        reply_markup=reply_markup, 
        parse_mode=enums.ParseMode.HTML
        )
    
    
@Client.on_callback_query(filters.regex(r"config\((.+)\)"), group=2)
async def cb_config(bot, update: CallbackQuery):
    """
    A Callback Funtion For Chaning The Number Of Total Pages / 
    Total Results / Results Per pages
    """
    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    chat_name = remove_emoji(update.message.chat.title)
    user_id = update.from_user.id
    
    if user_id not in VERIFY.get(str(chat_id)):
        return

    chat_id = re.findall(r"config\((.+)\)", query_data)[0]
    
    settings = await db.find_chat(int(chat_id))
    
    mp_count = settings["configs"]["max_pages"]
    mf_count = settings["configs"]["max_results"]
    mr_count = settings["configs"]["max_per_page"]
    accuracy_point = settings["configs"].get("accuracy", 0.80)
    
    text=f"<i><b>Configure Your <u><code>{chat_name}</code></u> Group's Filter Settings...</b></i>\n"
    
    text+=f"\n<i>{chat_name}</i> Current Settings:\n"

    text+=f"\n - Max Filter: <code>{mf_count}</code>\n"
    
    text+=f"\n - Max Pages: <code>{mp_count}</code>\n"
    
    text+=f"\n - Max Filter Per Page: <code>{mr_count}</code>\n"

    text+=f"\n - Accuracy Percentage: <code>{accuracy_point}</code>\n"
    
    text+="\nAdjust Above Value Using Buttons Below... "
    buttons=[
        [
            InlineKeyboardButton
                (
                    "Filter Per Page", callback_data=f"mr_count({mr_count}|{chat_id})"
                ), 
    
            InlineKeyboardButton
                (
                    "Max Pages",       callback_data=f"mp_count({mp_count}|{chat_id})"
                )
        ]
    ]


    buttons.append(
        [
            InlineKeyboardButton
                (
                    "Total Filter Count", callback_data=f"mf_count({mf_count}|{chat_id})"
                )
        ]
    )


    buttons.append(
        [
            InlineKeyboardButton
                (
                    "Result's Accuracy", callback_data=f"accuracy({accuracy_point}|{chat_id})"
                )
        ]
    )


    buttons.append(
        [
            InlineKeyboardButton
                (
                    "🔙 Back", callback_data=f"settings"
                )
        ]
    )
    
    
    reply_markup=InlineKeyboardMarkup(buttons)
    
    await update.message.edit_text(
        text, 
        reply_markup=reply_markup, 
        parse_mode=enums.ParseMode.HTML
    )

    
  
@Client.on_callback_query(filters.regex(r"mr_count\((.+)\)"), group=2)
async def cb_max_buttons(bot, update: CallbackQuery):
    """
    A Callback Funtion For Changing The Count Of Result To Be Shown Per Page
    """
    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    chat_name = remove_emoji(update.message.chat.title)
    user_id = update.from_user.id
    
    if user_id not in VERIFY.get(str(chat_id)):
        return

    count, chat_id = re.findall(r"mr_count\((.+)\)", query_data)[0].split("|", 1)

    text = f"<i>Choose Your Desired 'Max Filter Count Per Page' For Every Filter Results Shown In</i> <code>{chat_name}</code>"

    buttons = [
        [
            InlineKeyboardButton
                (
                    "5 Filters", callback_data=f"set(per_page|5|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "10 Filters", callback_data=f"set(per_page|10|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "15 Filters", callback_data=f"set(per_page|15|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "20 Filters", callback_data=f"set(per_page|20|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "25 Filters", callback_data=f"set(per_page|25|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "30 Filters", callback_data=f"set(per_page|30|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "🔙 Back", callback_data=f"config({chat_id})"
                )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)

    await update.message.edit_text(
        text, reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML
    )



@Client.on_callback_query(filters.regex(r"mp_count\((.+)\)"), group=2)
async def cb_max_page(bot, update: CallbackQuery):
    """
    A Callback Funtion For Changing The Count Of Maximum Result Pages To Be Shown
    """
    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    chat_name = remove_emoji(update.message.chat.title)
    user_id = update.from_user.id
    
    if user_id not in VERIFY.get(str(chat_id)):
        return

    count, chat_id = re.findall(r"mp_count\((.+)\)", query_data)[0].split("|", 1)
    
    text = f"<i>Choose Your Desired 'Max Filter Page Count' For Every Filter Results Shown In</i> <code>{chat_name}</code>"
    
    buttons = [

        [
            InlineKeyboardButton
                (
                    "2 Pages", callback_data=f"set(pages|2|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "4 Pages", callback_data=f"set(pages|4|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "6 Pages", callback_data=f"set(pages|6|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "8 Pages", callback_data=f"set(pages|8|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "10 Pages", callback_data=f"set(pages|10|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "🔙 Back", callback_data=f"config({chat_id})"
                )
        ]

    ]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await update.message.edit_text(
        text, reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML
    )



@Client.on_callback_query(filters.regex(r"mf_count\((.+)\)"), group=2)
async def cb_max_results(bot, update: CallbackQuery):
    """
    A Callback Funtion For Changing The Count Of Maximum Files TO Be Fetched From Database
    """
    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    chat_name = remove_emoji(update.message.chat.title)
    user_id = update.from_user.id
    
    if user_id not in VERIFY.get(str(chat_id)):
        return

    count, chat_id = re.findall(r"mf_count\((.+)\)", query_data)[0].split("|", 1)

    text = f"<i>Choose Your Desired 'Max Filter' To Be Fetched From DB For Every Filter Results Shown In</i> <code>{chat_name}</code>"

    buttons = [

        [
            InlineKeyboardButton
                (
                    "50 Results", callback_data=f"set(results|50|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "100 Results", callback_data=f"set(results|100|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "150 Results", callback_data=f"set(results|150|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "200 Results", callback_data=f"set(results|200|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "250 Results", callback_data=f"set(results|250|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "300 Results", callback_data=f"set(results|300|{chat_id}|{count})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "🔙 Back", callback_data=f"config({chat_id})"
                )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)

    await update.message.edit_text(
        text, reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML
    )
    
    
    
@Client.on_callback_query(filters.regex(r"accuracy\((.+)\)"), group=2)
async def cb_accuracy(bot, update: CallbackQuery):
    """
    A Callaback Funtion to control the accuracy of matching results
    that the bot should return for a query....
    """
    global VERIFY
    chat_id = update.message.chat.id
    chat_name = update.message.chat.title
    user_id = update.from_user.id
    query_data = update.data
    
    
    if user_id not in VERIFY.get(str(chat_id)):
        return

    val, chat_id = re.findall(r"accuracy\((.+)\)", query_data)[0].split("|", 1)
    
    text = f"<i>Choose Your Desired 'Accuracy Perceentage' For Every Filter Results Shown In</i> <code>{chat_name}</code>\n\n"
    text+= f"<i>NB: Higher The Value Better Matching Results Will Be Provided... And If Value Is Lower It Will Show More Results \
        Which Is Fimilary To Query Search (Wont Be Accurate)....</i>"

    buttons = [
        [
            InlineKeyboardButton
                (
                    "100 %", callback_data=f"set(accuracy|1.00|{chat_id}|{val})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "80 %", callback_data=f"set(accuracy|0.80|{chat_id}|{val})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "65 %", callback_data=f"set(accuracy|0.65|{chat_id}|{val})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "60 %", callback_data=f"set(accuracy|0.60|{chat_id}|{val})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "55 %", callback_data=f"set(accuracy|0.55|{chat_id}|{val})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "50 %", callback_data=f"set(accuracy|0.50|{chat_id}|{val})"
                )
        ],
        [
            InlineKeyboardButton
                (
                    "🔙 Back", callback_data=f"config({chat_id})"
                )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)

    await update.message.edit_text(
        text, reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML
    )
    
    
    
@Client.on_callback_query(filters.regex(r"set\((.+)\)"), group=2)
async def cb_set(bot, update: CallbackQuery):
    """
    A Callback Funtion Support For config()
    """
    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    
    if user_id not in VERIFY.get(str(chat_id)):
        return

    action, val, chat_id, curr_val = re.findall(r"set\((.+)\)", query_data)[0].split("|", 3)

    try:
        val, chat_id, curr_val = float(val), int(chat_id), float(curr_val)
    except:
        chat_id = int(chat_id)
    
    if val == curr_val:
        await update.answer("New Value Cannot Be Old Value...Please Choose Different Value...!!!", show_alert=True)
        return
    
    prev = await db.find_chat(chat_id)

    accuracy = float(prev["configs"].get("accuracy", 0.80))
    max_pages = int(prev["configs"].get("max_pages"))
    max_results = int(prev["configs"].get("max_results"))
    max_per_page = int(prev["configs"].get("max_per_page"))
    
    if action == "accuracy": # Scophisticated way 😂🤣
        accuracy = val
    
    elif action == "pages":
        max_pages = int(val)
        
    elif action == "results":
        max_results = int(val)
        
    elif action == "per_page":
        max_per_page = int(val)
        

    new = dict(
        accuracy=accuracy,
        max_pages=max_pages,
        max_results=max_results,
        max_per_page=max_per_page,
    )
    
    append_db = await db.update_configs(chat_id, new)
    
    if not append_db:
        text="Something Wrong Please Check Bot Log For More Information...."
        await update.answer(text=text, show_alert=True)
        return
    
    text=f"Your Request Was Updated Sucessfully....\nNow All Upcoming Results Will Show According To This Settings..."
        
    buttons = [
        [
            InlineKeyboardButton
                (
                    "Back 🔙", callback_data=f"config({chat_id})"
                ),
            
            InlineKeyboardButton
                (
                    "Close 🔐", callback_data="close"
                )
        ]
    ]
    
    reply_markup=InlineKeyboardMarkup(buttons)
    
    await update.message.edit_text(
        text, reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML
    )
