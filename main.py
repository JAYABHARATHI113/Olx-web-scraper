import time
import requests
from bs4 import BeautifulSoup

# OLX தமிழ்நாடு பைக் தேடல் லிங்க்
OLX_URL = "https://www.olx.in/tamil-nadu_g2001173/motorcycles_c81" 

# உங்களோட Railway n8n Webhook URL
N8N_WEBHOOK_URL = "https://n8n-production-d2b9a.up.railway.app/webhook/olx-bikes"

seen_ads = set()

def check_olx():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(OLX_URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        ads = soup.find_all('li', {'data-aut-id': 'itemBox'})
        
        for ad in ads:
            try:
                link_tag = ad.find('a')
                if not link_tag:
                    continue
                
                link = "https://www.olx.in" + link_tag['href']
                title = ad.find('span', {'data-aut-id': 'itemTitle'}).text.strip()
                price = ad.find('span', {'data-aut-id': 'itemPrice'}).text.strip()
                
                if link not in seen_ads:
                    seen_ads.add(link)
                    data = {
                        "title": title,
                        "price": price,
                        "link": link
                    }
                    requests.post(N8N_WEBHOOK_URL, json=data)
                    print(f"[NEW AD] {title} - {price}")
            except Exception:
                continue
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("OLX Scraper இயங்கத் தொடங்கியது...")
    while True:
        check_olx()
        time.sleep(240) # 5 நிமிடத்திற்கு ஒருமுறை சோதிக்கும்
