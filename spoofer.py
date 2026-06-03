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
    print(f"🚀 मशीन-{machine_id}: टनल मोड में स्टार्ट हो रही है...")
    from playwright.async_api import async_playwright
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-infobars'
                ],
                # 🎯 गिटहब के अंदर बनी लोकल टनल से ट्रैफिक भेजना (0% PC Load)
                proxy={
                    "server": "http://127.0.0.1:8118"
                }
            )
            
            context = await browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                locale="hi-IN",
                timezone_id="Asia/Kolkata"
            )
            
            page = await context.new_page()
            await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print(f"📡 मशीन-{machine_id}: यूट्यूब पर जा रहे हैं...")
            await page.goto("https://www.youtube.com", timeout=90000)
            await human_delay(6, 12)
            
            home_img = f"home_M{machine_id}.png"
            await page.screenshot(path=home_img)
            with open(home_img, 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption=f"📸 मशीन-{machine_id}: यूट्यूब होमपेज (Tunnel Mode)")
            os.remove(home_img)
            
            print(f"🔥 मशीन-{machine_id}: शॉर्ट्स चेक...")
            await page.goto("https://www.youtube.com/shorts", timeout=90000)
            await human_delay(8, 15)
            
            shorts_img = f"shorts_M{machine_id}.png"
            await page.screenshot(path=shorts_img)
            with open(shorts_img, 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption=f"🔥 मशीन-{machine_id}: शॉर्ट्स लाइव डन!")
            os.remove(shorts_img)

            await browser.close()
            
    except Exception as e:
        print(f"❌ मशीन-{machine_id} एरर: {str(e)}")
        try:
            bot.send_message(CHAT_ID, f"❌ मशीन-{machine_id} एरर:\n{str(e)[:150]}")
        except:
            pass

if __name__ == "__main__":
    asyncio.run(run_youtube_check())
