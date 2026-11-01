import math
import requests
from shapely.geometry import LineString, Point
import streamlit as st

st.set_page_config(
    page_title="TN Village-to-Village Route & Fare Calculator",
    page_icon="🚕",
    layout="wide",
)

# ------------------------------------------------------------------
# 1. DATABASE: ACTIVE FASTAG TOLL PLAZAS IN TAMIL NADU (COORDINATES & RATES)
# ------------------------------------------------------------------
TN_TOLL_PLAZAS = [
    {
        "name": "Krishnagiri Plaza (NH 44)",
        "lat": 12.5855,
        "lon": 78.2163,
        "single": 95,
        "return": 140,
    },
    {
        "name": "Thoppur Plaza (NH 44)",
        "lat": 11.9442,
        "lon": 78.0673,
        "single": 115,
        "return": 175,
    },
    {
        "name": "Omalur Plaza (NH 44)",
        "lat": 11.7588,
        "lon": 78.0772,
        "single": 95,
        "return": 140,
    },
    {
        "name": "Vaniyambadi Plaza (NH 48)",
        "lat": 12.6978,
        "lon": 78.6186,
        "single": 105,
        "return": 160,
    },
    {
        "name": "Pallikonda Plaza (NH 48)",
        "lat": 12.8727,
        "lon": 78.9664,
        "single": 110,
        "return": 165,
    },
    {
        "name": "Chennasamudram Plaza (NH 48)",
        "lat": 12.9248,
        "lon": 79.3789,
        "single": 65,
        "return": 100,
    },
    {
        "name": "Nemili / Sriperumbudur (NH 48)",
        "lat": 12.9866,
        "lon": 79.8821,
        "single": 70,
        "return": 105,
    },
    {
        "name": "Paranur Plaza (NH 45)",
        "lat": 12.7231,
        "lon": 79.9934,
        "single": 75,
        "return": 115,
    },
    {
        "name": "Athur / Tindivanam (NH 45)",
        "lat": 12.2036,
        "lon": 79.6644,
        "single": 65,
        "return": 100,
    },
    {
        "name": "Vikravandi Plaza (NH 45)",
        "lat": 12.0308,
        "lon": 79.5292,
        "single": 115,
        "return": 175,
    },
    {
        "name": "Sengurichi Plaza (NH 45)",
        "lat": 11.6062,
        "lon": 79.0347,
        "single": 65,
        "return": 100,
    },
    {
        "name": "Thirumandurai Plaza (NH 45)",
        "lat": 11.3916,
        "lon": 78.9634,
        "single": 75,
        "return": 115,
    },
    {
        "name": "Samayapuram Plaza (NH 45)",
        "lat": 10.9324,
        "lon": 78.7431,
        "single": 60,
        "return": 90,
    },
    {
        "name": "Mettupatti Plaza (NH 79)",
        "lat": 11.6611,
        "lon": 78.3308,
        "single": 90,
        "return": 135,
    },
    {
        "name": "Nallur Plaza (NH 79)",
        "lat": 11.6186,
        "lon": 78.7428,
        "single": 100,
        "return": 150,
    },
    {
        "name": "Vaiguntham Plaza (NH 544)",
        "lat": 11.5975,
        "lon": 77.9221,
        "single": 95,
        "return": 140,
    },
    {
        "name": "Vijayamangalam Plaza (NH 544)",
        "lat": 11.2336,
        "lon": 77.4776,
        "single": 105,
        "return": 160,
    },
    {
        "name": "Kaniyur Plaza (NH 544)",
        "lat": 11.0844,
        "lon": 77.1472,
        "single": 125,
        "return": 190,
    },
    {
        "name": "Rasampalayam Plaza (NH 44)",
        "lat": 11.1895,
        "lon": 78.1408,
        "single": 95,
        "return": 140,
    },
    {
        "name": "Palayam Plaza (NH 44)",
        "lat": 10.6975,
        "lon": 78.0772,
        "single": 95,
        "return": 140,
    },
    {
        "name": "Kodai Road Plaza (NH 44)",
        "lat": 10.1983,
        "lon": 77.9622,
        "single": 95,
        "return": 140,
    },
    {
        "name": "Boothakudi Plaza (NH 38)",
        "lat": 10.4912,
        "lon": 78.4719,
        "single": 105,
        "return": 160,
    },
    {
        "name": "Chittampatti Plaza (NH 38)",
        "lat": 10.0211,
        "lon": 78.2389,
        "single": 105,
        "return": 160,
    },
    {
        "name": "Kappalur Plaza (NH 44)",
        "lat": 9.8055,
        "lon": 78.0163,
        "single": 100,
        "return": 150,
    },
    {
        "name": "Etturvattam Plaza (NH 44)",
        "lat": 9.2789,
        "lon": 77.8931,
        "single": 100,
        "return": 150,
    },
    {
        "name": "Salaipudur Plaza (NH 44)",
        "lat": 8.9213,
        "lon": 77.7812,
        "single": 125,
        "return": 190,
    },
    {
        "name": "Nanguneri Plaza (NH 44)",
        "lat": 8.4875,
        "lon": 77.6534,
        "single": 110,
        "return": 165,
    },
    {
        "name": "Morattandi Plaza (NH 32)",
        "lat": 12.0012,
        "lon": 79.7945,
        "single": 55,
        "return": 85,
    },
    {
        "name": "Kallakudi Plaza (NH 81)",
        "lat": 10.9856,
        "lon": 78.9542,
        "single": 80,
        "return": 125,
    },
    {
        "name": "Karagadahalli Plaza (NH 844)",
        "lat": 12.4215,
        "lon": 78.0931,
        "single": 90,
        "return": 135,
    },
    {
        "name": "Kariyamangalam Plaza (NH 77)",
        "lat": 12.3321,
        "lon": 78.3612,
        "single": 60,
        "return": 90,
    },
    {
        "name": "Madukkarai Plaza (Cbe Bypass)",
        "lat": 10.9021,
        "lon": 76.9534,
        "single": 50,
        "return": 75,
    },
]

