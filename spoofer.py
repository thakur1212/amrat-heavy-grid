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

# असली इंसानी व्यवहार दिखाने के लिए रैंडम डिले फंक्शन
async def human_delay(min_sec=3, max_sec=7):
    await asyncio.sleep(random.uniform(min_sec, max_sec))

async def run_youtube_check():
    print(f"🚀 मशीन-{machine_id} स्टार्ट हो रही है (No Proxy + Full Stealth Mode)...")
    try:
        async with async_playwright() as p:
            # 🌐 प्रॉक्सी हटा दी गई है, अब सीधा गिटहब के सुपरफ़ास्ट नेटवर्क से चलेगा
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled', # बोट डिटेक्शन बाईपास करने के लिए
                    '--no-sandbox',
                    '--disable-infobars',
                    '--window-size=1366,768'
                ]
            )
            
            context = await browser.new_context(
                viewport={"width": 1366, "height": 768},
                # एकदम लेटेस्ट और रियल विंडोज क्रोम का यूजर एजेंट
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                locale="hi-IN",
                timezone_id="Asia/Kolkata"
            )
            
            page = await context.new_page()
            
            # ब्राउज़र के अंदर से 'webdriver: true' का निशान मिटाने के लिए जावासक्रिप्ट
            await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # ====== 1. यूट्यूब होमपेज ======
            print(f"📡 मशीन-{machine_id}: यूट्यूब होमपेज लोड हो रहा है...")
            # बिना प्रॉक्सी के नेटवर्क तेज़ होगा, इसलिए डिफ़ॉल्ट 60 सेकंड टाइमआउट काफी है
            await page.goto("https://www.youtube.com", timeout=60000, wait_until="domcontentloaded")
            await human_delay(4, 8) # पेज को पूरी तरह रेंडर होने का समय दें
            
            home_img = f"home_M{machine_id}.png"
            await page.screenshot(path=home_img)
            with open(home_img, 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption=f"📸 मशीन-{machine_id}: यूट्यूब होमपेज! (No Proxy)")
            os.remove(home_img)
            
            # ====== 2. रैंडम वीडियो प्ले ======
            video_links = await page.query_selector_all("a#video-title-link, ytd-rich-grid-media a[href*='/watch']")
            if video_links:
                # पहले 3 वीडियो में से कोई भी एक रैंडम वीडियो सेलेक्ट करेगा
                chosen_video = random.choice(video_links[:3]) if len(video_links) > 3 else video_links[0]
                await chosen_video.click()
                print(f"▶️ मशीन-{machine_id}: रैंडम वीडियो पर क्लिक कर दिया है...")
                await human_delay(10, 15) # वीडियो प्ले होने और बफ़र होने का इंतज़ार
                
                video_img = f"video_M{machine_id}.png"
                await page.screenshot(path=video_img)
                with open(video_img, 'rb') as f:
                    bot.send_photo(CHAT_ID, f, caption=f"▶️ मशीन-{machine_id}: वीडियो प्ले सक्सेसफुल!")
                os.remove(video_img)
                
            # ====== 3. यूट्यूब शॉर्ट्स ======
            print(f"🔥 मशीन-{machine_id}: शॉर्ट्स पेज ओपन हो रहा है...")
            await page.goto("https://www.youtube.com/shorts", timeout=60000, wait_until="domcontentloaded")
            await human_delay(7, 12)
            
            shorts_img = f"shorts_M{machine_id}.png"
            await page.screenshot(path=shorts_img)
            with open(shorts_img, 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption=f"🔥 मशीन-{machine_id}: शॉर्ट्स फीड लाइव!")
            os.remove(shorts_img)

            await browser.close()
            print(f"✅ मशीन-{machine_id}: सभी टास्क पूरे हुए।")
            
    except Exception as e:
        print(f"❌ मशीन-{machine_id} एरर: {str(e)}")
        try:
            bot.send_message(CHAT_ID, f"❌ मशीन-{machine_id} पर एरर आया भाई:\n{str(e)[:150]}")
        except:
            pass

if __name__ == "__main__":
    asyncio.run(run_youtube_check())
