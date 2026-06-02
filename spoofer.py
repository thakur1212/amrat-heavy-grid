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
            browser = await p.firefox.launch(headless=True)
            context = await browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0"
            )
            page = await context.new_page()
            
            # ====== STEP 1: यूट्यूब होमपेज खोलना ======
            print("⏳ यूट्यूब होमपेज लोड हो रहा है...")
            await page.goto("https://www.youtube.com", timeout=60000, wait_until="networkidle")
            await asyncio.sleep(5)
            
            home_img = f"1_home_M{machine_id}.png"
            await page.screenshot(path=home_img)
            with open(home_img, 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption=f"📸 मशीन-{machine_id}: [STEP 1] यूट्यूब होमपेज!")
            os.remove(home_img)
            
            # ====== STEP 2: डायरेक्ट यूट्यूब शॉर्ट्स खोलना ======
            print("⏳ यूट्यूब शॉर्ट्स लोड हो रहा है...")
            await page.goto("https://www.youtube.com/shorts", timeout=60000, wait_until="networkidle")
            await asyncio.sleep(8)
            
            shorts_img = f"2_shorts_M{machine_id}.png"
            await page.screenshot(path=shorts_img)
            with open(shorts_img, 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption=f"🔥 मशीन-{machine_id}: [STEP 2] यूट्यूब शॉर्ट्स चालू है!")
            os.remove(shorts_img)
                
            # ====== STEP 3: वापस होमपेज पर जाकर लॉन्ग वीडियो प्ले करना ======
            print("⏳ वापस होमपेज पर जाकर लॉन्ग वीडियो ढूंढी जा रही है...")
            await page.goto("https://www.youtube.com", timeout=60000, wait_until="networkidle")
            await asyncio.sleep(5)
            
            # होमपेज पर जो भी पहली लंबी वीडियो दिखे, उसपर क्लिक करना
            video_links = await page.query_selector_all("a#video-title-link, ytd-rich-grid-media a#video-title")
            if video_links:
                await video_links[0].click()
                print("⏳ लॉन्ग वीडियो प्ले हो रही है, 12 सेकंड का वेट...")
                await asyncio.sleep(12) # वीडियो को थोड़ा चलने दो
                
                long_video_img = f"3_long_M{machine_id}.png"
                await page.screenshot(path=long_video_img)
                with open(long_video_img, 'rb') as f:
                    bot.send_photo(CHAT_ID, f, caption=f"▶️ मशीन-{machine_id}: [STEP 3] लंबी वीडियो (Long Video) सक्सेसफुली चल रही है!")
                os.remove(long_video_img)
            else:
                print("❌ कोई लॉन्ग वीडियो लिंक नहीं मिला")

            await browser.close()
            print(f"✅ मशीन-{machine_id} का काम पूरा हुआ!")
            
    except Exception as e:
        print(f"❌ मशीन-{machine_id} एरर: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_youtube_check())
