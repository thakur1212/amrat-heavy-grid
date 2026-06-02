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

# सर्च करने के लिए कुछ बिल्कुल साधारण कीवर्ड्स
SEARCH_KEYWORDS = ["technology updates 2026", "new tech gadgets", "amazing facts", "gaming highlights"]

async def run_youtube_check():
    print(f"🚀 मशीन-{machine_id} [PC इन्कॉग्निटो मोड] में स्टार्ट हो रही है...")
    try:
        async with async_playwright() as p:
            # क्रोमियम (Chromium) का इस्तेमाल करेंगे जो बिल्कुल आपके पीसी के क्रोम/इन्कॉग्निटो जैसा काम करेगा
            browser = await p.chromium.launch(headless=True)
            
            # हुबहू आपके पीसी के इन्कॉग्निटो ब्राउज़र की सेटिंग
            context = await browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                locale="en-IN",
                timezone_id="Asia/Kolkata",
                accept_downloads=False
            )
            
            page = await context.new_page()
            
            # 🔥 सीक्रेट बाईपास: यूट्यूब को पूरी तरह धोखा देने के लिए ब्राउज़र की अंदरूनी सेटिंग्स बदलना
            await page.add_init_script("""
                # 1. वेबड्राइवर सिग्नल को डिलीट करना
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                # 2. नकली क्रोम टोकन डालना
                window.chrome = { runtime: {}, loadTimes: function() {}, csi: function() {} };
                # 3. नकली लैंग्वेजेस और प्लेटफॉर्म सेट करना
                Object.defineProperty(navigator, 'languages', {get: () => ['en-IN', 'en-US', 'hi']});
                Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
                # 4. नकली सिग्नल्स ताकि यूट्यूब बोट न पकड़ पाए
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ? Promise.resolve({ state: Notification.permission }) : originalQuery(parameters)
                );
            """)
            
            # ====== STEP 1: यूट्यूब लोड करना ======
            print("⏳ यूट्यूब पर पीसी यूजर की तरह एंट्री हो रही है...")
            await page.goto("https://www.youtube.com", timeout=60000, wait_until="networkidle")
            await asyncio.sleep(5)
            
            # होमपेज का स्क्रीनशॉट
            home_img = f"1_home_M{machine_id}.png"
            await page.screenshot(path=home_img)
            with open(home_img, 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption=f"📸 मशीन-{machine_id}: [PC मोड] यूट्यूब होमपेज!")
            os.remove(home_img)
            
            # ====== STEP 2: सर्च बार का उपयोग करके वीडियो प्ले करना ======
            search_keyword = random.choice(SEARCH_KEYWORDS)
            print(f"🔍 सर्च बॉक्स में टाइप किया जा रहा है: {search_keyword}")
            
            search_input = await page.wait_for_selector("input[name='search_query']", timeout=10000)
            if search_input:
                # इंसानों की तरह धीरे-धीरे टाइप करना (Human-like typing delay)
                await search_input.click()
                for char in search_keyword:
                    await page.keyboard.write(char)
                    await asyncio.sleep(random.uniform(0.1, 0.3))
                
                await asyncio.sleep(1)
                await search_input.press("Enter")
                print("⚡ सर्च बटन दबा दिया गया है...")
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(5)
            
            # वीडियो ढूंढकर उसपर असली माउस की तरह क्लिक करना
            print("⏳ वीडियो पर माउस ले जाकर क्लिक किया जा रहा है...")
            await page.evaluate("window.scrollTo(0, 200)")
            await asyncio.sleep(2)
            
            # सर्च रिजल्ट की पहली वीडियो का लिंक निकालना
            video_link = await page.wait_for_selector("ytd-video-renderer a#video-title-link", timeout=10000)
            if video_link:
                # माउस को पहले लिंक पर ले जाओ (Hover) फिर क्लिक करो
                await video_link.hover()
                await asyncio.sleep(1)
                await video_link.click()
                
                print("▶️ लॉन्ग वीडियो प्ले हो चुकी है! 15 सेकंड चलने देते हैं...")
                await asyncio.sleep(15)
                
                long_video_img = f"2_long_M{machine_id}.png"
                await page.screenshot(path=long_video_img)
                with open(long_video_img, 'rb') as f:
                    bot.send_photo(CHAT_ID, f, caption=f"▶️ मशीन-{machine_id}: [PC मोड] वीडियो सफलतापूर्वक चल रही है अमरत भाई!")
                os.remove(long_video_img)
            else:
                print("❌ सर्च रिजल्ट में कोई वीडियो लिंक नहीं मिला।")
                
            # ====== STEP 3: शॉर्ट्स खोलना ======
            print("⏳ अब शॉर्ट्स सेक्शन की चेकिंग...")
            await page.goto("https://www.youtube.com/shorts", timeout=60000, wait_until="networkidle")
            await asyncio.sleep(8)
            
            shorts_img = f"3_shorts_M{machine_id}.png"
            await page.screenshot(path=shorts_img)
            with open(shorts_img, 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption=f"🔥 मशीन-{machine_id}: [PC मोड] यूट्यूब शॉर्ट्स चालू है!")
            os.remove(shorts_img)

            await browser.close()
            print(f"✅ मशीन-{machine_id} का काम पूरा हुआ!")
            
    except Exception as e:
        print(f"❌ मशीन-{machine_id} एरर आया: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_youtube_check())
