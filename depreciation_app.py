from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
import io

st.header("Capital Assets")
if 'manager' not in st.session_state:
    class DepreciationScheduleManager:
        def __init__(self):
            self.assets = []

        def add_asset(self, address, city, state, zipcode, description, tax_basis, placed_in_service_date, recovery_period, safe_harbor_small, safe_harbor_de_minimis, safe_harbor_routine, bonus_depreciation, section_179):
            asset = {
                "address": address,
                "city": city,
                "state": state,
                "zipcode": zipcode,
                "description": description,
                "tax_basis": tax_basis,
                "placed_in_service_date": datetime.strptime(placed_in_service_date, "%m-%d-%Y"),
                "recovery_period": recovery_period,
                "monthly_depreciation": tax_basis / (recovery_period * 12),
                "yearly_depreciation": tax_basis / recovery_period,
                "safe_harbor_small": safe_harbor_small,
                "safe_harbor_de_minimis": safe_harbor_de_minimis,
                "safe_harbor_routine": safe_harbor_routine,
                "bonus_depreciation": bonus_depreciation,
                "section_179": section_179
            }
            self.assets.append(asset)

        def export_asset_list(self):
            df = pd.DataFrame(self.assets)
            df["placed_in_service_date"] = df["placed_in_service_date"].dt.strftime("%m-%d-%Y")
            df.rename(columns={
                "address": "Property Address",
                "city": "City",
                "state": "State",
                "zipcode": "Zipcode",
                "description": "Asset Description",
                "tax_basis": "Tax Basis ($)",
                "placed_in_service_date": "Placed in Service Date",
                "recovery_period": "Recovery Period (Years)",
                "monthly_depreciation": "Monthly Depreciation ($)",
                "yearly_depreciation": "Yearly Depreciation ($)",
                "safe_harbor_small": "Safe Harbor for Small Taxpayers",
                "safe_harbor_de_minimis": "De Minimis Safe Harbor",
                "safe_harbor_routine": "Routine Maintenance Safe Harbor",
                "bonus_depreciation": "Bonus Depreciation",
                "section_179": "Section 179"
            }, inplace=True)
            return df

    st.session_state.manager = DepreciationScheduleManager()

manager = st.session_state.manager

st.title("Depreciation Schedule")

with st.sidebar:
    st.header("Add an Asset")
    
    st.subheader("Property Address")
    address = st.text_input("Street Address", help="Enter the street address of the property.")
    city = st.text_input("City", help="Enter the city where the property is located.")
    state = st.text_input("State", help="Enter the state abbreviation (e.g., TX, CA, NY).")
    zipcode = st.text_input("Zipcode", help="Enter the 5-digit ZIP code of the property.")
    
    st.subheader("Schedule Inputs")
    description = st.text_input("Asset Description", help="Provide a brief description of the asset (e.g., HVAC system, Roof Replacement).")
    tax_basis = st.number_input("Tax Basis ($)", min_value=0.0, step=100.0, help="Enter the cost basis of the asset for depreciation purposes.")
    placed_in_service_date = st.date_input("Placed in Service Date", format="MM/DD/YYYY", help="Select the date the asset was placed into service.")
    recovery_period = st.selectbox("Recovery Period", [5, 7, 15, 27.5, 39], help="Select the IRS-defined recovery period for this asset.")
    
    st.subheader("Applicable IRS Safe Harbors")
    safe_harbor_small = st.checkbox("Safe Harbor for Small Taxpayers", help="Applies to small taxpayers performing routine repairs and maintenance within specified financial limits.")
    safe_harbor_de_minimis = st.checkbox("De Minimis Safe Harbor", help="Allows taxpayers to deduct small expenses for tangible property below a certain threshold.")
    safe_harbor_routine = st.checkbox("Routine Maintenance Safe Harbor", help="Used for regularly scheduled maintenance to keep the asset in operating condition.")
    bonus_depreciation = st.checkbox("Bonus Depreciation", help="Allows immediate depreciation deductions for qualified property placed in service.")
    section_179 = st.checkbox("Section 179", help="Enables full expensing of eligible business assets up to an annual limit.")

    if st.button("Add Asset"):
        manager.add_asset(address, city, state, zipcode, description, tax_basis, placed_in_service_date.strftime("%m-%d-%Y"), recovery_period, safe_harbor_small, safe_harbor_de_minimis, safe_harbor_routine, bonus_depreciation, section_179)
        st.success(f"Asset '{description}' added successfully!")
        
        # Reset input fields
        st.session_state["address"] = ""
        st.session_state["city"] = ""
        st.session_state["state"] = ""
        st.session_state["zipcode"] = ""
        st.session_state["description"] = ""
        st.session_state["tax_basis"] = 0.0
        st.session_state["safe_harbor_small"] = False
        st.session_state["safe_harbor_de_minimis"] = False
        st.session_state["safe_harbor_routine"] = False
        st.session_state["bonus_depreciation"] = False
        st.session_state["section_179"] = False