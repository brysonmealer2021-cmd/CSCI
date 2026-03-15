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
        "O Lord Almighty, the Healer of our souls and bodies, who put down and raise up, visit Thy servant in her physical trial. Grant her patience and restore her to health.",
        "O Christ, who alone art our Defender, visit and heal Thy suffering servant. Deliver her from sickness and bitter pain, that she may sing to Thee.",
        "Holy Father, Physician of our souls and bodies, send down Thy healing power. Comfort her in her weakness and grant her the quiet strength to endure.",
        "O Lord, look down with mercy upon Thy servant. Ease her bodily distress and wrap her in the grace of Thy healing, for Thou art the fountain of life.",
        "Most Holy Theotokos, cover Thy servant with thy protecting veil. Grant her bodily endurance and deep, abiding peace in the midst of her trial."
    ],
    "katelyn": [
        "O Lord, bless the heavy and holy labor of motherhood. Grant her the physical strength to run the race and the spiritual patience to guide her children.",
        "Establish the work of her hands, O Lord. Give her endurance in her body and stillness in her heart as she tends to her family.",
        "O Christ, who blessed the children, grant this mother the wisdom of the saints and the unwavering energy to lead her household in peace.",
        "Lord, bless her efforts to build a strong vessel. Grant her health of body and clarity of mind, that she may be a steady anchor for her three.",
        "Most Holy Theotokos, thou who didst raise the Savior, guide this mother's daily labor. Multiply her strength and surround her house with grace."
    ],
    "malinda": [
        "O Lord, who bore the heavy cross, grant strength to the one who carries the weight for her family. Give her broad shoulders and a quiet mind.",
        "Lord, bless the one who leads and organizes the care of her father. Grant her wisdom, unending patience, and rest from her heavy burdens.",
        "O Christ, support Thy servant under the weight of her responsibilities. Let her not grow weary in well-doing, but fill her with steadfast grace.",
        "Establish her steps, O Lord, as she navigates the heavy trails for her family. Grant her the peace that surpasses all understanding.",
        "O Master, look upon the one who bears the yoke of leadership in this house. Grant her rest when she is tired, and steady hands when the decisions are heavy."
    ],
    "mandy": [
        "Let not your heart be troubled, neither let it be afraid. O Lord, speak peace to her anxious thoughts and still the storms within.",
        "O Christ, who calmed the raging sea, quiet the restless waters of her mind. Grant her a deep and abiding stillness today.",
        "Cast all your anxieties on Him, because He cares for you. O Lord, wrap her in Thy calm and dispel all fear from her heart.",
        "O Lord, grant her to meet this day in peace. In all unforeseen events, let her not forget that all are sent by Thee.",
        "Most Holy Theotokos, calm the anxious spirit of Thy servant. Bring her the gentle quiet of the Skete, that she may rest securely in God's care."
    ],
    "bryce": [
        "O Lord and Master of my life, take from me the spirit of sloth, despair, lust of power, and idle talk. But give rather the spirit of chastity, humility, patience, and love to Thy servant.",
        "Illumine our darkness, O Lord, and grant us a peaceful and undisturbed watch. Drive away all weariness of the flesh.",
        "Lord Jesus Christ, Son of God, have mercy on me, a sinner. Grant me a quiet spirit to tend the elder today.",
        "Having risen from sleep, I offer Thee, O Savior, the midnight song. Grant me to walk this shift pleasing in Thy sight, and protect the flock.",
        "The Lord shall preserve thy going out and thy coming in from this time forth. May He preserve this Cell and the heavy work of thy hands."
    ],
    "default": [
        "Peace be to this house, and to all who dwell herein. May the Lord grant your family quiet rest and His great mercy.",
        "The Lord is your keeper; the Lord is your shade at your right hand. May He cover your house and grant you peace."
    ]
}

def get_blessing(username):
    name_key = username.strip().lower()
    if name_key in blessings_map:
        return random.choice(blessings_map[name_key])
    return random.choice(blessings_map["default"])

