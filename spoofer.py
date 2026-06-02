import sys
import asyncio
import os
import random
import telebot
from playwright.async_api import async_playwright

BOT_TOKEN = "8760393896:AAECRmPN-1FatZuW3I_XzXp6lpDXpgm2i-Y"
bot = telebot.TeleBot(BOT_TOKEN)

# 🚨 अमरत भाई, यहाँ अपनी असली टेलीग्राम चैट आईडी डाल देना
CHAT_ID = "8571870755" 

machine_id = sys.argv[1] if len(sys.argv) > 1 else "1"

# रैंडम सर्च कीवर्ड्स ताकि यूट्यूब को शक न हो
SEARCH_KEYWORDS = ["trending video 2026", "new shorts", "amazing facts", "funny video", "viral shorts"]

async def run_youtube_check():
    print(f"🚀 मशीन-{machine_id} एंटी-बॉट मोड में स्टार्ट हो रही है...")
    try:
        async with async_playwright() as p:
            # 1. बिल्कुल असली दिखने वाला ब्राउज़र कॉन्फ़िगरेशन
            browser = await p.firefox.launch(headless=True)
            context = await browser.new_context(
                viewport={"width": 1366, "height": 768},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                locale="en-US",
                timezone_id="Asia/Kolkata"
            )
            
            # 🕵️ सीक्रेट लॉजिक: ऑटोमेशन के सिग्नल्स को छुपाना (Stealth)
            page = await context.new_page()
            await page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                window.chrome = { runtime: {} };
            """)
            
            # ====== STEP 1: यूट्यूब खोलना और सर्च करना ======
            print("⏳ यूट्यूब पर असली यूजर की तरह सर्च किया जा रहा है...")
            await page.goto("https://www.youtube.com", timeout=60000, wait_until="load")
            await asyncio.sleep(4)
            
            # खाली होमपेज का स्क्रीनशॉट ले लो पहले
            home_img = f"1_home_M{machine_id}.png"
            await page.screenshot(path=home_img)
            with open(home_img, 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption=f"📸 मशीन-{machine_id}: [STEP 1] यूट्यूब होमपेज!")
            os.remove(home_img)
            
            # यूट्यूब के सर्च बॉक्स में रैंडम कीवर्ड डालना
            search_keyword = random.choice(SEARCH_KEYWORDS)
            search_input = await page.wait_for_selector("input[name='search_query']", timeout=15000)
            if search_input:
                await search_input.fill(search_keyword)
                await asyncio.sleep(1)
                await search_input.press("Enter")
                print(f"🔍 '{search_keyword}' सर्च कर दिया गया है...")
                await asyncio.sleep(5)
            
            # ====== STEP 2: सर्च रिजल्ट से लॉन्ग वीडियो प्ले करना ======
            print("⏳ सर्च रिजल्ट से लंबी वीडियो ढूंढी जा रही है...")
            # गिटहब सर्वर्स पर वीडियो रेंडर होने में टाइम लगता है, इसलिए थोड़ा वेट
            await page.evaluate("window.scrollTo(0, 300)")
            await asyncio.sleep(2)
            
            video_selectors = [
                "ytd-video-renderer a#video-title", 
                "ytd-search a#video-title-link",
                "a[href*='/watch']"
            ]
            
            video_clicked = False
            for selector in video_selectors:
                links = await page.query_selector_all(selector)
                if links:
                    # पहली या दूसरी वीडियो पर रैंडमली क्लिक करना ताकि पैटर्न न बने
                    idx = 0 if len(links) == 1 else random.randint(0, 1)
                    await links[idx].click()
                    video_clicked = True
                    break
            
            if video_clicked:
                print("⏳ लॉन्ग वीडियो प्ले हो गई है, 15 सेकंड का वॉच टाइम...")
                await asyncio.sleep(15)
                
                long_video_img = f"2_long_M{machine_id}.png"
                await page.screenshot(path=long_video_img)
                with open(long_video_img, 'rb') as f:
                    bot.send_photo(CHAT_ID, f, caption=f"▶️ मशीन-{machine_id}: [STEP 2] सर्च करके लॉन्ग वीडियो चला दी!")
                os.remove(long_video_img)
            else:
                print("❌ कोई डायरेक्ट वीडियो लिंक क्लिक नहीं हो पाया")

            # ====== STEP 3: एंटी-बॉट बाईपास करके शॉर्ट्स खोलना ======
            print("⏳ अब शॉर्ट्स सेक्शन की तरफ बढ़ रहे हैं...")
            # डायरेक्ट /shorts यूआरएल की जगह हम सर्च करके शॉर्ट्स पर जाएंगे ताकि 'Not a bot' एरर न आए
            await page.goto(f"https://www.youtube.com/results?search_query={search_keyword}+shorts", timeout=60000)
            await asyncio.sleep(5)
            
            shorts_link = await page.query_selector("a[href*='/shorts/']")
            if shorts_link:
                await shorts_link.click()
                print("⏳ शॉर्ट्स पर क्लिक कर दिया है...")
                await asyncio.sleep(10)
            else:
                # अगर क्लिक न हो तो बैकअप में डायरेक्ट यूआरएल लगा रखा है
                await page.goto("https://www.youtube.com/shorts", timeout=60000)
                await asyncio.sleep(8)
                
            shorts_img = f"3_shorts_M{machine_id}.png"
            await page.screenshot(path=shorts_img)
            with open(shorts_img, 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption=f"🔥 मशीन-{machine_id}: [STEP 3] यूट्यूब शॉर्ट्स स्टेटस!")
            os.remove(shorts_img)

            await browser.close()
            print(f"✅ मशीन-{machine_id} का एंटी-बॉट मिशन पूरा!")
            
    except Exception as e:
        print(f"❌ मशीन-{machine_id} फेल हुई: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_youtube_check())
