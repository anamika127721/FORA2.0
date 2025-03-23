import streamlit as st
import pandas as pd
import os
from PIL import Image
import uuid
import qrcode
from io import BytesIO
import matplotlib.pyplot as plt
import time

# File paths
DONATIONS_FILE = "donations.csv"
SALES_FILE = "sales.csv"
VOLUNTEER_FILE = "volunteer_items.csv"

# Load or create CSV files
def load_data(file):
    if os.path.exists(file) and os.path.getsize(file) > 0:
        return pd.read_csv(file)
    else:
        return pd.DataFrame(columns=["Food Item", "Image Name", "Servings", "Price"])


def save_data(file, entry):
    df = load_data(file)
    new_df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    new_df.to_csv(file, index=False)

# Inject custom CSS
st.markdown("""
    <style>
    .main-title {
        font-size: 40px;
        color: #c20a0a ;
        text-align: center;
        font-weight: bold;
    }
    .subheading {
        font-size: 24px;
        color: #333333;
        margin-top: 30px;
    }
    .quote {
        font-size: 20px;
        font-style: italic;
        color: #555;
        text-align: center;
        margin-bottom: 20px;
    }
    .section-label {
        font-size: 18px;
        color: #222;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
if "page" not in st.session_state:
    st.session_state.page = "Home"

st.sidebar.title("Navigation")

if st.sidebar.button("Home"):
    st.session_state.page = "Home"

if st.sidebar.button("Provider"):
    st.session_state.page = "Provider"

if st.sidebar.button("Consumer"):
    st.session_state.page = "Consumer"

if st.sidebar.button("Community Storage"):
    st.session_state.page = "Community Storage"

if st.sidebar.button("Volunteer"):
    st.session_state.page = "Volunteer"

if st.sidebar.button("Dashboard"):
    st.session_state.page = "Dashboard"

if st.sidebar.button("Help Desk"):
    st.session_state.page = "Help Desk"

# Home Page
if st.session_state.page == "Home":
    # ✅ Path to the image
    top_image_path = r"C:\Users\Anamika\Downloads\images\image4.jpg"
    top_image = Image.open(top_image_path)

    # ✅ Convert image to bytes for embedding
    import base64
    from io import BytesIO

    buffer = BytesIO()
    top_image.save(buffer, format="JPEG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    # ✅ Display centered image with styled caption
    st.markdown(f"""
        <div style='text-align: center;'>
            <img src="data:image/jpeg;base64,{img_str}" style='width: 500px; border-radius: 10px;'/>
            <p style='font-size: 16px;font-weight: bold;  margin-top: 10px;'>Join the Movement to Stop Hunger</p>
        </div>
    """, unsafe_allow_html=True)
#Tagline
    st.markdown("""
    <div style="text-align: center; margin-top: 30px;">
        <p style="
            font-style: italic;
            font-size: 30px;
            color: brown;
            font-family: 'Georgia', serif;">
            No food left behind, no stomach left hungry
        </p>
    </div>
""", unsafe_allow_html=True)




    st.markdown("<div class='main-title' style='text-align:center; font-size:32px; margin-top:20px;'>Welcome to Our Food Network</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
     

    image_paths = [
        r"C:\Users\Anamika\Downloads\images\image1.jpg",
        r"C:\Users\Anamika\Downloads\images\image2.jpg",
        r"C:\Users\Anamika\Downloads\images\image3.jpg"
    ]

    if "slider_index" not in st.session_state:
        st.session_state.slider_index = 0

    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        if st.button("⬅️", key="prev_img") and st.session_state.slider_index > 0:
            st.session_state.slider_index -= 1
    with col3:
        if st.button("➡️", key="next_img") and st.session_state.slider_index < len(image_paths) - 1:
            st.session_state.slider_index += 1

    # Show selected image
    image = Image.open(image_paths[st.session_state.slider_index])
    st.image(image, caption="Discover Amazing Restaurants!", use_container_width=True)

    # ✅ Description block
    description = """
    ### Fora: A Beacon of Hope Against Hunger

    Fora is more than just an organization; it is a movement to eliminate hunger and food wastage while fostering a culture of care and responsibility. 
    Hunger remains one of the most pressing challenges worldwide, yet millions of tons of food go to waste every year. At Fora, we saw this disparity 
    not as an insurmountable problem but as an opportunity to create change—and that's exactly what we've been doing.

    Through tireless efforts, Fora has distributed a significant amount of food to those who need it the most. From urban neighborhoods to remote communities, 
    we've reached thousands of individuals, offering not just meals but a lifeline of hope and humanity. Our work bridges the gap between food providers—such as 
    hotels, supermarkets, homemakers, event organizers, NGOs, and more—and the countless individuals struggling to find their next meal.
    """
    st.markdown(description)

    # Events section
    st.subheader("Community Events")
    events = ["No events"]
    selected_event = st.selectbox("Select an event", events)



# Provider Page
elif st.session_state.page == "Provider":
    st.markdown("<div class='main-title'>Provider Dashboard</div>", unsafe_allow_html=True)
    provider_name = st.text_input("Enter your name (for tracking your items)")

    if provider_name:
        provider_type = st.selectbox("Select Category", ["Hotels", "Events", "Supermarkets", "Homemakers", "NGO", "Others"])
        action = st.radio("Do you want to Donate or Sell?", ["Donate", "Sell"])
        st.markdown(f"<div class='subheading'>What would you like to {action.lower()}?</div>", unsafe_allow_html=True)

        item = st.text_input("Food Item")
        uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
        servings = st.text_input("Number of Servings")

        price = "Free"
        if action == "Sell":
            price = st.text_input("Enter Price (₹)")

        if st.button("Submit"):
            if not item or not servings:
                st.error("Please fill all required fields.")
            elif uploaded_file is None:
                st.error("Please upload an image.")
            else:
                upload_folder = "uploads"
                os.makedirs(upload_folder, exist_ok=True)
                image_path = os.path.join(upload_folder, uploaded_file.name)
                with open(image_path, "wb") as f:
                    f.write(uploaded_file.read())

                data = {
                    "Provider Name": provider_name,
                    "Food Item": item,
                    "Image Name": image_path,
                    "Servings": servings,
                    "Price": price if action == "Sell" else "Free"
                }

                file = SALES_FILE if action == "Sell" else DONATIONS_FILE
                df = load_data(file)
                df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
                df.to_csv(file, index=False)
                st.success(f"{item} submitted successfully!")

        # Show provider's submitted items
        st.markdown(f"<div class='subheading'>Your Added Items</div>", unsafe_allow_html=True)
        if action == "Sell":
           file = SALES_FILE
        else:
           file = DONATIONS_FILE  # New CSV for volunteer-managed donations
        df = load_data(file)

        if not df.empty and "Provider Name" in df.columns:
            provider_items = df[df["Provider Name"] == provider_name]
            if provider_items.empty:
                st.info("You haven't added any items yet.")
            else:
                for i, row in provider_items.iterrows():
                    with st.container():
                        st.markdown("---")
                        if os.path.exists(row["Image Name"]):
                            st.image(row["Image Name"], width=250)
                        st.markdown(f"**🍽️ Item:** {row['Food Item']}")
                        st.markdown(f"**🔢 Servings:** {row['Servings']}")
                        st.markdown(f"**💰 Price:** ₹{row['Price']}" if row['Price'] != "Free" else "**💰 Price:** Free")

                        if st.button("❌ Remove", key=f"remove_{i}"):
                            df = df.drop(row.name)
                            df.to_csv(file, index=False)
                            st.success(f"{row['Food Item']} removed.")
                            st.rerun()


# Consumer Page
elif st.session_state.page == "Consumer":
    st.markdown("<div class='main-title'>Consumer Section</div>", unsafe_allow_html=True)

    # ✅ Removed Free Food option
    df = load_data(SALES_FILE)

    st.markdown("<div class='subheading'>Available Food for Sale</div>", unsafe_allow_html=True)

    if df.empty:
        st.info("No items available.")
    else:
        for i, row in df.iterrows():
            with st.container():
                st.markdown("---")
                image_path = row['Image Name']
                if os.path.exists(image_path):
                    st.image(image_path, width=250)
                else:
                    st.warning("Image not found.")

                st.markdown(f"**🍽️ Item:** {row['Food Item']}")
                st.markdown(f"**🔢 Servings:** {row['Servings']}")
                st.markdown(f"**💰 Price:** ₹{row['Price']}" if row['Price'] != "Free" else "**💰 Price:** Free")

                quantity_key = f"quantity_{i}"
                if quantity_key not in st.session_state:
                    st.session_state[quantity_key] = 0

                col1, col2, col3 = st.columns([1, 1, 2])
                with col1:
                    if st.button("➖", key=f"minus_{i}"):
                        if st.session_state[quantity_key] > 0:
                            st.session_state[quantity_key] -= 1
                with col2:
                    if st.button("➕", key=f"plus_{i}"):
                        st.session_state[quantity_key] += 1
                with col3:
                    st.write(f"**Quantity:** {st.session_state[quantity_key]}")

                if st.button("🛒 Get", key=f"get_{i}"):
                    if st.session_state[quantity_key] > 0:
                        st.success(f"{st.session_state[quantity_key]} x {row['Food Item']} selected!")
                    else:
                        st.warning("Please select at least 1 quantity.")


# Community Storage Page
elif st.session_state.page == "Community Storage":
    st.markdown("<div class='main-title'>Community Storage</div>", unsafe_allow_html=True)

    # ✅ Description block
    description = """
    ### Fora: A Beacon of Hope Against Hunger

      A Safe and Accessible Space for Food Donations Our Community Storage feature is a secure and accessible space where food providers can store their surplus food, making it easily available to those in need. This innovative solution helps reduce food waste, supports the community, and fosters a sense of social responsibility. 
      
      "Community Fridge" - a innovative food distribution app feature that allows hostellers to store perishable food items in communal refrigerators. Users can deposit/withdraw food by scanning a unique QR code, with payments deducted/incentives rewarded through the app.
    """
    st.markdown(description)


    unique_id = str(uuid.uuid4())
    qr = qrcode.make(f"Unique ID: {unique_id}")
    buffer = BytesIO()
    qr.save(buffer)
    st.image(buffer.getvalue(), caption="Your Unique QR Code", use_container_width=False)
    st.success(f"QR Code ID: {unique_id}")

#Volunteer
elif st.session_state.page == "Volunteer":
    st.markdown("<div class='main-title'>Volunteer Dashboard</div>", unsafe_allow_html=True)
    df = load_data(DONATIONS_FILE)


    st.markdown("<div class='subheading'>Donated Items for Distribution</div>", unsafe_allow_html=True)

    if df.empty:
        st.info("No donated items available yet.")
    else:
        for i, row in df.iterrows():
            with st.container():
                st.markdown("---")
                image_path = row["Image Name"]
                if os.path.exists(image_path):
                    st.image(image_path, width=250)
                else:
                    st.warning("Image not found.")

                st.markdown(f"**🍽️ Item:** {row['Food Item']}")
                st.markdown(f"**🔢 Servings:** {row['Servings']}")
                st.markdown("**🧍 Provided by:** " + str(row.get("Provider Name", "Unknown")))


                quantity_key = f"vol_quantity_{i}"
                if quantity_key not in st.session_state:
                    st.session_state[quantity_key] = 0

                col1, col2, col3 = st.columns([1, 1, 2])
                with col1:
                    if st.button("➖", key=f"vol_minus_{i}"):
                        if st.session_state[quantity_key] > 0:
                            st.session_state[quantity_key] -= 1
                with col2:
                    if st.button("➕", key=f"vol_plus_{i}"):
                        st.session_state[quantity_key] += 1
                with col3:
                    st.write(f"**Quantity to Distribute:** {st.session_state[quantity_key]}")
                if st.button("🛒 Get", key=f"get_{i}"):
                    if st.session_state[quantity_key] > 0:
                        st.success(f"{st.session_state[quantity_key]} x {row['Food Item']} selected!")
                    else:
                        st.warning("Please select at least 1 quantity.")



# MyDashboard
elif st.session_state.page == "Dashboard":
    st.markdown("<div class='main-title'>Dashboard</div>", unsafe_allow_html=True)

    # Sample Data
    charity_data = {"Provider": ["Foodie's", "T&T", "NMR", "KFC", "Annapurnna"], "Donations": [50, 75, 100, 125, 150]}
    ratings_data = {"Providers": ["Foodie's", "T&T", "NMR", "KFC", "Annapurnna"], "Ratings": [4.2, 4.5, 4.6, 4.7, 4.8]}

    charity_df = pd.DataFrame(charity_data)
    ratings_df = pd.DataFrame(ratings_data)

    # Charity Bar Graph
    st.subheader("Total Donations by Provider")
    fig1, ax1 = plt.subplots()
    ax1.bar(charity_df["Provider"], charity_df["Donations"], color="skyblue")
    ax1.set_xlabel("Provider")
    ax1.set_ylabel("Total Donations")
    ax1.set_title("Donations per Provider")
    st.pyplot(fig1)

    # Ratings Bar Graph
    st.subheader("Provider Ratings")
    fig2, ax2 = plt.subplots()
    ax2.bar(ratings_df["Providers"], ratings_df["Ratings"], color="orange")
    ax2.set_xlabel("Provider")
    ax2.set_ylabel("Average Rating")
    ax2.set_title("User Ratings per Provider")
    st.pyplot(fig2)
#Help Desk
elif st.session_state.page == "Help Desk":
    st.title("Help Desk")
    st.write("For any queries, contact us through the following:")
    st.markdown("📷 Instagram: [Your Instagram Handle](https://instagram.com/yourhandle)")
    st.markdown("📞 Contact Number: +1234567890")
    st.markdown("📘 Facebook: [Your Facebook Page](https://facebook.com/yourpage)")