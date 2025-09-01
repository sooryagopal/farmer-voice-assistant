def identify_intent(text):
    """Identifies the user's intent based on keywords."""
    text = text.lower()
    intent = 'unknown'
    details = {}

    if any(keyword in text for keyword in ['weather', 'climate', 'forecast', 'rain']):
        intent = 'weather_report'
        if 'for' in text:
            parts = text.split('for')
            location = parts[-1].strip()
            details['location'] = location
    elif any(keyword in text for keyword in ['price', 'rate', 'cost', 'sell']):
        intent = 'crop_price_forecast'
        if 'for' in text:
            parts = text.split('for')
            crop = parts[-1].strip()
            details['crop'] = crop
    elif any(keyword in text for keyword in ['yield', 'produce', 'how much', 'harvest']):
        intent = 'crop_yield_prediction'
        if 'of' in text and 'at' in text:
            parts = text.split('of')
            crop = parts[1].split('at')[0].strip()
            location = parts[1].split('at')[1].strip()
            details['crop'] = crop
            details['location'] = location
        # Dummy soil parameters for demonstration
        details['soil'] = {'N': 90, 'P': 42, 'K': 43}
    
    return intent, details