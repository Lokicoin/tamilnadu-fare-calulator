import streamlit as st

st.set_page_config(
    page_title="TN Trip & Fare Calculator",
    page_icon="🚗",
    layout="wide",
)

# -------------------------------------------------------------
# 1. DATABASE: TOLL PLAZAS IN TAMIL NADU
# -------------------------------------------------------------
TOLLS_DB = {
    "krishnagiri": {
        "name": "Krishnagiri Plaza (NH 44)",
        "single": 95,
        "return": 140,
    },
    "vaniyambadi": {
        "name": "Vaniyambadi Plaza (NH 48)",
        "single": 105,
        "return": 160,
    },
    "pallikonda": {
        "name": "Pallikonda Plaza (NH 48)",
        "single": 110,
        "return": 165,
    },
    "chennasamudram": {
        "name": "Chennasamudram / Walajahpet (NH 48)",
        "single": 65,
        "return": 100,
    },
    "nemili": {
        "name": "Nemili / Sriperumbudur (NH 48)",
        "single": 70,
        "return": 105,
    },
    "thoppur": {
        "name": "Thoppur Plaza (NH 44)",
        "single": 115,
        "return": 175,
    },
    "omallur": {"name": "Omallur Plaza (NH 44)", "single": 95, "return": 140},
    "mettupatti": {
        "name": "Mettupatti Plaza (NH 68)",
        "single": 90,
        "return": 135,
    },
    "nallur": {"name": "Nallur Plaza (NH 68)", "single": 100, "return": 150},
    "vikravandi": {
        "name": "Vikravandi Plaza (NH 45)",
        "single": 115,
        "return": 175,
    },
    "athur": {
        "name": "Athur / Tindivanam (NH 45)",
        "single": 65,
        "return": 100,
    },
    "paranur": {
        "name": "Paranur / Chengalpattu (NH 45)",
        "single": 75,
        "return": 115,
    },
    "sengurichi": {
        "name": "Sengurichi Plaza (NH 45)",
        "single": 65,
        "return": 100,
    },
    "thirumandurai": {
        "name": "Thirumandurai Plaza (NH 45)",
        "single": 75,
        "return": 115,
    },
    "samayapuram": {
        "name": "Samayapuram Plaza (NH 45)",
        "single": 60,
        "return": 90,
    },
    "vaikuntam": {
        "name": "Vaikuntam / Sankari (NH 544)",
        "single": 95,
        "return": 140,
    },
    "vijayamangalam": {
        "name": "Vijayamangalam Plaza (NH 544)",
        "single": 105,
        "return": 160,
    },
    "kaniyanur": {
        "name": "Kaniyanur Plaza (NH 544)",
        "single": 65,
        "return": 95,
    },
    "boothakudi": {
        "name": "Boothakudi Plaza (NH 38)",
        "single": 105,
        "return": 160,
    },
    "chittampatti": {
        "name": "Chittampatti Plaza (NH 38)",
        "single": 105,
        "return": 160,
    },
    "kappalur": {
        "name": "Kappalur Plaza (NH 44)",
        "single": 100,
        "return": 150,
    },
    "etturvattam": {
        "name": "Etturvattam Plaza (NH 44)",
        "single": 100,
        "return": 150,
    },
    "salaipudur": {
        "name": "Salaipudur Plaza (NH 44)",
        "single": 125,
        "return": 190,
    },
    "nanguneri": {
        "name": "Nanguneri Plaza (NH 44)",
        "single": 110,
        "return": 165,
    },
    "palayam": {"name": "Palayam Plaza (NH 44)", "single": 95, "return": 140},
    "kodai_road": {
        "name": "Kodai Road Plaza (NH 44)",
        "single": 95,
        "return": 140,
    },
    "morattandi": {
        "name": "Morattandi Plaza (NH 32)",
        "single": 55,
        "return": 85,
    },
}

