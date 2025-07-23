import streamlit as st
from utils.crawler import fetch_deals

st.set_page_config(page_title="Smart Deal Finder", layout="wide")

st.title("🛍️ Smart Deal Finder")
st.markdown("Find the best online deals in your country using AI-powered search and web crawling.")

# 1. Category selection
category = st.selectbox("Select Category", ["Electronics", "Garments"])

details = {}

# 2. Sub-category / Model input
if category == "Electronics":
    subcat = st.selectbox("Choose Subcategory", ["Mobiles", "Laptops"])
    details["subcategory"] = subcat

    model = st.text_input(f"Enter {subcat} model to search for deals (optional)")
    details["model"] = model.strip()

elif category == "Garments":
    subcat = st.selectbox("Choose Garment Type", ["Men", "Women", "Kids"])
    details["subcategory"] = subcat

    if subcat == "Kids":
        size = st.text_input("Enter size or age range (e.g., 2-4 yrs, size 6)")
        details["size"] = size.strip()
    else:
        garment_type = st.multiselect("Select categories", ["Shirts", "Trousers", "Suits", "Shoes"])
        details["types"] = garment_type

# 3. Country/Region input
country = st.text_input("Enter your country or region", value="Pakistan")

# 4. Discount filter
discount_only = st.checkbox("Only show discounted deals", value=False)

# Search trigger and results
if st.button("Search Deals"):
    if not country:
        st.warning("Please enter a country/region.")
    else:
        with st.spinner("Searching deals online..."):
            results, debug = fetch_deals(category, details, country, discount_only)

st.subheader("🛠️ Debug Info")
for msg in debug:
    st.write(msg)

if results:
    st.subheader("Search Results")
    for deal in results:
        if deal.get("img"):
            st.image(deal["img"], width=200)
        st.markdown(f"### [{deal['title']}]({deal['url']})")
        st.markdown(f"**Price:** {deal['price']}  \n**Source:** {deal.get('source','Unknown')}")
        st.write("---")
else:
    st.warning("No deals found.")
