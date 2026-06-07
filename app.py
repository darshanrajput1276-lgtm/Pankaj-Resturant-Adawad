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

# --- CONFIGURATION & STORAGE ---
SHOP_WHATSAPP_NUMBER = "918623864774" 
DATA_FILE = "menu.json"
ADMIN_PASSWORD = "pankaj_admin"  
MAPS_URL = "https://www.google.com/maps/place/Pankaj+Restaurant/@21.221159,75.4379684,17z/data=!3m1!4b1!4m6!3m5!1s0x3bd8e3005bbea4c9:0xab8ea2e4475c5b41!8m2!3d21.221159!4d75.4405433!16s%2Fg%2F11zkrvhsft?entry=ttu&g_ep=EgoyMDI2MDYwMy4xIKXMDSoASAFQAw%3D%3D"

# Master Bilingual Menu Items list
DEFAULT_MENU = {
    "Sweets / मिठाई 👑": [
        {"name": "Kaju Katli / काजू कतली (1kg)", "price": 800, "desc": "Premium cashew sweet / प्रीमियम काजूची ताजी मिठाई"},
        {"name": "Gulab Jamun / गुलाब जामुन (1kg)", "price": 400, "desc": "Soft, juicy saffron sugar syrup / मऊ आणि रसाळ गुलाब जाम"},
        {"name": "Rasgulla / रसगुल्ला (12 Pcs)", "price": 250, "desc": "Spongy, authentic Bengali style / स्पंजसारखा मऊ बंगाली रसगुल्ला"},
        {"name": "Rasmalai / रसमलाई (Per Plate)", "price": 50, "desc": "Rich, creamy saffron milk sweet / केशरयुक्त मलईदार आणि चविष्ट रसमलाई"},
        {"name": "Badam Barfi / बादाम बर्फी (1kg)", "price": 450, "desc": "Made with real almonds and ghee / शुद्ध तूप आणि बदामाची स्वादिष्ट बर्फी"},
    ],
    "Snacks / नाश्ता 🌶️": [
        {"name": "Pav Vada / पाव वडा (Per Pc)", "price": 10, "desc": "Spicy potato fritter inside fresh bread / germa-garam chavista pav vada"},
        {"name": "Aloo Vada / बटाटा वडा (Per Pc)", "price": 20, "desc": "Deep fried spiced potato dumpling / paramparik chavdar batata vada"},
        {"name": "Samosa / समोसा (Per Pc)", "price": 10, "desc": "Crispy pastry with spiced potatoes / गरमागरम बटाटा सारण भरलेला कुरकुरीत समोसा"},
        {"name": "Kachori / कचोरी (Per Pc)", "price": 10, "desc": "Flaky crust with savory lentil filling / खमंग मसाला आणि डाळीने भरलेली शेव कचोरी"},
        {"name": "Jalebi / जिलेबी (250g)", "price": 30, "desc": "Soft, juicy and crispy tempered with ghee / शुद्ध तुपात तळलेली कुरकुरीत रसाळ जिलेबी"},
        {"name": "Bhajiya / भजी (Per Plate)", "price": 10, "desc": "Crispy fried onion or potato fritters / गरमागरम आणि कुरकुरीत कांदा किंवा बटाटा भजी"},
        {"name": "Poha / पोहे (Per Plate)", "price": 10, "desc": "Traditional spiced flattened rice / सुप्रसिद्ध चवदार कांदा पोहे"},
    ],
}

# Helper functions to load and save data permanently
def load_menu():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                saved_data = json.load(f)
                if "Sweets / मिठाई 👑" not in saved_data:
                    save_menu(DEFAULT_MENU)
                    return DEFAULT_MENU
                return saved_data
        except Exception:
            return DEFAULT_MENU
    return DEFAULT_MENU

