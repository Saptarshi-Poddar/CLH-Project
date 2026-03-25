import pandas as pd
from business_rules import service_allowed
def valid_route(flight, origin, destination, routes_df):
# Route validation function to check if the flight has a valid route (direct or via hub) for the given origin and destination

    flight = str(flight).replace(" ", "").strip()

    df = routes_df.copy()
    
    df["Flight_Number"] = df["Flight_Number"].str.replace(" ", "").str.strip()
    
    # Filter routes for that flight
    flight_rows = df[df["Flight_Number"] == flight]

    if flight_rows.empty:
        return False

    # Build graph for this flight
    graph = {}
    for _, row in flight_rows.iterrows():
        o = row["Origin"]
        d = row["Destination"]

        if o not in graph:
            graph[o] = []
        graph[o].append(d)

    # BFS traversal to check reachability
    from collections import deque
    max_hops = 2  # Allow direct or 1-hop routes
    
    queue = deque([(origin, 0)])  # (node, hops)

    while queue:
        node, depth = queue.popleft()

        if depth > max_hops:
            continue

        if node == destination:
            return True

        for neighbor in graph.get(node, []):
            queue.append((neighbor, depth + 1))

    return False
    
def assign_flight(top3, shipment_weight, capacity_df, pickup_day_num, service, destination, routes_df, origin,schedule_df):
# Main function to assign the best flight based on the top 3 predictions, business rules, and capacity constraints
    airline_map = {
        "6E": "Indigo",
        "AI": "AI",
        "EK": "EK",
        "FX": "FX",
        "QR": "QR"
    }

   # day_map_num = {
   #     "Monday":1,
   #     "Tuesday":2,
    #    "Wednesday":3,
    #    "Thursday":4,
    #    "Friday":5,
    #    "Saturday":6,
    #    "Sunday":7
   # }

    CLEARENCE_DAYS = 2  # Assuming a default clearance time of 2 days for all shipments (can be adjusted based on actual data)

    routes_df["Flight_Number"] = routes_df["Flight_Number"].astype(str).str.replace(" ","").str.strip()
    #pickup_day_num = day_map_num.get(day)
    
    if pd.isna(pickup_day_num) :
        print("pickup_day_num is NAN -> SKIPPING")
        return None,None
    
    earliest_day = ((pickup_day_num + CLEARENCE_DAYS - 1) % 7) + 1  # Calculate earliest possible flight day considering clearance time

    # PRIORITIZE FEDEX FOR IP
    if service == "IP":
        top3["Flight"] = top3["Flight"].astype(str).str.replace(" ", "").str.strip()
        top3["Priority"] = top3["Flight"].str.startswith("FX").astype(int)
        top3 = top3.sort_values(["Priority", "Probability"], ascending=[False, False])

    # =========================================
    # STEP 1: TRY TOP 3 (STRICT PRIORITY)
    # =========================================
    
    for flight in top3["Flight"]:
        
        flight = str(flight).replace(" ", "").strip()
        
        if not service_allowed(service, flight):
            continue

        if not valid_route(flight, origin, destination, routes_df):
            continue
        
        #import streamlit as st
       # st.write("Trying Flight:",flight)

        valid_days = schedule_df[schedule_df["Flight_Number"].str.replace(" ","").str.strip()== flight.replace(" ","").strip()]["Operating_Day"].unique()
        valid_days = [str(day).strip() for day in valid_days]   
        
       # print("\n=============================================")
        #print("Flight trying:" ,flight)
        #print("Valid days:",valid_days)
        #print("Earliest day:",earliest_day)
       # print("Service",service)
        #print("Destination:",destination)
       # print("Schedule flights sample:",schedule_df["Flight_Number"].unique()[:10])
        #print("\n=============================================\n") 
        airline_code = flight[:2]
        airline = airline_map.get(airline_code)
        
        # Get valid operating days for this flight
        #valid_days = schedule_df[schedule_df["Flight_Number"] == flight]["Day_of_Week"].unique()
        print("Valid Operating Days:",valid_days)
        print("Earliest Allowed Day:",earliest_day)
        
        # SAME WEEK
        same_week = capacity_df[
            (capacity_df["Airline"] == airline) &
            #(capacity_df["Day_Num"] >= earliest_day)&
            (capacity_df["Day_of_Week"].isin(valid_days))
        ]

        # NEXT WEEK
        next_week = capacity_df[
            (capacity_df["Airline"] == airline) &
           # (capacity_df["Day_Num"] < earliest_day)&
            (capacity_df["Day_of_Week"].isin(valid_days))
        ]

        rows = pd.concat([same_week, next_week])
        print("Flitered Capacity Rows:")
        
        if rows.empty:
            print("No rows found")
            continue
        
        print(rows[["Airline","Day_of_Week","Day_Num"]])
        
        # Load balancing
        rows["Load_Percentage"] = (
            rows["Loaded_So_Far"] / rows["Capacity_KG"]
        )

        rows["day_priority"] = (rows["Day_Num"] - earliest_day) % 7
        rows = rows.sort_values(["day_priority","Load_Percentage"])

        for idx in rows.index:
            flight_day_num = capacity_df.loc[idx,"Day_Num"]
            

            remaining_capacity = (
                capacity_df.loc[idx, "Capacity_KG"]
                - capacity_df.loc[idx, "Loaded_So_Far"]
            )

            if remaining_capacity >= shipment_weight:
    
                
                capacity_df.loc[idx, "Loaded_So_Far"] += shipment_weight
                return flight, capacity_df.loc[idx, "Day_of_Week"],capacity_df.loc[idx,"Day_Num"]
                
    # =========================================
    # STEP 2: FALLBACK (CONTROLLED)
    # =========================================

    possible_flights = routes_df[routes_df["Destination"] == destination]["Flight_Number"].unique()

    for flight in possible_flights:
        flight = str(flight).replace(" ", "").strip()

        if not valid_route(flight, origin, destination, routes_df):
            continue
        
        if not service_allowed(service, flight):
            continue

        airline_code = flight[:2]
        airline = airline_map.get(airline_code)

        if airline is None:
            continue

        # Get valid operating days for this fligyt
        valid_days = schedule_df[schedule_df["Flight_Number"].str.replace(" ","").str.strip()== flight.replace(" ","").strip()]["Operating_Day"].unique()
        
        valid_days = [str(day).strip() for day in valid_days]
        
        print("Valid Operating Days:",valid_days)
        print("Earliest Allowed Day:",earliest_day)
        
        same_week = capacity_df[
            (capacity_df["Airline"] == airline) &
           # (capacity_df["Day_Num"] >= earliest_day) &
            (capacity_df["Day_of_Week"].isin(valid_days))
        ]

        next_week = capacity_df[
            (capacity_df["Airline"] == airline) &
           # (capacity_df["Day_Num"] < earliest_day)&
            (capacity_df["Day_of_Week"].isin(valid_days))
        ]

        rows = pd.concat([same_week, next_week])
        print("Flitered Capacity Rows:")
        
            
        if rows.empty:
            print("No rows found")
            continue

        print(rows[["Airline","Day_of_Week","Day_Num"]])
        
        rows["Load_Percentage"] = (
            rows["Loaded_So_Far"] / rows["Capacity_KG"]
        )

        rows["day_priority"] = (rows["Day_Num"] - earliest_day) % 7
        rows = rows.sort_values(["day_priority","Load_Percentage"])

        for idx in rows.index:
            flight_day_num = capacity_df.loc[idx,"Day_Num"]
           

            remaining = (
                capacity_df.loc[idx, "Capacity_KG"]
                - capacity_df.loc[idx, "Loaded_So_Far"]
            )

            if remaining >= shipment_weight:
                capacity_df.loc[idx, "Loaded_So_Far"] += shipment_weight
                
                capacity_df.loc[idx, "Loaded_So_Far"] += shipment_weight
                return flight, capacity_df.loc[idx, "Day_of_Week"],capacity_df.loc[idx,"Day_Num"]

    # =========================================
    # FINAL FALLBACK
    # =========================================

    possible_flights = routes_df[
        (routes_df["Origin"] == origin) &
        (routes_df["Destination"] == destination)
    ]["Flight_Number"].unique()

    for flight in possible_flights:
        flight = str(flight).replace(" ", "").strip()

        if not service_allowed(service, flight):
            continue
        
        if valid_route(flight, origin, destination, routes_df):
            return flight, None

    return None,None
    