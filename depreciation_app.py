from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
import io

if 'manager' not in st.session_state:
    class DepreciationScheduleManager:
        def __init__(self):
            self.assets = []

        def add_asset(self, description, tax_basis, placed_in_service_date, recovery_period, safe_harbor_small, safe_harbor_de_minimis, safe_harbor_routine, bonus_depreciation, section_179):
            asset = {
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

        def edit_asset(self, index, description, tax_basis, placed_in_service_date, recovery_period, safe_harbor_small, safe_harbor_de_minimis, safe_harbor_routine, bonus_depreciation, section_179):
            self.assets[index] = {
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

        def export_asset_list(self):
            df = pd.DataFrame(self.assets)
            df["placed_in_service_date"] = df["placed_in_service_date"].dt.strftime("%m-%d-%Y")
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