import sys
import asyncio
import os
import telebot
from playwright.async_api import async_playwright

BOT_TOKEN = "8760393896:AAECRmPN-1FatZuW3I_XzXp6lpDXpgm2i-Y"
bot = telebot.TeleBot(BOT_TOKEN)

# 🚨 अमरत भाई, यहाँ अपनी असली टेलीग्राम चैट आईडी (नंबर) डाल दो
CHAT_ID = "8571870755" 

async def run_on_amrat_pc():
    async with async_playwright() as p:
        try:
            # 🔥 तुम्हारा एकदम असली और तैयार किया हुआ रिमोट लिंक
            pc_browser_url = "ws://unmodificative-hostless-destinee.ngrok-free.dev/devtools/browser/7997ccbb-19d1-4b1c-afb3-4410e4c7d83c"
            
            print("🔗 अमरत भाई के पीसी से कनेक्ट हो रहा है...")
            browser = await p.chromium.connect_over_cdp(pc_browser_url)
            
            # पीसी पर खुले हुए क्रोम के पहले टैब को पकड़ना
            context = browser.contexts[0]
            page = context.pages[0] if context.pages else await context.new_page()
            
            # ====== 1. यूट्यूब होमपेज ======
            print("🚀 यूट्यूब होमपेज लोड हो रहा है...")
            await page.goto("https://www.youtube.com", timeout=60000)
            await asyncio.sleep(5)
            
            await page.screenshot(path="1_pc_home.png")
            with open("1_pc_home.png", 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption="📸 [PC मोड] यूट्यूब होमपेज आपके पीसी पर खुल गया है!")
            os.remove("1_pc_home.png")
            
            # ====== 2. शॉर्ट्स सेक्शन ======
            print("🚀 शॉर्ट्स चालू की जा रही है...")
            await page.goto("https://www.youtube.com/shorts", timeout=60000)
            await asyncio.sleep(8)
            
            await page.screenshot(path="2_pc_shorts.png")
            with open("2_pc_shorts.png", 'rb') as f:
                bot.send_photo(CHAT_ID, f, caption="🔥 [PC मोड] यूट्यूब शॉर्ट्स आपके पीसी पर लाइव चल रहा है!")
            os.remove("2_pc_shorts.png")
            
            # ====== 3. लॉन्ग वीडियो सर्च और प्ले ======
            print("🚀 वीडियो सर्च की जा रही है...")
            await page.goto("https://www.youtube.com", timeout=60000)
            await asyncio.sleep(4)
            
            search_input = await page.wait_for_selector("input[name='search_query']")
            if search_input:
                await search_input.click()
                await page.keyboard.write("lofi songs hindi")
                await search_input.press("Enter")
                await asyncio.sleep(5)
                
                video_link = await page.wait_for_selector("ytd-video-renderer a#video-title-link")
                if video_link:
                    await video_link.click()
                    print("▶️ लॉन्ग वीडियो प्ले हो गई है...")
                    await asyncio.sleep(15)
                    
                    await page.screenshot(path="3_pc_long.png")
                    with open("3_pc_long.png", 'rb') as f:
                        bot.send_photo(CHAT_ID, f, caption="▶️ [PC मोड] लंबी वीडियो बिना किसी एरर के चल रही है भाई!")
                    os.remove("3_pc_long.png")

            print("✅ अमरत भाई, सारा काम एकदम सक्सेसफुल हो गया!")
            
        except Exception as e:
            print(f"❌ एरर आया भाई: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_on_amrat_pc())
