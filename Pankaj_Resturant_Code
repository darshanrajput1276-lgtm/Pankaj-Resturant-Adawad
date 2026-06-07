import streamlit as st
import urllib.parse

# Set page configuration
st.set_page_config(
    page_title="Pankaj Restaurant - Snacks & Sweets",
    page_icon="🍬",
    layout="wide",
)

# ❗ CHANGE THIS to your shop's WhatsApp number (Include Country Code, No "+" sign)
SHOP_WHATSAPP_NUMBER = "919876543210" 

# --- INITIALIZE DATA (Using Session State so changes persist during the session) ---
if "menu_data" not in st.session_state:
    st.session_state.menu_data = {
        "Sweets 👑": [
            {"name": "Kaju Katli (1kg)", "price": 800, "desc": "Premium cashew sweet made with 100% silver foil"},
            {"name": "Gulab Jamun (1kg)", "price": 400, "desc": "Soft, juicy, and dipped in saffron sugar syrup"},
            {"name": "Motichoor Laddoo (1kg)", "price": 350, "desc": "Made with pure desi ghee and dry fruits"},
            {"name": "Rasgulla (12 Pcs)", "price": 250, "desc": "Spongy, light, and authentic Bengali style"},
        ],
        "Snacks 🌶️": [
            {"name": "Samosa (Per Pc)", "price": 20, "desc": "Crispy pastry filled with perfectly spiced potatoes"},
            {"name": "Kachori (Per Pc)", "price": 25, "desc": "Flaky crust with a savory, spiced lentil filling"},
            {"name": "Dhokla (250g)", "price": 60, "desc": "Soft, fluffy steamed gram flour tempered with mustard seeds"},
            {"name": "Aloo Tikki (Per Plate)", "price": 50, "desc": "Crispy potato patties served with sweet & tangy chutneys"},
        ],
    }

if "cart" not in st.session_state:
    st.session_state.cart = {}

# --- NAVIGATION SIDEBAR ---
st.sidebar.title("🏪 Pankaj Restaurant")
app_mode = st.sidebar.radio("Go to Page:", ["✨ Customer Menu", "🔒 Admin Dashboard"])

# ==============================================================================
# VIEW 1: CUSTOMER MENU & ORDERING
# ==============================================================================
if app_mode == "✨ Customer Menu":
    st.title("🏪 Pankaj Restaurant")
    st.subheader("Your Favorite Destination for Delicious Snacks & Authentic Sweets!")
    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    # Left Column: Menu Browsing & Ordering
    with col1:
        st.header("📋 Explore Our Menu")

        for category, items in st.session_state.menu_data.items():
            if items:  # Only show category if it has items
                st.subheader(category)

                for item in items:
                    item_col, price_col, action_col = st.columns([3, 1, 1.5])

                    with item_col:
                        st.markdown(f"**{item['name']}**")
                        st.caption(item["desc"])

                    with price_col:
                        st.markdown(f"**₹{item['price']}**")

                    with action_col:
                        btn_key = f"add_{item['name']}"
                        if st.button(f"Add to Cart", key=btn_key):
                            if item["name"] in st.session_state.cart:
                                st.session_state.cart[item["name"]]["qty"] += 1
                            else:
                                st.session_state.cart[item["name"]] = {
                                    "price": item["price"],
                                    "qty": 1,
                                }
                            st.rerun()
                st.markdown("---")

    # Right Column: Shopping Cart & Checkout
    with col2:
        st.header("🛒 Your Basket")

        if not st.session_state.cart:
            st.info("Your cart is empty. Add some tasty items from the menu!")
        else:
            total_bill = 0
            items_to_remove = []
            order_summary_text = ""

            for item_name, details in list(st.session_state.cart.items()):
                item_total = details["price"] * details["qty"]
                total_bill += item_total
                order_summary_text += f"- {item_name} x {details['qty']} (₹{item_total})\n"

                cart_col1, cart_col2 = st.columns([3, 1])
                with cart_col1:
                    st.write(f"**{item_name}** x {details['qty']}")
                    st.caption(f"Price: ₹{item_total}")
                with cart_col2:
                    if st.button("❌", key=f"remove_{item_name}"):
                        items_to_remove.append(item_name)

            if items_to_remove:
                for item in items_to_remove:
                    del st.session_state.cart[item]
                st.rerun()

            st.markdown("---")
            st.write(f"### **Total Amount: ₹{total_bill}**")

            # Checkout Form
            st.subheader("🚚 Delivery Details")
            name = st.text_input("Your Name*", placeholder="Enter full name")
            phone = st.text_input("Phone Number*", placeholder="10-digit mobile number")
            order_type = st.radio("Order Type", ["Home Delivery", "Store Pickup"])
            address = st.text_area("Delivery Address", placeholder="Required for Home Delivery")

            if st.button("Place Order via WhatsApp ✅", use_container_width=True):
                if not name or not phone:
                    st.error("Please fill out your Name and Phone Number.")
                elif order_type == "Home Delivery" and not address:
                    st.error("Please provide a delivery address for Home Delivery.")
                else:
                    whatsapp_msg = (
                        f"🔔 *NEW ORDER - PANKAJ RESTAURANT*\n\n"
                        f"👤 *Customer:* {name}\n"
                        f"📞 *Phone:* {phone}\n"
                        f"📦 *Type:* {order_type}\n"
                        f"📍 *Address:* {address if order_type == 'Home Delivery' else 'N/A'}\n\n"
                        f"📋 *Items Ordered:*\n{order_summary_text}\n"
                        f"💰 *Total Bill Amount:* ₹{total_bill}\n\n"
                        f"Please confirm my order!"
                    )
                    
                    encoded_msg = urllib.parse.quote(whatsapp_msg)
                    whatsapp_url = f"https://wa.me/{SHOP_WHATSAPP_NUMBER}?text={encoded_msg}"
                    
                    st.success("🎉 Order details generated!")
                    st.markdown(f'[👉 Click Here to Send Order via WhatsApp]({whatsapp_url})')

