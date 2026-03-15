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
    .draft-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #f0f8ff;
        border: 2px dashed #1a5276;
        color: #1a5276;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SESSION STATE (The Watch Memory)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'steward_name' not in st.session_state:
    st.session_state.steward_name = ""
if 'steward_role' not in st.session_state:
    st.session_state.steward_role = ""
if 'blessing_received' not in st.session_state:
    st.session_state.blessing_received = False

# The Vigil Buffer (For Consolidation - Corrected keys)
if 'shift_data' not in st.session_state:
    st.session_state.shift_data = {
        "bp": "", "hr": "", "spo2": "", "glucose": "",
        "nutrition": [], "hydration": 0, 
        "output_type": "None", "output_details": "",
        "meds": [], "hygiene": [], "notes": ""
    }

# 4. THE PRAYER RINGS (Personalized Gates)
blessings_map = {
    "gay": [
        "O Lord Almighty, the Healer of our souls and bodies, visit Thy servant in her physical trial. Grant her patience and restore her to health.",
        "O Christ, our Defender, visit and heal Thy suffering servant. Deliver her from sickness and bitter pain.",
        "Holy Father, Physician of our souls and bodies, send down Thy healing power."
    ],
    "katelyn": [
        "O Lord, bless the heavy and holy labor of motherhood. Grant her physical strength and spiritual patience.",
        "Establish the work of her hands, O Lord. Give her endurance in her body as she tends to her family.",
        "Most Holy Theotokos, guide this mother's daily labor. Multiply her strength."
    ],
    "malinda": [
        "O Lord, who bore the heavy cross, grant strength to the one who carries the weight for her family. Give her broad shoulders.",
        "Lord, bless the one who leads and organizes the care of her father. Grant her wisdom, unending patience, and rest.",
        "O Master, look upon the one who bears the yoke of leadership. Grant her steady hands."
    ],
    "mandy": [
        "Let not your heart be troubled, neither let it be afraid. O Lord, speak peace to her anxious thoughts and still the storms within.",
        "O Christ, who calmed the raging sea, quiet the restless waters of her mind. Grant her deep stillness.",
        "Most Holy Theotokos, calm the anxious spirit of Thy servant."
    ],
    "bryce": [
        "O Lord and Master of my life, grant the spirit of chastity, humility, patience, and love to Thy servant.",
        "Illumine our darkness, O Lord, and grant us a peaceful and undisturbed watch. Drive away all weariness.",
        "Lord Jesus Christ, Son of God, have mercy on me, a sinner."
    ]
}

def get_blessing(username):
    name_key = username.strip().lower()
    return random.choice(blessings_map.get(name_key, ["Peace be to this house."]))

