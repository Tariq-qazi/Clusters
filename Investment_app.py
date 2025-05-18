import streamlit as st
import pandas as pd

# Load ROI + cluster strategy data
df = pd.read_csv("data/roi_segments_by_area_type_clustered.csv")
profiles = pd.read_csv("data/cluster_profiles.csv")
df = df.merge(profiles[['cluster_id', 'strategy_label']], on='cluster_id', how='left')

# Goal-to-strategy mapping
GOAL_MATCH = {
    "Yield": ["💸 High Yield – Entry Level", "🧱 Stable Core Holdings"],
    "Growth": ["🚀 Growth-Oriented Zones"],
    "Balanced": ["🏡 Balanced Premium Assets"]
}

# Streamlit UI
st.title("📊 Property Investment Advisor")
st.subheader("Choose your budget and goal to discover top areas")

# Sidebar inputs
budget = st.slider("Select your budget (AED)", 300000, 5000000, 1000000, step=50000)
goal = st.selectbox("Investment Goal", list(GOAL_MATCH.keys()))

# Filter & recommend logic
strategies = GOAL_MATCH[goal]
df_filtered = df[(df['median_price'] <= budget) & (df['strategy_label'].isin(strategies))]

if goal == "Yield":
    df_filtered = df_filtered.sort_values(by='rental_yield', ascending=False)
elif goal == "Growth":
    df_filtered = df_filtered.sort_values(by='growth_stage_encoded', ascending=True)
else:
    df_filtered = df_filtered.sort_values(by=['rental_yield', 'growth_stage_encoded'], ascending=[False, True])

# Display recommendations
st.markdown("### 📈 Top 5 Recommendations")
if df_filtered.empty:
    st.warning("No matching areas found. Try increasing your budget.")
else:
    top = df_filtered.head(5).copy()
    for i, row in top.iterrows():
        yield_pct = round(row['rental_yield'] * 100, 1)
        price = f"AED {int(row['median_price']):,}"
        st.markdown(f"""
        #### {row['area_name_en']} – {row['property_type_en']}
        **{row['strategy_label']}**  
        Entry Price: {price}  
        Estimated Yield: {yield_pct}%  
        Growth Stage: {row['growth_stage']}  
        Cluster: {row['cluster_id']}
        ---
        """)
