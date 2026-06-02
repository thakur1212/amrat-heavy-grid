import time
import requests
from playwright.sync_api import sync_playwright

# 🚨 टेलीग्राम डिटेल्स
TELEGRAM_BOT_TOKEN = "8860714255:AAGTh253cvoHaZPNZzI_41vGBMco9EwNJ7U"  
TELEGRAM_CHAT_ID = "8571870755"      

# 🌐 प्रॉक्सि डिटेल्स (अगर प्रॉक्सी की वजह से बोट अटके, तो इसे खाली "" कर देना भाई)
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
    try:
        with open(photo_path, 'rb') as photo:
            files = {'photo': photo}
            data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': caption_title, 'parse_mode': 'Markdown'}
            response = requests.post(url, files=files, data=data)
            if response.status_code == 200:
                print(f"✅ {photo_path} टेलीग्राम पर भेज दिया गया है!")
            else:
                send_msg_to_telegram(f"❌ फोटो भेजने में टेलीग्राम एरर: {response.text}")
    except Exception as e:
        send_msg_to_telegram(f"❌ टेलीग्राम फोटो एरर: {str(e)}")

def run():
    send_msg_to_telegram("🚀 अमरत भाई, बिना कुकीज़ वाला फ्रेश बोट गिटहब पर चालू हो गया है!")
    
    with sync_playwright() as p:
        proxy_settings = None
        if PROXY_SERVER and PROXY_SERVER != "":
            proxy_settings = {"server": PROXY_SERVER}
            print(f"📡 प्रॉक्सि एक्टिव: {PROXY_SERVER}")

        try:
            # फ्रेश ब्राउज़र लॉन्च (कोई कुकीज़ नहीं)
            browser = p.chromium.launch(headless=True, proxy=proxy_settings)
        except Exception as e:
            send_msg_to_telegram(f"❌ ब्राउज़र चालू नहीं हुआ, प्रॉक्सि बंद हो सकती है:\n`{str(e)}`")
            return
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
            locale="en-US",
            timezone_id="America/New_York"
        )
            
        page = context.new_page()
        
        # 🏠 स्टेप 1: सीधे यूट्यूब का मुख्य पेज खोलना
        try:
            print("🌐 1. यूट्यूब होम पेज पर जा रहे हैं...")
            page.goto("https://www.youtube.com", wait_until="networkidle", timeout=45000)
            time.sleep(6) # पेज को सेट होने का पूरा टाइम दें
            
            home_img = "home_page_status.png"
            page.screenshot(path=home_img)
            send_screenshot_to_telegram(home_img, f"🏠 **बिना कुकीज़ - होम पेज लाइव!**\n📝 टाइटल: {page.title()}")
        except Exception as e:
            send_msg_to_telegram(f"❌ होम पेज पर एरर आया:\n`{str(e)}`")
        
        # 🩳 स्टेप 2: शॉर्ट्स वाले यूआरएल पर मूव करना
        try:
            print("🌐 2. अब शॉर्ट्स पेज पर ट्रांसफर हो रहे हैं...")
            page.goto("https://www.youtube.com/shorts", wait_until="networkidle", timeout=45000)
            
            # वीडियो प्ले होने और स्क्रीन सेट होने के लिए 12 सेकंड का इंतज़ार
            print("⏳ शॉर्ट्स वीडियो लोड होने का इंतज़ार...")
            time.sleep(12)
            
            shorts_img = "shorts_page_status.png"
            page.screenshot(path=shorts_img)
            send_screenshot_to_telegram(shorts_img, f"🩳 **बिना कुकीज़ - शॉर्ट्स लाइव!**\n📝 टाइटल: {page.title()}")
        except Exception as e:
            send_msg_to_telegram(f"❌ शॉर्ट्स लोड करने में गड़बड़ हुई:\n`{str(e)}`")
        
        browser.close()
        send_msg_to_telegram("🏁 अमरत भाई, बोट का रन पूरा हुआ!")

if __name__ == "__main__":
    run()
