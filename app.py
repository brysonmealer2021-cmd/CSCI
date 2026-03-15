import streamlit as st
import pandas as pd
from supabase import create_client
import random
from datetime import datetime, timedelta

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
if 'blessing_received' not in st.session_state:
    st.session_state.blessing_received = False
if 'daily_blessing' not in st.session_state:
    st.session_state.daily_blessing = ""

# --- THE PRAYER RINGS ---
blessings_map = {
    "gay": [
        "O Lord Almighty, the Healer of our souls and bodies, visit Thy servant in her physical trial. Grant her patience and restore her to health.",
        "O Christ, who alone art our Defender, visit and heal Thy suffering servant. Deliver her from sickness and bitter pain.",
        "Holy Father, Physician of our souls and bodies, send down Thy healing power. Comfort her in her weakness and grant her quiet strength.",
        "O Lord, look down with mercy upon Thy servant. Ease her bodily distress and wrap her in the grace of Thy healing.",
        "Most Holy Theotokos, cover Thy servant with thy protecting veil. Grant her bodily endurance and deep, abiding peace."
    ],
    "katelyn": [
        "O Lord, bless the heavy and holy labor of motherhood. Grant her the physical strength to run the race and the spiritual patience to guide her children.",
        "Establish the work of her hands, O Lord. Give her endurance in her body and stillness in her heart as she tends to her family.",
        "O Christ, who blessed the children, grant this mother the wisdom of the saints and the unwavering energy to lead her household in peace.",
        "Lord, bless her efforts to build a strong vessel. Grant her health of body and clarity of mind, that she may be a steady anchor for her three.",
        "Most Holy Theotokos, guide this mother's daily labor. Multiply her strength and surround her house with grace."
    ],
    "malinda": [
        "O Lord, who bore the heavy cross, grant strength to the one who carries the weight for her family. Give her broad shoulders and a quiet mind.",
        "Lord, bless the one who leads and organizes the care of her father. Grant her wisdom, unending patience, and rest from her heavy burdens.",
        "O Christ, support Thy servant under the weight of her responsibilities. Let her not grow weary in well-doing.",
        "Establish her steps, O Lord, as she navigates the heavy trails for her family. Grant her the peace that surpasses all understanding.",
        "O Master, look upon the one who bears the yoke of leadership in this house. Grant her rest when she is tired and steady hands."
    ],
    "mandy": [
        "Let not your heart be troubled, neither let it be afraid. O Lord, speak peace to her anxious thoughts and still the storms within.",
        "O Christ, who calmed the raging sea, quiet the restless waters of her mind. Grant her a deep and abiding stillness today.",
        "Cast all your anxieties on Him, because He cares for you. O Lord, wrap her in Thy calm and dispel all fear from her heart.",
        "O Lord, grant her to meet this day in peace. In all unforeseen events, let her not forget that all are sent by Thee.",
        "Most Holy Theotokos, calm the anxious spirit of Thy servant. Bring her the gentle quiet of the Skete."
    ],
    "bryce": [
        "O Lord and Master of my life, grant the spirit of chastity, humility, patience, and love to Thy servant.",
        "Illumine our darkness, O Lord, and grant us a peaceful and undisturbed watch. Drive away all weariness of the flesh.",
        "Lord Jesus Christ, Son of God, have mercy on me, a sinner. Grant me a quiet spirit to tend the elder today.",
        "Having risen from sleep, I offer Thee, O Savior, the midnight song. Grant me to walk this shift pleasing in Thy sight.",
        "The Lord shall preserve thy going out and thy coming in. May He preserve this Cell and the heavy work of thy hands."
    ],
    "default": [
        "Peace be to this house, and to all who dwell herein. May the Lord grant your family quiet rest and His great mercy.",
        "The Lord is your keeper; the Lord is your shade at your right hand. May He cover your house and grant you peace."
    ]
}

def get_blessing(username):
    name_key = username.strip().lower()
    return random.choice(blessings_map.get(name_key, blessings_map["default"]))

