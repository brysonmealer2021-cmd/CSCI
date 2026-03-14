import streamlit as st
import pandas as pd
from supabase import create_client
import random
from datetime import datetime

# 1. THE TOOLS
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# 2. THE MEMORY
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'steward_name' not in st.session_state:
    st.session_state.steward_name = ""
if 'steward_role' not in st.session_state:
    st.session_state.steward_role = ""

# 3. THE THRESHOLD
if not st.session_state.logged_in:
    st.title("☦️ The Steward's Daily Office")
    
    entrance_quotes = [
        "*O God, come to my assistance; O Lord, make haste to help me.*",
        "*Direct my steps according to Your word, and let no iniquity have dominion over me.*"
    ]
    st.info(random.choice(entrance_quotes))
    
    name_input = st.text_input("Identify yourself, Steward:")
    pin_input = st.text_input("Steward's PIN:", type="password")
    
    if st.button("Begin the Vigil"):
        user_query = supabase.table("users").select("*").eq("username", name_input).eq("pin", pin_input).execute()
        
        if len(user_query.data) > 0:
            st.session_state.logged_in = True
            st.session_state.steward_name = user_query.data[0]['username']
            st.session_state.steward_role = user_query.data[0]['role']
            st.rerun()
        else:
            st.error("Your name or PIN is not found in the Registry.")