# 5. THE THRESHOLD (LOGIN)
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
                st.error("The gate remains closed. Verify credentials.")
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
    # Sidebar Restoration with Specific Titles
    current_hour = datetime.now().hour
    if 6 <= current_hour < 12: d_title, wt, wq = "🌅 Morning Offering", "🌅 Morning Light", "“Greet the day in peace.”"
    elif 12 <= current_hour < 18: d_title, wt, wq = "☀️ Midday Labor", "☀️ Midday Labor", "“Establish the work of our hands.”"
    elif 18 <= current_hour < 21: d_title, wt, wq = "🕯️ Evening Sacrifice", "🕯️ Evening Watch", "“Let my prayer arise as incense.”"
    else: d_title, wt, wq = "🌌 Night Vigil", "🌌 Night Vigil", "“Behold, the Bridegroom comes.”"

    st.sidebar.write(f"**Steward:** {st.session_state.steward_name}")
    st.sidebar.divider()
    st.sidebar.subheader(wt)
    st.sidebar.caption(f"*{wq}*")
    st.sidebar.divider()
    st.sidebar.subheader("☦️ The Jesus Prayer")
    st.sidebar.caption("*Lord Jesus Christ, Son of God, have mercy on me, a sinner.*")
    st.sidebar.divider()
    st.sidebar.subheader("☦️ The Trisagion")
    st.sidebar.caption("*Holy God, Holy Mighty, Holy Immortal, have mercy on us.*")
    st.sidebar.divider()
    if st.sidebar.button("Lock the Cell"):
        st.session_state.logged_in = False
        st.rerun()

    st.title(f"☦️ {d_title}")
    
    # Rotating St. Ephrem (Top)
    st.info(random.choice([
        "“O Lord and Master of my life, take from me the spirit of sloth, despair, lust of power, and idle talk.”",
        "“But give rather the spirit of chastity, humility, patience, and love to Thy servant.”",
        "“Yea, O Lord and King, grant me to see my own transgressions, and not to judge my brother.”"
    ]))

    if st.session_state.steward_role.strip().lower() == "daughter":
        st.success("The watch is steady. Historical records are available below.")
    else:
        shift = st.radio("Active Vigil:", ["Day", "Night", "Overnight"], horizontal=True)

        # --- VITALS ---
        with st.expander("🩺 Vitals Update", expanded=False):
            st.caption(random.choice(["“A man ought to take heed to his own measure.”", "“The work of your hands is a vigil.”", "“Keep watch over your heart with all diligence.”"]))
            v1, v2, v3, v4 = st.columns(4)
            bp_i = v1.text_input("BP", value=st.session_state.shift_data["bp"])
            hr_i = v2.text_input("HR", value=st.session_state.shift_data["hr"])
            sp_i = v3.text_input("SpO2", value=st.session_state.shift_data["spo2"])
            gl_i = v4.text_input("Gluc", value=st.session_state.shift_data["glucose"])
            if st.button("Update Shift Vitals"):
                st.session_state.shift_data.update({"bp": bp_i, "hr": hr_i, "spo2": sp_i, "glucose": gl_i})
                st.toast("Vitals added to memory.")

        # --- NUTRITION & HYDRATION ---
        with st.expander("🍲 Nutrition & Hydration", expanded=False):
            st.caption(random.choice(["“He satisfieth the longing soul, and filleth the hungry soul with goodness.”", "“Whether you eat or drink, do all to the glory of God.”", "“The eyes of all look to Thee with hope.”"]))
            c_nut, c_hyd = st.columns(2)
            with c_nut:
                st.markdown("### 🍞 Food")
                f_item = st.text_input("What was eaten?", key="f_input")
                f_pct = st.slider("% Consumed", 0, 100, 0, 10)
                if st.button("Add Food to Vigil"):
                    st.session_state.shift_data["nutrition"].append(f"{f_item} ({f_pct}%)")
                    st.toast("Food added.")
            with c_hyd:
                st.markdown("### 💧 Hydration")
                d_oz = st.number_input("Amount (oz)", min_value=0, max_value=64, step=1)
                if st.button("Add Water to Vigil"):
                    st.session_state.shift_data["hydration"] += d_oz
                    st.toast(f"Total: {st.session_state.shift_data['hydration']}oz")

        # --- CONTINENCE (Restored & Fixed) ---
        with st.expander("🕒 Continence Round", expanded=False):
            st.caption(random.choice(["“In serving the least of these, we serve Christ.”", "“Blessed is he that considereth the poor and needy.”", "“Be merciful, even as your Father is merciful.”"]))
            c_type = st.radio("Output Observed:", ["None", "Urine", "Bowel Movement", "Both"], horizontal=True)
            c_details = st.text_input("Details / Appearance:", value=st.session_state.shift_data["output_details"])
            if st.button("Update Continence in Memory"):
                st.session_state.shift_data.update({"output_type": c_type, "output_details": c_details})
                st.toast("Continence data saved to draft.")

        # --- MEDICATIONS & TASKS ---
        st.header("💊 Medications & Care Check")
        st.caption(random.choice(["“To instruct your neighbor is like building a church.”", "“Blessed is the steward who watches over the elder.”", "“Do not be weary in well-doing.”"]))
        with st.container(border=True):
            current_meds = []
            if shift == "Day":
                st.markdown("**🌅 Day Doses**")
                if st.checkbox("Potassium Chloride"): current_meds.append("Potassium Chloride")
                if st.checkbox("Citalopram"): current_meds.append("Citalopram")
                if st.checkbox("Furosemide"): current_meds.append("Furosemide")
                if st.checkbox("Lantus"): current_meds.append("Lantus")
                if st.checkbox("Aspirin/Metoprolol"): current_meds.append("Aspirin/Metoprolol")
                if st.checkbox("Dorzolamide/Timolol"): current_meds.append("Dorzolamide/Timolol")
            elif shift == "Night":
                st.markdown("**🌙 Night Doses**")
                if st.checkbox("Magnesium Oxide"): current_meds.append("Magnesium Oxide")
                if st.checkbox("Oxybutynin"): current_meds.append("Oxybutynin")
                if st.checkbox("Donepezil"): current_meds.append("Donepezil")
                if st.checkbox("Finasteride/Melatonin"): current_meds.append("Finasteride/Melatonin")
                if st.checkbox("Latanoprost"): current_meds.append("Latanoprost")
            
            st.markdown("**➕ PRN Meds**")
            p1, p2 = st.columns(2)
            with p1:
                if st.checkbox("Acetaminophen"): current_meds.append("Acetaminophen")
                if st.checkbox("Phenazopyridine"): current_meds.append("Phenazopyridine")
                if st.checkbox("Guaifenesin"): current_meds.append("Guaifenesin")
            with p2:
                if st.checkbox("Novolog"): current_meds.append("Novolog")
                if st.checkbox("Diclofenac"): current_meds.append("Diclofenac")
                if st.checkbox("Ondansetron"): current_meds.append("Ondansetron")

            st.divider()
            st.markdown("**🧹 Hygiene**")
            h_list = []
            c1, c2 = st.columns(2)
            if c1.checkbox("Oral Care"): h_list.append("Oral Care")
            if c1.checkbox("Bathing/Dressing"): h_list.append("Bathing/Dressing")
            if c2.checkbox("Laundry/Surfaces"): h_list.append("Laundry/Surfaces")
            if c2.checkbox("Room/Trash"): h_list.append("Room/Trash")

            notes_i = st.text_area("Shift Observations:")

            # --- THE DRAFT REVIEW WINDOW ---
            st.divider()
            st.subheader("📋 Vigil Draft Review")
            st.markdown(f"""
            <div class="draft-box">
                <b>Shift:</b> {shift}<br>
                <b>Vitals:</b> BP: {st.session_state.shift_data['bp']} | HR: {st.session_state.shift_data['hr']} | SpO2: {st.session_state.shift_data['spo2']} | GL: {st.session_state.shift_data['glucose']}<br>
                <b>Nutrition:</b> {", ".join(st.session_state.shift_data['nutrition']) if st.session_state.shift_data['nutrition'] else "None"}<br>
                <b>Hydration:</b> {st.session_state.shift_data['hydration']}oz total<br>
                <b>Output:</b> {st.session_state.shift_data['output_type']} ({st.session_state.shift_data['output_details']})<br>
                <b>Meds Selected:</b> {", ".join(current_meds) if current_meds else "None"}<br>
                <b>Hygiene:</b> {", ".join(h_list) if h_list else "None"}
            </div>
            """, unsafe_allow_html=True)

            # THE FINAL SEAL
            if st.button("☦️ SEAL & END VIGIL", type="primary"):
                final_meds = ", ".join(current_meds) if current_meds else "None"
                final_nuts = " | ".join(st.session_state.shift_data["nutrition"]) if st.session_state.shift_data["nutrition"] else "None"
                final_hygs = ", ".join(h_list) if h_list else "None"
                
                supabase.table("care_logs").insert({
                    "steward": st.session_state.steward_name,
                    "shift": shift,
                    "bp": st.session_state.shift_data["bp"],
                    "hr": st.session_state.shift_data["hr"],
                    "spo2": st.session_state.shift_data["spo2"],
                    "glucose": st.session_state.shift_data["glucose"],
                    "output_type": st.session_state.shift_data["output_type"],
                    "output_details": st.session_state.shift_data["output_details"],
                    "meal_info": f"Food: {final_nuts} | Total Water: {st.session_state.shift_data['hydration']}oz",
                    "medications": final_meds,
                    "notes": f"Hygiene: {final_hygs} | Obs: {notes_i}"
                }).execute()
                
                # Clear memory
                st.session_state.shift_data = {"bp":"", "hr":"", "spo2":"", "glucose":"", "nutrition":[], "hydration":0, "output_type":"None", "output_details":"", "meds":[], "hygiene":[], "notes":""}
                st.success("The Vigil has been consolidated and sealed.")
                st.rerun()

    # --- HISTORY & REPORTING ---
    st.divider()
    st.header("📜 Consolidated History")
    filter_v = st.selectbox("View Range:", ["Today", "Last 48 Hours", "Full Week"])
    try:
        days = 1 if filter_v == "Today" else (2 if "48" in filter_v else 7)
        limit_t = (datetime.now() - timedelta(days=days)).isoformat()
        res = supabase.table("care_logs").select("*").gt("created_at", limit_t).order("created_at", desc=True).execute()
        if res.data:
            df = pd.DataFrame(res.data)
            df['Date/Time'] = pd.to_datetime(df['created_at']).dt.strftime('%m/%d %H:%M')
            cols_to_drop = ["created_at", "toileting", "fluid_oz", "meds_given", "vitals_hr_spo2", "Blood_Pressure"]
            df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])
            st.dataframe(df, use_container_width=True)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(f"🖨️ Export {filter_v} Report", data=csv, file_name=f"Care_Report_{filter_v}.csv", mime="text/csv")
    except:
        st.warning("History currently syncing...")
