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

def suggest_mood_outfit(sentiment):
    # Suggest outfits based on sentiment
    if sentiment == 'positive':
        return "Bright colors (e.g., red, yellow) or vibrant patterns with a T-shirt and Jeans"
    elif sentiment == 'negative':
        return "Muted colors (e.g., grey, navy) or cozy fabrics with a Sweater and Pants"
    else:  # neutral
        return "Neutral tones (e.g., beige, white) or classic styles with a Shirt and Chinos"