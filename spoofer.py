import os
import time
import requests  # 🚀 टेलीग्राम पर फोटो भेजने के लिए
from playwright.sync_api import sync_playwright

# 🚨 यहाँ अपने टेलीग्राम बोट की डिटेल्स डालें
TELEGRAM_BOT_TOKEN = "8860714255:AAGTh253cvoHaZPNZzI_41vGBMco9EwNJ7U"  # अपना बोट टोकन यहाँ पेस्ट करें
TELEGRAM_CHAT_ID = "8571870755"      # अपनी चैट आईडी यहाँ पेस्ट करें

def load_netscape_cookies(file_path):
    """
    Netscape format (cookies.txt) को Playwright के फॉर्मेट में बदलने का फंक्शन
    """
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

def send_screenshot_to_telegram(photo_path, title):
    """
    📸 स्क्रीनशॉट को सीधे आपके टेलीग्राम पर भेजने का फंक्शन
    """
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE":
        print("⚠️ टेलीग्राम टोकन या चैट आईडी सेट नहीं है! कृपया कोड में अपनी डिटेल्स डालें।")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    caption_text = f"📸 **अमरत भाई, लाइव स्टेटस!**\n📝 पेज टाइटल: {title}\n⏰ समय: {time.strftime('%H:%M:%S')}"
    
    try:
        with open(photo_path, 'rb') as photo:
            files = {'photo': photo}
            data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': caption_text, 'parse_mode': 'Markdown'}
            response = requests.post(url, files=files, data=data)
            if response.status_code == 200:
                print("✅ स्क्रीनशॉट टेलीग्राम पर सफलतापूर्वक भेज दिया गया है!")
            else:
                print(f"❌ टेलीग्राम पर भेजने में एरर आया: {response.text}")
    except Exception as e:
        print(f"❌ टेलीग्राम भेजने में गड़बड़ हुई: {str(e)}")

def run():
    print("🚀 अमरत भाई, बोट शुरू हो रहा है...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        
        cookie_file = "cookies.txt"
        if os.path.exists("youtube.com_cookies.txt"):
            cookie_file = "youtube.com_cookies.txt"
            
        print(f"📦 {cookie_file} से लॉगिन कुकीज पढ़ी जा रही हैं...")
        playwright_cookies = load_netscape_cookies(cookie_file)
        
        if playwright_cookies:
            context.add_cookies(playwright_cookies)
            print(f"✅ {len(playwright_cookies)} कुकीज सेट हो गईं!")
            
        page = context.new_page()
        
        # 📺 यहाँ अपना यूट्यूब वीडियो या चैनल का लिंक डालें
        target_url = "https://www.youtube.com" 
        print(f"🌐 {target_url} पर जा रहे हैं...")
        
        page.goto(target_url, wait_until="networkidle", timeout=60000)
        
        print("⏳ पेज लोड हो चुका है, 10 सेकंड का इंतज़ार...")
        time.sleep(10)
        
        page_title = page.title()
        print(f"📝 वर्तमान पेज का टाइटल है: {page_title}")
        
        # 📸 स्क्रीनशॉट लेना
        screenshot_name = "youtube_live_status.png"
        print("📸 स्क्रीनशॉट लिया जा रहा है...")
        page.screenshot(path=screenshot_name, full_page=False)
        
        # 🚀 टेलीग्राम पर भेजना (नया लॉजिक)
        print("📤 टेलीग्राम पर स्क्रीनशॉट भेजा जा रहा है...")
        send_screenshot_to_telegram(screenshot_name, page_title)
        
        browser.close()
        print("🏁 बोट का काम पूरा हुआ!")

if __name__ == "__main__":
    run()
