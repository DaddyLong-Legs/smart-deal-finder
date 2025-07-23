import requests
from bs4 import BeautifulSoup

def fetch_deals(category, details, country, discount_only):
    debug = []
    results = []

    search_term = details.get("model") or "smartphone"
    debug.append(f"Search term: {search_term}")

    q = search_term.replace(" ", "-").lower()
    debug.append(f"Search query param: {q}")

    if category == "Electronics" and details.get("subcategory") == "Mobiles":
        url = f"https://www.olx.com.pk/items/q-{q}"
        debug.append(f"Crawling URL: {url}")

        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        debug.append(f"HTTP status code: {res.status_code}")

        if res.status_code != 200:
            return results, debug

        soup = BeautifulSoup(res.text, "html.parser")
        cards = soup.find_all("li", class_="EIR5N")
        debug.append(f"Found {len(cards)} listing cards")

        for item in cards[:5]:
            title_tag = item.find("span", class_="_2tW1I")
            price_tag = item.find("span", class_="_89yzn")
            url_tag = item.find("a", href=True)
            img_tag = item.find("img")

            if not (title_tag and price_tag and url_tag):
                debug.append("Skipping item due to missing fields")
                continue

            title = title_tag.text.strip()
            price = price_tag.text.strip()
            link = "https://www.olx.com.pk" + url_tag["href"]
            img = img_tag["src"] if img_tag and img_tag.has_attr("src") else None

            results.append({
                "title": title,
                "price": price,
                "url": link,
                "img": img,
                "source": "OLX"
            })
            debug.append(f"Added deal: {title} | {price}")

    debug.append(f"Total deals gathered: {len(results)}")
    return results, debug