# ==============================================================================
# VIEW 2: ADMIN DASHBOARD (Manage Prices & Items)
# ==============================================================================
elif app_mode == "🔒 Admin Dashboard":
    st.title("🛠️ Pankaj Restaurant - Management Panel")
    st.caption("Update prices, add new stock, or remove items on the fly.")
    st.markdown("---")

    # SECTION 1: ADD NEW ITEM
    st.subheader("➕ Add New Item to Menu")
    with st.form("add_item_form", clear_on_submit=True):
        new_category = st.selectbox("Select Category", ["Sweets 👑", "Snacks 🌶️"])
        new_name = st.text_input("Product Name (e.g., Kaju Katli (500g))")
        new_price = st.number_input("Price (₹)", min_value=1, step=5)
        new_desc = st.text_input("Short Description")
        
        submit_new_item = st.form_submit_button("Add Item to Menu")
        if submit_new_item:
            if new_name and new_price:
                st.session_state.menu_data[new_category].append({
                    "name": new_name, "price": int(new_price), "desc": new_desc
                })
                st.success(f"Added '{new_name}' to {new_category} successfully!")
                st.rerun()
            else:
                st.error("Please fill in Name and Price details.")

    st.markdown("---")

    # SECTION 2: EDIT PRICES OR REMOVE ITEMS
    st.subheader("⚙️ Current Inventory Management")
    
    for category, items in st.session_state.menu_data.items():
        st.write(f"### {category}")
        
        for index, item in enumerate(items):
            edit_col1, edit_col2, edit_col3 = st.columns([3, 2, 1])
            
            with edit_col1:
                st.write(f"**{item['name']}**")
                st.caption(item['desc'])
                
            with edit_col2:
                # Direct price editing input box
                new_p = st.number_input(f"Price (₹)", min_value=1, value=item['price'], key=f"price_input_{category}_{index}")
                if new_p != item['price']:
                    st.session_state.menu_data[category][index]['price'] = int(new_p)
                    st.toast(f"Updated price for {item['name']}!")
                    
            with edit_col3:
                # Delete item button
                if st.button("🗑️ Delete", key=f"delete_{category}_{index}"):
                    st.session_state.menu_data[category].pop(index)
                    st.rerun()
        st.markdown("---")
