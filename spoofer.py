import sys
import asyncio
import os
import telebot
from playwright.async_api import async_playwright

BOT_TOKEN = "8760393896:AAECRmPN-1FatZuW3I_XzXp6lpDXpgm2i-Y"
bot = telebot.TeleBot(BOT_TOKEN)

# 🚨 अमरत भाई, यहाँ अपनी असली टेलीग्राम चैट आईडी डाल देना
CHAT_ID = "8571870755" 

machine_id = sys.argv[1] if len(sys.argv) > 1 else "1"

async def run_youtube_check():
    print(f"🚀 मशीन-{machine_id} स्टार्ट हो रही है...")
    try:
        async with async_playwright() as p:
            # बिना किसी प्रॉक्सी या टोर के सीधा और तेज़ फ़ायरफ़ॉक्स
            browser = await p.firefox.launch(headless=True)
            context = await browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0"
            )
            page = await context.new_page()
            
            # ====== 1. यूट्यूब होमपेज ======
            await page.goto("https://www.youtube.com", timeout=60000, wait_until="networkidle")
            await asyncio.sleep(5)
            home_img = f"home_M{machine_id}.png"
            await page.screenshot(path=home_img)
            with open(home_img, 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption=f"📸 मशीन-{machine_id}: यूट्यूब होमपेज!")
            os.remove(home_img)
            
            # ====== 2. रैंडम वीडियो प्ले ======
            video_links = await page.query_selector_all("a#video-title-link, ytd-rich-grid-media a")
            if video_links:
                await video_links[0].click()
                await asyncio.sleep(10)
                video_img = f"video_M{machine_id}.png"
                await page.screenshot(path=video_img)
                with open(video_img, 'rb') as f:
                    bot.send_photo(CHAT_ID, f, caption=f"▶️ मशीन-{machine_id}: रैंडम वीडियो चालू है!")
                os.remove(video_img)
                
            # ====== 3. यूट्यूब शॉर्ट्स ======
            await page.goto("https://www.youtube.com/shorts", timeout=60000)
            await asyncio.sleep(8)
            shorts_img = f"shorts_M{machine_id}.png"
            await page.screenshot(path=shorts_img)
            with open(shorts_img, 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption=f"🔥 मशीन-{machine_id}: शॉर्ट्स चालू है!")
            os.remove(shorts_img)

            await browser.close()
            
    except Exception as e:
        print(f"❌ मशीन-{machine_id} एरर: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_youtube_check())
