import streamlit as st
import pandas as pd
import joblib
import os

from data_processing import prepare_features
from prediction import predict_flights
from routing import assign_flight

# -------------------------------
# LOAD MODEL FILES
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR,"flight_model.pkl"))
encoder = joblib.load(os.path.join(BASE_DIR,"flight_encoder.pkl"))
feature_columns = joblib.load(os.path.join(BASE_DIR,"feature_columns.pkl"))

# -------------------------------
# STREAMLIT PAGE CONFIG
# -------------------------------

st.set_page_config(
    page_title="Smart Flight Assignment System",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<div class="header-card">
    <h1>✈ Intelligent Flight Allocation Engine</h1>
    <p>AI-driven system for optimizing shipment routing, capacity utilization, and delivery commitments across global air networks.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="status-bar">
    <span>🟢 System Active</span>
    <span>⚡ Model Loaded</span>
    <span>📦 Real-time Assignment Enabled</span>
</div>
""", unsafe_allow_html=True)


#st.markdown("<hr style='border:1px solid #374151;'>", unsafe_allow_html=True)


st.markdown("""
<style>

/* ===== STATUS BAR ===== */
.status-bar {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
    font-size: 13px;
    color: #94a3b8;
}

.status-bar span {
    background: rgba(30,41,59,0.6);
    padding: 6px 12px;
    border-radius: 8px;
}

/* ===== FIX TOP RIGHT ICON VISIBILITY ===== */
header svg {
    fill: white !important;
    color: white !important;
}

header button {
    color: white !important;
}

/* Hover */
header button:hover {
    background-color: rgba(255,255,255,0.1) !important;
}


/* ===== MAIN BACKGROUND ===== */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top left, #1e1b4b, #020617);
}


/* ===== STRONG WHITE TITLE ===== */

h1 {
    color: #ffffff !important;
    font-weight: 800;
    letter-spacing: 0.5px;
    text-shadow: 0 2px 8px rgba(255,255,255,0.15);
}

/* ===== FORCE GLASS EFFECT ===== */
.card {
    background: rgba(30, 41, 59, 0.55) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.08);
    padding: 20px;
    margin-bottom: 20px;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 15px 35px rgba(0,0,0,0.6);
}

/* ===== FADE IN ===== */
[data-testid="stAppViewContainer"] {
    animation: fadeIn 0.6s ease-in-out;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ===== BACKGROUND GLOW ===== */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    top: -200px;
    left: -200px;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(37,99,235,0.25), transparent 70%);
    z-index: 0;
}

/* ===== PREMIUM BUTTON ===== */
.stDownloadButton button {
    background: linear-gradient(135deg, #7c3aed, #a855f7);
    color: white;
    border-radius: 12px;
    border: none;
    font-weight: 600;
    box-shadow: 0 0 20px rgba(168,85,247,0.5);
}

.stDownloadButton button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 35px rgba(168,85,247,0.9);
}

/* ===== UPLOADER UPGRADE ===== */
[data-testid="stFileUploader"] {
    border-radius: 12px;
    border: 1px dashed #475569;
    padding: 10px;
    background: rgba(15, 23, 42, 0.6);
}

/* ===== TITLES ===== */
h1 {
    font-size: 32px;
}

h2 {
    font-size: 22px;
}

h3 {
    font-size: 18px;
}

/* ===== KPI CARDS ===== */
.metric-card {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    border-radius: 16px;
    padding: 22px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.05);
    transition: 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 25px rgba(0,0,0,0.6);
}

/* Label below */
.metric-label {
    font-size: 13px;
    color: #94a3b8 !important;
}

/* ===== KPI GLOW EFFECT ===== */
.metric-value {
    font-size: 42px;
    font-weight: 800;
    color: #c084fc;    /* purple glow */ 
    letter-spacing: 1px;
    text-shadow: 0 0 20px rgba(168,85,247,0.8);
}

/* ===== PREMIUM GLOW HEADER ===== */

