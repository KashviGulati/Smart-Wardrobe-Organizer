def suggest_outfit(weather):
    # Unpack the weather tuple (temperature, weather_condition)
    temp, weather_condition = weather

    # Default outfit
    outfit = "T-shirt and Jeans"

    # Suggest outfits based on weather condition
    if "rain" in weather_condition.lower():
        outfit = "Raincoat, Umbrella, Waterproof shoes"
    elif "cloud" in weather_condition.lower():
        outfit = "Sweater or Light Jacket"
    elif "clear" in weather_condition.lower() or "sunny" in weather_condition.lower():
        # Adjust outfit based on temperature
        if temp > 25:
            outfit = "Shorts and a T-shirt"
        elif 15 < temp <= 25:
            outfit = "T-shirt and Jeans"
        else:
            outfit = "Sweater or Jacket"

    return outfit
