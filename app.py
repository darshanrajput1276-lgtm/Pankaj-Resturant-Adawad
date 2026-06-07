import streamlit as st
import urllib.parse
from PIL import Image
import os
import json

# Set page configuration
st.set_page_config(
    page_title="Pankaj Restaurant & Sweets",
    page_icon="🍬",
    layout="wide",
)

# --- BRIGHT, HIGH-CONTRAST & ANIMATED VISUAL THEME ---
st.markdown("""
    <style>
    /* Light vibrant background */
    .stApp {
        background: linear-gradient(135deg, #FFFDF6 0%, #FFFFFF 100%);
    }
    
    /* CRITICAL COLOR FIX: Force all text labels to be highly visible */
    .product-title {
        color: #1A1A1A !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        margin-bottom: 2px !important;
    }
    .product-desc {
        color: #555555 !important;
        font-size: 0.9rem !important;
    }
    .product-price {
        color: #C62828 !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
    }
    
    /* Smooth Fade-In Animation for Main Page */
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(15px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .block-container {
        animation: fadeIn 0.8s ease-out;
    }

    /* Interactive Pulsing Buttons */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.04); box-shadow: 0 4px 15px rgba(255, 152, 0, 0.4); }
        100% { transform: scale(1); }
    }
    
    div.stButton > button:first-child {
        background-color: #FF9800 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 20px !important;
        border: none !important;
        transition: all 0.3s ease;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #E65100 !important;
        animation: pulse 1s infinite;
    }

    /* Out of Stock Indicator Style */
    .oos-badge {
        background-color: #FFEBEE;
        color: #C62828;
        padding: 5px 12px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        border: 1px solid #FFB3B3;
        text-align: center;
    }

    /* Animated Google Maps Button CSS */
    @keyframes bounceGlow {
        0%, 100% { transform: translateY(0); box-shadow: 0 4px 10px rgba(76, 175, 80, 0.3); }
        50% { transform: translateY(-6px); box-shadow: 0 10px 20px rgba(76, 175, 80, 0.6); }
    }
    .map-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
        color: white !important;
        padding: 12px 20px;
        border-radius: 25px;
        text-decoration: none !important;
        font-weight: bold;
        font-size: 0.95rem;
        margin: 15px 0;
        animation: bounceGlow 2.5s infinite ease-in-out;
        transition: all 0.3s ease;
        border: 1px solid #1B5E20;
    }
    .map-btn:hover {
        filter: brightness(1.1);
    }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURATION & STORAGE ---
SHOP_WHATSAPP_NUMBER = "918623864774" 
DATA_FILE = "menu.json"
ADMIN_PASSWORD = "pankaj_admin"

MAPS_URL = "https://www.google.com/maps/place/Pankaj+Restaurant/@21.221159,75.4379684,17z/data=!3m1!4b1!4m6!3m5!1s0x3bd8e3005bbea4c9:0xab8ea2e4475c5b41!8m2!3d21.221159!4d75.4405433!16s%2Fg%2F11zkrvhsft?entry=ttu&g_ep=EgoyMDI2MDYwMy4xIKXMDSoASAFQAw%3D%3D"

DEFAULT_MENU = {
    "Sweets 👑": [
        {"name": "Kaju Katli (1kg)", "price": 800, "desc": "Premium cashew sweet made with 100% silver foil", "available": True},
        {"name": "Gulab Jamun (1kg)", "price": 400, "desc": "Soft, juicy, and dipped in saffron sugar syrup", "available": True},
        {"name": "Motichoor Laddoo (1kg)", "price": 350, "desc": "Made with pure desi ghee and dry fruits", "available": True},
        {"name": "Rasgulla (12 Pcs)", "price": 250, "desc": "Spongy, light, and authentic Bengali style", "available": True},
    ],
    "Snacks 🌶️": [
        {"name": "Samosa (Per Pc)", "price": 20, "desc": "Crispy pastry filled with perfectly spiced potatoes", "available": True},
        {"name": "Kachori (Per Pc)", "price": 25, "desc": "Flaky crust with a savory, spiced lentil filling", "available": True},
        {"name": "Dhokla (250g)", "price": 60, "desc": "Soft, fluffy steamed gram flour tempered with mustard seeds", "available": True},
        {"name": "Aloo Tikki (Per Plate)", "price": 50, "desc": "Crispy potato patties served with sweet & tangy chutneys", "available": True},
    ],
}

def load_menu():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return DEFAULT_MENU
    return DEFAULT_MENU

def save_menu(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if "menu_data" not in st.session_state:
    st.session_state.menu_data = load_menu()

if "cart" not in st.session_state:
    st.session_state.cart = {}

# --- SIDEBAR LOGO & NAVIGATION ---
st.sidebar.markdown("<center>", unsafe_allow_html=True)
if os.path.exists("viru logo cmyk.jpg"):
    logo_img = Image.open("viru logo cmyk.jpg")
    st.sidebar.image(logo_img, use_column_width=True)
else:
    st.sidebar.title("🏪 पंकज रेस्टोरेंट")
st.sidebar.markdown("</center>", unsafe_allow_html=True)

st.sidebar.markdown("---")
app_mode = st.sidebar.radio("पंकज रेस्टोरेंट मेनू:", ["✨ Order Sweets & Snacks", "🔒 Admin Dashboard"])
st.sidebar.markdown("---")

st.sidebar.info("📍 पत्ता: अडावद\n📞 मो. 9623886387")

# Animated Location Button inside Sidebar
st.sidebar.markdown(f'<a href="{MAPS_URL}" target="_blank" class="map-btn">📍 Find Us on Google Maps 🗺️</a>', unsafe_allow_html=True)


# ==============================================================================
# VIEW 1: BRANDED CUSTOMER MENU
# ==============================================================================
if app_mode == "✨ Order Sweets & Snacks":
    # Render the main upper banner image
    if os.path.exists("pankaj res.jpg"):
        banner_img = Image.open("pankaj res.jpg")
        st.image(banner_img, use_column_width=True)
    else:
        st.markdown("<h1 style='text-align: center; color:#D32F2F;'>पंकज रेस्टोरेंट अँड स्वीट्स - अडावद</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #cc0000;'>आमच्याकडे सर्व प्रकारचे ऑर्डर स्वीकारल्या जातील.</h4>", unsafe_allow_html=True)
    
    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    # Left Column: Interactive Menu List
    with col1:
        st.header("📋 Explore Our Menu")

        for category, items in st.session_state.menu_data.items():
            if items: 
                st.subheader(category)

                for item in items:
                    item_col, price_col, action_col = st.columns([3, 1, 1.5])
                    is_available = item.get("available", True)

                    with item_col:
                        # Color fixed HTML injections
                        st.markdown(f'<div class="product-title">{item["name"]}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="product-desc">{item["desc"]}</div>', unsafe_allow_html=True)

                    with price_col:
                        st.markdown(f'<div class="product-price">₹{item["price"]}</div>', unsafe_allow_html=True)

                    with action_col:
                        btn_key = f"add_{item['name']}_{category}"
                        if is_available:
                            if st.button(f"Add to Cart 🛒", key=btn_key):
                                if item["name"] in st.session_state.cart:
                                    st.session_state.cart[item["name"]]["qty"] += 1
                                else:
                                    st.session_state.cart[item["name"]] = {
                                        "price": item["price"],
                                        "qty": 1,
                                    }
                                st.rerun()
                        else:
                            st.markdown('<div class="oos-badge">Out of Stock 🚫</div>', unsafe_allow_html=True)
                st.markdown("---")

    # Right Column: Cart System & WhatsApp Generation
    with col2:
        st.header("🛒 Your Basket")

        if not st.session_state.cart:
            st.info("Your cart is empty. Add items from the menu!")
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
                    st.markdown(f"**{item_name}** x {details['qty']}")
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

            # Form fields
            st.subheader("🚚 Delivery Details")
            name = st.text_input("Your Name*", placeholder="Enter full name")
            phone = st.text_input("Phone Number*", placeholder="10-digit mobile number")
            order_type = st.radio("Order Type", ["Home Delivery", "Store Pickup"])
            address = st.text_area("Delivery Address", placeholder="Required for Home Delivery")

            if st.button("Place Order via WhatsApp ✅", use_container_width=True):
                if not name or not phone:
                    st.error("Please fill out your Name and Phone Number.")
                elif order_type == "Home Delivery" and not address:
                    st.error("Please provide a delivery address.")
                else:
                    whatsapp_msg = (
                        f"🔔 *NEW ORDER - PANKAJ RESTAURANT & SWEETS*\n\n"
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
                    
                    st.success("🎉 Order formatted cleanly!")
                    st.markdown(f'[👉 Click Here to Complete Order on WhatsApp]({whatsapp_url})')


# ==============================================================================
# VIEW 2: MANAGEMENT CONTROL
# ==============================================================================
elif app_mode == "🔒 Admin Dashboard":
    st.title("🛠️ Pankaj Restaurant - Management Panel")
    st.caption("Add stock or alter items instantaneously.")
    st.markdown("---")

    passwd_input = st.text_input("Enter Admin Password to Unlock Panel", type="password")
    
    if passwd_input == ADMIN_PASSWORD:
        st.success("Access Granted!")
        
        st.subheader("➕ Add New Item to Menu")
        with st.form("add_item_form", clear_on_submit=True):
            new_category = st.selectbox("Select Category", list(st.session_state.menu_data.keys()))
            new_name = st.text_input("Product Name")
            new_price = st.number_input("Price (₹)", min_value=1, step=5)
            new_desc = st.text_input("Short Description")
            
            submit_new_item = st.form_submit_button("Add Item")
            if submit_new_item:
                if new_name and new_price:
                    st.session_state.menu_data[new_category].append({
                        "name": new_name, "price": int(new_price), "desc": new_desc, "available": True
                    })
                    save_menu(st.session_state.menu_data)
                    st.success(f"Added '{new_name}' successfully!")
                    st.rerun()

        st.markdown("---")
        st.subheader("⚙️ Current Inventory Management")
        
        for category, items in st.session_state.menu_data.items():
            st.write(f"### {category}")
            
            for index, item in enumerate(items):
                edit_col1, edit_col2, edit_col3, edit_col4 = st.columns([2.5, 1.5, 1.5, 1])
                current_availability = item.get("available", True)
                
                with edit_col1:
                    st.markdown(f'<div class="product-title">{item["name"]}</div>', unsafe_allow_html=True)
                with edit_col2:
                    new_p = st.number_input(f"Price (₹)", min_value=1, value=item['price'], key=f"p_{category}_{index}")
                    if new_p != item['price']:
                        st.session_state.menu_data[category][index]['price'] = int(new_p)
                        save_menu(st.session_state.menu_data)
                with edit_col3:
                    stock_status = st.checkbox("In Stock ✅", value=current_availability, key=f"stock_{category}_{index}")
                    if stock_status != current_availability:
                        st.session_state.menu_data[category][index]['available'] = stock_status
                        save_menu(st.session_state.menu_data)
                        st.rerun()
                with edit_col4:
                    if st.button("🗑️", key=f"del_{category}_{index}"):
                        st.session_state.menu_data[category].pop(index)
                        save_menu(st.session_state.menu_data)
                        st.rerun()
    elif passwd_input != "":
        st.error("Incorrect Password. Please try again.")