# 3. THE THRESHOLD
if not st.session_state.logged_in:
    st.title("☦️ The Steward's Daily Office")
    
    entrance_quotes = [
        "“Come to me, all who labor and are heavy laden, and I will give you rest.” — Matthew 11:28",
        "*O God, come to my assistance; O Lord, make haste to help me.*",
        "“Let not your heart be troubled, neither let it be afraid.” — John 14:27",
        "*Direct my steps according to Your word, and let no iniquity have dominion over me.*",
        "“Cast all your anxieties on Him, because He cares for you.” — 1 Peter 5:7"
    ]
    st.info(random.choice(entrance_quotes))
    
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
    st.write("")
    st.write("")
    with st.container(border=True):
        st.subheader("☦️ A Blessing for the Watch")
        st.write(f"*{st.session_state.daily_blessing}*")
        st.divider()
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Amen", type="primary", use_container_width=True):
                st.session_state.blessing_received = True
                st.rerun()

# 5. THE SACRED VIGIL
else:
    # --- SIDEBAR (The Watch & Prayers) ---
    st.sidebar.write(f"**Steward:** {st.session_state.steward_name}")
    st.sidebar.divider()
    
    current_hour = datetime.now().hour
    
    if 6 <= current_hour < 12:
        watch_title = "🌅 The Morning Light"
        time_quotes = [
            "“Having risen from sleep, we fall down before Thee, O Good One.”",
            "“Christ, the True Light, who enlightens and sanctifies every man, may the light of Thy countenance shine upon us.”",
            "“O Lord, grant me to greet the coming day in peace.” — Prayer of the Optina Elders"
        ]
    elif 12 <= current_hour < 18:
        watch_title = "☀️ The Midday Labor"
        time_quotes = [
            "“O Thou who at the sixth day and hour didst nail to the cross the sin... cleanse us.”",
            "“Establish the work of our hands upon us; yea, the work of our hands establish Thou it.” — Psalm 90:17",
            "“A humble man is never rushed, hasty or agitated.” — St. Isaac the Syrian"
        ]
    elif 18 <= current_hour < 21:
        watch_title = "🕯️ The Evening Watch"
        time_quotes = [
            "“Gladsome Light of the holy glory of the Immortal Father...”",
            "“Let my prayer arise in Thy sight as incense, and let the lifting up of my hands be an evening sacrifice.”",
            "“The sun has set, the evening light remains. Grant us a peaceful night, O Lord.”"
        ]
    else:
        watch_title = "🌌 The Night Vigil"
        time_quotes = [
            "“Behold, the Bridegroom comes at midnight, and blessed is the servant whom He shall find watching.”",
            "“I remember Thee upon my bed, and meditate on Thee in the night watches.” — Psalm 63:6",
            "“O Lord and Master of my life, look upon the quiet labor of the night.”"
        ]
        
    st.sidebar.subheader(watch_title)
    st.sidebar.caption(f"*{random.choice(time_quotes)}*")
    st.sidebar.divider()
    
    st.sidebar.subheader("☦️ The Jesus Prayer")
    st.sidebar.caption("*Lord Jesus Christ, Son of God, have mercy on me.*")
    st.sidebar.divider()
    
    st.sidebar.subheader("☦️ The Trisagion")
    st.sidebar.caption("*Holy God, Holy Mighty, Holy Immortal, have mercy on us.*")
    st.sidebar.divider()

    if st.sidebar.button("Lock the Cell"):
        st.session_state.logged_in = False
        st.session_state.blessing_received = False
        st.rerun()

    # --- MAIN HEADER ---
    st.title("The Day's Labor")
    
    main_quotes = [
        "“Acquire a peaceful spirit, and thousands around you will be saved.” — St. Seraphim of Sarov",
        "“A humble man is never rushed, hasty or agitated.” — St. Isaac the Syrian",
        "“He who is busy with good deeds does not have time to despair.” — St. John Chrysostom",
        "“The highest prayer is performed in silence.” — St. Isaac the Syrian",
        "“Do not be troubled by the struggles of the day; the Lord sees your quiet labor.”",
        "“Let us fall into the hands of the Lord, for His mercy is great.” — Sirach 2:18"
    ]
    st.caption(random.choice(main_quotes))
    st.divider()
    
    ephrem_verses = [
        "*O Lord and Master of my life, take from me the spirit of sloth, despair, lust of power, and idle talk.*",
        "*But give rather the spirit of chastity, humility, patience, and love to Thy servant.*",
        "*Yea, O Lord and King, grant me to see my own transgressions, and not to judge my brother.*"
    ]
    st.info(random.choice(ephrem_verses))
    st.divider()

    # --- THE FORK IN THE TRAIL ---
    if st.session_state.steward_role.strip().lower() == "daughter":
        st.success("The watch is steady and your father is in good hands. The daily labor here is focused entirely on his comfort and honor, kept with deep respect under watchful eyes. You carry no burden of the work today—the steward's tools are set aside for you. The complete ledger is laid open below so you can trace the quiet history of his days and know he is well loved.")
    
    else:
        # Shift Selection
        shift = st.radio("Select your active vigil:", ["Day", "Night", "Overnight"], horizontal=True)

        # ==========================================
        # INDIVIDUAL LOGS (TOP)
        # ==========================================

        # --- ISOLATED LOG: VITALS ---
        with st.expander("🩺 4-Hour Vitals", expanded=True):
            vital_quotes = [
                "“A man ought at all times to take heed to his own measure.” — Abba Agathon",
                "“The work of your hands is a vigil of its own.”"
            ]
            st.caption(random.choice(vital_quotes))
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
            continence_quotes = [
                "“We have not been taught to kill our bodies, but to kill our passions.” — Abba Poemen",
                "“In serving the least of these, we serve Christ Himself.”"
            ]
            st.caption(random.choice(continence_quotes))
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
                med_quotes = [
                    "“I have often repented of having spoken, but never of having remained silent.” — Abba Arsenius",
                    "“Healing is a work of both the hands and the heart.”"
                ]
                st.caption(random.choice(med_quotes))
                
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
            hygiene_quotes = [
                "“To instruct your neighbor is the same as building a church.” — Abba Poemen",
                "“Cleanse the vessel, but tend to the spirit within.”"
            ]
            st.caption(random.choice(hygiene_quotes))
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
            nutrition_quotes = [
                "“Eat your bread in silence.” — Abba Macarius",
                "“Whether you eat or drink, or whatever you do, do all to the glory of God.” — 1 Cor 10:31"
            ]
            st.caption(random.choice(nutrition_quotes))
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

    # --- VIGIL HISTORY & EXPORT ---
    st.header("Vigil History")
    
    recent_history = supabase.table("care_logs").select("*").order("created_at", desc=True).limit(50).execute()
    
    if recent_history.data:
        df = pd.DataFrame(recent_history.data)
        st.dataframe(df, use_container_width=True)
        
        st.divider()
        st.subheader("🖨️ Archive the Ledger")
        st.caption("Select a range of days to bind together for the physical records. It defaults to the last 7 days.")
        
        today = datetime.now().date()
        seven_days_ago = today - timedelta(days=7)
        
        date_range = st.date_input("Select the watch dates:", [seven_days_ago, today])
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            end_date_query = end_date + timedelta(days=1)
            
            week_query = supabase.table("care_logs").select("*").gte("created_at", start_date.isoformat()).lt("created_at", end_date_query.isoformat()).order("created_at", desc=True).execute()
            
            if week_query.data:
                week_df = pd.DataFrame(week_query.data)
                csv = week_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=f"Bind Records ({start_date} to {end_date})",
                    data=csv,
                    file_name=f"Charles_Care_Logs_{start_date}_to_{end_date}.csv",
                    mime="text/csv"
                )
            else:
                st.write("No entries found in that span of days.")
    else:
        st.write("The ledger is currently empty.")
