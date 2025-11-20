import streamlit as st
import qrcode
from io import BytesIO
from PIL import Image
import json
from datetime import datetime
import uuid

# Page configuration
st.set_page_config(
    page_title="Orange Crate Manager", 
    page_icon="🍊", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Title
st.title("🍊 Orange Crate Management System")
st.markdown("---")

# Create two columns for layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("Crate Details")
    
    # Input form
    with st.form("crate_form"):
        st.subheader("Enter Crate Information")
        
        # Farm details
        farm_name = st.text_input("Farm Name*", placeholder="e.g., Sunny Valley Orchards")
        farm_location = st.text_input("Farm Location*", placeholder="e.g., California, USA")
        
        # Orange details
        orange_variety = st.selectbox(
            "Orange Variety*",
            ["Valencia", "Navel", "Blood Orange", "Mandarin", "Clementine", "Tangerine", "Cara Cara", "Other"]
        )
        
        if orange_variety == "Other":
            orange_variety = st.text_input("Specify Variety")
        
        # Crate details
        weight_kg = st.number_input("Weight (kg)*", min_value=0.1, max_value=1000.0, value=20.0, step=0.1)
        quantity = st.number_input("Quantity (pieces)*", min_value=1, max_value=10000, value=100, step=1)
        
        # Quality grade
        quality_grade = st.selectbox(
            "Quality Grade*",
            ["Premium", "Grade A", "Grade B", "Grade C"]
        )
        
        # Harvest date
        harvest_date = st.date_input("Harvest Date*", value=datetime.now())
        
        # Additional details
        organic = st.checkbox("Organic Certified")
        notes = st.text_area("Additional Notes", placeholder="Any special remarks...")
        
        # Submit button
        submit_button = st.form_submit_button("Generate Crate ID & QR Code", use_container_width=True)

with col2:
    st.header("Generated Details")
    
    if submit_button:
        # Validate required fields
        if not farm_name or not farm_location:
            st.error("Please fill in all required fields marked with *")
        else:
            # Generate unique crate ID
            crate_id = f"ORC-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
            
            # Compile all crate data
            crate_data = {
                "Crate ID": crate_id,
                "Farm Name": farm_name,
                "Farm Location": farm_location,
                "Orange Variety": orange_variety,
                "Weight (kg)": weight_kg,
                "Quantity (pieces)": quantity,
                "Quality Grade": quality_grade,
                "Harvest Date": harvest_date.strftime("%Y-%m-%d"),
                "Organic": "Yes" if organic else "No",
                "Generated On": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Notes": notes if notes else "N/A"
            }
            
            # Display crate information
            st.success(f"✅ Crate ID Generated: **{crate_id}**")
            st.subheader("Crate Information")
            
            for key, value in crate_data.items():
                if key != "Notes":
                    st.text(f"{key}: {value}")
                else:
                    st.text(f"{key}: {value[:50]}..." if len(str(value)) > 50 else f"{key}: {value}")
            
            # Generate QR code
            qr_data = json.dumps(crate_data, indent=2)
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to bytes for display
            buf = BytesIO()
            qr_img.save(buf, format="PNG")
            buf.seek(0)
            
            st.subheader("QR Code")
            st.image(buf, caption=f"QR Code for {crate_id}", width=300)
            
            # Download button for QR code
            st.download_button(
                label="📥 Download QR Code",
                data=buf,
                file_name=f"{crate_id}_QR.png",
                mime="image/png",
                use_container_width=True
            )
            
            # Print button (downloads a printable version)
            st.markdown("---")
            st.subheader("Print Label")
            
            # Create printable label
            print_data = f"""
ORANGE CRATE LABEL
{'='*50}

Crate ID: {crate_id}
Farm: {farm_name}
Location: {farm_location}
Variety: {orange_variety}
Weight: {weight_kg} kg
Quantity: {quantity} pieces
Quality: {quality_grade}
Harvest Date: {harvest_date.strftime("%Y-%m-%d")}
Organic: {'Yes' if organic else 'No'}

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Notes: {notes if notes else 'N/A'}

{'='*50}
Scan QR code for full details
"""
            
            st.download_button(
                label="🖨️ Download Print Label (Text)",
                data=print_data,
                file_name=f"{crate_id}_Label.txt",
                mime="text/plain",
                use_container_width=True
            )
            
            # JSON download option
            st.download_button(
                label="📄 Download Data (JSON)",
                data=json.dumps(crate_data, indent=2),
                file_name=f"{crate_id}_Data.json",
                mime="application/json",
                use_container_width=True
            )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Orange Crate Management System | Track your harvest efficiently 🍊</p>
</div>
""", unsafe_allow_html=True)
