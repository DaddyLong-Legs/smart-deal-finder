import requests
from bs4 import BeautifulSoup
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_search_keywords(category, details):
    prompt = f"Generate concise search keywords for category {category} with details {details}"
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an e‑commerce assistant generating product search keywords."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=20,
            temperature=0.5
        )
        return resp['choices'][0]['message']['content'].strip()
    except:
        return details.get("model", category)

def parse_site(url, selectors):
    resp = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    items = soup.select(selectors['item'])
    for item in items[:10]:
        title = item.select_one(selectors.get('title', '')).get_text(strip=True) if selectors.get('title') else None
        price = item.select_one(selectors.get('price', '')).get_text(strip=True) if selectors.get('price') else None
        link = item.select_one(selectors.get('link', '')).get('href', '')
        if selectors.get('link_prefix'):
            link = selectors['link_prefix'] + link
        img = item.select_one(selectors.get('img','')).get('src') if selectors.get('img') else None
        if title and price and link:
            results.append({"title": title, "price": price, "url": link, "img": img})
    return results

def fetch_deals(category, details, country, discount_only):
    results = []
    search_term = details.get("model") or generate_search_keywords(category, details)
    q = search_term.replace(" ", "+")

    # Daraz
    daraz = parse_site(
        f"https://www.daraz.pk/catalog/?q={q}",
        selectors={
            "item": "div[data-qa-locator='product-item']",
            "title": "div[data-qa-locator='product-item-title']",
            "price": "span[data-qa-locator='product-item-price']",
            "link": "a",
            "link_prefix": "https:",
            "img": "img[data-src]"
        }
    )
    for d in daraz:
        if not discount_only or "%" in d['title'].lower() or "off" in d['title'].lower():
            d['source'] = "Daraz.pk"; results.append(d)

    # PriceOye (scraping search results)
    po = parse_site(
        f"https://www.priceoye.pk/search?q={q}",
        selectors={
            "item": ".product-list-item",
            "title": ".product-title",
            "price": ".price",
            "link": "a",
            "link_prefix": "https://www.priceoye.pk",
            "img": "img"
        }
    )
    for d in po:
        d['source'] = "PriceOye"; results.append(d)

    # OLX Pakistan (classified snapshot)
    olx = parse_site(
        f"https://www.olx.com.pk/items/q-{q}",
        selectors={
            "item": "li.EIR5N",
            "title": "span._2tW0J",
            "price": "span._89yzn",
            "link": "a",
            "link_prefix": "https://www.olx.com.pk",
            "img": "img"
        }
    )
    for d in olx:
        d['source'] = "OLX Pakistan"; results.append(d)

    # Telemart
    tm = parse_site(
        f"https://telemart.pk/catalogsearch/result/?q={q}",
        selectors={
            "item": "div.product-item-info",
            "title": "a.product-item-link",
            "price": "span.price",
            "link": "a.product-item-link",
            "link_prefix": "",
            "img": "img.product-image-photo"
        }
    )
    for d in tm:
        d['source'] = "Telemart"; results.append(d)

    # Shophive
    sh = parse_site(
        f"https://www.shophive.com/catalogsearch/result/?q={q}",
        selectors={
            "item": "div.product-item",
            "title": "a.product-item-link",
            "price": "span.price",
            "link": "a.product-item-link",
            "link_prefix": "",
            "img": "img.product-image-photo"
        }
    )
    for d in sh:
        d['source'] = "Shophive"; results.append(d)

    return results
