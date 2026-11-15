
# Streamlit interface for entering S-rank items.
import os  
import streamlit as st
from product_ai import identify_product  #ai prompts in other file

st.set_page_config(page_title="2nd Street Buying Assistant", layout="wide")
st.title("2nd Street Buying Assistant")
st.caption("S-rank buying form — AI-assisted identification proof of concept.")

# Dropdown choices 
GENERAL_CATEGORIES = ["Clothing", "Footwear", "Accessories"]
SPECIFIC_CATEGORIES = ["Men's tops", "Men's bottoms", "Women's tops", "Women's bottoms", "Men's footwear", "Women's footwear", "Accessories"]
ITEM_TYPES = ["Jacket", "Blazer", "Shirt", "T-shirt", "Sweater", "Sweatshirt", "Jeans", "Trousers", "Dress", "Sneakers", "Boots", "Bag", "Other"]
MATERIALS = ["Cotton", "Denim", "Wool", "Leather", "Polyester", "Nylon", "Silk", "Other / Unknown"]
COLORS = ["Black", "White", "Gray", "Brown", "Beige", "Blue", "Green", "Red", "Yellow", "Pink", "Purple", "Multicolor", "Other / Unknown"]
PATTERNS = ["Solid", "Striped", "Plaid", "Graphic", "Floral", "Camouflage", "Other / Unknown"]

OPTIONS = {
    "general_category": GENERAL_CATEGORIES,
    "specific_category": SPECIFIC_CATEGORIES,
    "item_type": ITEM_TYPES,
    "material": MATERIALS,
    "color": COLORS,
    "pattern": PATTERNS,
}

# Keep estimate items available while this session is open
if "estimate" not in st.session_state:
    st.session_state.estimate = []

# defaults
FORM_DEFAULTS = {
    "designer": "", "item_name": "", "product_code": "", "season": "",
    "general_category": None, "specific_category": None, "item_type": None,
    "material": None, "color": None, "pattern": None, "size": "",
    "selling_price": 0.0, "buying_price": 0.0,
}
for field, default in FORM_DEFAULTS.items():
    if field not in st.session_state:
        st.session_state[field] = default

# code/photo inputs
st.subheader("Identify an item with Gemini")
ai_designer = st.text_input("Designer / brand hint (optional)")
ai_code = st.text_input("Product code from tag (optional)")
photos = st.file_uploader(
    "Upload garment or tag photos (optional, up to 4)",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True,
)

if st.button("Identify with Gemini"):
    if not (ai_designer.strip() or ai_code.strip() or photos):
        st.warning("Enter a designer, a product code, or upload a photo first.")
    elif len(photos) > 4:
        st.warning("Please upload no more than four photos for this version.")
    else:
        # api key not in source code
        api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            try:
                api_key = st.secrets["GEMINI_API_KEY"]
            except (KeyError, FileNotFoundError):
                pass

        if not api_key:
            st.error("Missing GEMINI_API_KEY. Add it to .streamlit/secrets.toml locally.")
        else:
            try:
                with st.spinner("Identifying item..."):
                    result = identify_product(
                        api_key=api_key,
                        designer_hint=ai_designer,
                        product_code=ai_code,
                        photos=photos,
                        options=OPTIONS,
                    )

                # fill feilds
                for field in ("designer", "item_name", "product_code", "season"):
                    st.session_state[field] = (result.get(field) or "").strip()
                if not st.session_state.designer:
                    st.session_state.designer = ai_designer.strip()
                if not st.session_state.product_code:
                    st.session_state.product_code = ai_code.strip()

                # dropdowns
                unmatched = []
                for field, allowed in OPTIONS.items():
                    suggestion = (result.get(field) or "").strip()
                    match = next((v for v in allowed if v.casefold() == suggestion.casefold()), None)
                    st.session_state[field] = match
                    if suggestion and not match:
                        unmatched.append(f"{field.replace('_', ' ')}: {suggestion}")

                # manual input for pricing
                st.session_state.size = ""
                st.session_state.selling_price = 0.0
                st.session_state.buying_price = 0.0
                st.session_state.ai_notes = result.get("notes", "")
                st.success("Identification complete. Review the fields below.")
                if unmatched:
                    st.warning("Suggestions not in the dropdown options: " + "; ".join(unmatched))
            except Exception as error:
                st.error(f"Gemini identification failed: {error}")


if st.session_state.get("ai_notes"):
    st.info("AI notes: " + st.session_state.ai_notes)

with st.form("item_form"):
    st.subheader("S-rank item details")
   
    designer = st.text_input("Designer / Brand", key="designer")
    item_name = st.text_input("Item name (optional)", key="item_name")
    product_code = st.text_input("Product code (optional)", key="product_code")
    season = st.text_input("Season / collection (optional)", key="season")  

    general_category = st.selectbox("General category", GENERAL_CATEGORIES, index=None, key="general_category")
    specific_category = st.selectbox("Specific category", SPECIFIC_CATEGORIES, index=None, key="specific_category")
    item_type = st.selectbox("Type of item", ITEM_TYPES, index=None, key="item_type")
    material = st.selectbox("Material", MATERIALS, index=None, key="material")
    color = st.selectbox("Color", COLORS, index=None, key="color")
    pattern = st.selectbox("Pattern", PATTERNS, index=None, key="pattern")
    size = st.text_input("Size", key="size")

    st.subheader("Pricing")
    left, right = st.columns(2)
    with left:
        selling_price = st.number_input("Selling price ($)", min_value=0.0, step=1.0, format="%.2f", key="selling_price")
    with right:
        buying_price = st.number_input("Buying price / customer payout ($)", min_value=0.0, step=1.0, format="%.2f", key="buying_price")

    submitted = st.form_submit_button("Add to estimate", type="primary")

if submitted:
    if not designer.strip() or selling_price <= 0 or buying_price <= 0:
        st.warning("Enter a designer and both prices before adding the item.")
    else:
        item = {
            "Designer": designer.strip(),
            "Item name": item_name.strip(),
            "Product code": product_code.strip(),
            "Season": season.strip(),  # optionl field
            "General category": general_category or "",
            "Specific category": specific_category or "",
            "Type": item_type or "",
            "Material": material or "",
            "Color": color or "",
            "Pattern": pattern or "",
            "Size": size.strip(),
            "Selling price ($)": selling_price,
            "Buying price ($)": buying_price,
        }
        st.session_state.estimate.append(item)
        st.success("Item added to the estimate.")

st.subheader("Mock buying estimate")
if st.session_state.estimate:
    st.dataframe(st.session_state.estimate, hide_index=True, width="stretch")
    total = sum(item["Buying price ($)"] for item in st.session_state.estimate)
    st.metric("Total customer payout", f"${total:.2f}")
    if st.button("Clear estimate"):
        st.session_state.estimate = []
        st.rerun()
else:
    st.info("No items added yet.")
