import sys
import asyncio
import os
import random
import telebot
from playwright.async_api import async_playwright

BOT_TOKEN = "8760393896:AAECRmPN-1FatZuW3I_XzXp6lpDXpgm2i-Y"
bot = telebot.TeleBot(BOT_TOKEN)
CHAT_ID = "8571870755" 

machine_id = sys.argv[1] if len(sys.argv) > 1 else "1"

# 🌐 आपका लाइव Ngrok लिंक यहाँ है
YOUR_PC_PROXY = "https://unmodificative-hostless-destinee.ngrok-free.dev"

async def human_delay(min_sec=3, max_sec=6):
    await asyncio.sleep(random.uniform(min_sec, max_sec))

async def run_youtube_check():
    print(f"🚀 मशीन-{machine_id} गिटहब पर स्टार्ट हो रही है (Tunnel Fix Active)...")
    try:
        async with async_playwright() as p:
            
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-infobars',
                    '--window-size=1366,768',
                    '--ignore-certificate-errors' # 🛠️ टनल के सर्टिफिकेट एरर को बायपास करने के लिए
                ],
                # 🎯 टनल कनेक्शन फेल होने से बचाने के लिए डायरेक्ट सर्वर पास किया
                proxy={
                    "server": YOUR_PC_PROXY
                }
            )
            
            context = await browser.new_context(
                viewport={"width": 1366, "height": 768},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                locale="hi-IN",
                timezone_id="Asia/Kolkata"
            )
            
            page = await context.new_page()
            await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # ====== 1. यूट्यूब होमपेज ======
            print(f"📡 मशीन-{machine_id}: टनल के रास्ते यूट्यूब होमपेज पर जा रहे हैं...")
            # टनल स्लो होने के कारण और कनेक्शन एस्टेब्लिश करने के लिए wait_until को हटाकर लोड टाइम दिया
            await page.goto("https://www.youtube.com", timeout=90000)
            await human_delay(6, 10)
            
            home_img = f"home_M{machine_id}.png"
            await page.screenshot(path=home_img)
            with open(home_img, 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption=f"📸 मशीन-{machine_id}: यूट्यूब होमपेज लोड हुआ! (Tunnel Fixed)")
            os.remove(home_img)
            
            # ====== 2. रैंडम वीडियो प्ले ======
            video_links = await page.query_selector_all("a#video-title-link, ytd-rich-grid-media a[href*='/watch']")
            if video_links:
                chosen_video = random.choice(video_links[:3]) if len(video_links) > 3 else video_links[0]
                await chosen_video.click()
                print(f"▶️ मशीन-{machine_id}: वीडियो पर क्लिक हो गया है...")
                await human_delay(12, 18)
                
                video_img = f"video_M{machine_id}.png"
                await page.screenshot(path=video_img)
                with open(video_img, 'rb') as f:
                    bot.send_photo(CHAT_ID, f, caption=f"▶️ मशीन-{machine_id}: वीडियो सक्सेसफुली प्ले हुआ!")
                os.remove(video_img)
                
            # ====== 3. यूट्यूब शॉर्ट्स ======
            print(f"🔥 मशीन-{machine_id}: शॉर्ट्स पेज लोड हो रहा है...")
            await page.goto("https://www.youtube.com/shorts", timeout=90000)
            await human_delay(8, 14)
            
            shorts_img = f"shorts_M{machine_id}.png"
            await page.screenshot(path=shorts_img)
            with open(shorts_img, 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption=f"🔥 मशीन-{machine_id}: शॉर्ट्स फीड बाईपास डन!")
            os.remove(shorts_img)

            await browser.close()
            print(f"✅ मशीन-{machine_id}: पूरा काम हो गया।")
            
    except Exception as e:
        print(f"❌ मशीन-{machine_id} एरर: {str(e)}")
        try:
            bot.send_message(CHAT_ID, f"❌ मशीन-{machine_id} टनल/प्रॉक्सी एरर:\n{str(e)[:150]}")
        except:
            pass

if __name__ == "__main__":
    asyncio.run(run_youtube_check())
