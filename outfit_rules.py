import sqlite3
from itertools import product

def get_db():
    conn = sqlite3.connect('wardrobe.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_matching_clothes(category, season=None):
    """Find all matching clothes in the wardrobe based on category and optional season"""
    conn = get_db()
    query = "SELECT * FROM wardrobe WHERE category = ?"
    params = [category]
    
    if season:
        query += " AND season = ?"
        params.append(season)
    
    clothes = conn.execute(query, params).fetchall()
    conn.close()
    return clothes

def get_season_from_temp(temp):
    """Determine season based on temperature"""
    if temp > 20:
        return "summer"
    else:
        return "winter"

def suggest_outfit(weather):
    """Suggest all possible outfits based on weather and available wardrobe items"""
    temp, weather_condition = weather
    season = get_season_from_temp(temp)
    
    # Define outfit categories: separate tops+bottoms and standalone dresses
    if "rain" in weather_condition.lower():
        tops_bottoms = [["Jacket", "Sweater"], ["Jeans", "Shorts"], ["T-shirt", "Shirt"]]
        standalone = [["Dress"]]
        description = "Raincoat, Umbrella, Waterproof shoes, or a jacket with jeans/shorts, or a dress"
    elif "cloud" in weather_condition.lower():
        tops_bottoms = [["Sweater", "Jacket"], ["Jeans", "Shorts"], ["T-shirt", "Shirt"]]
        standalone = [["Dress"]]
        description = "Sweater or Jacket with Jeans/Shorts and a T-shirt/Shirt, or a dress"
    elif "clear" in weather_condition.lower() or "sunny" in weather_condition.lower():
        if temp > 25:
            tops_bottoms = [["T-shirt", "Shirt"], ["Shorts", "Jeans"]]
            standalone = [["Dress"]]
            description = "T-shirt/Shirt with Shorts/Jeans, or a dress"
        elif 15 < temp <= 25:
            tops_bottoms = [["T-shirt", "Shirt"], ["Jeans", "Shorts"]]
            standalone = [["Dress"]]
            description = "T-shirt/Shirt with Jeans/Shorts, or a dress"
        else:
            tops_bottoms = [["Sweater", "Jacket"], ["Jeans"], ["T-shirt", "Shirt"]]
            standalone = [["Dress"]]
            description = "Sweater/Jacket with Jeans and a T-shirt/Shirt, or a dress"
    else:
        tops_bottoms = [["T-shirt", "Shirt"], ["Jeans", "Shorts"]]
        standalone = [["Dress"]]
        description = "T-shirt/Shirt with Jeans/Shorts, or a dress"
    
    # Fetch items for tops+bottoms combinations
    tops_bottoms_items = []
    for category_group in tops_bottoms:
        group_items = []
        for category in category_group:
            items = get_matching_clothes(category, season=season)
            if items:
                group_items.extend(items)
        tops_bottoms_items.append(group_items if group_items else [None])
    
    # Fetch items for standalone dresses
    standalone_items = []
    for category_group in standalone:
        group_items = []
        for category in category_group:
            items = get_matching_clothes(category, season=season)
            if items:
                group_items.extend(items)
        standalone_items.append(group_items if group_items else [None])
    
    # Generate tops+bottoms outfit combinations
    outfits = []
    for combo in product(*tops_bottoms_items):
        if None not in combo:
            outfits.append(list(combo))
    
    # Add standalone dress outfits
    for dress in standalone_items[0]:
        if dress:
            outfits.append([dress])
    
    # If no outfits, return all categories for recommendation
    missing_categories = []
    if not outfits:
        for category_group in tops_bottoms:
            missing_categories.extend(category_group)
        for category_group in standalone:
            missing_categories.extend(category_group)
    
    return {
        'outfits': outfits,  # List of outfit combinations
        'description': description,
        'categories': missing_categories,
        'season': season
    }

def get_mood_colors(sentiment):
    """Get color recommendations based on sentiment"""
    if sentiment == 'positive':
        return "bright colors (e.g., red, yellow, orange) or vibrant patterns"
    elif sentiment == 'negative':
        return "muted colors (e.g., grey, navy, deep blue) or cozy fabrics"
    else:  # neutral
        return "neutral tones (e.g., beige, white, light blue) or classic styles"

def suggest_mood_outfit(sentiment):
    """Suggest all possible outfits based on sentiment and available wardrobe items"""
    # Define outfit categories: separate tops+bottoms and standalone dresses
    if sentiment == 'positive':
        tops_bottoms = [["T-shirt", "Shirt"], ["Jeans", "Shorts"]]
        standalone = [["Dress"]]
        description = "Bright and vibrant T-shirt or Shirt with Jeans/Shorts, or a dress"
    elif sentiment == 'negative':
        tops_bottoms = [["Sweater", "Jacket"], ["Jeans"]]
        standalone = [["Dress"]]
        description = "Cozy Sweater or Jacket with Jeans, or a cozy dress"
    else:  # neutral
        tops_bottoms = [["Shirt", "T-shirt"], ["Jeans", "Shorts"]]
        standalone = [["Dress"]]
        description = "Classic Shirt or T-shirt with Jeans/Shorts, or a classic dress"
    
    # Fetch items for tops+bottoms combinations
    tops_bottoms_items = []
    for category_group in tops_bottoms:
        group_items = []
        for category in category_group:
            items = get_matching_clothes(category)
            if items:
                group_items.extend(items)
        tops_bottoms_items.append(group_items if group_items else [None])
    
    # Fetch items for standalone dresses
    standalone_items = []
    for category_group in standalone:
        group_items = []
        for category in category_group:
            items = get_matching_clothes(category)
            if items:
                group_items.extend(items)
        standalone_items.append(group_items if group_items else [None])
    
    # Generate tops+bottoms outfit combinations
    outfits = []
    for combo in product(*tops_bottoms_items):
        if None not in combo:
            outfits.append(list(combo))
    
    # Add standalone dress outfits
    for dress in standalone_items[0]:
        if dress:
            outfits.append([dress])
    
    # If no outfits, return all categories for recommendation
    missing_categories = []
    if not outfits:
        for category_group in tops_bottoms:
            missing_categories.extend(category_group)
        for category_group in standalone:
            missing_categories.extend(category_group)
    
    return {
        'outfits': outfits,  # List of outfit combinations
        'description': description,
        'categories': missing_categories,
        'colors': get_mood_colors(sentiment)
    }