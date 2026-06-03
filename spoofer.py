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

# प्रॉक्सी स्लो होने के कारण इंसानी डिले को थोड़ा और ऑप्टिमाइज किया
async def human_delay(min_sec=4, max_sec=8):
    await asyncio.sleep(random.uniform(min_sec, max_sec))

async def run_youtube_check():
    print(f"🚀 मशीन-{machine_id} स्टार्ट हो रही है (Proxy + Stealth Mode)...")
    try:
        async with async_playwright() as p:
            # क्रोमियम इंजन के साथ प्रॉक्सी और बोट छुपाने के आर्गुमेंट्स
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-infobars'
                ],
                # 🌐 यहाँ आपकी एक्टिव प्रॉक्सी जोड़ दी गई है
                proxy={
                    "server": "http://91.233.223.147:3128"
                }
            )
            
            context = await browser.new_context(
                viewport={"width": 1366, "height": 768},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                locale="hi-IN",
                timezone_id="Asia/Kolkata"
            )
            
            page = await context.new_page()
            # रोबोट डिटेक्शन बायपास करने के लिए स्क्रिप्ट
            await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # ====== 1. यूट्यूब होमपेज ======
            print(f"📡 मशीन-{machine_id}: यूट्यूब होमपेज लोड हो रहा है (प्रॉक्सी स्लो है, थोड़ा इंतज़ार करें)...")
            # स्लो प्रॉक्सी के लिए timeout को 120000ms (2 मिनट) किया और wait_until को 'commit' किया
            await page.goto("https://www.youtube.com", timeout=120000, wait_until="commit")
            await human_delay(6, 12) # पेज को थोड़ा और सेटल होने का समय दिया
            
            home_img = f"home_M{machine_id}.png"
            await page.screenshot(path=home_img)
            with open(home_img, 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption=f"📸 मशीन-{machine_id}: यूट्यूब होमपेज लोड हुआ! (Proxy Active)")
            os.remove(home_img)
            
            # ====== 2. रैंडम वीडियो प्ले ======
            video_links = await page.query_selector_all("a#video-title-link, ytd-rich-grid-media a[href*='/watch']")
            if video_links:
                chosen_video = random.choice(video_links[:3]) if len(video_links) > 3 else video_links[0]
                await chosen_video.click()
                print(f"▶️ मशीन-{machine_id}: वीडियो पर क्लिक कर दिया है, बफ़र होने का इंतज़ार...")
                await human_delay(12, 18) # स्लो नेटवर्क के कारण वीडियो लोड होने के लिए एक्स्ट्रा टाइम
                
                video_img = f"video_M{machine_id}.png"
                await page.screenshot(path=video_img)
                with open(video_img, 'rb') as f:
                    bot.send_photo(CHAT_ID, f, caption=f"▶️ मशीन-{machine_id}: रैंडम वीडियो प्ले की कोशिश!")
                os.remove(video_img)
                
            # ====== 3. यूट्यूब शॉर्ट्स ======
            print(f"🔥 मशीन-{machine_id}: शॉर्ट्स पेज पर जा रहे हैं...")
            await page.goto("https://www.youtube.com/shorts", timeout=120000, wait_until="commit")
            await human_delay(9, 15)
            
            shorts_img = f"shorts_M{machine_id}.png"
            await page.screenshot(path=shorts_img)
            with open(shorts_img, 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption=f"🔥 मशीन-{machine_id}: शॉर्ट्स पेज स्टेटस!")
            os.remove(shorts_img)

            await browser.close()
            print(f"✅ मशीन-{machine_id}: काम पूरा हुआ और ब्राउज़र बंद हुआ।")
            
    except Exception as e:
        print(f"❌ मशीन-{machine_id} एरर: {str(e)}")
        try:
            bot.send_message(CHAT_ID, f"❌ मशीन-{machine_id} प्रॉक्सी एरर या टाइमआउट:\n{str(e)[:150]}")
        except:
            pass

if __name__ == "__main__":
    asyncio.run(run_youtube_check())