.header-card {
    position: relative;
    background: linear-gradient(135deg, rgba(30,41,59,0.9), rgba(15,23,42,0.95));
    padding: 32px;
    border-radius: 18px;
    margin-bottom: 25px;
    border: 1px solid rgba(255,255,255,0.08);
    overflow: hidden;
    backdrop-filter: blur(12px);
}

/* Glow layer */
.header-card::before {
    content: "";
    position: absolute;
    top: -80px;
    left: -80px;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(37,99,235,0.35), transparent 70%);
    z-index: 0;
}

/* Content stays above glow */
.header-card * {
    position: relative;
    z-index: 1;
}

.header-card::after {
    content: "";
    position: absolute;
    bottom: -60px;
    right: -60px;
    width: 250px;
    height: 250px;
    background: radial-gradient(circle, rgba(6,182,212,0.25), transparent 70%);
}

/* Title */
.header-card h1 {
    font-size: 34px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 8px;
}

/* Subtitle */
.header-card p {
    color: #cbd5e1;
    font-size: 15px;
    max-width: 600px;
}

/* ===== DATA TABLE ===== */
[data-testid="stDataFrame"] {
    background: rgba(15,23,42,0.9);
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.05);
}

/* Header */
[data-testid="stDataFrame"] thead tr th {
    background: #1e293b !important;
    font-weight: 600;
}

/* Row hover */
[data-testid="stDataFrame"] tbody tr:hover {
    background-color: rgba(37,99,235,0.15) !important;
}


/* ===== Keep header but style it =====*/
header {
    background: transparent !important;
}

/* Optional: hide only logo */
header [data-testid="stToolbar"] {
    right: 10px;
}

/* ===== FILE UPLOADER FULL FIX ===== */
[data-testid="stFileUploader"] {
    background: #1f2937 !important;
    border: 1px solid #475569;
    border-radius: 12px;
    padding: 12px;
}

/* ===== ONLY DRAG TEXT BLACK ===== */

[data-testid="stFileUploader"] {
    background: #1f2937 !important;
}

