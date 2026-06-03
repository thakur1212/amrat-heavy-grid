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
    print(f"🚀 मशीन-{machine_id}: डकडकगो री-रूट मोड चालू...")
    from playwright.async_api import async_playwright
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-infobars'
                ]
            )
            
            context = await browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            )
            
            page = await context.new_page()
            await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # 🎯 हटके जुगाड़: डायरेक्ट यूट्यूब न खोलकर, DuckDuckGo के रास्ते इमेज/पेज फेच करना
            # यह यूट्यूब के बोट फिल्टर को पूरी तरह अंधा कर देता है
            print(f"📡 मशीन-{machine_id}: डकडकगो प्रॉक्सी टनलिंग...")
            ddg_url = f"https://html.duckduckgo.com/html?q=site:youtube.com/shorts"
            await page.goto(ddg_url, timeout=90000)
            await human_delay(4, 7)
            
            # अब यहाँ से सीधे यूट्यूब शॉर्ट्स पर जंप मारना ताकि रेफरर हेडर (Referer Header) बदल जाए
            print(f"🔥 मशीन-{machine_id}: असली शॉर्ट्स पर डाइव मार रहे हैं...")
            await page.goto("https://www.youtube.com/shorts", timeout=90000)
            await human_delay(8, 15)
            
            shorts_img = f"shorts_M{machine_id}.png"
            await page.screenshot(path=shorts_img)
            with open(shorts_img, 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption=f"🔥 मशीन-{machine_id}: डकडकगो रूट से शॉर्ट्स बाईपास डन!")
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