def save_menu(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Initialize session state for menu data
if "menu_data" not in st.session_state:
    st.session_state.menu_data = load_menu()

if "cart" not in st.session_state:
    st.session_state.cart = {}

# --- SIDEBAR LOGO & NAVIGATION ---
st.sidebar.markdown("<center>", unsafe_allow_html=True)

# Checks for logo images, defaults to text title if missing
if os.path.exists("viru logo copy.jpg"):
    st.sidebar.image(Image.open("viru logo copy.jpg"), use_container_width=True)
elif os.path.exists("viru logo cmyk.jpg"):
    st.sidebar.image(Image.open("viru logo cmyk.jpg"), use_container_width=True)
else:
    st.sidebar.title("🏪 पंकज रेस्टोरेंट")

st.sidebar.markdown("</center>", unsafe_allow_html=True)
st.sidebar.markdown("---")
app_mode = st.sidebar.radio("पंकज रेस्टोरेंट मेनू:", ["✨ Order Sweets & Snacks", "🔒 Admin Dashboard"])
st.sidebar.markdown("---")

st.sidebar.info("📍 पत्ता: अडावद\n📞 मो. 9623886387\n👨‍🍳 प्रो.प्रा. पंकज बैरागी / एम. बी. बैरागी")
st.sidebar.link_button("📍 View Shop on Google Maps", MAPS_URL, use_container_width=True)


# ==============================================================================
# VIEW 1: BRANDED CUSTOMER MENU
# ==============================================================================
if app_mode == "✨ Order Sweets & Snacks":
    if os.path.exists("pankaj res.jpg"):
        st.image(Image.open("pankaj res.jpg"), use_container_width=True)
    else:
        st.title("पंकज रेस्टोरेंट अँड स्वीट्स - अडावद")
    
    st.markdown("<h4 style='text-align: center; color: #cc0000; font-weight: bold;'>🍽️ शुद्धता, गुणवत्ता आणि अप्रतिम चव यांचा संगम  !! आमच्याकडे सर्व प्रकारचे ऑर्डर स्वीकारले जातील..</h4>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns([1.8, 1.2])

    # Left Column: Interactive Menu List & Showcase Image
    with col1:
        st.header("📋 Explore Our Menu / आमचा मेनू")
        
        if os.path.exists("4 by 6 pankaj res copy_2.jpg"):
            st.image(Image.open("4 by 6 pankaj res copy_2.jpg"), caption="Our Special Sweets & Snacks", use_container_width=True)
            st.markdown("---")
        elif os.path.exists("4 by 6 pankaj res copy.jpg"):
            st.image(Image.open("4 by 6 pankaj res copy.jpg"), caption="Our Special Sweets & Snacks", use_container_width=True)
            st.markdown("---")

        for category, items in st.session_state.menu_data.items():
            if items: 
                st.subheader(category)

                for item in items:
                    item_col, price_col, action_col = st.columns([3, 1, 1.5])

                    with item_col:
                        st.markdown(f"**{item['name']}**")
                        st.caption(item["desc"])

                    with price_col:
                        st.markdown(f"**₹{item['price']}**")

                    with action_col:
                        btn_key = f"add_{item['name']}_{category}"
                        if st.button("Add to Cart / जोडा", key=btn_key, use_container_width=True):
                            if item["name"] in st.session_state.cart:
                                st.session_state.cart[item["name"]]["qty"] += 1
                            else:
                                st.session_state.cart[item["name"]] = {
                                    "price": item["price"],
                                    "qty": 1,
                                }
                            st.rerun()
                st.markdown("---")

    # Right Column: Cart System & WhatsApp Generation
    with col2:
        st.header("🛒 Your Basket / तुमची टोपली")

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

            # Form fields
            st.subheader("🚚 Delivery Details / पत्ता तपशील")
            name = st.text_input("Your Name*", placeholder="Enter full name").strip()
            phone = st.text_input("Phone Number*", placeholder="10-digit mobile number").strip()
            order_type = st.radio("Order Type", ["Home Delivery / घरपोच सेवा", "Store Pickup / दुकानातून घेणे"])
            address = st.text_area("Delivery Address", placeholder="Required for Home Delivery (घरपोच सेवेसाठी आवश्यक)").strip()

            if st.button("Place Order via WhatsApp ✅", use_container_width=True):
                if not name or not phone:
                    st.error("Please fill out your Name and Phone Number.")
                elif "Home Delivery" in order_type and not address:
                    st.error("Please provide a delivery address.")
                else:
                    customer_phone = str(phone)
                    customer_name = str(name)
                    
                    whatsapp_msg = (
                        f"🔔 *NEW ORDER - PANKAJ RESTAURANT & SWEETS*\n\n"
                        f"👤 *Customer:* {customer_name}\n"
                        f"📞 *Phone:* {customer_phone}\n"
                        f"📦 *Type:* {order_type}\n"
                        f"📍 *Address:* {address if 'Home Delivery' in order_type else 'N/A'}\n\n"
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
            new_name = st.text_input("Product Name (e.g. Kaju Katli / काजू कतली)")
            new_price = st.number_input("Price (₹)", min_value=1, step=5)
            new_desc = st.text_input("Short Description (English & Marathi)")
            
            submit_new_item = st.form_submit_button("Add Item")
            if submit_new_item:
                if new_name and new_price:
                    st.session_state.menu_data[new_category].append({
                        "name": new_name, "price": int(new_price), "desc": new_desc
                    })
                    save_menu(st.session_state.menu_data) 
                    st.success(f"Added '{new_name}' successfully!")
                    st.rerun()

        st.markdown("---")
        st.subheader("⚙️ Current Inventory Management")
        
        # Track layout adjustments during continuous loop execution
        action_triggered = False

        for category, items in st.session_state.menu_data.items():
            st.write(f"### {category}")
            
            for index, item in enumerate(items):
                edit_col1, edit_col2, edit_col3 = st.columns([3, 2, 1])
                with edit_col1:
                    st.write(f"**{item['name']}**")
                    st.caption(item['desc'])
                with edit_col2:
                    new_p = st.number_input(f"Price (₹)", min_value=1, value=item['price'], key=f"p_{category}_{index}")
                    if new_p != item['price']:
                        st.session_state.menu_data[category][index]['price'] = int(new_p)
                        save_menu(st.session_state.menu_data) 
                with edit_col3:
                    st.write("") 
                    if st.button("🗑️ Delete", key=f"del_{category}_{index}", use_container_width=True):
                        st.session_state.menu_data[category].pop(index)
                        save_menu(st.session_state.menu_data) 
                        action_triggered = True
                        break 
            
            if action_triggered:
                st.rerun()
                
    elif passwd_input != "":
        st.error("Incorrect Password. Please try again.")