# -------------------------------------------------------------
# 2. CORRIDOR ROUTE MATRIX (DISTANCES & TOLL PLAZAS)
# -------------------------------------------------------------
CORRIDORS = {
    # Dharmapuri Hub
    ("Dharmapuri", "Chennai"): {
        "km": 295,
        "via": "Krishnagiri, Vellore, Kanchipuram (NH 44 & NH 48)",
        "tolls": [
            "krishnagiri",
            "vaniyambadi",
            "pallikonda",
            "chennasamudram",
            "nemili",
        ],
    },
    ("Dharmapuri", "Salem"): {
        "km": 68,
        "via": "Thoppur, Omalur (NH 44)",
        "tolls": ["thoppur", "omallur"],
    },
    ("Dharmapuri", "Coimbatore"): {
        "km": 230,
        "via": "Salem, Sankari, Bhavani, Avinashi (NH 44 & NH 544)",
        "tolls": ["thoppur", "omallur", "vaikuntam", "vijayamangalam"],
    },
    ("Dharmapuri", "Madurai"): {
        "km": 305,
        "via": "Salem, Namakkal, Karur, Dindigul (NH 44)",
        "tolls": ["thoppur", "omallur", "palayam", "kodai_road"],
    },
    ("Dharmapuri", "Trichy"): {
        "km": 210,
        "via": "Thoppur, Salem, Namakkal, Musiri (NH 44 & SH)",
        "tolls": ["thoppur", "omallur"],
    },
    # Chennai Hub
    ("Chennai", "Salem"): {
        "km": 345,
        "via": "Tindivanam, Villupuram, Ulundurpet, Attur (NH 45 & NH 68)",
        "tolls": [
            "paranur",
            "athur",
            "vikravandi",
            "sengurichi",
            "nallur",
            "mettupatti",
        ],
    },
    ("Chennai", "Trichy"): {
        "km": 330,
        "via": "Chengalpattu, Tindivanam, Villupuram, Perambalur (NH 45)",
        "tolls": [
            "paranur",
            "athur",
            "vikravandi",
            "sengurichi",
            "thirumandurai",
            "samayapuram",
        ],
    },
    ("Chennai", "Madurai"): {
        "km": 460,
        "via": "Trichy Bypass, Melur (NH 45 & NH 38)",
        "tolls": [
            "paranur",
            "athur",
            "vikravandi",
            "sengurichi",
            "thirumandurai",
            "samayapuram",
            "boothakudi",
            "chittampatti",
        ],
    },
    ("Chennai", "Coimbatore"): {
        "km": 505,
        "via": "Vellore, Krishnagiri, Salem, Erode (NH 48 & NH 544)",
        "tolls": [
            "nemili",
            "chennasamudram",
            "pallikonda",
            "vaniyambadi",
            "krishnagiri",
            "thoppur",
            "omallur",
            "vaikuntam",
            "vijayamangalam",
        ],
    },
    ("Chennai", "Tirunelveli"): {
        "km": 625,
        "via": "Trichy, Madurai, Virudhunagar, Kovilpatti (NH 45 & NH 44)",
        "tolls": [
            "paranur",
            "athur",
            "vikravandi",
            "sengurichi",
            "thirumandurai",
            "samayapuram",
            "boothakudi",
            "chittampatti",
            "kappalur",
            "etturvattam",
            "salaipudur",
        ],
    },
    ("Chennai", "Kanyakumari"): {
        "km": 705,
        "via": "Madurai, Tirunelveli, Nanguneri (NH 45 & NH 44)",
        "tolls": [
            "paranur",
            "athur",
            "vikravandi",
            "sengurichi",
            "thirumandurai",
            "samayapuram",
            "boothakudi",
            "chittampatti",
            "kappalur",
            "etturvattam",
            "salaipudur",
            "nanguneri",
        ],
    },
    ("Chennai", "Pondicherry"): {
        "km": 155,
        "via": "East Coast Road (ECR) / GST Tindivanam (NH 32)",
        "tolls": ["paranur", "athur", "morattandi"],
    },
    ("Chennai", "Hosur"): {
        "km": 310,
        "via": "Sriperumbudur, Vellore, Krishnagiri (NH 48)",
        "tolls": [
            "nemili",
            "chennasamudram",
            "pallikonda",
            "vaniyambadi",
            "krishnagiri",
        ],
    },
    # Salem Hub
    ("Salem", "Coimbatore"): {
        "km": 165,
        "via": "Sankari, Bhavani, Avinashi (NH 544)",
        "tolls": ["vaikuntam", "vijayamangalam"],
    },
    ("Salem", "Madurai"): {
        "km": 235,
        "via": "Namakkal, Karur, Dindigul (NH 44)",
        "tolls": ["palayam", "kodai_road"],
    },
    ("Salem", "Trichy"): {
        "km": 140,
        "via": "Namakkal, Thottiyam, Musiri (NH 44 & SH)",
        "tolls": [],
    },
    # Coimbatore Hub
    ("Coimbatore", "Madurai"): {
        "km": 215,
        "via": "Palladam, Dharapuram, Oddanchatram, Dindigul (NH 83)",
        "tolls": ["kodai_road"],
    },
    ("Coimbatore", "Trichy"): {
        "km": 220,
        "via": "Palladam, Kangeyam, Karur (NH 81)",
        "tolls": [],
    },
    # Madurai Hub
    ("Madurai", "Tirunelveli"): {
        "km": 160,
        "via": "Virudhunagar, Sattur, Kovilpatti (NH 44)",
        "tolls": ["kappalur", "etturvattam", "salaipudur"],
    },
    ("Madurai", "Kanyakumari"): {
        "km": 245,
        "via": "Tirunelveli, Valliyur, Nagercoil bypass (NH 44)",
        "tolls": ["kappalur", "etturvattam", "salaipudur", "nanguneri"],
    },
    ("Madurai", "Rameshwaram"): {
        "km": 175,
        "via": "Manamadurai, Paramakudi, Ramanathapuram (NH 87)",
        "tolls": [],
    },
}

