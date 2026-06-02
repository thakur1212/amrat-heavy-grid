import os
import time
import json
import requests
from playwright.sync_api import sync_playwright

# 🚨 टेलीग्राम डिटेल्स (अमरत भाई की सेट की हुई)
TELEGRAM_BOT_TOKEN = "8860714255:AAGTh253cvoHaZPNZzI_41vGBMco9EwNJ7U"  
TELEGRAM_CHAT_ID = "8571870755"      

# 🌐 प्रॉक्सि डिटेल्स (अमरत भाई की सेट की हुई यूएस प्रॉक्सी)
PROXY_SERVER = "http://23.247.136.254:80" 
PROXY_USERNAME = ""  
PROXY_PASSWORD = ""  

def send_screenshot_to_telegram(photo_path, caption_title):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    caption_text = f"{caption_title}\n⏰ समय: {time.strftime('%H:%M:%S')}"
    try:
        with open(photo_path, 'rb') as photo:
            files = {'photo': photo}
            data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': caption_text, 'parse_mode': 'Markdown'}
            response = requests.post(url, files=files, data=data)
            if response.status_code == 200:
                print(f"✅ {photo_path} टेलीग्राम पर भेज दिया गया है!")
            else:
                print(f"❌ टेलीग्राम एरर: {response.text}")
    except Exception as e:
        print(f"❌ टेलीग्राम भेजने में गड़बड़: {str(e)}")

def run():
    print("🚀 अमरत भाई, फुल सेटअप बोट शुरू हो रहा है...")
    
    with sync_playwright() as p:
        # प्रॉक्सि कॉन्फ़िगरेशन सेट करना
        proxy_settings = None
        if PROXY_SERVER and "YOUR_PROXY_IP" not in PROXY_SERVER:
            proxy_settings = {"server": PROXY_SERVER}
            print(f"📡 प्रॉक्सि एक्टिव कर दी गई है: {PROXY_SERVER}")

        # ब्राउज़र लॉन्च
        browser = p.chromium.launch(headless=True, proxy=proxy_settings)
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
            locale="en-US",  # यूएस प्रॉक्सी है इसलिए लोकेल भी यूएस कर दिया
            timezone_id="America/New_York"
        )
        
        # 🍪 JSON कुकीज लोड करना
        cookie_file = "cookies.json"
        if os.path.exists(cookie_file):
            with open(cookie_file, "r", encoding="utf-8") as f:
                cookies = json.load(f)
                context.add_cookies(cookies)
            print(f"✅ JSON कुकीज सेट हो गईं!")
        else:
            print("❌ Error: cookies.json फाइल नहीं मिली भाई! चेक करो कि गिटहब पर cookies.json नाम से फाइल है या नहीं।")
            browser.close()
            return
            
        page = context.new_page()
        
        # 🏠 स्टेप 1: होम पेज लाइव स्टेटस
        home_url = "https://www.youtube.com" 
        print(f"🌐 1. होम पेज पर जा रहे हैं...")
        page.goto(home_url, wait_until="networkidle", timeout=60000)
        time.sleep(5)
        
        home_img = "home_page_status.png"
        page.screenshot(path=home_img)
        send_screenshot_to_telegram(home_img, f"🏠 **होम पेज लाइव स्टेटस!**\n📝 टाइटल: {page.title()}")
        
        # 🩳 स्टेप 2: शॉर्ट्स पेज लाइव स्टेटस
        shorts_url = "https://www.youtube.com/shorts"
        print(f"🌐 2. अब शॉर्ट्स पेज पर जा रहे हैं...")
        page.goto(shorts_url, wait_until="networkidle", timeout=60000)
        
        print("⏳ शॉर्ट्स वीडियो प्ले होने का इंतज़ार...")
        time.sleep(12)
        
        shorts_img = "shorts_page_status.png"
        page.screenshot(path=shorts_img)
        send_screenshot_to_telegram(shorts_img, f"🩳 **शॉर्ट्स पेज लाइव स्टेटस (प्रॉक्सि के साथ)!**\n📝 टाइटल: {page.title()}")
        
        browser.close()
        print("🏁 बोट का काम पूरा हुआ!")

if __name__ == "__main__":
    run()
