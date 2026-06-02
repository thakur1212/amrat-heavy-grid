import time
import requests
from playwright.sync_api import sync_playwright

# 🚨 आपकी डिटेल्स
TELEGRAM_BOT_TOKEN = "8860714255:AAGTh253cvoHaZPNZzI_41vGBMco9EwNJ7U"  
TELEGRAM_CHAT_ID = "8571870755"      

# 🌐 आपकी पूरी प्रॉक्सी लिस्ट
PROXY_LIST = [
    "http://185.125.19.32:3128",
    # ... (आपकी पूरी लिस्ट यहाँ कोड में है) ...
    "http://134.209.15.92:443"
]

def send_to_telegram(text, photo_path=None):
    url_msg = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    url_photo = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    
    if photo_path:
        with open(photo_path, 'rb') as photo:
            requests.post(url_photo, files={'photo': photo}, data={'chat_id': TELEGRAM_CHAT_ID, 'caption': text})
    else:
        requests.post(url_msg, data={'chat_id': TELEGRAM_CHAT_ID, 'text': text})

def run():
    send_to_telegram("🚀 अमरत भाई, प्रॉक्सी चेकर बोट शुरू हो गया है! अब एक-एक करके सबको टेस्ट कर रहा हूँ...")
    
    with sync_playwright() as p:
        for proxy in PROXY_LIST:
            print(f"🕵️‍♂️ टेस्टिंग: {proxy}")
            
            try:
                browser = p.chromium.launch(headless=True, proxy={"server": proxy})
                context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
                page = context.new_page()
                
                # होम पेज चेक
                page.goto("https://www.youtube.com", timeout=30000)
                time.sleep(3)
                page.screenshot(path="home.png")
                
                # शॉर्ट्स चेक
                page.goto("https://www.youtube.com/shorts", timeout=30000)
                time.sleep(5)
                page.screenshot(path="shorts.png")
                
                send_to_telegram(f"✅ प्रॉक्सी काम कर रही है: {proxy}", "home.png")
                send_to_telegram(f"🩳 शॉर्ट्स पेज:", "shorts.png")
                browser.close()
                break # अगर एक सही मिल गई तो रुक जाएगा
                
            except Exception as e:
                send_to_telegram(f"❌ प्रॉक्सी खराब है: {proxy}\nError: {str(e)[:50]}")
                try: browser.close()
                except: pass

if __name__ == "__main__":
    run()
