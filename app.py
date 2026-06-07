import streamlit as st
import urllib.parse
from PIL import Image
import os

# Set layout and page tab details
st.set_page_config(
    page_title="Pankaj Restaurant & Sweets",
    page_icon="🍬",
    layout="wide",
)

# --- INJECT ADVANCED CSS FOR STYLING & ANIMATIONS ---
st.markdown("""
    <style>
    /* Main background and font adjustments */
    .stApp {
        background-color: #fcf8f2;
    }
    
    /* Food card container styling with hover animation */
    .food-card {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 20px;
        border-left: 5px solid #b51c1c; /* Deep Red Accent */
    }
    .food-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(181, 28, 28, 0.15);
    }
    
    /* Disabled out of stock card styling */
    .oos-card {
        background-color: #f2f2f2;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 20px;
        border-left: 5px solid #7f8c8d; /* Grey Accent */
        opacity: 0.6;
    }
    
    /* Button custom animations */
    div.stButton > button {
        background-color: #f39c12; /* Golden Saffron */
        color: white !important;
        border-radius: 8px;
        border: none;
        transition: all 0.2s ease-in-out;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #b51c1c !important; /* Changes to Red on hover */
        transform: scale(1.03);
    }
    
    /* Custom subheaders */
    .category-title {
        color: #b51c1c;
        font-family: 'Arial Black', sans-serif;
        border-bottom: 2px solid #f39c12;
        padding-bottom: 5px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)


# --- SHOP REGISTRATION DATA ---
SHOP_WHATSAPP_NUMBER = "919623886387" 

# --- INITIALIZE DATABASE VIA SESSION STATE ---
if "menu_data" not in st.session_state:
    st.session_state.menu_data = {
        "Sweets 👑": [
            {
                "name": "Kaju Katli (1kg)", 
                "price": 800, 
                "desc": "Premium cashew sweet made with 100% silver foil",
                "image": "https://images.unsplash.com/photo-1626132647523-66f5bf380027?w=400",
                "available": True
            },
            {
                "name": "Gulab Jamun (1kg)", 
                "price": 400, 
                "desc": "Soft, juicy, and dipped in saffron sugar syrup",
                "image": "https://images.unsplash.com/photo-1589135303623-0309903fa6f4?w=400",
                "available": True
            },
            {
                "name": "Motichoor Laddoo (1kg)", 
                "price": 350, 
                "desc": "Made with pure desi ghee and dry fruits",
                "image": "https://images.unsplash.com/photo-1605684954998-685c79d6a018?w=400",
                "available": False  # Initialized as Out of Stock for testing
            }
        ],
        "Snacks 🌶️": [
            {
                "name": "Samosa (Per Pc)", 
                "price": 20, 
                "desc": "Crispy pastry filled with perfectly spiced potatoes",
                "image": "https://images.unsplash.com/photo-1601050690597-df056fb4ce78?w=400",
                "available": True
            },
            {
                "name": "Kachori (Per Pc)", 
                "price": 25, 
                "desc": "Flaky crust with a savory, spiced lentil filling",
                "image": "https://images.unsplash.com/photo-1626132647523-66f5bf380027?w=400",
                "available": True
            },
            {
                "name": "Dhokla (250g)", 
                "price": 60, 
                "desc": "Soft, fluffy steamed gram flour tempered with mustard seeds",
                "image": "https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=400",
                "available": True
            }
        ],
        "Beverages 🥤": [
            {
                "name": "Special Masala Chai", 
                "price": 15, 
                "desc": "Brewed with fresh ginger, cardamom, and tea leaves",
                "image": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?w=400",
                "available": True
            },
            {
                "name": "Mango Lassi", 
                "price": 50, 
                "desc": "Thick, rich yogurt drink prepared with sweet mango pulp",
                "image": "https://images.unsplash.com/photo-1546173152-318a724de9a6?w=400",
                "available": True
            }
        ]
    }

if "cart" not in st.session_state:
    st.session_state.cart = {}

# --- SIDEBAR BRANDING & NAVIGATION ---
st.sidebar.markdown("<center>", unsafe_allow_html=True)
if os.path.exists("logo.jpg"):
    st.sidebar.image(Image.open("logo.jpg"), use_container_width=True)
else:
    st.sidebar.title("🏪 पंकज रेस्टोरेंट")
st.sidebar.markdown("</center>", unsafe_allow_html=True)

st.sidebar.markdown("---")
app_mode = st.sidebar.radio("Navigate Application:", ["✨ Customer Digital Menu", "🔒 Admin Dashboard Portal"])
st.sidebar.markdown("---")
st.sidebar.markdown("⏱️ **Status:** Open (7:00 AM - 10:00 PM)")
st.sidebar.info("📍 Location: Adavad, Maharashtra\n📞 Contact: +91 9623886387")


# ==============================================================================
# VIEW 1: PREMIUM CUSTOMER INTERFACE WITH IMAGES & ANIMATIONS
# ==============================================================================
if app_mode == "✨ Customer Digital Menu":
    # Top Banner Layout
    if os.path.exists("banner.jpg"):
        st.image(Image.open("banner.jpg"), use_container_width=True)
    else:
        st.title("पंकज रेस्टोरेंट अँड स्वीट्स - अडावद")
        
    st.markdown("<h3 style='text-align: center; color: #b51c1c; font-family: sans-serif;'>💥 ताजे आणि स्वादिष्ट पदार्थ मिळण्याचे एकमेव ठिकाण! 💥</h3>", unsafe_allow_html=True)
    st.markdown("---")

    # Split workspace into Menu layout and Cart Layout
    menu_col, cart_col = st.columns([2, 1])

    with menu_col:
        for category, items in st.session_state.menu_data.items():
            if items:
                st.markdown(f"<h2 class='category-title'>{category}</h2>", unsafe_allow_html=True)
                st.write("") # Padding space
                
                for item in items:
                    is_available = item.get("available", True)
                    card_class = "food-card" if is_available else "oos-card"
                    
                    st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
                    img_col, details_col, actions_col = st.columns([1.2, 2.5, 1.3])
                    
                    with img_col:
                        img_url = item.get("image", "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400")
                        st.image(img_url, use_container_width=True)
                        
                    with details_col:
                        if is_available:
                            st.markdown(f"### {item['name']}")
                        else:
                            st.markdown(f"### {item['name']} <span style='color: #7f8c8d; font-size: 1rem;'>(🔴 Out of Stock)</span>", unsafe_allow_html=True)
                        
                        st.markdown(f"<span style='color:#e67e22; font-size:1.2rem; font-weight:bold;'>Price: ₹{item['price']}</span>", unsafe_allow_html=True)
                        st.write(item["desc"])
                        
                    with actions_col:
                        st.write(" ") 
                        st.write(" ")
                        if is_available:
                            if st.button("➕ Add to Cart", key=f"add_{category}_{item['name']}"):
                                if item["name"] in st.session_state.cart:
                                    st.session_state.cart[item["name"]]["qty"] += 1
                                else:
                                    st.session_state.cart[item["name"]] = {"price": item["price"], "qty": 1}
                                st.toast(f"Added {item['name']} to Basket! 🛒")
                                st.rerun()
                        else:
                            # Disabled look-alike button if out of stock
                            st.button("🚫 Out of Stock", key=f"disabled_{category}_{item['name']}", disabled=True)
                            
                    st.markdown('</div>', unsafe_allow_html=True)

    # Cart System
    with cart_col:
        st.markdown("<h2 style='color:#b51c1c; text-align:center;'>🛒 Your Order Basket</h2>", unsafe_allow_html=True)
        st.markdown("---")
        
        if not st.session_state.cart:
            st.info("Your basket feels lonely. Choose items from the left menu panel!")
        else:
            total_bill = 0
            order_summary_string = ""
            items_to_remove = []

            for item_name, data in list(st.session_state.cart.items()):
                sub_total = data["price"] * data["qty"]
                total_bill += sub_total
                order_summary_string += f"- {item_name} x {data['qty']} (₹{sub_total})\n"

                c_row1, c_row2 = st.columns([3, 1])
                with c_row1:
                    st.markdown(f"**{item_name}**")
                    st.caption(f"₹{data['price']} × {data['qty']} = **₹{sub_total}**")
                with c_row2:
                    if st.button("❌", key=f"del_cart_{item_name}"):
                        items_to_remove.append(item_name)
                st.markdown("<hr style='margin: 5px 0px; border-top: 1px dashed #ccc;'>", unsafe_allow_html=True)

            if items_to_remove:
                for target in items_to_remove:
                    del st.session_state.cart[target]
                st.rerun()

            st.markdown(f"<h3 style='text-align:right; color:#b51c1c;'>Grand Total: ₹{total_bill}</h3>", unsafe_allow_html=True)
            st.markdown("---")

            # Checkout form fields
            st.subheader("🚚 Quick Delivery/Pickup Form")
            cust_name = st.text_input("Your Full Name*", placeholder="Ex. Rahul Patil")
            cust_phone = st.text_input("Mobile Number*", placeholder="10-digit smartphone number")
            delivery_mode = st.radio("Dispatch Method", ["Home Delivery", "Self-Store Pickup"])
            cust_address = st.text_area("Full Address (N/A for Pickup)", placeholder="Type complete home/shop address...")

            if st.button("🚀 Place Order & Launch WhatsApp", use_container_width=True):
                if not cust_name or not cust_phone:
                    st.error("Please enter your name and phone number to continue.")
                elif delivery_mode == "Home Delivery" and not cust_address:
                    st.error("Address is mandatory for home delivery orders.")
                else:
                    whatsapp_payload = (
                        f"🔔 *NEW DIGITAL ORDER - PANKAJ RESTAURANT*\n\n"
                        f"👤 *Customer:* {cust_name}\n"
                        f"📞 *Phone Contact:* {cust_phone}\n"
                        f"📦 *Delivery Mode:* {delivery_mode}\n"
                        f"📍 *Address:* {cust_address if delivery_mode == 'Home Delivery' else 'N/A'}\n\n"
                        f"📋 *Items Ordered:*\n{order_summary_string}\n"
                        f"💰 *Total Payable Bill:* ₹{total_bill}\n\n"
                        f"Please process my order as soon as possible!"
                    )
                    
                    encoded_payload = urllib.parse.quote(whatsapp_payload)
                    dispatch_link = f"https://wa.me/{SHOP_WHATSAPP_NUMBER}?text={encoded_payload}"
                    
                    st.success("Order packed perfectly inside application pipeline!")
                    st.markdown(f"[✨ Click Here to Instantly Send Order Message on WhatsApp]({dispatch_link})")


# ==============================================================================
# VIEW 2: FULL ADMIN SYSTEM WITH OUT OF STOCK TOGGLES
# ==============================================================================
elif app_mode == "🔒 Admin Dashboard Portal":
    st.title("🛠️ Pankaj Restaurant Management Console")
    st.caption("Add stock records, modify values, toggle availability, or remove entries.")
    st.markdown("---")

    # Part 1: Creation form layout
    st.subheader("➕ Inventory Item Enrollment Setup")
    with st.form("enrollment_form", clear_on_submit=True):
        col_form1, col_form2 = st.columns(2)
        
        with col_form1:
            chosen_cat = st.selectbox("Category Allocation", list(st.session_state.menu_data.keys()))
            prod_name = st.text_input("Item Name (e.g., Special Samosa Chaat)")
            prod_price = st.number_input("Item Selling Rate (₹)", min_value=1, value=50, step=5)
            
        with col_form2:
            prod_desc = st.text_input("Short Tasty Description", placeholder="Crispy crust mixed with...")
            prod_img_url = st.text_input("Product Web Image Link (URL)", value="https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400")
            
        submit_creation = st.form_submit_button("Publish Product Item Online")
        
        if submit_creation:
            if prod_name and prod_price:
                st.session_state.menu_data[chosen_cat].append({
                    "name": prod_name,
                    "price": int(prod_price),
                    "desc": prod_desc,
                    "image": prod_img_url,
                    "available": True # Default to available on creation
                })
                st.success(f"Successfully published '{prod_name}' to {chosen_cat} inventory grid!")
                st.rerun()

    st.markdown("---")
    
    # Part 2: Interactive Pricing & Stock Updates
    st.subheader("⚙️ Live Inventory & Stock Management")
    
    for section_cat, stock_items in st.session_state.menu_data.items():
        with st.expander(f"Manage Category: {section_cat} ({len(stock_items)} items)", expanded=True):
            for entry_idx, entry in enumerate(stock_items):
                r_col1, r_col2, r_col3, r_col4 = st.columns([2.5, 1.5, 1.5, 1])
                
                with r_col1:
                    st.markdown(f"**{entry['name']}**")
                    st.caption(entry["desc"])
                    
                with r_col2:
                    updated_price_value = st.number_input(
                        f"Rate (₹)", 
                        min_value=1, 
                        value=entry["price"], 
                        key=f"inline_edit_{section_cat}_{entry_idx}"
                    )
                    if updated_price_value != entry["price"]:
                        st.session_state.menu_data[section_cat][entry_idx]["price"] = int(updated_price_value)
                        st.toast(f"Price updated for {entry['name']}!")
                        
                with r_col3:
                    # THE OUT OF STOCK TOGGLE
                    stock_status = st.checkbox(
                        "In Stock ✅", 
                        value=entry.get("available", True), 
                        key=f"stock_toggle_{section_cat}_{entry_idx}"
                    )
                    if stock_status != entry.get("available", True):
                        st.session_state.menu_data[section_cat][entry_idx]["available"] = stock_status
                        st.rerun()
                        
                with r_col4:
                    st.write("") 
                    if st.button("🗑️ Remove", key=f"inline_del_{section_cat}_{entry_idx}"):
                        # If the item being deleted is in the active cart, clean it up
                        if entry['name'] in st.session_state.cart:
                            del st.session_state.cart[entry['name']]
                        st.session_state.menu_data[section_cat].pop(entry_idx)
                        st.rerun()
