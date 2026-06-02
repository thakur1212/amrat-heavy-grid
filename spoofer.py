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
SEARCH_KEYWORDS = ["technology updates 2026", "new tech gadgets", "amazing facts", "gaming highlights", "lofi songs hindi"]

# 🖱️ असली इंसान की तरह माउस हिलाने का लॉजिक
async def human_mouse_move(page, start_x, start_y, end_x, end_y, steps=10):
    for i in range(steps):
        # रैंडम टेढ़े-मेढ़े रास्ते से माउस ले जाना ताकि रोबोटिक न लगे
        current_x = start_x + (end_x - start_x) * (i / steps) + random.randint(-3, 3)
        current_y = start_y + (end_y - start_y) * (i / steps) + random.randint(-3, 3)
        await page.mouse.move(current_x, current_y)
        await asyncio.sleep(random.uniform(0.01, 0.03))

async def run_youtube_check():
    print(f"🚀 मशीन-{machine_id} [अल्ट्रा-ह्यूमन मोड] में स्टार्ट हो रही है...")
    try:
        async with async_playwright() as p:
            # क्रोमियम का इस्तेमाल करेंगे जो बिल्कुल नॉर्मल क्रोम ब्राउज़र है
            browser = await p.chromium.launch(headless=True)
            
            context = await browser.new_context(
                viewport={"width": 1366, "height": 768},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                locale="en-IN",
                timezone_id="Asia/Kolkata",
                has_touch=False
            )
            
            page = await context.new_page()
            
            # 🔥 सुपर सीक्रेट बाईपास: यूट्यूब को 100% यकीन दिलाना कि यह असली पीसी है
            await page.add_init_script("""
                # 1. वेबड्राइवर सिग्नल को खत्म करना
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                
                # 2. नकली 8GB रैम और 4-कोर प्रोसेसर दिखाना
                Object.defineProperty(navigator, 'deviceMemory', {get: () => 8});
                Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 4});
                
                # 3. नकली ग्राफिक्स कार्ड सेट करना (NVIDIA GeForce) ताकि डेटा सेंटर न पकड़ा जाए
                const getParameter = WebGLRenderingContext.prototype.getParameter;
                WebGLRenderingContext.prototype.getParameter = function(parameter) {
                    if (parameter === 37445) return 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 Direct3D11 vs_5_0 ps_5_0, ps_5_0)';
                    if (parameter === 37446) return 'Google Inc. (NVIDIA)';
                    return getParameter.apply(this, arguments);
                };
                
                # 4. नकली बैटरी स्टेटस दिखाना (95% चार्ज्ड और प्लग्ड इन)
                navigator.getBattery = () => Promise.resolve({
                    charging: true,
                    chargingTime: 0,
                    dischargingTime: Infinity,
                    level: 0.95
                });
                
                # 5. नकली प्लगइन्स की लिस्ट जोड़ना जो हर पीसी में होती हैं
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            """)
            
            # ====== STEP 1: यूट्यूब ओपन करना ======
            print("⏳ यूट्यूब लोड हो रहा है...")
            await page.goto("https://www.youtube.com", timeout=60000, wait_until="networkidle")
            await asyncio.sleep(random.uniform(4, 6)) # रैंडम टाइम वेट ताकि पैटर्न न बने
            
            home_img = f"1_home_M{machine_id}.png"
            await page.screenshot(path=home_img)
            with open(home_img, 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption=f"📸 मशीन-{machine_id}: [ह्यूमन मोड] होमपेज लोड हुआ!")
            os.remove(home_img)
            
            # ====== STEP 2: इंसानी स्टाइल में सर्च करना ======
            search_keyword = random.choice(SEARCH_KEYWORDS)
            search_input = await page.wait_for_selector("input[name='search_query']", timeout=12000)
            
            if search_input:
                # माउस को धीरे से सर्च बॉक्स पर ले जाकर क्लिक करना
                box = await search_input.bounding_box()
                await human_mouse_move(page, 100, 100, box['x'] + 10, box['y'] + 10)
                await search_input.click()
                await asyncio.sleep(0.5)
                
                # इंसानी उंगलियों की तरह रैंडम स्पीड में टाइप करना
                for char in search_keyword:
                    await page.keyboard.write(char)
                    await asyncio.sleep(random.uniform(0.15, 0.35))
                
                await asyncio.sleep(1)
                await search_input.press("Enter")
                print(f"🔍 सर्च कर दिया: {search_keyword}")
                await asyncio.sleep(6)
            
            # ====== STEP 3: वीडियो ढूंढना और नेचुरल स्क्रॉल करना ======
            print("⏳ पेज को धीरे-धीरे नीचे स्क्रॉल किया जा रहा है...")
            # असली यूजर की तरह पहले थोड़ा नीचे और फिर थोड़ा ऊपर स्क्रॉल करना
            await page.evaluate("window.scrollBy(0, 400);")
            await asyncio.sleep(1.5)
            await page.evaluate("window.scrollBy(0, -150);")
            await asyncio.sleep(1)
            
            video_link = await page.wait_for_selector("ytd-video-renderer a#video-title-link", timeout=12000)
            if video_link:
                # माउस को वीडियो के थंबनेल/टाइटल पर ले जाकर क्लिक करना
                v_box = await video_link.bounding_box()
                await human_mouse_move(page, box['x'], box['y'], v_box['x'] + 5, v_box['y'] + 5)
                await video_link.click()
                
                print("▶️ लॉन्ग वीडियो चालू है, असली व्यू काउंट हो रहा है...")
                await asyncio.sleep(15) # वीडियो चलने का टाइम
                
                # वीडियो चलने के दौरान माउस को थोड़ा स्क्रीन पर हिलाना (जैसे यूजर प्लेयर चेक करता है)
                await page.mouse.move(random.randint(200, 600), random.randint(200, 500))
                
                long_video_img = f"2_long_M{machine_id}.png"
                await page.screenshot(path=long_video_img)
                with open(long_video_img, 'rb') as f:
                    bot.send_photo(CHAT_ID, f, caption=f"▶️ मशीन-{machine_id}: [ह्यूमन मोड] वीडियो लाइव प्ले हो रही है!")
                os.remove(long_video_img)
            else:
                print("❌ वीडियो लिंक नहीं मिला")
                
            # ====== STEP 4: शॉर्ट्स सेक्शन चेकिंग ======
            print("⏳ शॉर्ट्स पर जा रहे हैं...")
            await page.goto("https://www.youtube.com/shorts", timeout=60000, wait_until="networkidle")
            await asyncio.sleep(8)
            
            # शॉर्ट्स पेज पर भी माउस का थोड़ा मूवमेंट
            await page.mouse.move(400, 400)
            
            shorts_img = f"3_shorts_M{machine_id}.png"
            await page.screenshot(path=shorts_img)
            with open(shorts_img, 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption=f"🔥 मशीन-{machine_id}: [ह्यूमन मोड] शॉर्ट्स चल रही है!")
            os.remove(shorts_img)

            await browser.close()
            print(f"✅ मशीन-{machine_id} का काम पूरा हुआ!")
            
    except Exception as e:
        print(f"❌ मशीन-{machine_id} एरर: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_youtube_check())
