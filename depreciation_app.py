from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
import io

st.header("Assets Table")
if 'manager' not in st.session_state:
    class DepreciationScheduleManager:
        def __init__(self):
            self.assets = []

        def add_asset(self, description, tax_basis, placed_in_service_date, recovery_period, safe_harbor_small, safe_harbor_de_minimis, safe_harbor_routine, bonus_depreciation, section_179):
            asset = {
                "description": description,
                "tax_basis": tax_basis,
                "placed_in_service_date": datetime.strptime(placed_in_service_date, "%Y-%m-%d"),
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

        def edit_asset(self, index, description, tax_basis, placed_in_service_date, recovery_period, safe_harbor_small, safe_harbor_de_minimis, safe_harbor_routine, bonus_depreciation, section_179):
            self.assets[index] = {
                "description": description,
                "tax_basis": tax_basis,
                "placed_in_service_date": datetime.strptime(placed_in_service_date, "%Y-%m-%d"),
                "recovery_period": recovery_period,
                "monthly_depreciation": tax_basis / (recovery_period * 12),
                "yearly_depreciation": tax_basis / recovery_period,
                "safe_harbor_small": safe_harbor_small,
                "safe_harbor_de_minimis": safe_harbor_de_minimis,
                "safe_harbor_routine": safe_harbor_routine,
                "bonus_depreciation": bonus_depreciation,
                "section_179": section_179
            }

        def export_asset_list(self):
            df = pd.DataFrame(self.assets)
            df["placed_in_service_date"] = df["placed_in_service_date"].dt.strftime("%Y-%m-%d")
            df.rename(columns={
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

st.title("Depreciation Schedule Manager")

with st.sidebar:
    st.header("Add or Edit an Asset")
    asset_options = [f"{i + 1}: {asset['description']}" for i, asset in enumerate(manager.assets)]
    selected_asset = st.selectbox("Select an asset to edit or leave blank to add a new one", ["Add New Asset"] + asset_options)

    # IRS standard recovery periods sorted by duration
    recovery_periods = {
        "Equipment (5 years)": 5,
        "Vehicles (5 years)": 5,
        "Furniture (7 years)": 7,
        "Land Improvements (15 years)": 15,
        "Residential Real Estate (27.5 years)": 27.5,
        "Commercial Real Estate (39 years)": 39
    }

    if selected_asset == "Add New Asset":
        description = st.text_input("Asset Description")
        tax_basis = st.number_input("Tax Basis ($)", min_value=0.0, step=100.0)
        placed_in_service_date = st.date_input("Placed in Service Date", min_value=datetime(1900, 1, 1))
        recovery_period_label = st.selectbox("Recovery Period", list(recovery_periods.keys()))
        recovery_period = recovery_periods[recovery_period_label]

        st.subheader("IRS Safe Harbors")
        safe_harbor_small = st.checkbox("Safe Harbor for Small Taxpayers", help="Applicable to small taxpayers who meet specific eligibility criteria for routine repairs and maintenance.")
        safe_harbor_de_minimis = st.checkbox("De Minimis Safe Harbor", help="Allows taxpayers to deduct certain expenses for tangible property up to a specified dollar amount.")
        safe_harbor_routine = st.checkbox("Routine Maintenance Safe Harbor", help="Covers recurring maintenance activities expected to be performed as part of normal operations.")

        bonus_depreciation = st.checkbox("Bonus Depreciation", help="Allows a percentage of the asset cost to be deducted immediately in the year placed in service.")
        section_179 = st.checkbox("Section 179", help="Permits immediate expensing of certain asset purchases up to a specified dollar limit.")

        if st.button("Add Asset"):
            manager.add_asset(description, tax_basis, placed_in_service_date.strftime("%m-%d-%Y"), recovery_period, safe_harbor_small, safe_harbor_de_minimis, safe_harbor_routine, bonus_depreciation, section_179)
            st.success(f"Asset '{description}' added successfully!")
    else:
        index = int(selected_asset.split(":")[0]) - 1
        asset = manager.assets[index]

        description = st.text_input("Asset Description", value=asset["description"])
        tax_basis = st.number_input("Tax Basis ($)", min_value=0.0, step=100.0, value=asset["tax_basis"])
        placed_in_service_date = st.date_input("Placed in Service Date", value=asset["placed_in_service_date"])
        recovery_period_label = st.selectbox("Recovery Period", list(recovery_periods.keys()), index=list(recovery_periods.values()).index(asset["recovery_period"]))
        recovery_period = recovery_periods[recovery_period_label]

        st.subheader("IRS Safe Harbors")
        safe_harbor_small = st.checkbox("Safe Harbor for Small Taxpayers", value=asset["safe_harbor_small"], help="Applicable to small taxpayers who meet specific eligibility criteria for routine repairs and maintenance.")
        safe_harbor_de_minimis = st.checkbox("De Minimis Safe Harbor", value=asset["safe_harbor_de_minimis"], help="Allows taxpayers to deduct certain expenses for tangible property up to a specified dollar amount.")
        safe_harbor_routine = st.checkbox("Routine Maintenance Safe Harbor", value=asset["safe_harbor_routine"], help="Covers recurring maintenance activities expected to be performed as part of normal operations.")

        bonus_depreciation = st.checkbox("Bonus Depreciation", value=asset["bonus_depreciation"], help="Allows a percentage of the asset cost to be deducted immediately in the year placed in service.")
        section_179 = st.checkbox("Section 179", value=asset["section_179"], help="Permits immediate expensing of certain asset purchases up to a specified dollar limit.")

        if st.button("Save Changes"):
            manager.edit_asset(index, description, tax_basis, placed_in_service_date.strftime("%Y-%m-%d"), recovery_period, safe_harbor_small, safe_harbor_de_minimis, safe_harbor_routine, bonus_depreciation, section_179)
            st.success(f"Asset '{description}' updated successfully!")

if manager.assets:
    df = manager.export_asset_list()
    st.dataframe(df)  # Replaced AgGrid with a basic Streamlit table for compatibility

if st.button("Export All Assets"):
    df = manager.export_asset_list()
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Assets")
    buffer.seek(0)
    st.download_button("Download Asset List", buffer, file_name="assets.xlsx", mime="application/vnd.ms-excel")