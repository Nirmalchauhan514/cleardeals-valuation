import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- Helper function to get base price ---
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

# --- Price adjustment based on features ---
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

# --- PDF generation ---
def generate_pdf(name, contact, area, bhk, size, price, price_low, price_high):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Property Valuation Report", ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "Valuation Powered by ClearDeals - Gandhinagar", ln=True)
    pdf.ln(10)
    pdf.cell(0, 10, f"Client Name: {name}", ln=True)
    pdf.cell(0, 10, f"Contact: {contact}", ln=True)
    pdf.cell(0, 10, f"Area: {area}", ln=True)
    pdf.cell(0, 10, f"BHK: {bhk}", ln=True)
    pdf.cell(0, 10, f"Size: {size} sq. ft", ln=True)
    pdf.cell(0, 10, f"Estimated Price: ₹{price}/sq.ft", ln=True)
    pdf.cell(0, 10, f"Estimated Total: ₹{price * size:,}", ln=True)
    pdf.cell(0, 10, f"Price Range: ₹{price_low * size:,} - ₹{price_high * size:,}", ln=True)

    pdf.ln(20)
    pdf.set_font("Arial", "I", 11)
    pdf.cell(0, 10, "Created by:", ln=True)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Nirmal Chauhan", ln=True)
    pdf.cell(0, 8, "Head of Gandhinagar", ln=True)
    pdf.cell(0, 8, "Phone: 6356190197", ln=True)

    filename = f"valuation_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

# --- Streamlit UI ---
st.title("ClearDeals Property Valuation Tool – Gandhinagar")

with st.form("valuation_form"):
    name = st.text_input("Client Name")
    contact = st.text_input("Contact Number")
    area = st.selectbox("Area", ["Vavol", "Pethapur", "Kalol", "Randesan", "Randheja", "Koba", "Gift City", "Bhat", "Sughad"])
    bhk = st.selectbox("BHK", ["1 BHK", "2 BHK", "3 BHK", "Villa", "Commercial", "Plot"])
    size = st.number_input("Size (sq. ft)", min_value=100)
    furnishing = st.selectbox("Furnishing", ["Unfurnished", "Furnished"])
    overlooking = st.selectbox("Overlooking", ["None", "Garden", "Main road"])
    property_age = st.selectbox("Property Age", ["0-5 years", "5-10 years", "10+ years"])
    amenities = st.multiselect("Amenities", ["Swimming Pool", "Garden", "Club house", "Covered Parking", "Security"])

    submitted = st.form_submit_button("Generate Valuation Report")

    if submitted:
        base_price = get_price_per_sqft(area)
        adjusted_price = adjust_price(base_price, furnishing, overlooking, amenities, property_age)

        price_low = int(adjusted_price * 0.95)
        price_high = int(adjusted_price * 1.05)

        pdf_file = generate_pdf(name, contact, area, bhk, size, adjusted_price, price_low, price_high)
        st.success("✅ Report Generated Successfully!")

        with open(pdf_file, "rb") as f:
            st.download_button("Download Valuation Report PDF", f, file_name=pdf_file, mime="application/pdf")
