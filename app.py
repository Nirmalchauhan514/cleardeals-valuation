# app.py - ClearDeals Gandhinagar Property Valuation Tool

import streamlit as st
from fpdf import FPDF
import pandas as pd
import os
from datetime import datetime

# Logo path
LOGO_PATH = "cleardeal_logo_converted.png"

# CSV for storing leads
LEADS_CSV = "leads_data.csv"

# Area-wise base pricing (₹ per sq.ft.)
PRICE_MAP = {
    "Vavol": 3300,
    "Pethapur": 3000,
    "Kalol": 2700,
    "Randesan": 3400,
    "Randheja": 2900,
    "Koba": 3600,
    "Gift City": 7000,
    "Bhat": 3100,
    "Sughad": 3200
}

# Amenities impact on pricing (in %)
AMENITY_IMPACT = {
    "Furnished": 0.05,
    "Unfurnished": 0.0,
    "Garden View": 0.02,
    "Main Road View": 0.01,
    "Swimming Pool": 0.03,
    "Club House": 0.02,
    "Covered Parking": 0.015,
    "Security": 0.01
}

# Title and logo
st.set_page_config(page_title="ClearDeals Gandhinagar Valuation", layout="centered")
st.image(LOGO_PATH, width=180)
st.title("🏠 Gandhinagar Property Valuation Tool")
st.caption("Valuation powered by ClearDeals – Gandhinagar")

st.markdown("---")

with st.form("valuation_form"):
    st.subheader("📋 Enter Property Details")

    name = st.text_input("Your Name")
    phone = st.text_input("Mobile Number")

    area = st.selectbox("Select Area", list(PRICE_MAP.keys()))
    property_type = st.selectbox("Property Type", ["1 BHK Flat", "2 BHK Flat", "3 BHK Flat", "Villa", "Commercial Shop", "Plot/Land"])
    sq_ft = st.number_input("Total Area (Sq. Ft.)", min_value=100)
    age = st.selectbox("Age of Property", ["New (0-3 yrs)", "4-7 yrs", "8+ yrs"])

    furnishing = st.radio("Furnishing", ["Furnished", "Unfurnished"])
    view = st.radio("Overlooking", ["Garden View", "Main Road View"])
    amenities = st.multiselect("Other Amenities", ["Swimming Pool", "Club House", "Covered Parking", "Security"])

    submit = st.form_submit_button("Get Valuation Report")

if submit:
    base_price = PRICE_MAP.get(area, 3000)
    multiplier = 1.0 + AMENITY_IMPACT.get(furnishing, 0) + AMENITY_IMPACT.get(view, 0)
    for am in amenities:
        multiplier += AMENITY_IMPACT.get(am, 0)

    final_price_per_sqft = base_price * multiplier
    total_value = final_price_per_sqft * sq_ft
    low_range = total_value * 0.95
    high_range = total_value * 1.05

    # Save lead
    lead_data = pd.DataFrame([[datetime.now(), name, phone, area, property_type, sq_ft, int(total_value)]],
                             columns=["Timestamp", "Name", "Phone", "Area", "Property Type", "Sq. Ft.", "Estimated Value"])

    if os.path.exists(LEADS_CSV):
        lead_data.to_csv(LEADS_CSV, mode='a', header=False, index=False)
    else:
        lead_data.to_csv(LEADS_CSV, index=False)

    # Show result
    st.success("✅ Valuation Complete!")
    st.write(f"**Estimated Value:** ₹{int(total_value):,} ({int(low_range):,} – {int(high_range):,})")

    # Create downloadable PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, x=10, y=8, w=40)
    pdf.ln(25)
    pdf.cell(200, 10, txt="Property Valuation Report", ln=True, align="C")
    pdf.ln(10)

    lines = [
        f"Name: {name}",
        f"Mobile: {phone}",
        f"Area: {area}",
        f"Property Type: {property_type}",
        f"Size: {sq_ft} sq.ft.",
        f"Furnishing: {furnishing}",
        f"Overlooking: {view}",
        f"Amenities: {', '.join(amenities) if amenities else 'None'}",
        f"Age of Property: {age}",
        "-----------------------------------",
        f"Estimated Price: ₹{int(total_value):,}",
        f"Price Range: ₹{int(low_range):,} – ₹{int(high_range):,}"
    ]
    for line in lines:
        pdf.cell(200, 10, txt=line, ln=True)

    output_pdf_path = f"valuation_{name.replace(' ', '_')}.pdf"
    pdf.output(output_pdf_path)

    with open(output_pdf_path, "rb") as f:
        st.download_button(label="📥 Download Valuation PDF",
                           data=f,
                           file_name=output_pdf_path,
                           mime="application/pdf")
