import streamlit as st
from utils.crawler import fetch_deals

st.set_page_config(page_title="Smart Deal Finder", layout="centered")

st.title("🔎 Smart Deal Finder")

# 1. Category Selection
category = st.selectbox("Choose a category:", ["Electronics", "Garments"])

# 2. Subcategory Options
details = {}
if category == "Electronics":
    subcat = st.radio("Choose type:", ["Mobiles", "Laptops"])
    details["subcategory"] = subcat
    
    mode = st.radio(f"What do you want to search for in {subcat}?", ["Available deals", "Search for specific model"])
    
    if mode == "Search for specific model":
        model = st.text_input(f"Enter {subcat} model name (e.g., iPhone 14, Dell XPS 13):")
        details["model"] = model
    details["search_mode"] = mode

elif category == "Garments":
    subcat = st.radio("Who are you shopping for?", ["Men", "Women", "Kids"])
    details["subcategory"] = subcat

    if subcat == "Kids":
        age_range = st.selectbox("Select age group:", ["0-2", "3-5", "6-9", "10-12", "13+"])
        details["age_range"] = age_range
    else:
        clothing_type = st.multiselect("Select categories:", ["Shirts", "Trousers", "Shoes", "Accessories"])
        details["clothing_type"] = clothing_type

# 3. Country Selection
country = st.text_input("Enter the country or region to search in (e.g., Pakistan):")

# 4. Discount Filter
discount_only = st.checkbox("Show only discounted deals?", value=True)

# 5. Submit Button
if st.button("Search Deals"):
    if not country:
        st.warning("Please enter a country/region.")
    else:
        with st.spinner("Searching deals online..."):
            results = fetch_deals(category, details, country, discount_only)
            
            if results:
                for deal in results:
                    st.markdown(f"### [{deal['title']}]({deal['url']})")
                    st.markdown(f"**Price:** {deal['price']}  \n**Source:** {deal['source']}")
                    st.write("---")
            else:
                st.info("No deals found. Try adjusting the search criteria.")