# ------------------------------------------------------------------
# 2. VEHICLE CATEGORIES & BILLING RULES
# ------------------------------------------------------------------
VEHICLE_OPTIONS = {
    "Hatchback (Swift, WagonR, Tiago)": {
        "rate": 12,
        "min_km": 250,
        "batta": 500,
    },
    "Sedan (Dzire, Etios, Aura)": {"rate": 14, "min_km": 250, "batta": 500},
    "MUV / 7-Seater (Ertiga, Triber)": {
        "rate": 18,
        "min_km": 300,
        "batta": 600,
    },
    "Premium SUV (Innova, Crysta)": {
        "rate": 22,
        "min_km": 300,
        "batta": 700,
    },
    "Tempo Traveller (12/14 Seater)": {
        "rate": 26,
        "min_km": 300,
        "batta": 800,
    },
}

# ------------------------------------------------------------------
# 3. HELPER FUNCTIONS: GEOCODING, ROUTING & TOLL INTERSECTIONS
# ------------------------------------------------------------------


def get_lat_lon(place_name):
    """Geocodes any village, town, or taluk in Tamil Nadu using OpenStreetMap Nominatim."""
    url = "https://nominatim.openstreetmap.org/search"
    query = f"{place_name}, Tamil Nadu, India"
    params = {"q": query, "format": "json", "limit": 1}
    headers = {"User-Agent": "TamilNaduTravelCalculatorApp/1.0"}
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"]), data[0]["display_name"]
    except Exception:
        return None, None, None
    return None, None, None


def get_osrm_route(start_lat, start_lon, end_lat, end_lon):
    """Fetches accurate driving route road distance and coordinate path from OSRM."""
    url = f"https://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}?overview=full&geometries=geojson"
    try:
        response = requests.get(url, timeout=12)
        data = response.json()
        if data.get("routes"):
            distance_km = round(data["routes"][0]["distance"] / 1000.0, 1)
            coords = data["routes"][0]["geometry"]["coordinates"]
            return distance_km, coords
    except Exception:
        return None, None
    return None, None


def detect_tolls_on_route(route_coords, toll_plazas, tolerance_km=3.5):
    """Detects which FASTag toll plazas are crossed along the driving route geometry."""
    if not route_coords or len(route_coords) < 2:
        return []

    route_line = LineString(route_coords)
    detected = []

    # 1 degree of latitude is roughly 111 km
    tolerance_deg = tolerance_km / 111.0

    for toll in toll_plazas:
        toll_point = Point(toll["lon"], toll["lat"])
        if route_line.distance(toll_point) <= tolerance_deg:
            detected.append(toll)

    return detected


# ------------------------------------------------------------------
# 4. APP USER INTERFACE
# ------------------------------------------------------------------
st.title("🚖 Tamil Nadu Village-to-Village Route, Toll & Fare Calculator")
st.write(
    "Type **any village, town, or city** in Tamil Nadu. The app calculates exact road kilometers, identifies crossed NHAI toll gates, and provides car and driver rent."
)
st.write("---")

col1, col2 = st.columns(2)

with col1:
    origin_input = st.text_input(
        "📍 Pickup Village / Town (From):",
        value="Dharmapuri",
        placeholder="e.g., Pappinaickanahalli, Pennagaram, Harur, Salem",
    )
    trip_type = st.radio(
        "🔄 Trip Type",
        ["One-Way (Drop)", "Round-Trip (Return)"],
        horizontal=True,
    )
    num_days = st.number_input(
        "📅 Total Trip Days:", min_value=1, max_value=30, value=1
    )

with col2:
    destination_input = st.text_input(
        "🎯 Drop Village / Town (To):",
        value="Vadapalani, Chennai",
        placeholder="e.g., Vadapalani, Sholinganallur, Siruvachur",
    )
    vehicle_type = st.selectbox(
        "🚗 Vehicle Category:", list(VEHICLE_OPTIONS.keys())
    )
    extra_local_km = st.number_input(
        "Sightseeing / Local Village Extra KM (Optional):",
        min_value=0,
        value=0,
        step=10,
    )

