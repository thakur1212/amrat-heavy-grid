import os
import time
import json
import requests
from playwright.sync_api import sync_playwright

# 🚨 टेलीग्राम डिटेल्स
TELEGRAM_BOT_TOKEN = "8860714255:AAGTh253cvoHaZPNZzI_41vGBMco9EwNJ7U"  
TELEGRAM_CHAT_ID = "8571870755"      

# 🌐 प्रॉक्सि डिटेल्स (अगर यह काम न करे तो इसे खाली "" छोड़ देना भाई)
PROXY_SERVER = "http://23.247.136.254:80" 

def send_msg_to_telegram(text):
    """टेलीग्राम पर टेक्स्ट मैसेज भेजने का फंक्शन"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={'chat_id': TELEGRAM_CHAT_ID, 'text': text, 'parse_mode': 'Markdown'})
    except Exception as e:
        print(f"टेलीग्राम मैसेज एरर: {str(e)}")

def send_screenshot_to_telegram(photo_path, caption_title):
    """📸 स्क्रीनशॉट को टेलीग्राम पर भेजने का फंक्शन"""
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
                send_msg_to_telegram(f"❌ फोटो भेजने में टेलीग्राम एरर: {response.text}")
    except Exception as e:
        send_msg_to_telegram(f"❌ टेलीग्राम फोटो एरर: {str(e)}")

def run():
    send_msg_to_telegram("🚀 अमरत भाई, बोट गिटहब सर्वर पर चालू हो गया है! चेकिंग शुरू...")
    
    with sync_playwright() as p:
        proxy_settings = None
        if PROXY_SERVER and "YOUR_PROXY_IP" not in PROXY_SERVER and PROXY_SERVER != "":
            proxy_settings = {"server": PROXY_SERVER}
            print(f"📡 प्रॉक्सि एक्टिव: {PROXY_SERVER}")

        try:
            browser = p.chromium.launch(headless=True, proxy=proxy_settings)
        except Exception as e:
            send_msg_to_telegram(f"❌ ब्राउज़र चालू नहीं हो पाया (प्रॉक्सि खराब हो सकती है):\n`{str(e)}`")
            return
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
            locale="en-US",
            timezone_id="America/New_York"
        )
        
        # 🍪 कुकीज चेक करना (दोनों नाम चेक करेगा ताकि एरर न आए)
        cookie_file = "cookies.json"
        if not os.path.exists(cookie_file) and os.path.exists("youtube.com_cookies.json"):
            cookie_file = "youtube.com_cookies.json"
            
        if os.path.exists(cookie_file):
            with open(cookie_file, "r", encoding="utf-8") as f:
                cookies = json.load(f)
                context.add_cookies(cookies)
            print("✅ JSON कुकीज लोड हो गईं!")
        else:
            send_msg_to_telegram("❌ एरर: गिटहब पर `cookies.json` फाइल नहीं मिली भाई! नाम चेक करो।")
            browser.close()
            return
            
        page = context.new_page()
        
        # 🏠 स्टेप 1: होम पेज खोलना
        try:
            print("🌐 1. होम पेज पर जा रहे हैं...")
            page.goto("https://www.youtube.com", wait_until="networkidle", timeout=45000)
            time.sleep(5)
            home_img = "home_page_status.png"
            page.screenshot(path=home_img)
            send_screenshot_to_telegram(home_img, f"🏠 **होम पेज लाइव स्टेटस!**\n📝 टाइटल: {page.title()}")
        except Exception as e:
            send_msg_to_telegram(f"❌ होम पेज लोड करने में एरर आया (प्रॉक्सि स्लो है):\n`{str(e)}`")
        
        # 🩳 स्टेप 2: शॉर्ट्स पेज खोलना
        try:
            print("🌐 2. अब शॉर्ट्स पेज पर जा रहे हैं...")
            page.goto("https://www.youtube.com/shorts", wait_until="networkidle", timeout=45000)
            time.sleep(12)
            shorts_img = "shorts_page_status.png"
            page.screenshot(path=shorts_img)
            send_screenshot_to_telegram(shorts_img, f"🩳 **शॉर्ट्स पेज लाइव स्टेटस!**\n📝 टाइटल: {page.title()}")
        except Exception as e:
            send_msg_to_telegram(f"❌ शॉर्ट्स पेज लोड करने में एरर आया:\n`{str(e)}`")
        
        browser.close()
        send_msg_to_telegram("🏁 बोट का रन पूरा हो गया है!")

if __name__ == "__main__":
    run()
