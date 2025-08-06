import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- Helper function to calculate price per sq. ft based on area ---
def get_price_per_sqft(area):
    price_map = {
        "Vavol": 3200,
        "Pethapur": 3100,
        "Kalol": 2800,
        "Randesan": 4000,
        "Randheja": 3000,
        "Koba": 3900,
        "Gift City": 6500,
        "Bhat": 3600,
        "Sughad": 3500,
    }
    return price_map.get(area, 3500)

# --- Calculate adjusted price based on amenities ---
def adjust_price(base_price, furnishing, overlooking, amenities, property_age):
    price = base_price

    if furnishing == "Furnished":
        price += 200

    if overlooking in ["Garden", "Main road"]:
        price += 100

    amenity_bonus = {
        "Swimming Pool": 100,
        "Garden": 50,
        "Club house": 80,
        "Covered Parking": 60,
        "Security": 50,
    }

    for item in amenities:
        price += amenity_bonus.get(item, 0)

    if property_age == "0-5 years":
        price += 100
    elif property_age == "5-10 years":
        price += 50
    elif property_age == "10+ years":
        price -= 100

    return price

# --- PDF Generation ---
def generate_pdf(name, contact, area, bhk, size, price, price_low, price_high):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "🏠 Property Valuation Report", ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "Valuation Powered by ClearDeals – Gandhinagar", ln=True)
    pdf.cell(0, 10, f"Name: {name}", ln=True)
    pdf.cell(0, 10, f"Contact: {contact}", ln=True)
    pdf.cell(0, 10, f"Area: {area}", ln=True)
    pdf.cell(0, 10, f"Property Type: {bhk}", ln=True)
    pdf.cell(0, 10, f"Size: {size} sq. ft", ln=True)
    pdf.cell(0, 10, f"Estimated Price: ₹{price:,.0f}", ln=True)
    pdf.cell(0, 10, f"Price Range: ₹{price_low:,.0f} - ₹{price_high:,.0f}", ln=True)

    filename = f"valuation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

# --- Streamlit App ---
st.set_page_config(page_title="ClearDeals Property Valuation", layout="centered")
st.title("🏠 Gandhinagar Property Valuation Tool")

with st.form("valuation_form"):
    name = st.text_input("Your Name")
    contact = st.text_input("Contact Number")
    area = st.selectbox("Select Area", [
        "Vavol", "Pethapur", "Kalol", "Randesan", "Randheja", "Koba", "Gift City", "Bhat", "Sughad"
    ])
    bhk = st.selectbox("Property Type", ["1 BHK", "2 BHK", "3 BHK", "Villa", "Plot/Land", "Commercial Shop"])
    size = st.number_input("Property Size (sq. ft)", min_value=100)

    furnishing = st.selectbox("Furnishing", ["Furnished", "Unfurnished"])
    overlooking = st.selectbox("Overlooking", ["None", "Garden", "Main road"])
    property_age = st.selectbox("Property Age", ["0-5 years", "5-10 years", "10+ years"])

    amenities = st.multiselect(
        "Other Amenities",
        ["Swimming Pool", "Garden", "Club house", "Covered Parking", "Security"]
    )

    submitted = st.form_submit_button("Generate Valuation Report")

    if submitted:
        base_price = get_price_per_sqft(area)
        final_price_per_sqft = adjust_price(base_price, furnishing, overlooking, amenities, property_age)
        total_price = final_price_per_sqft * size
        price_low = total_price * 0.95
        price_high = total_price * 1.05

        pdf_file = generate_pdf(name, contact, area, bhk, size, total_price, price_low, price_high)

        with open(pdf_file, "rb") as f:
            st.success(f"📄 Report Generated! Estimated price ₹{int(total_price):,}")
            st.download_button("⬇️ Download PDF Report", f, file_name=pdf_file, mime='application/pdf')
