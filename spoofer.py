import sys
import asyncio
import os
import random
import telebot

BOT_TOKEN = "8760393896:AAECRmPN-1FatZuW3I_XzXp6lpDXpgm2i-Y"
bot = telebot.TeleBot(BOT_TOKEN)
CHAT_ID = "8571870755" 

machine_id = sys.argv[1] if len(sys.argv) > 1 else "1"

async def human_delay(min_sec=5, max_sec=10):
    await asyncio.sleep(random.uniform(min_sec, max_sec))

async def run_youtube_check():
    print(f"🚀 मशीन-{machine_id}: ScraperAPI मोड में चालू हो रही है...")
    from playwright.async_api import async_playwright
    
    # गिटहब सीक्रेट से एपीआई की (Key) उठाना
    api_key = os.environ.get("SCRAPER_API_KEY")
    if not api_key:
        print("❌ एरर: GitHub Secrets में SCRAPER_API_KEY नहीं मिला!")
        bot.send_message(CHAT_ID, f"❌ मशीन-{machine_id}: कृपया गिटहब सीक्रेट्स में SCRAPER_API_KEY सेट करें!")
        return

    try:
        async with async_playwright() as p:
            # 🎯 कड़क जुगाड़: ScraperAPI के रोटेटिंग प्रॉक्सी सर्वर को प्लेराइट में जोड़ना
            # यह गिटहब की आईपी को छुपाकर हर बार असली मोबाइल/घर की आईपी बनाएगा
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-infobars',
                    '--ignore-certificate-errors' # एपीआई के टनल सर्टिफिकेट एरर को बायपास करने के लिए
                ],
                proxy={
                    "server": "http://proxy-server.scraperapi.com:8001",
                    "username": f"scraperapi",
                    "password": api_key
                }
            )
            
            context = await browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            )
            
            page = await context.new_page()
            await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # ======= स्टेप 1: यूट्यूब होमपेज =======
            print(f"📡 मशीन-{machine_id}: कड़क आईपी के साथ यूट्यूब लोड हो रहा है...")
            await page.goto("https://www.youtube.com", timeout=90000, wait_until="domcontentloaded")
            await human_delay(6, 12)
            
            home_img = f"home_M{machine_id}.png"
            await page.screenshot(path=home_img)
            with open(home_img, 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption=f"📸 मशीन-{machine_id}: यूट्यूब होमपेज (ScraperAPI बाईपास सक्सेस!)")
            os.remove(home_img)
            
            # ======= स्टेप 2: शॉर्ट्स फीड =======
            print(f"🔥 मशीन-{machine_id}: शॉर्ट्स पर जा रहे हैं...")
            await page.goto("https://www.youtube.com/shorts", timeout=90000, wait_until="domcontentloaded")
            await human_delay(8, 15)
            
            shorts_img = f"shorts_M{machine_id}.png"
            await page.screenshot(path=shorts_img)
            with open(shorts_img, 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption=f"🔥 मशीन-{machine_id}: शॉर्ट्स एकदम लाइव चल गई!")
            os.remove(shorts_img)

            await browser.close()
            print(f"✅ मशीन-{machine_id}: टास्क बिना एरर के पूरा हुआ।")
            
    except Exception as e:
        print(f"❌ मशीन-{machine_id} एरर: {str(e)}")
        try:
            bot.send_message(CHAT_ID, f"❌ मशीन-{machine_id} एरर:\n{str(e)[:150]}")
        except:
            pass

if __name__ == "__main__":
    asyncio.run(run_youtube_check())
