import sys
import asyncio
import os
import random
import telebot

# बोट डिटेल्स (अमरत भाई आपका ओरिजिनल टोकन और चैट आईडी)
BOT_TOKEN = "8760393896:AAECRmPN-1FatZuW3I_XzXp6lpDXpgm2i-Y"
bot = telebot.TeleBot(BOT_TOKEN)
CHAT_ID = "8571870755" 

# मशीन आईडी रिसीव करना
machine_id = sys.argv[1] if len(sys.argv) > 1 else "1"

async def human_delay(min_sec=5, max_sec=10):
    """इंसानी व्यवहार दिखाने के लिए रैंडम टाइम गैप"""
    await asyncio.sleep(random.uniform(min_sec, max_sec))

async def run_youtube_check():
    print(f"🚀 मशीन-{machine_id}: गिटहब क्लाउड पर 'असली क्रोम मोड' में चालू हो रही है...")
    
    # प्लेराइट को बिना आपके पीसी के लोड के गिटहब पर ही स्टार्ट करना
    from playwright.async_api import async_playwright
    
    try:
        async with async_playwright() as p:
            # 🎯 असली क्रोम चैनल को एक्टिवेट करना
            browser = await p.chromium.launch(
                headless=True,
                channel="chrome", 
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-infobars',
                    '--disable-gpu',
                    '--mute-audio'
                ]
            )
            
            # गिटहब के अमेरिकी आईपी के साथ टाइमज़ोन और भाषा मैच करना ताकि यूट्यूब शक न करे
            context = await browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                locale="en-US",
                timezone_id="America/New_York"
            )
            
            page = await context.new_page()
            
            # बोट डिटेक्शन को पूरी तरह चकमा देने वाली स्क्रिप्ट
            await page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                window.chrome = { runtime: {} };
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            """)
            
            # ======= स्टेप 1: यूट्यूब होमपेज पर जाना =======
            print(f"📡 मशीन-{machine_id}: यूट्यूब होमपेज लोड हो रहा है...")
            await page.goto("https://www.youtube.com", timeout=90000, wait_until="domcontentloaded")
            await human_delay(6, 12)
            
            # कुकीज़ या पॉपअप को हटाने के लिए थोड़ा नीचे स्क्रॉल करना
            await page.evaluate("window.scrollTo(0, 500);")
            await human_delay(3, 6)
            
            # होमपेज का स्क्रीनशॉट टेलीग्राम पर भेजना
            home_img = f"home_M{machine_id}.png"
            await page.screenshot(path=home_img)
            with open(home_img, 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption=f"📸 मशीन-{machine_id}: यूट्यूब होमपेज सक्सेस! (Real Chrome)")
            os.remove(home_img)
            
            # ======= स्टेप 2: रैंडम वीडियो प्ले करके एक्टिविटी दिखाना =======
            print(f"▶️ मशीन-{machine_id}: रैंडम वीडियो पर क्लिक करने की कोशिश...")
            video_links = await page.query_selector_all("a#video-title-link, ytd-rich-grid-media a[href*='/watch']")
            if video_links:
                chosen_video = random.choice(video_links[:3]) if len(video_links) > 3 else video_links[0]
                await chosen_video.click()
                await human_delay(12, 18)
                
                video_img = f"video_M{machine_id}.png"
                await page.screenshot(path=video_img)
                with open(video_img, 'rb') as f:
                    bot.send_photo(CHAT_ID, f, caption=f"▶️ मशीन-{machine_id}: वीडियो प्ले हो गया भाई!")
                os.remove(video_img)
            
            # ======= स्टेप 3: शॉर्ट्स पेज पर जाना =======
            print(f"🔥 मशीन-{machine_id}: शॉर्ट्स फीड बाईपास चेक...")
            await page.goto("https://www.youtube.com/shorts", timeout=90000, wait_until="domcontentloaded")
            await human_delay(8, 15)
            
            # शॉर्ट्स का लाइव स्क्रीनशॉट भेजना
            shorts_img = f"shorts_M{machine_id}.png"
            await page.screenshot(path=shorts_img)
            with open(shorts_img, 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption=f"🔥 मशीन-{machine_id}: शॉर्ट्स लाइव चल गई बिना किसी एरर के!")
            os.remove(shorts_img)

            # ब्राउज़र क्लोज करना
            await browser.close()
            print(f"✅ मशीन-{machine_id}: पूरा टास्क बिना किसी रुकावट के खत्म हुआ।")
            
    except Exception as e:
        print(f"❌ मशीन-{machine_id} एरर: {str(e)}")
        try:
            bot.send_message(CHAT_ID, f"❌ मशीन-{machine_id} एरर विवरण:\n{str(e)[:150]}")
        except:
            pass

if __name__ == "__main__":
    asyncio.run(run_youtube_check())
