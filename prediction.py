import pandas as pd    #predicts the best flights

def predict_flights(model, encoder, features): # Predicts the top 3 flights based on the input features

    probs = model.predict_proba(features)[0]  # Get probabilities for the first (and only) sample

    flights = encoder.inverse_transform(list(range(len(probs))))  # Get flight names where converted into numbers during training

    df = pd.DataFrame({
        "Flight": flights,  # Flight names
        "Probability": probs * 100  # Corresponding probabilities (as percentages)
    })

    return df.sort_values(
        "Probability",
        ascending=False
    ).head(3)
    
    