/* Browse button */
[data-testid="stFileUploader"] button {
    background: linear-gradient(135deg, #2563eb, #06b6d4);
    color: white !important;
    border-radius: 8px;
    border: none;
    font-weight: 600;
    padding: 6px 12px;
}

/* Hover */
[data-testid="stFileUploader"] button:hover {
    background: linear-gradient(135deg, #1d4ed8, #0891b2);
}

/* ===== HEADINGS FIX ===== */
h2, h3 {
    color: #ffffff !important;
    font-weight: 700;
}

/* ===== FIX SELECTED VALUE (MAIN ISSUE) ===== */
[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {
    color:  #e2e8f0 !important;
    font-weight: 600;
}

/* Also force inner text */
[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] span {
    color:  #e2e8f0 !important;
}

/* ===== FINAL FORCE FIX (WORKS IN ALL STREAMLIT VERSIONS) ===== */

/* Target the white drop area using BaseWeb structure */
[data-testid="stFileUploader"] div[data-baseweb="file-uploader"] * {
    color: #000000 !important;
}

/* Strong override */
[data-testid="stFileUploader"] div[data-baseweb="file-uploader"] span {
    color: #000000 !important;
    font-weight: 600;
}

[data-testid="stFileUploader"] div[data-baseweb="file-uploader"] small {
    color: #000000 !important;
    font-size: 12px;
}

/* ===== FORCE FIX LABEL TEXT ===== */
[data-testid="stFileUploader"] > label,
[data-testid="stFileUploader"] p {
    color: #ffffff !important;
    font-weight: 600;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #020617);
    border-right: 1px solid rgba(139,92,246,0.2);
    box-shadow: 6px 0 30px rgba(139,92,246,0.15);
}

[data-testid="stSidebar"] .stRadio label {
    padding: 12px 16px;
    border-radius: 10px;
    margin-bottom: 8px;
    font-weight: 500;
    opacity: 1 !important;
    transition: all 0.25s ease;
    position: relative;
    display: flex;
    align-items: center;
}

[data-testid="stSidebar"] h2::after {
    content: "";
    display: block;
    height: 3px;
    width: 50px;
    margin-top: 6px;
    border-radius: 2px;

    background: linear-gradient(135deg, #7c3aed, #a855f7);

    box-shadow: 0 0 10px rgba(168, 85, 247, 0.8);
}


[data-testid="stSidebar"] .stRadio label span {
    color: #ffffff !important;  
}  

/* Improve visibility of unselected */
[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.05);
}

/* Better hover */
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(77, 171, 247, 0.15);
}

/* ===== ULTRA FORCE SIDEBAR TEXT FIX ===== */

/* Target EVERYTHING inside radio label */
[data-testid="stSidebar"] .stRadio label * {
    color: #ffffff !important;
    opacity: 1 !important;
    transition: all 0.25s ease;
    cursor: pointer;
}

/* Specifically fix text node */
[data-testid="stSidebar"] .stRadio label div {
    color: #ffffff !important;
    opacity: 1 !important;
}

/* Fix BaseWeb radio wrapper */
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] {
    opacity: 1 !important;
}

/* ===== GLOW SIDEBAR ITEMS ===== */
[data-testid="stSidebar"] .stRadio label {
    box-shadow: 0 0 8px rgba(37, 99, 235, 0.2);
}

/* RESET the big container effect */
[data-testid="stSidebar"] .stRadio > div {
    background: transparent !important;
    padding: 0 !important;
    box-shadow: none !important;
}

[data-testid="stSidebar"] .stRadio label {
    display: block;
    padding: 10px 14px;
    border-radius: 8px;
    margin-bottom: 6px;
    transition: all 0.2s ease;
    cursor: pointer;
}
[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: #228be6 !important;
    color: white !important;
    font-weight: 600;
}
[data-testid="stSidebar"] .stRadio label:has(input:checked) * {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)



#----------------------------------------
#FILE UPLOAD INSTRUCTIONS
#----------------------------------------
st.sidebar.markdown("## ✈ Navigation")

page = st.sidebar.radio(
    "",
    ["✈ Main Assignment", "📊 Debug Dashboard"]
)

if "Main Assignment" in page:
    page = "Main Assignment"
else:
    page = "Debug Dashboard"

# -------------------------------
# FILE UPLOAD SECTION
# -------------------------------
st.markdown('<div class="card">', unsafe_allow_html = True)

st.markdown("### Upload Required Files")

# your uploaders here

shipment_file = st.file_uploader(
    "Upload Shipment Dataset",
    type=["csv","xlsx","xls"]
)

schedule_file = st.file_uploader(
    "Upload Flight Schedule Dataset",
    type=["csv","xlsx","xls"]
)

routes_file = st.file_uploader(
    "Upload Flight Routes Dataset",
    type=["csv","xlsx","xls"]
)

capacity_file = st.file_uploader(
    "Upload Flight Capacity Dataset",
    type=["csv","xlsx","xls"]
)
st.markdown('</div>', unsafe_allow_html=True)
# Create a Universal File Reader Function

def read_uploaded_file(file):

    file_name = file.name.lower()

    if file_name.endswith(".csv"):
        df = pd.read_csv(file)

    elif file_name.endswith(".xlsx") or file_name.endswith(".xls"):
        df = pd.read_excel(file)

    else:
        st.error("Unsupported file format")
        return None

    return df

def get_actual_route(flight, origin, destination, routes_df):

    df = routes_df.copy()
    df["Flight_Number"] = df["Flight_Number"].str.replace(" ", "").str.strip()

    flight_rows = df[df["Flight_Number"] == flight]

    if flight_rows.empty:
        return f"{origin} → {destination}"

    # 1️⃣ Check DIRECT
    direct = flight_rows[
        (flight_rows["Origin"] == origin) &
        (flight_rows["Destination"] == destination)
    ]

    if not direct.empty:
        return f"{origin} → {destination}"

    # 2️⃣ Check HUB
    possible_splits = flight_rows[
        flight_rows["Origin"] == origin
    ]["Destination"].unique()

    for split in possible_splits:

        leg2 = flight_rows[
            (flight_rows["Origin"] == split) &
            (flight_rows["Destination"] == destination)
        ]

        if not leg2.empty:
            return f"{origin} → {split} → {destination}"

    return f"{origin} → {destination}"

# -------------------------------
# PROCESS DATA AFTER UPLOAD
# -------------------------------

if page == "Main Assignment":
   if shipment_file and schedule_file and routes_file and capacity_file:

    st.success("All files uploaded successfully")

    shipment_df = read_uploaded_file(shipment_file)
    schedule_df = read_uploaded_file(schedule_file)
    routes_df = read_uploaded_file(routes_file)
    capacity_df = read_uploaded_file(capacity_file)
    
    
    schedule_df["Flight_Number"] = schedule_df["Flight_Number"].astype(str).str.replace(" ","").str.strip()
    routes_df["Flight_Number"] = routes_df["Flight_Number"].astype(str).str.replace(" ","").str.strip()
    
    # -------------------------------
    # CLEAN COLUMN NAMES
    # -------------------------------

    shipment_df.columns = shipment_df.columns.str.strip()
    # Remove leading/trailing spaces from column names in all dataframes
    # This is crucial to avoid issues during merging and feature engineering
    routes_df.columns = routes_df.columns.str.strip()
    schedule_df.columns = schedule_df.columns.str.strip()
    capacity_df.columns = capacity_df.columns.str.strip()

    # -------------------------------
    # CONVERT NUMERIC COLUMNS
    # -------------------------------

    shipment_df["Weight"] = pd.to_numeric(shipment_df["Weight"], errors="coerce")
    shipment_df["Pieces"] = pd.to_numeric(shipment_df["Pieces"], errors="coerce")
    shipment_df["Invoice Value"] = pd.to_numeric(shipment_df["Invoice Value"], errors="coerce")

    # -------------------------------
    # CREATE WEEKDAY FEATURES
    # -------------------------------

    shipment_df["Pickup Weekday Number"] = pd.to_numeric(shipment_df["Shipment Pickup_DOW"],errors = "coerce")
    # Map numeric day to weekday name for better readability and merging with schedule/capacity data
    # The model can still use the numeric version if needed,
    # but having the weekday name helps with understanding and merging

    day_map = {
        1:"Monday",
        2:"Tuesday",
        3:"Wednesday",
        4:"Thursday",
        5:"Friday",
        6:"Saturday",
        7:"Sunday"
    }

    shipment_df["Day_of_Week"] = shipment_df["Shipment Pickup_DOW"].map(day_map)

    # -------------------------------
    # FIX SCHEDULE DATA
    # -------------------------------

    schedule_df["Day_of_Week"] = schedule_df["Operating_Day"].astype(str).str.strip()
    # Ensure that the day of week in schedule data is in the same format as in shipment data for merging and filtering
    # This is important because sometimes the schedule data might have extra spaces or 
    # different formatting for days of the week, which can cause issues
    # when we try to filter available flights based on the shipment's pickup day.
    capacity_df["Day_of_Week"] = capacity_df["Day_of_Week"].astype(str).str.strip()
    
    day_map_num = {
    "Monday":1,
    "Tuesday":2,
    "Wednesday":3,
    "Thursday":4,
    "Friday":5,
    "Saturday":6,
    "Sunday":7
    }

    capacity_df["Day_Num"] = capacity_df["Day_of_Week"].map(day_map_num)
    # -------------------------------
    # CAPACITY TRACKING
    # -------------------------------

    capacity_df["Loaded_So_Far"] = 0
    capacity_df["Remaining_Capacity"] = capacity_df["Capacity_KG"]
    capacity_df["Load_Percentage"] = 0

    # -------------------------------
    # CREATE DELIVERY WINDOW
    # -------------------------------

    shipment_df["Pickup_Date"] = pd.to_datetime(shipment_df["Pickup_Date"])
    # Convert Commit_Date safely to datetime, coercing errors to NaT (Not a Time) which can be handled later
    shipment_df["Commit_Date"] = pd.to_datetime(shipment_df["Commit_Date"],errors="coerce")

    # -------------------------------
    # FILL MISSING COMMIT DATES
    # -------------------------------

    def generate_commit_date(row):

       if pd.notnull(row["Commit_Date"]):
        return row["Commit_Date"]

       service = row["Service"]
       pickup = row["Pickup_Date"]

       if service == "IP":
        return pickup + pd.Timedelta(days=3)
       
       elif service == "IE":
        return pickup + pd.Timedelta(days=5)
    
       elif service == "IPF":
        return pickup + pd.Timedelta(days=5)

       elif service == "IEF":
        return pickup + pd.Timedelta(days=7)

       else:
        return pickup + pd.Timedelta(days=5)  # default fallback

    shipment_df["Commit_Date"] = shipment_df.apply(generate_commit_date, axis=1)
    shipment_df["Delivery_Window"] = (
        shipment_df["Commit_Date"] - shipment_df["Pickup_Date"]
    ).dt.days

    # -------------------------------
    # CALCULATE URGENCY LEVEL
    # -------------------------------

    def urgency_level(x):
        if x <= 3:
            return "Critical"
        elif x <= 5:
            return "High"
        elif x <= 7:
            return "Medium"
        else:
            return "Low"

    shipment_df["Urgency_Level"] = shipment_df["Delivery_Window"].apply(urgency_level)

    shipment_df.drop(columns=["Destination"], inplace=True,errors="ignore")

    # -------------------------------
    # PREVIEW SHIPMENT DATA
    # -------------------------------

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Shipment Data Preview")
    st.dataframe(shipment_df.head(), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------
    # FILTER FLIGHTS BY DESTINATION
    # -------------------------------

    destination = shipment_df.iloc[0]["Destination_Hub"]

    routes_filtered = routes_df[
        routes_df["Destination"] == destination
    ]

    # -------------------------------
    # FILTER FLIGHTS BY DAY
    # -------------------------------

    day = shipment_df.iloc[0]["Day_of_Week"]

    schedule_filtered = schedule_df[
        schedule_df["Day_of_Week"] == day
    ]

    # -------------------------------
    # FIND AVAILABLE FLIGHTS
    # -------------------------------

    available_flights = routes_filtered.merge(
        schedule_filtered,
        on="Flight_Number",
        how="inner"
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Available Flights for Destination")
    st.dataframe(available_flights, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.dataframe(available_flights)
    
     
    
     
    # -------------------------------
    # FEATURE ENGINEERING
    # -------------------------------
    shipment_df= shipment_df.drop_duplicates(subset=["AWB"])
    
    
    processed = prepare_features(shipment_df, feature_columns)

    # -------------------------------
    # PREDICT + ASSIGN FLIGHTS
    # -------------------------------

    assigned_flights = []
    route_output = []
    top3_results = []
    flight_days = []
    
    # Debug storage
    st.session_state["debug_data"] = []
    
    routes_output = []
    
    for i in range(len(processed)):

        features = processed.iloc[[i]]

        top3 = predict_flights(model, encoder, features)
        
        top3["Flight"] = top3["Flight"].astype(str).str.replace(" ", "").str.strip()
        
        shipment_weight = shipment_df.iloc[i]["Weight"]
        pickup_day_num  = shipment_df.iloc[i]["Pickup Weekday Number"]

    
        
        # add _probability %
        
        top3["Probability"] = top3["Probability"]*1
        top3["Prob_Display"] = top3["Probability"]*1
        top3["Prob_Display"] = top3.apply(lambda x: f"{x['Flight']} ({x['Prob_Display']:.1f}%)", axis=1)

       # shipment_weight = shipment_df.iloc[i]["Weight"]
       # pickup_day_num  = shipment_df.iloc[i]["Pickup Weekday Number"]

        service = shipment_df.iloc[i]["Service"]

        destination = shipment_df.iloc[i]["Destination_Hub"]
        
        origin = "BOM"  # Assuming all shipments originate from BOM, this can be modified if needed
        
       
        #split = shipment_df.iloc[i]["Split"]
        
        result = assign_flight(
           top3,
           shipment_weight,
           capacity_df,
           pickup_day_num,
           service,
           destination,
           routes_df,
           origin,
           schedule_df
        )
        
        if isinstance(result,tuple) and len(result) == 3:
            best_flight, flight_day ,day_num = result
            
        elif isinstance(result, tuple) and len(result) == 2:
            best_flight, flight_day = result
            day_num = None
            
        else:
            print("Unexpected result:",result)
            best_flight, flight_day ,day_num= None, None , None
 
        assigned_flights.append(best_flight)
        flight_days.append(day_num)

        top3_results.append(
            ", ".join(top3["Prob_Display"].tolist())
        )   
        top3 = top3.reset_index(drop=True)
        
        route_str = get_actual_route(best_flight, origin, destination, routes_df)
        routes_output.append(route_str)
        
        # Store Debug
        st.session_state["debug_data"].append({
            "AWB": shipment_df.iloc[i]["AWB"],
            "Top3_Flights": top3["Prob_Display"].tolist(),
            "Assigned": best_flight,
            "Route": route_str,
            "Service": service,
            "Weight": shipment_weight
            
        })
        
    # -------------------------------
    # ADD RESULTS
    # -------------------------------

    shipment_df["Top3_Predicted_Flights"] = top3_results
    shipment_df["Assigned_Flight"] = assigned_flights
    shipment_df["Route"] = routes_output
    shipment_df["Operating_Day_Num"] = flight_days
    
    # -------------------------------
    # DISPLAY RESULTS
    # -------------------------------
    
    col1, col2 = st.columns(2)

    with col1:
      st.markdown(f"""
      <div class="metric-card">
        <div class="metric-value" style="color:#60a5fa;">
            {len(shipment_df)}
        </div>
        <div class="metric-label">Total Shipments</div>
      </div>
      """, unsafe_allow_html=True)

    with col2:
      st.markdown(f"""
      <div class="metric-card">
        <div class="metric-value" style="color:#34d399;">
            {shipment_df["Assigned_Flight"].nunique()}
        </div>
        <div class="metric-label">Unique Assigned Flights</div>
      </div>
      """, unsafe_allow_html=True)
    

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Flight Assignment Results")
    st.dataframe(
    shipment_df[["AWB", "Pieces","Weight","Service","Top3_Predicted_Flights","Pickup_Date","Commit_Date","Assigned_Flight","Operating_Day_Num","Route"]]
    ,use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    
    # -------------------------------
    # DISPLAY DEBUG INFORMATION
    # -------------------------------

    import io

    output = io.BytesIO()
    
    shipment_df = shipment_df.drop(columns=["Clearance_Delay"],errors = "ignore")
    shipment_df = shipment_df.drop(columns=["Shipment Pickup_DOW"],errors = "ignore")
    
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
      shipment_df.to_excel(writer, index=False, sheet_name="Results")

    excel_data = output.getvalue()

    st.download_button(
       label="Download Flight Assignment Results",
       data=excel_data,
       file_name="flight_assignment_results.xlsx",
       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
) 

elif page == "Debug Dashboard":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## Debug Dashboard")

    if "debug_data" in st.session_state:
        debug_df = pd.DataFrame(st.session_state["debug_data"])
        st.dataframe(debug_df, use_container_width=True)

        # Download button
        import io
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            debug_df.to_excel(writer, index=False, sheet_name="Debug")

        st.download_button(
            label="Download Debug Data",
            data=output.getvalue(),
            file_name="debug_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:
        st.warning("Run Main Assignment first to generate debug data.")

    st.markdown('</div>', unsafe_allow_html=True)
    
    
    st.title("Debug Dashboard")
    
    if "debug_data" in st.session_state:
        debug_df = pd.DataFrame(st.session_state["debug_data"])
        st.dataframe(debug_df)
       
    else:
        st.warning("Run Main Assignment first to generate debug data.")
   
else:

    st.info(
        "Please upload all four files to start flight prediction."
    )
    
    
    