# -------------------------------------------------------------
# 3. VEHICLE FLEET & PRICING RULES
# -------------------------------------------------------------
VEHICLE_FLEET = {
    "Hatchback (Swift, WagonR, Tiago)": {
        "rate_per_km": 12,
        "min_km_day": 250,
        "driver_batta": 500,
        "seating": "4 + 1 Driver",
    },
    "Sedan (Dzire, Etios, Aura)": {
        "rate_per_km": 14,
        "min_km_day": 250,
        "driver_batta": 500,
        "seating": "4 + 1 Driver",
    },
    "MUV / Compact SUV (Ertiga, Triber)": {
        "rate_per_km": 18,
        "min_km_day": 300,
        "driver_batta": 600,
        "seating": "6 + 1 Driver",
    },
    "Premium SUV (Innova, Crysta)": {
        "rate_per_km": 22,
        "min_km_day": 300,
        "driver_batta": 700,
        "seating": "7 + 1 Driver",
    },
    "Tempo Traveller (12 Seater)": {
        "rate_per_km": 26,
        "min_km_day": 300,
        "driver_batta": 800,
        "seating": "12 + 1 Driver",
    },
}

# -------------------------------------------------------------
# 4. APP INTERFACE
# -------------------------------------------------------------
st.title("🚗 Tamil Nadu Outstation Route, Toll & Rental Calculator")
st.caption(
    "Automated fare generator including highway distances, NHAI FASTag toll gates, car rentals, and driver allowances."
)
st.write("---")

LOCATIONS = sorted(
    list(
        set(
            [k[0] for k in CORRIDORS.keys()] + [k[1] for k in CORRIDORS.keys()]
        )
    )
)

col_input1, col_input2, col_input3 = st.columns(3)

with col_input1:
    origin = st.selectbox(
        "📍 Pickup Location (From)", LOCATIONS, index=LOCATIONS.index("Dharmapuri")
    )
    destination = st.selectbox(
        "🎯 Drop Location (To)", LOCATIONS, index=LOCATIONS.index("Chennai")
    )

with col_input2:
    trip_type = st.radio(
        "🔄 Trip Type",
        ["One-Way (Drop)", "Round-Trip (Return)"],
        horizontal=True,
    )
    total_days = st.number_input(
        "📅 Number of Days", min_value=1, max_value=30, value=1
    )

with col_input3:
    selected_vehicle_name = st.selectbox(
        "🚘 Select Car Category", list(VEHICLE_FLEET.keys())
    )
    custom_km = st.number_input(
        "Custom/Local Sightseeing KM (Optional)", min_value=0, value=0, step=10
    )

# -------------------------------------------------------------
# 5. CORE CALCULATION ENGINE
# -------------------------------------------------------------
if origin == destination:
    st.warning("⚠️ Origin and Destination cannot be the same city.")
