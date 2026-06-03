import asyncio
import random
import sys
import telebot
from playwright.async_api import async_playwright
# 🛠️ यहाँ बदलाव किया है: सीधे stealth इम्पोर्ट करेंगे
from playwright_stealth import stealth

# अपनी सेटिंग्स
BOT_TOKEN = "8760393896:AAECRmPN-1FatZuW3I_XzXp6lpDXpgm2i-Y"
CHAT_ID = "8571870755" # अपनी टेलीग्राम चैट आईडी यहाँ डालें
bot = telebot.TeleBot(BOT_TOKEN)

machine_id = sys.argv[1] if len(sys.argv) > 1 else "1"

async def run_automation():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        # 🛠️ यहाँ भी बदलाव किया है: stealth(page) का इस्तेमाल करेंगे
        await stealth(page)

        try:
            print(f"🚀 मशीन-{machine_id}: यूट्यूब होमपेज पर जा रहे हैं...")
            # 1. होमपेज स्क्रीनशॉट
            await page.goto("https://www.youtube.com")
            await asyncio.sleep(7) # पेज ठीक से लोड होने का समय
            await page.screenshot(path=f"home_{machine_id}.png")
            with open(f"home_{machine_id}.png", "rb") as photo:
                bot.send_photo(CHAT_ID, photo, caption=f"📸 मशीन-{machine_id}: यूट्यूब होमपेज")

            print(f"🔥 मशीन-{machine_id}: शॉर्ट्स पेज पर जा रहे हैं...")
            # 2. शॉर्ट्स पेज
            await page.goto("https://www.youtube.com/shorts")
            await asyncio.sleep(10) # शॉर्ट्स और रील्स लोड होने का समय
            await page.screenshot(path=f"shorts_{machine_id}.png")
            with open(f"shorts_{machine_id}.png", "rb") as photo:
                bot.send_photo(CHAT_ID, photo, caption=f"🔥 मशीन-{machine_id}: यूट्यूब शॉर्ट्स")

            bot.send_message(CHAT_ID, f"✅ अमरत भाई, मशीन-{machine_id} का काम पूरा हो गया है!")
            
        except Exception as e:
            bot.send_message(CHAT_ID, f"❌ एरर मशीन-{machine_id}: {str(e)}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_automation())
