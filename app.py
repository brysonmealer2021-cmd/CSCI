import streamlit as st
import pandas as pd
from supabase import create_client
import random
from datetime import datetime, timedelta

# 1. THE TOOLS (DATABASE CONNECTION)
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# 2. THE CUSTOM THEME (Teal Buttons & Deep Blue Titles)
st.markdown("""
    <style>
    div.stButton > button {
        background-color: #008080 !important;
        color: white !important;
        border-radius: 8px;
        border: none;
        width: 100%;
        font-weight: bold;
        height: 3em;
    }
    div.stButton > button:hover {
        background-color: #20b2aa !important;
        color: white !important;
    }
    h1, h2, h3 {
        color: #1a5276 !important;
        font-weight: bold;
    }
    .stExpander {
        border: 1px solid #008080 !important;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SESSION STATE
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'steward_name' not in st.session_state:
    st.session_state.steward_name = ""
if 'steward_role' not in st.session_state:
    st.session_state.steward_role = ""
if 'blessing_received' not in st.session_state:
    st.session_state.blessing_received = False

# 4. THE PRAYER RINGS
blessings_map = {
    "gay": [
        "O Lord Almighty, the Healer of our souls and bodies, who put down and raise up, visit Thy servant in her physical trial. Grant her patience and restore her to health.",
        "O Christ, who alone art our Defender, visit and heal Thy suffering servant. Deliver her from sickness and bitter pain.",
        "Holy Father, Physician of our souls and bodies, send down Thy healing power. Comfort her in her weakness and grant her the quiet strength to endure."
    ],
    "katelyn": [
        "O Lord, bless the heavy and holy labor of motherhood. Grant her the physical strength to run the race and the spiritual patience.",
        "Establish the work of her hands, O Lord. Give her endurance in her body and stillness in her heart as she tends to her family.",
        "Most Holy Theotokos, guide this mother's daily labor. Multiply her strength and surround her house with grace."
    ],
    "malinda": [
        "O Lord, who bore the heavy cross, grant strength to the one who carries the weight for her family. Give her broad shoulders and a quiet mind.",
        "Lord, bless the one who leads and organizes the care of her father. Grant her wisdom, unending patience, and rest from her heavy burdens.",
        "O Master, look upon the one who bears the yoke of leadership in this house. Grant her rest when she is tired, and steady hands when the decisions are heavy."
    ],
    "mandy": [
        "Let not your heart be troubled, neither let it be afraid. O Lord, speak peace to her anxious thoughts and still the storms within.",
        "O Christ, who calmed the raging sea, quiet the restless waters of her mind. Grant her a deep and abiding stillness today.",
        "Most Holy Theotokos, calm the anxious spirit of Thy servant. Bring her the gentle quiet of the Skete, that she may rest securely in God's care."
    ],
    "bryce": [
        "O Lord and Master of my life, grant the spirit of chastity, humility, patience, and love to Thy servant.",
        "Illumine our darkness, O Lord, and grant us a peaceful and undisturbed watch. Drive away all weariness of the flesh.",
        "Lord Jesus Christ, Son of God, have mercy on me, a sinner. Grant me a quiet spirit to tend the elder today."
    ]
}

def get_blessing(username):
    name_key = username.strip().lower()
    return random.choice(blessings_map.get(name_key, ["Peace be to this house, and to all who dwell herein."]))

# 5. LOGIN SCREEN
if not st.session_state.logged_in:
    st.title("☦️ The Steward's Daily Office")
    name_input = st.text_input("Identify yourself:")
    pin_input = st.text_input("PIN:", type="password")
    if st.button("Cross the Threshold"):
        try:
            user_query = supabase.table("users").select("*").eq("username", name_input).eq("pin", pin_input).execute()
            if user_query.data:
                st.session_state.logged_in = True
                st.session_state.steward_name = user_query.data[0]['username']
                st.session_state.steward_role = user_query.data[0]['role']
                st.session_state.blessing_received = False
                st.session_state.daily_blessing = get_blessing(st.session_state.steward_name)
                st.rerun()
            else:
                st.error("The gate remains closed. Verify your name and PIN.")
        except Exception as e:
            st.error(f"Connection failure: {e}")

# 6. THE BLESSING GATE
elif not st.session_state.blessing_received:
    with st.container(border=True):
        st.subheader("☦️ A Blessing for the Watch")
        st.write(f"*{st.session_state.daily_blessing}*")
        st.divider()
        if st.button("Amen", type="primary", use_container_width=True):
            st.session_state.blessing_received = True
            st.rerun()

# 7. THE MAIN LABOR
else:
    # Dynamic Titles
    current_hour = datetime.now().hour
    if 6 <= current_hour < 12: dynamic_title, wt, wq = "🌅 The Morning Offering", "🌅 Morning Light", "“Grant me to greet the day in peace.”"
    elif 12 <= current_hour < 18: dynamic_title, wt, wq = "☀️ The Midday Labor", "☀️ Midday Labor", "“Establish the work of our hands.”"
    elif 18 <= current_hour < 21: dynamic_title, wt, wq = "🕯️ The Evening Sacrifice", "🕯️ Evening Watch", "“Let my prayer arise as incense.”"
    else: dynamic_title, wt, wq = "🌌 The Night Vigil", "🌌 Night Vigil", "“Behold, the Bridegroom comes at midnight.”"

    # Sidebar
    st.sidebar.write(f"**Steward:** {st.session_state.steward_name}")
    st.sidebar.divider()
    st.sidebar.subheader("☦️ The Jesus Prayer")
    st.sidebar.caption("*Lord Jesus Christ, Son of God, have mercy on me, a sinner.*")
    st.sidebar.divider()
    st.sidebar.subheader("☦️ The Trisagion")
    st.sidebar.caption("*Holy God, Holy Mighty, Holy Immortal, have mercy on us.*")
    if st.sidebar.button("Lock the Cell"):
        st.session_state.logged_in = False
        st.rerun()

    st.title(f"☦️ {dynamic_title}")
    
    # Rotating St. Ephrem
    st.info(random.choice([
        "“O Lord and Master of my life, take from me the spirit of sloth, despair, lust of power, and idle talk.”",
        "“But give rather the spirit of chastity, humility, patience, and love to Thy servant.”",
        "“Yea, O Lord and King, grant me to see my own transgressions, and not to judge my brother.”"
    ]))

    if st.session_state.steward_role.strip().lower() == "daughter":
        st.success("The watch is steady and your father is in good hands. The complete ledger is laid open below.")
    else:
        shift = st.radio("Select Vigil Shift:", ["Day", "Night", "Overnight"], horizontal=True)

        # --- NUTRITION & HYDRATION (Mapped to meal_info) ---
        with st.expander("🍲 Nutrition & Hydration", expanded=True):
            forty_eight_ago = (datetime.now() - timedelta(hours=48)).isoformat()
            try:
                logs = supabase.table("care_logs").select("meal_info").gt("created_at", forty_eight_ago).execute()
                data_list = logs.data if logs.data else []
            except:
                data_list = []
            
            total_oz = sum(int(e['meal_info'].split('(')[1].split('oz')[0]) for e in data_list if e.get('meal_info') and "Drink:" in e['meal_info'])
            food_p = [int(e['meal_info'].split('(')[1].split('%')[0]) for e in data_list if e.get('meal_info') and "Food:" in e['meal_info']]
            avg_food = int(sum(food_p)/len(food_p)) if food_p else 0

            col_nut, col_hyd = st.columns(2)
            with col_nut:
                st.markdown(f"### 🍞 Nutrition ({avg_food}% avg)")
                food_item = st.text_input("What was eaten?", key="f_input_v3")
                food_slider = st.slider("% Consumed", 0, 100, 0, 10)
                if st.button("Seal Nutrition"):
                    supabase.table("care_logs").insert({
                        "steward": st.session_state.steward_name, "shift": shift,
                        "meal_info": f"Food: {food_item} ({food_slider}%)"
                    }).execute()
                    st.rerun()

            with col_hyd:
                st.markdown(f"### 💧 Hydration ({total_oz}oz total)")
                drink_item = st.text_input("What was drunk?", key="d_input_v3")
                drink_oz = st.number_input("Amount (oz)", min_value=0, max_value=64, value=0, step=1)
                if st.button("Seal Hydration", type="primary"):
                    supabase.table("care_logs").insert({
                        "steward": st.session_state.steward_name, "shift": shift,
                        "meal_info": f"Drink: {drink_item} ({drink_oz}oz)"
                    }).execute()
                    st.rerun()

        # --- VITALS (Explicitly Mapped to bp, hr, spo2, glucose) ---
        with st.expander("🩺 Vitals", expanded=False):
            st.caption("“A man ought to take heed to his own measure.”")
            v1, v2, v3, v4 = st.columns(4)
            bp_val = v1.text_input("BP")
            hr_val = v2.text_input("HR")
            sp_val = v3.text_input("SpO2 %")
            gl_val = v4.text_input("Glucose")
            if st.button("Seal Vitals"):
                supabase.table("care_logs").insert({
                    "steward": st.session_state.steward_name, "shift": shift,
                    "bp": bp_val, "hr": hr_val, "spo2": sp_val, "glucose": gl_val
                }).execute()
                st.success("Vitals sealed in designated columns.")

        # --- CONTINENCE (Explicitly Mapped to output_type, output_details) ---
        with st.expander("🕒 Continence Round", expanded=False):
            st.caption("“Blessed is he that considereth the poor and needy.”")
            bm_ur = st.radio("Output:", ["None", "Urine", "Bowel Movement", "Both"], horizontal=True)
            det = st.text_input("Details / Appearance:")
            if st.button("Seal Continence"):
                supabase.table("care_logs").insert({
                    "steward": st.session_state.steward_name, "shift": shift,
                    "output_type": bm_ur, "output_details": det
                }).execute()
                st.success("Continence sealed in designated columns.")

        # --- MEDICATIONS & CARE (Explicitly Mapped to medications, notes) ---
        st.header("💊 Medications & General Care")
        with st.container(border=True):
            current_meds = []
            if shift == "Day":
                st.markdown("**🌅 Scheduled Day Doses**")
                if st.checkbox("Potassium Chloride (10 MEQ)"): current_meds.append("Potassium Chloride (10 MEQ)")
                if st.checkbox("Citalopram (20 mg)"): current_meds.append("Citalopram (20 mg)")
                if st.checkbox("Furosemide (20 mg)"): current_meds.append("Furosemide (20 mg)")
                if st.checkbox("Lantus (20 units)"): current_meds.append("Lantus (20 units)")
                if st.checkbox("Aspirin/Metoprolol"): current_meds.append("Aspirin/Metoprolol")
                if st.checkbox("Dorzolamide/Timolol Drops"): current_meds.append("Dorzolamide/Timolol Drops")
            elif shift == "Night":
                st.markdown("**🌙 Scheduled Night Doses**")
                if st.checkbox("Magnesium Oxide (400 mg)"): current_meds.append("Magnesium Oxide (400 mg)")
                if st.checkbox("Oxybutynin (5 mg)"): current_meds.append("Oxybutynin (5 mg)")
                if st.checkbox("Donepezil (10 mg)"): current_meds.append("Donepezil (10 mg)")
                if st.checkbox("Finasteride/Melatonin"): current_meds.append("Finasteride/Melatonin")
                if st.checkbox("Latanoprost Drops"): current_meds.append("Latanoprost Drops")
            
            st.markdown("**➕ PRN Medications**")
            p1, p2, p3 = st.columns(3)
            with p1:
                if st.checkbox("Phenazopyridine"): current_meds.append("Phenazopyridine")
                if st.checkbox("Acetaminophen (500 mg)"): current_meds.append("Acetaminophen (500 mg)")
                if st.checkbox("Guaifenesin"): current_meds.append("Guaifenesin")
            with p2:
                if st.checkbox("Novolog Insulin"): current_meds.append("Novolog Insulin")
                if st.checkbox("Diclofenac Sodium Gel"): current_meds.append("Diclofenac Sodium Gel")
            with p3:
                if st.checkbox("Ondansetron (4 mg)"): current_meds.append("Ondansetron (4 mg)")
                if st.checkbox("Pantoprazole (40 mg)"): current_meds.append("Pantoprazole (40 mg)")

            st.divider()
            st.markdown("**🧹 Hygiene Tasks**")
            h1, h2 = st.columns(2)
            with h1: oc = st.checkbox("Oral Care / Dentures Checked"); bg = st.checkbox("Bathing / Grooming / Dressing")
            with h2: lg = st.checkbox("Laundry / Surfaces Wiped"); rt = st.checkbox("Room Tidied / Trash Emptied")

            care_notes = st.text_area("Detailed Care Notes:")
            
            if st.button("Seal the General Ledger", type="primary"):
                med_list = ", ".join(current_meds) if current_meds else "None"
                hygiene_info = "Hygiene Recorded" if any([oc, bg, lg, rt]) else "No hygiene recorded"
                
                # FINAL COLUMN MAPPING
                supabase.table("care_logs").insert({
                    "steward": st.session_state.steward_name,
                    "shift": shift,
                    "medications": med_list,
                    "notes": f"{hygiene_info} | {care_notes}"
                }).execute()
                st.success("Meds and Notes sealed in their own columns.")

    # --- HISTORY & CSV ---
    st.divider()
    st.header("📜 Vigil History")
    try:
        recent = supabase.table("care_logs").select("*").order("created_at", desc=True).limit(50).execute()
        if recent.data:
            df = pd.DataFrame(recent.data)
            if 'created_at' in df.columns:
                df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%m/%d %H:%M')
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("🖨️ Bind Records to CSV", data=csv, file_name=f"Care_Logs_{datetime.now().strftime('%m_%d_%Y')}.csv", mime="text/csv", use_container_width=True)
    except Exception as e:
        st.warning(f"History veiled: {e}")