else:
    route_key = (origin, destination)
    rev_key = (destination, origin)
    route_info = CORRIDORS.get(route_key) or CORRIDORS.get(rev_key)

    if not route_info:
        st.error(
            f"Direct corridor data between {origin} and {destination} is not mapped yet in the default table."
        )
    else:
        one_way_km = route_info["km"]
        actual_running_km = (
            (one_way_km * 2) if "Round-Trip" in trip_type else one_way_km
        )
        actual_running_km += custom_km

        v_data = VEHICLE_FLEET[selected_vehicle_name]
        min_chargeable_km = v_data["min_km_day"] * total_days
        billed_km = max(actual_running_km, min_chargeable_km)

        # Rental Cost
        vehicle_charge = billed_km * v_data["rate_per_km"]

        # Driver Allowance
        driver_allowance = v_data["driver_batta"] * total_days

        # Toll Gate Charges
        toll_plaza_keys = route_info["tolls"]
        toll_breakdown = []
        total_toll_cost = 0

        for t_key in toll_plaza_keys:
            toll = TOLLS_DB.get(t_key)
            if toll:
                if "Round-Trip" in trip_type:
                    # Same plaza round-trip discounted rate if within single/few days
                    fee = (
                        toll["return"]
                        if total_days <= 1
                        else (toll["single"] * 2)
                    )
                else:
                    fee = toll["single"]
                total_toll_cost += fee
                toll_breakdown.append(
                    {"Plaza Name": toll["name"], "Applicable Fee (₹)": fee}
                )

        grand_total = vehicle_charge + driver_allowance + total_toll_cost

        # -------------------------------------------------------------
        # 6. OUTPUT DASHBOARD
        # -------------------------------------------------------------
        st.write("---")
        st.subheader(
            f"📋 Trip Summary: {origin} ➜ {destination} ({trip_type})"
        )
        st.info(f"**Primary Route:** {route_info['via']}")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric(
            label="Total Distance",
            value=f"{actual_running_km} KM",
            delta=f"Billed: {billed_km} KM",
        )
        c2.metric(
            label="Toll Charges",
            value=f"₹{total_toll_cost:,}",
            delta=f"{len(toll_breakdown)} Plazas",
        )
        c3.metric(
            label="Car Rent + Driver",
            value=f"₹{(vehicle_charge + driver_allowance):,}",
        )
        c4.metric(
            label="Grand Total Quote",
            value=f"₹{grand_total:,}",
            delta="All-Inclusive",
        )

        st.write("---")

        tab1, tab2, tab3 = st.tabs(
            [
                "💵 Fare Quotation Card",
                "🛣️ Toll Gate Breakdown",
                "📄 Billing Terms",
            ]
        )

        with tab1:
            st.markdown(
                f"""
            | Item Description | Quantity / Details | Amount |
            | :--- | :--- | :--- |
            | **Base Vehicle Tariff** | {billed_km} KM × ₹{v_data['rate_per_km']}/km ({selected_vehicle_name}) | ₹{vehicle_charge:,} |
            | **Driver Batta / Allowance** | {total_days} Day(s) × ₹{v_data['driver_batta']}/day | ₹{driver_allowance:,} |
            | **FASTag Toll Gate Charges** | {len(toll_breakdown)} Highway Plaza(s) | ₹{total_toll_cost:,} |
            | **Final Estimated Fare** | **All In (Fuel + Driver + Toll)** | **₹{grand_total:,}** |
            """
            )

        with tab2:
            if toll_breakdown:
                st.write(
                    f"Highway toll plazas encountered along **{origin} ➜ {destination}**:"
                )
                st.table(toll_breakdown)
            else:
                st.success(
                    "No major NHAI toll plazas recorded on this route corridor."
                )

        with tab3:
            st.markdown(
                f"""
            - **Minimum Distance Rule:** {v_data['min_km_day']} KM charged per calendar day. (Actual: {actual_running_km} KM | Billed: {billed_km} KM).
            - **Driver Allowance:** Covers driver's food and stay per calendar day (6:00 AM to 10:00 PM).
            - **Night Driving:** Driving between 10:00 PM and 6:00 AM usually attracts an additional night allowance (₹300/night).
            - **Parking & State Permit:** Parking charges at destinations (railway stations, airports, temples) and interstate taxes (if crossing into KA/KL/PY) are extra on actuals.
            """
            )
