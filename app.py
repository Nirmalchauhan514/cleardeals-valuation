import streamlit as st
from fpdf import FPDF
import os
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

    # Furnishing adjustment
    if furnishing == "Furnished":
        price += 200

    # Overlooking adjustment
    if overlooking in ["Garden", "Main road"]:
        price += 100

    # Other amenities
    amenity_bonus = {
        "Swimming Pool": 100,
        "Garden": 50,
        "Club house": 80,
        "Covered Parking": 60,
        "Security": 50,
    }

    for item in amenities:
        price += amenity_bonus.get(item, 0)

    # Property age adjustment
    if property_age == "0-5 years":
        price += 100
    elif property_age == "5-10 years":
        price += 50
    elif property_age == "10+ years":
        price -= 100

    return price

# --- Generate PDF ---
def generate_pdf(name, contact, area, bhk, size, price, price_low, price_high):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "🏠 Property Valuation Report", ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Valuation Powered by ClearDeals – Gandhinagar", ln=True)
