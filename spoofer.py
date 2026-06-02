import os
import time
import requests
from playwright.sync_api import sync_playwright

# 🚨 यहाँ अपने टेलीग्राम बोट की डिटेल्स डालें
TELEGRAM_BOT_TOKEN = "8860714255:AAGTh253cvoHaZPNZzI_41vGBMco9EwNJ7U"  # अपना बोट टोकन यहाँ पेस्ट करें
TELEGRAM_CHAT_ID = "8571870755"      # अपनी चैट आईडी यहाँ पेस्ट करें

def load_netscape_cookies(file_path):
    """Netscape format (cookies.txt) को Playwright के फॉर्मेट में बदलने का फंक्शन"""
    cookies = []
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} फाइल नहीं मिली!")
        return cookies

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            tokens = line.strip().split('\t')
            if len(tokens) < 7:
                continue
            domain = tokens[0]
            if domain.startswith('.'):
                domain = domain[1:]
                
            cookie = {
                'domain': domain,
                'path': tokens[2],
                'secure': tokens[3].upper() == 'TRUE',
                'expires': int(tokens[4]) if tokens[4].isdigit() else -1,
                'name': tokens[5],
                'value': tokens[6]
            }
            cookies.append(cookie)
    return cookies

def send_screenshot_to_telegram(photo_path, caption_title):
    """📸 स्क्रीनशॉट को टेलीग्राम पर भेजने का फंक्शन"""
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE":
        print("⚠️ टेलीग्राम टोकन या चैट आईडी सेट नहीं है!")
        return

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
    print("🚀 अमरत भाई, डबल स्क्रीनशॉट बोट शुरू हो रहा है...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        
        cookie_file = "cookies.txt"
        if os.path.exists("youtube.com_cookies.txt"):
            cookie_file = "youtube.com_cookies.txt"
            
        print(f"📦 {cookie_file} से लॉगिन कुकीज लोड की जा रही हैं...")
        playwright_cookies = load_netscape_cookies(cookie_file)
        
        if playwright_cookies:
            context.add_cookies(playwright_cookies)
            print("✅ कुकीज सफलतापूर्वक सेट हो गईं!")
            
        page = context.new_page()
        
        # --------------------------------------------------------
        # 🏠 स्टेप 1: होम पेज खोलना और पहला स्क्रीनशॉट लेना
        # --------------------------------------------------------
        home_url = "https://www.youtube.com" 
        print(f"🌐 1. होम पेज पर जा रहे हैं: {home_url}")
        page.goto(home_url, wait_until="networkidle", timeout=60000)
        
        print("⏳ होम पेज लोड होने के लिए 5 सेकंड रुक रहे हैं...")
        time.sleep(5)
        
        home_title = page.title()
        home_img = "home_page_status.png"
        page.screenshot(path=home_img)
        
        print("📤 होम पेज का स्क्रीनशॉट टेलीग्राम पर भेजा जा रहा है...")
        send_screenshot_to_telegram(home_img, f"🏠 **होम पेज लाइव स्टेटस!**\n📝 टाइटल: {home_title}")
        
        # --------------------------------------------------------
        # 🩳 स्टेप 2: शॉर्ट्स पेज पर जाना और दूसरा स्क्रीनशॉट लेना
        # --------------------------------------------------------
        shorts_url = "https://www.youtube.com/shorts"
        print(f"🌐 2. अब शॉर्ट्स पेज पर जा रहे हैं: {shorts_url}")
        page.goto(shorts_url, wait_until="networkidle", timeout=60000)
        
        # शॉर्ट्स वीडियो को लोड होकर प्ले होने के लिए थोड़ा ज्यादा (12 सेकंड) टाइम देंगे
        print("⏳ शॉर्ट्स वीडियो प्ले होने और बफरिंग का 12 सेकंड इंतज़ार...")
        time.sleep(12)
        
        shorts_title = page.title()
        shorts_img = "shorts_page_status.png"
        page.screenshot(path=shorts_img)
        
        print("📤 शॉर्ट्स पेज का स्क्रीनशॉट टेलीग्राम पर भेजा जा रहा है...")
        send_screenshot_to_telegram(shorts_img, f"🩳 **शॉर्ट्स पेज लाइव स्टेटस (Playing)!**\n📝 टाइटल: {shorts_title}")
        
        browser.close()
        print("🏁 अमरत भाई, दोनों स्क्रीनशॉट भेजकर बोट का काम पूरा हुआ!")

if __name__ == "__main__":
    run()
