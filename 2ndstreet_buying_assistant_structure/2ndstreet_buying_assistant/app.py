
# streamlit interface for entering single item. no ai currently
import streamlit as st

st.set_page_config(page_title="2nd Street Buying Assistant", layout="wide")
st.title("2nd Street Buying Assistant")
st.caption("S-rank buying form — early proof of concept. AI autofill will be added later.")

# dropdown choices
GENERAL_CATEGORIES = ["Clothing", "Footwear", "Accessories"]
SPECIFIC_CATEGORIES = ["Men's tops", "Men's bottoms", "Women's tops", "Women's bottoms", "Men's footwear", "Women's footwear", "Accessories"]
ITEM_TYPES = ["Jacket", "Blazer", "Shirt", "T-shirt", "Sweater", "Sweatshirt" "Jeans", "Trousers", "Dress", "Sneakers", "Boots", "Bag", "Other"]
MATERIALS = ["Cotton", "Denim", "Wool", "Leather", "Polyester", "Nylon", "Silk", "Other / Unknown"]
COLORS = ["Black", "White", "Gray", "Brown", "Beige", "Blue", "Green", "Red", "Yellow", "Pink", "Purple", "Multicolor", "Other / Unknown"]
PATTERNS = ["Solid", "Striped", "Plaid", "Graphic", "Floral", "Camouflage", "Other / Unknown"]

# Keep estimate items available while this browser session is open
if "estimate" not in st.session_state:
    st.session_state.estimate = []

with st.form("item_form"):
    st.subheader("S-rank item details")
    designer = st.text_input("Designer / Brand")
    item_name = st.text_input("Item name (optional)")
    product_code = st.text_input("Product code (optional)")

    general_category = st.selectbox("General category", GENERAL_CATEGORIES, index=None)
    specific_category = st.selectbox("Specific category", SPECIFIC_CATEGORIES, index=None)
    item_type = st.selectbox("Type of item", ITEM_TYPES, index=None)
    material = st.selectbox("Material", MATERIALS, index=None)
    color = st.selectbox("Color", COLORS, index=None)
    pattern = st.selectbox("Pattern", PATTERNS, index=None)
    size = st.text_input("Size")

    st.subheader("Pricing")
    left, right = st.columns(2)
    with left:
        selling_price = st.number_input("Selling price ($)", min_value=0.0, step=1.0, format="%.2f")
    with right:
        buying_price = st.number_input("Buying price / customer payout ($)", min_value=0.0, step=1.0, format="%.2f")

    submitted = st.form_submit_button("Add to estimate", type="primary")

if submitted:
    if not designer.strip() or selling_price <= 0 or buying_price <= 0:
        st.warning("Enter a designer and both prices before adding the item.")
    else:
        item = {
            "Designer": designer.strip(),
            "Item name": item_name.strip(),
            "Product code": product_code.strip(),
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
