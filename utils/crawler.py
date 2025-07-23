import requests
from bs4 import BeautifulSoup
import openai
import os

# Load your GPT-4 API key from Streamlit secrets or environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_search_keywords(category, details):
    """
    Uses GPT-4 to generate smart keywords based on user input.
    """
    prompt = f"Generate search keywords for online shopping. Category: {category}. Details: {details}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an e-commerce assistant that generates precise product search keywords."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=20,
            temperature=0.5
        )
        keywords = response['choices'][0]['message']['content']
        return keywords.strip()
    except Exception as e:
        return "mobile phone"  # fallback default

def fetch_deals(category, details, country, discount_only):
    results = []

    # 🟦 ELECTRONICS → MOBILES Example with Daraz
    if category == "Electronics" and details.get("subcategory") == "Mobiles":
        # Use GPT-4 to enhance search keywords
        search_term = details.get("model")
        if not search_term:
            search_term = generate_search_keywords(category, details)
        search_term = search_term.replace(" ", "+")

        # Build URL
        url = f"https://www.daraz.pk/catalog/?q={search_term}"
        headers = {"User-Agent": "Mozilla/5.0"}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            # Parse deal items
            items = soup.select("div[data-qa-locator='product-item']")
            for item in items[:10]:  # limit results
                title_elem = item.select_one("div[data-qa-locator='product-item-title']")
                price_elem = item.select_one("span[data-qa-locator='product-item-price']")
                link_elem = item.find("a", href=True)

                if not title_elem or not price_elem or not link_elem:
                    continue

                title = title_elem.get_text(strip=True)
                price = price_elem.get_text(strip=True)
                product_url = "https:" + link_elem["href"]

                if discount_only and "off" not in title.lower() and "%" not in title:
                    continue  # skip non-discounted items if filter is on

                results.append({
                    "title": title,
                    "price": price,
                    "url": product_url,
                    "source": "Daraz.pk"
                })

        except Exception as e:
            results.append({
                "title": "Error fetching Daraz deals",
                "price": "-",
                "url": "#",
                "source": str(e)
            })

    # 🟧 Placeholder for other categories or garment logic

    return results