calc_btn = st.button("🚀 Calculate Route & Fare", type="primary")

# ------------------------------------------------------------------
# 5. CALCULATION ON CLICK
# ------------------------------------------------------------------
if calc_btn:
    if not origin_input.strip() or not destination_input.strip():
        st.warning("Please enter both origin and destination names.")
    else:
        with st.spinner("Finding route coordinates and road network..."):
            start_lat, start_lon, start_address = get_lat_lon(origin_input)
            end_lat, end_lon, end_address = get_lat_lon(destination_input)

        if not start_lat or not start_lon:
            st.error(
                f"Could not locate '{origin_input}' in Tamil Nadu. Please check the spelling or add the taluk/district."
            )
        elif not end_lat or not end_lon:
            st.error(
                f"Could not locate '{destination_input}' in Tamil Nadu. Please check the spelling or add the taluk/district."
            )
        else:
            with st.spinner("Calculating road distance and toll gates..."):
                one_way_km, route_coords = get_osrm_route(
                    start_lat, start_lon, end_lat, end_lon
                )

            if not one_way_km:
                st.error(
                    "Could not generate road directions. Please verify both points are road-connected."
                )
            else:
                is_round_trip = "Round-Trip" in trip_type
                total_running_km = (
                    (one_way_km * 2) if is_round_trip else one_way_km
                ) + extra_local_km

                v_info = VEHICLE_OPTIONS[vehicle_type]
                min_chargeable_km = v_info["min_km"] * num_days
                billed_km = max(total_running_km, min_chargeable_km)

                car_rent_amount = billed_km * v_info["rate"]
                driver_batta_amount = v_info["batta"] * num_days

                # Toll analysis
                tolls_encountered = detect_tolls_on_route(
                    route_coords, TN_TOLL_PLAZAS
                )
                toll_table = []
                total_toll_cost = 0

                for t in tolls_encountered:
                    if is_round_trip:
                        fee = (
                            t["return"] if num_days <= 1 else (t["single"] * 2)
                        )
                    else:
                        fee = t["single"]
                    total_toll_cost += fee
                    toll_table.append(
                        {
                            "Toll Plaza Name": t["name"],
                            "FASTag Fee (₹)": fee,
                            "Plaza Type": "NHAI / State Toll",
                        }
                    )

                grand_total = (
                    car_rent_amount + driver_batta_amount + total_toll_cost
                )

                # Summary Display
                st.success("✅ Route Calculated Successfully!")
                st.caption(f"**From:** {start_address}")
                st.caption(f"**To:** {end_address}")

                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Trip Distance", f"{total_running_km} KM")
                m2.metric("Toll Charges", f"₹{total_toll_cost:,}")
                m3.metric(
                    "Car Rent + Driver",
                    f"₹{(car_rent_amount + driver_batta_amount):,}",
                )
                m4.metric("Grand Total Quote", f"₹{grand_total:,}")

                st.write("---")
                tab1, tab2, tab3 = st.tabs(
                    [
                        "💰 Fare Quotation",
                        "🛣️ Toll Gates Crossed",
                        "📋 Commercial Terms",
                    ]
                )

                with tab1:
                    st.markdown(
                        f"""
                    | Billing Item | Description | Amount |
                    | :--- | :--- | :--- |
                    | **Actual Distance** | {total_running_km} KM ({'Round-trip' if is_round_trip else 'One-way'}) | Included |
                    | **Billed Kilometers** | {billed_km} KM (Min rule: {v_info['min_km']} KM/day) | - |
                    | **Vehicle Rent** | {billed_km} KM × ₹{v_info['rate']}/km ({vehicle_type}) | ₹{car_rent_amount:,} |
                    | **Driver Batta** | {num_days} Day(s) × ₹{v_info['batta']}/day | ₹{driver_batta_amount:,} |
                    | **FASTag Toll Charges** | {len(toll_table)} Toll Plaza(s) | ₹{total_toll_cost:,} |
                    | **Total Trip Estimate** | **All In (Fuel + Car + Driver + Tolls)** | **₹{grand_total:,}** |
                    """
                    )

                with tab2:
                    if toll_table:
                        st.write(
                            f"Identified **{len(toll_table)} toll plaza(s)** along the vehicle trajectory:"
                        )
                        st.table(toll_table)
                    else:
                        st.info(
                            "No FASTag highway toll gates detected along this specific rural/highway route."
                        )

                with tab3:
                    st.markdown(
                        f"""
                    - **Daily Minimum:** Billed at a minimum of **{v_info['min_km']} km/day**.
                    - **Driver Duty Hours:** Standard outstation coverage from 6:00 AM to 10:00 PM.
                    - **Toll Fees:** Calculated based on official car/jeep FASTag rates.
                    - **Exclusions:** Parking fees (temple/airport/station) and interstate taxes (if entering KA/PY/KL) are payable directly by the customer on actuals.
                    """
                    )
