import pandas as pd
# -----------------------------------
# FEATURE ENGINEERING
# -----------------------------------

def prepare_features(df, feature_columns):
    
    # Derived feature
    df["Weight per Piece"] = df["Weight"] / df["Pieces"]

    # Weekend pickup
    if "Shipment Pickup_DOW" in df.columns:
        df["Weekend_Pickup"] = df["Shipment Pickup_DOW"].isin([6,7]).astype(int)
    else:
        df["Weekend_Pickup"] = 0

    # Clearance delay default
    if "Clearance_Delay" not in df.columns:
        df["Clearance_Delay"] = 0

    # Capacity based features (if capacity merged)
    if "Capacity_KG" in df.columns:

        df["Weight_to_Capacity"] = df["Weight"] / df["Capacity_KG"]

        if "Loaded_So_Far" in df.columns:
            df["Remaining_Capacity"] = df["Capacity_KG"] - df["Loaded_So_Far"]
            df["Load_Percentage"] = df["Loaded_So_Far"] / df["Capacity_KG"]

    # One hot encoding
    df = pd.get_dummies(
        df,
        columns=[
            "Urgency_Level",
            "Destination_Hub"
            
        ]
    )

    # Match training columns
    df = df.reindex(columns=feature_columns, fill_value=0)

    return df