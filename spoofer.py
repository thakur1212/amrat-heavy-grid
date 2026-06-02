import sys
import asyncio
import os
import shutil
import random
import telebot
from playwright.async_api import async_playwright

BOT_TOKEN = "8760393896:AAECRmPN-1FatZuW3I_XzXp6lpDXpgm2i-Y"
bot = telebot.TeleBot(BOT_TOKEN)
CHAT_ID = "8571870755" # 🚨 अमरत भाई अपनी असली चैट आईडी यहाँ डालना

machine_id = sys.argv[1] if len(sys.argv) > 1 else "1"

async def run_youtube_with_pc_profile():
    print(f"🚀 मशीन-{machine_id} गिटहब सर्वर पर अमरत भाई की क्रोम प्रोफाइल के साथ शुरू हो रही है...")
    
    # गिटहब सर्वर पर तुम्हारी पीसी वाली कुकीज़ को अनज़िप करना
    user_data_dir = f"./chrome_profile_m{machine_id}"
    if os.path.exists("Default.zip"):
        shutil.unpack_archive("Default.zip", user_data_dir)

    try:
        async with async_playwright() as p:
            # 🔥 सारा लोड गिटहब पर पड़ेगा, पर प्रोफाइल तुम्हारी यूज़ होगी!
            context = await p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=True,
                viewport={"width": 1366, "height": 768},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            )
            
            page = context.pages[0] if context.pages else await context.new_page()
            
            print("⏳ यूट्यूब लोड हो रहा है...")
            await page.goto("https://www.youtube.com", timeout=60000, wait_until="networkidle")
            await asyncio.sleep(5)
            
            # स्क्रीनशॉट लेकर टेलीग्राम पर भेजना
            img_path = f"pc_profile_M{machine_id}.png"
            await page.screenshot(path=img_path)
            with open(img_path, 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption=f"📸 मशीन-{machine_id}: लोड गिटहब का है, पर क्रोम प्रोफाइल अमरत भाई की है!")
            os.remove(img_path)
            
            await context.close()
            
    except Exception as e:
        print(f"❌ एरर आया: {str(e)}")
    finally:
        # काम खत्म होने के बाद गिटहब सर्वर से कचरा साफ़ करना
        if os.path.exists(user_data_dir):
            shutil.rmtree(user_data_dir)

if __name__ == "__main__":
    asyncio.run(run_youtube_with_pc_profile())