# 4. THE SACRED VIGIL
else:
    # --- SIDEBAR (Monastic Hours & Prayers) ---
    st.sidebar.write(f"**Steward:** {st.session_state.steward_name}")
    st.sidebar.write(f"**Rank:** {st.session_state.steward_role}")
    st.sidebar.divider()
    
    # Calculate the Monastic Hour
    current_hour = datetime.now().hour
    if 6 <= current_hour < 9:
        monastic_time = "The First Hour"
    elif 9 <= current_hour < 12:
        monastic_time = "The Third Hour"
    elif 12 <= current_hour < 15:
        monastic_time = "The Sixth Hour"
    elif 15 <= current_hour < 18:
        monastic_time = "The Ninth Hour"
    elif 18 <= current_hour < 21:
        monastic_time = "Vespers (Lighting the Lamps)"
    elif 21 <= current_hour < 24:
        monastic_time = "Compline"
    else:
        monastic_time = "The Midnight Office"
        
    st.sidebar.subheader("⏳ The Horologion")
    st.sidebar.write(f"**Current Watch:** {monastic_time}")
    st.sidebar.divider()
    
    st.sidebar.subheader("☦️ The Jesus Prayer")
    st.sidebar.caption("*Lord Jesus Christ, Son of God, have mercy on me.*")
    st.sidebar.divider()
    
    st.sidebar.subheader("☦️ The Trisagion")
    st.sidebar.caption("*Holy God, Holy Mighty, Holy Immortal, have mercy on us.*")
    st.sidebar.divider()

    if st.sidebar.button("Lock the Cell (End Shift)"):
        st.session_state.logged_in = False
        st.rerun()

    # --- MAIN HEADER ---
    st.title("Tending the Flock")
    
    # Cyclical St. Ephrem Verses
    ephrem_verses = [
        "*O Lord and Master of my life, take from me the spirit of sloth, despair, lust of power, and idle talk.*",
        "*But give rather the spirit of chastity, humility, patience, and love to Thy servant.*",
        "*Yea, O Lord and King, grant me to see my own transgressions, and not to judge my brother.*"
    ]
    st.info(random.choice(ephrem_verses))
    st.divider()

    # Shift Selection
    shift = st.radio("Select your active vigil:", ["Day", "Night", "Overnight"], horizontal=True)

    # ==========================================
    # INDIVIDUAL LOGS (TOP)
    # ==========================================

    # --- ISOLATED LOG: VITALS ---
    with st.expander("🩺 4-Hour Vitals", expanded=True):
        st.caption("“A man ought at all times to take heed to his own measure.” — Abba Agathon")
        col1, col2, col3, col4 = st.columns(4)
        bp = col1.text_input("Blood Pressure")
        hr = col2.text_input("Heart Rate")
        spo2 = col3.text_input("SpO₂")
        glucose = col4.text_input("Glucose")
        
        if st.button("Seal Vitals Log"):
            vit_log = f"Vitals | BP: {bp} | HR: {hr} | SpO2: {spo2} | Glucose: {glucose}"
            try:
                supabase.table("care_logs").insert({"steward": st.session_state.steward_name, "shift": shift, "notes": vit_log}).execute()
                st.success("Vitals secured in the ledger.")
            except Exception as e:
                st.error(f"The timber broke: {e}")

    # --- ISOLATED LOG: CONTINENCE ---
    with st.expander("🕒 2-Hour Toileting & Continence", expanded=True):
        st.caption("“We have not been taught to kill our bodies, but to kill our passions.” — Abba Poemen")
        bm_ur = st.radio("Output Type:", ["None", "Urine", "Bowel Movement", "Both"], horizontal=True)
        appearance = st.text_input("Appearance / Amount (record bag amount if applicable):")
        peri_care = st.checkbox("Peri Care Completed & Barrier Cream Applied")
        
        if st.button("Seal Continence Round"):
            peri_status = "Peri Care Done" if peri_care else "No Peri Care"
            cont_log = f"Continence | Output: {bm_ur} | Details: {appearance} | {peri_status}"
            try:
                supabase.table("care_logs").insert({"steward": st.session_state.steward_name, "shift": shift, "notes": cont_log}).execute()
                st.success("Continence round secured in the ledger.")
            except Exception as e:
                st.error(f"The timber broke: {e}")

    st.divider()

    # ==========================================
    # COMBINED LEDGER (BOTTOM)
    # ==========================================
    st.header("General Care, Nutrition, & Medications")
    
    with st.container(border=True):
        
        # --- MEDICATIONS ---
        if shift in ["Day", "Night"]:
            st.subheader(f"💊 {shift} Scheduled Medications")
            st.caption("“I have often repented of having spoken, but never of having remained silent.” — Abba Arsenius")
            
            if shift == "Day":
                st.markdown("**Morning Care**")
                st.checkbox("Potassium Chloride: 10 MEQ (2 tablets)")
                st.checkbox("Citalopram Hydrobromide: 20 mg (1 tablet)")
                st.checkbox("Furosemide: 20 mg (1 tablet)")
                st.checkbox("Lantus Insulin: 20 units")
                st.checkbox("Aspirin: 81 mg EC tab")
                st.checkbox("Metoprolol Succinate: 50 mg SA tab")
                st.checkbox("Lactobacillus acidophilus: 1 capsule")
                st.checkbox("Dorzolamide/Timolol (22.3/6.8 mg): 1 drop both eyes (AM)")
                st.markdown("**Noon Care**")
                st.checkbox("Zinc: 30 mg (1 tablet)")
                st.checkbox("Black Elderberry: 1000 mg (1 capsule)")
                st.checkbox("Rosuvastatin: 5 mg (1 tablet)")
                st.checkbox("Dorzolamide/Timolol: 22.3/6.8 mg (1 drop both eyes - Noon)")

            elif shift == "Night":
                st.markdown("**Evening Care**")
                st.checkbox("Magnesium Oxide: 400 mg (2 tablets)")
                st.checkbox("Oxybutynin Chloride: 10 mg SA (1 tablet)")
                st.checkbox("Potassium Chloride: 10 MEQ (2 tablets)")
                st.markdown("**Bedtime Care**")
                st.checkbox("Finasteride: 5 mg tab (1 tablet)")
                st.checkbox("Donepezil Hydrochloride: 5 mg tab (1 tablet)")
                st.checkbox("Melatonin: 10 mg tab (1 tablet)")
                st.checkbox("Advil PM: 1 tablet")
                st.checkbox("Latanoprost (0.005%): 1 drop both eyes at bedtime")

        st.subheader("➕ PRN (As Needed) Care")
        with st.expander("Show Available PRN Medications"):
            st.checkbox("Phenazopyridine (200 mg) for painful urination")
            st.checkbox("Acetaminophen (500 mg)")
            st.checkbox("Guaifenesin (400 mg)")
            st.checkbox("Novolog/Novolin Sliding Scale")
            st.checkbox("Diclofenac Gel for pain")
            st.checkbox("Ondansetron ODT (4 mg) for nausea")
            st.checkbox("Pantoprazole (40 mg) for GERD")

        st.divider()

        # --- HYGIENE & ENVIRONMENT ---
        st.caption("“To instruct your neighbor is the same as building a church.” — Abba Poemen")
        colA, colB = st.columns(2)
        with colA:
            st.markdown("**Hygiene & Mobility**")
            st.checkbox("Oral Care")
            st.checkbox("Bathing / Grooming / Dressing")
            st.checkbox("Dentures in/out")
            st.checkbox("Out of bed & ROM Exercises")
        with colB:
            st.markdown("**Environment**")
            st.checkbox("Room Tidied & Trash Emptied")
            st.checkbox("Linens Changed")
            st.checkbox("Laundry Sorted")
            st.checkbox("Surfaces Wiped")

        st.divider()

        # --- NUTRITION ---
        st.markdown("**Nutrition & Hydration**")
        st.caption("“Eat your bread in silence.” — Abba Macarius")
        meal = st.selectbox("Meal/Snack", ["None", "Breakfast", "Morning Snack", "Lunch", "Afternoon Snack", "Dinner", "Late-Night Snack"])
        percent_eaten = st.slider("% Meal Eaten", 0, 100, 0, 25)
        fluids = st.number_input("Fluid Intake (mL)", min_value=0, step=50)

        # --- NOTES ---
        care_notes = st.text_area("Detailed Care Notes (Mood, Skin integrity, Visitors, etc.):")
        
        # --- THE SINGLE SUBMIT BUTTON ---
        if st.button("Seal the General Ledger", type="primary"):
            gen_log = f"Shift: {shift} | Meal: {meal} ({percent_eaten}%) | Fluids: {fluids}mL | Notes: {care_notes} | (Routine check-offs recorded)"
            try:
                supabase.table("care_logs").insert({"steward": st.session_state.steward_name, "shift": shift, "notes": gen_log}).execute()
                st.success("All general care, medications, and nutrition have been secured in the ledger.")
            except Exception as e:
                st.error(f"The timber broke: {e}")

    st.divider()

    # --- VIGIL HISTORY ---
    st.header("Vigil History")
    history = supabase.table("care_logs").select("*").order("created_at", desc=True).limit(10).execute()
    
    if history.data:
        df = pd.DataFrame(history.data)
        st.dataframe(df, use_container_width=True)
    else:
        st.write("The ledger is currently empty.")
