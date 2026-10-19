import re

KEYWORDS_DB = {
    'water': {
        'category': 'Water Supply & Sanitation',
        'department': 'Rural Water Supply & Sanitation Dept',
        'default_priority': 'High',
        'keywords': ['water', 'pipe', 'leak', 'drainage', 'borewell', 'tap', 'drinking', 'sewage', 'dirty', 'tank', 'drain']
    },
    'electricity': {
        'category': 'Electricity & Power',
        'department': 'State Electricity Distribution Board',
        'default_priority': 'High',
        'keywords': ['power', 'electricity', 'transformer', 'wire', 'light', 'current', 'outage', 'voltage', 'pole', 'blackout']
    },
    'road': {
        'category': 'Roads & Infrastructure',
        'department': 'Panchayat Raj Engineering Dept',
        'default_priority': 'Medium',
        'keywords': ['road', 'pothole', 'street', 'bridge', 'pavement', 'mud', 'path', 'construction']
    },
    'health': {
        'category': 'Public Health & Sanitation',
        'department': 'Health & Family Welfare Dept',
        'default_priority': 'Critical',
        'keywords': ['hospital', 'doctor', 'medicine', 'fever', 'disease', 'garbage', 'trash', 'waste', 'mosquito', 'dengue', 'clinic', 'dead', 'death', 'animal']
    },
    'agriculture': {
        'category': 'Agriculture & Farming',
        'department': 'Department of Agriculture',
        'default_priority': 'Medium',
        'keywords': ['crop', 'fertilizer', 'pesticide', 'irrigation', 'farmer', 'seeds', 'field', 'soil']
    }
}

CRITICAL_WORDS = [
    'dead', 'death', 'died', 'dying', 'kill', 'danger', 'emergency', 
    'accident', 'fire', 'critical', 'severe', 'immediate', 'hazard', 
    'broken wire', 'current wire','collapsed'
]

HIGH_WORDS = [
    'overflow', 'no water', 'blocked', 'outage', 'leak', 
    'contamination', 'sick', 'urgent', 'problem', 'not coming', 'days'
]

def predict(text):
    if not text or not isinstance(text, str):
        return ("General", "Medium", "Panchayat Raj", 60)

    text_lower = text.lower().strip()
    words = re.findall(r'\w+', text_lower)

    predicted_category = "General"
    predicted_dept = "Panchayat Raj"
    predicted_priority = "Medium"
    
    matches = 0

    # 1. Category and Department matching
    for group, data in KEYWORDS_DB.items():
        group_matches = [kw for kw in data['keywords'] if kw in text_lower]
        if group_matches:
            matches += len(group_matches)
            if predicted_category == "General":
                predicted_category = data['category']
                predicted_dept = data['department']
                predicted_priority = data['default_priority']

    # 2. Priority Escalation
    is_critical = any(word in text_lower for word in CRITICAL_WORDS)
    if is_critical:
        predicted_priority = "Critical"
        matches += 2
    else:
        is_high = any(word in text_lower for word in HIGH_WORDS)
        if is_high and predicted_priority != "Critical":
            predicted_priority = "High"
            matches += 1

    # 3. Calculate Confidence Score (range 65% to 98%)
    base_confidence = 65
    if len(words) > 0:
        calculated_confidence = base_confidence + (matches * 10) + min(len(words), 8)
        confidence = min(calculated_confidence, 98)
    else:
        confidence = 60

    return (predicted_category, predicted_priority, predicted_dept, confidence)