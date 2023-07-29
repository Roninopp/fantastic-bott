import html

import bs4
import requests
from GabiBraunRobot import dispatcher
from GabiBraunRobot.modules.disable import DisableAbleCommandHandler
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ParseMode,
                      Update)
from telegram.ext import CallbackContext

info_btn = "More Information"
kaizoku_btn = "Kaizoku 💓"
kayo_btn = "Kayo 🏴‍☠️"
animeacedemy_btn = "AnimeAcedemy 👑"
tpx_btn = "TeamProjectX⚠️"
hsa_btn = "HindiSubbedAnime 👊"
tpx_btn = "Anime Subbing Team☠️"
atf_btn = "ATF Anime 🍿"
an_btn = "Anime Nagri⚔️⚔️"
cat_btn = "CATeam 🐱🐱"
dv_btn = "DvTeam"
prequel_btn = "⬅️ Prequel"
sequel_btn = "Sequel ➡️"
close_btn = "Close ❌"


def site_search(update: Update, context: CallbackContext, site: str):
    message = update.effective_message
    args = message.text.strip().split(" ", 1)
    more_results = True

    try:
        search_query = args[1]
    except IndexError:
        message.reply_text("Give something to search")
        return

    if site == "kaizoku":
        search_url = f"https://animekaizoku.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {'class': "post-title"})

        if search_result:
            result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKaizoku</code>: \n"
            for entry in search_result:
                post_link = "https://animekaizoku.com/" + entry.a['href']
                post_name = html.escape(entry.text)
                result += f"• <a href='{post_link}'>{post_name}</a>\n"
        else:
            more_results = False
            result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKaizoku</code>"

    elif site == "kayo":
        search_url = f"https://animekayo.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {'class': "title"})

        result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKayo</code>: \n"
        for entry in search_result:

            if entry.text.strip() == "Nothing Found":
                result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKayo</code>"
                more_results = False
                break

            post_link = entry.a['href']
            post_name = html.escape(entry.text.strip())
            result += f"• <a href='{post_link}'>{post_name}</a>\n"
            
    elif site == "aat":
        search_url = f"https://animeacademy.in/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {'class': "title"}) 
        
        result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeAcedemyTeam</code>: \n"
        for entry in search_result:
                 
           if entry.text.strip() == "Nothing Found":
                result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeAcedemyTeam</code>"
                more_results = False
                break
                
           post_link = entry.a['href']
           post_name = html.escape(entry.text.strip())
           result += f"• <a href='{post_link}'>{post_name}</a>\n"

    elif site == "tpx":
        search_url = f"https://hindisub.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {'class': "title"}) 
        
        result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>TPX</code>: \n"
        for entry in search_result:
                 
           if entry.text.strip() == "Nothing Found":
                result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>TPX</code>"
                more_results = False
                break
                
           post_link = entry.a['href']
           post_name = html.escape(entry.text.strip())
           result += f"• <a href='{post_link}'>{post_name}</a>\n"
           
    elif site == "hsa":
        search_url = f"https://www.hsaanime.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {'class': "title"}) 
        
        result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>HindiSubAnime</code>: \n"
        for entry in search_result:
                 
           if entry.text.strip() == "Nothing Found":
                result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>HindiSubAnime</code>"
                more_results = False
                break
                
           post_link = entry.a['href']
           post_name = html.escape(entry.text.strip())
           result += f"• <a href='{post_link}'>{post_name}</a>\n"
           
    elif site == "ast":
        search_url = f"https://animesubingteam.000webhostapp.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {'class': "title"})

        result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeSubbingTeam</code>: \n"
        for entry in search_result:

            if entry.text.strip() == "Nothing Found":
                result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AST</code>"
                more_results = False
                break

            post_link = entry.a['href']
            post_name = html.escape(entry.text.strip())
            result += f"• <a href='{post_link}'>{post_name}</a>\n"

    elif site == "atf":
        search_url = f"https://atfanime.in/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {'class': "title"})

        result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>ATF Anime</code>: \n"
        for entry in search_result:

            if entry.text.strip() == "Nothing Found":
                result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>ATF</code>"
                more_results = False
                break

            post_link = entry.a['href']
            post_name = html.escape(entry.text.strip())
            result += f"• <a href='{post_link}'>{post_name}</a>\n"

    elif site == "an":
        search_url = f"https://www.plyton.in/search?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {'class': "title"})

        result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>Anime Nagri</code>: \n"
        for entry in search_result:

            if entry.text.strip() == "Nothing Found":
                result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>Anime Nagri</code>"
                more_results = False
                break

            post_link = entry.a['href']
            post_name = html.escape(entry.text.strip())
            result += f"• <a href='{post_link}'>{post_name}</a>\n"


    elif site == "dv":
        search_url = f"http://DvAnime.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {'class': "title"}) 
        
        result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>Dv Team</code>: \n"
        for entry in search_result:
                 
           if entry.text.strip() == "Nothing Found":
                result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>DV Team</code>"
                more_results = False
                break
                
           post_link = entry.a['href']
           post_name = html.escape(entry.text.strip())
           result += f"• <a href='{post_link}'>{post_name}</a>\n"


    elif site == "cat":
        search_url = f"https://catotakus.blogspot.com/search?q={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {'class': "title"})

        result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>CAT Anime</code>: \n"
        for entry in search_result:

            if entry.text.strip() == "Nothing Found":
                result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>CAT Anime</code>"
                more_results = False
                break

            post_link = entry.a['href']
            post_name = html.escape(entry.text.strip())
            result += f"• <a href='{post_link}'>{post_name}</a>\n"

    buttons = [[InlineKeyboardButton("See all results🔍", url=search_url)]]

    if more_results:
        message.reply_text(
            result,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True)
    else:
        message.reply_text(
            result, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


def kaizoku(update: Update, context: CallbackContext):
    site_search(update, context, "kaizoku")


def kayo(update: Update, context: CallbackContext):
    site_search(update, context, "kayo")
    
def aat(update: Update, context: CallbackContext):
    site_search(update, context, "aat")

def dv(update: Update, context: CallbackContext):
    site_search(update, context, "dv")

def tpx(update: Update, context: CallbackContext):
    site_search(update, context, "tpx")
   
def hsa(update: Update, context: CallbackContext):
    site_search(update, context, "hsa")
    
def ast(update: Update, context: CallbackContext):
    site_search(update, context, "ast")

def atf(update: Update, context: CallbackContext):
    site_search(update, context, "atf")

def an(update: Update, context: CallbackContext):
    site_search(update, context, "an")

def cat(update: Update, context: CallbackContext):
    site_search(update, context, "cat")
    

KAIZOKU_SEARCH_HANDLER = DisableAbleCommandHandler("kaizoku", kaizoku, run_async=True)
KAYO_SEARCH_HANDLER = DisableAbleCommandHandler("kayo", kayo, run_async=True)
AAT_SEARCH_HANDLER = DisableAbleCommandHandler("aat", aat, run_async=True)
TPX_SEARCH_HANDLER = DisableAbleCommandHandler("tpx", tpx, run_async=True)
HSA_SEARCH_HANDLER = DisableAbleCommandHandler("hsa", hsa, run_async=True)
AST_SEARCH_HANDLER = DisableAbleCommandHandler("ast", ast, run_async=True)
ATF_SEARCH_HANDLER = DisableAbleCommandHandler("atf", atf, run_async=True)
AN_SEARCH_HANDLER = DisableAbleCommandHandler("an", an, run_async=True)
CAT_SEARCH_HANDLER = DisableAbleCommandHandler("cat", cat, run_async=True)
DV_SEARCH_HANDLER = DisableAbleCommandHandler("dv", dv, run_async=True)


dispatcher.add_handler(KAIZOKU_SEARCH_HANDLER)
dispatcher.add_handler(KAYO_SEARCH_HANDLER)
dispatcher.add_handler(AAT_SEARCH_HANDLER)
dispatcher.add_handler(TPX_SEARCH_HANDLER)
dispatcher.add_handler(HSA_SEARCH_HANDLER)
dispatcher.add_handler(AST_SEARCH_HANDLER)
dispatcher.add_handler(ATF_SEARCH_HANDLER)
dispatcher.add_handler(AN_SEARCH_HANDLER)
dispatcher.add_handler(CAT_SEARCH_HANDLER)
dispatcher.add_handler(DV_SEARCH_HANDLER)

__handlers__ = [KAIZOKU_SEARCH_HANDLER, KAYO_SEARCH_HANDLER, AAT_SEARCH_HANDLER, TPX_SEARCH_HANDLER, HSA_SEARCH_HANDLER,  
                AST_SEARCH_HANDLER,  ATF_SEARCH_HANDLER, AN_SEARCH_HANDLER, CAT_SEARCH_HANDLER, DV_SEARCH_HANDLER]