# 3. THE THRESHOLD
if not st.session_state.logged_in:
    st.title("☦️ The Steward's Daily Office")
    name_input = st.text_input("Identify yourself:")
    pin_input = st.text_input("PIN:", type="password")
    
    if st.button("Cross the Threshold"):
        user_query = supabase.table("users").select("*").eq("username", name_input).eq("pin", pin_input).execute()
        if len(user_query.data) > 0:
            st.session_state.logged_in = True
            st.session_state.steward_name = user_query.data[0]['username']
            st.session_state.steward_role = user_query.data[0]['role']
            st.session_state.blessing_received = False
            st.session_state.daily_blessing = get_blessing(st.session_state.steward_name)
            st.rerun()
        else:
            st.error("Your name or PIN is not found in the Registry.")

# 4. THE BLESSING GATE
elif not st.session_state.blessing_received:
    st.write("")
    with st.container(border=True):
        st.subheader("☦️ A Blessing for the Watch")
        st.write(f"*{st.session_state.daily_blessing}*")
        st.divider()
        if st.button("Amen", type="primary", use_container_width=True):
            st.session_state.blessing_received = True
            st.rerun()

# 5. THE SACRED VIGIL
else:
    # --- SIDEBAR & HEADER ---
    st.sidebar.write(f"**Steward:** {st.session_state.steward_name}")
    if st.sidebar.button("Lock the Cell"):
        st.session_state.logged_in = False
        st.session_state.blessing_received = False
        st.rerun()

    st.title("The Day's Labor")

    # --- THE DAUGHTER BEAM ---
    if st.session_state.steward_role.strip().lower() == "daughter":
        st.success("The watch is steady and your father is in good hands. The daily labor here is focused entirely on his comfort and honor, kept with deep respect under watchful eyes. You carry no burden of the work today—the steward's tools are set aside for you. The complete ledger is laid open below so you can trace the quiet history of his days and know he is well loved.")
    
    else:
        shift = st.radio("Select your active vigil:", ["Day", "Night", "Overnight"], horizontal=True)

        # --- VITALS ---
        with st.expander("🩺 Vitals", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            bp = col1.text_input("Blood Pressure")
            hr = col2.text_input("Heart Rate")
            spo2 = col3.text_input("SpO₂")
            glucose = col4.text_input("Glucose")
            if st.button("Seal Vitals"):
                supabase.table("care_logs").insert({
                    "steward": st.session_state.steward_name, "shift": shift,
                    "bp": bp, "hr": hr, "spo2": spo2, "glucose": glucose
                }).execute()
                st.success("Vitals recorded.")

        # --- CONTINENCE ---
        with st.expander("🕒 Continence Round", expanded=True):
            bm_ur = st.radio("Output:", ["None", "Urine", "Bowel Movement", "Both"], horizontal=True)
            appearance = st.text_input("Details (Appearance/Amount):")
            if st.button("Seal Continence"):
                supabase.table("care_logs").insert({
                    "steward": st.session_state.steward_name, "shift": shift,
                    "output_type": bm_ur, "output_details": appearance
                }).execute()
                st.success("Continence recorded.")

        # --- GENERAL CARE & MEDS ---
        st.subheader("General Care & Medications")
        care_notes = st.text_area("Meds given or Care notes:")
        meal = st.selectbox("Meal", ["None", "Breakfast", "Lunch", "Dinner", "Snack"])
        percent = st.slider("% Eaten", 0, 100, 0, 25)
        
        if st.button("Seal the General Ledger", type="primary"):
            supabase.table("care_logs").insert({
                "steward": st.session_state.steward_name, "shift": shift,
                "medications": care_notes,
                "meal_info": f"{meal}: {percent}%"
            }).execute()
            st.success("General ledger sealed.")

        # --- HISTORY & CSV ---
    st.divider()
    st.header("Vigil History")
    recent = supabase.table("care_logs").select("*").order("created_at", desc=True).limit(50).execute()
    
    if recent.data:
        df = pd.DataFrame(recent.data)
        
        # This is the "sanding" tool to smooth the timestamps
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%m/%d/%Y %H:%M')
        
        st.dataframe(df, use_container_width=True)
        
        # Binding/Printing
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Bind Records to CSV", 
            data=csv, 
            file_name=f"Care_Logs_{datetime.now().strftime('%m_%d_%Y')}.csv", 
            mime="text/csv"
        )
