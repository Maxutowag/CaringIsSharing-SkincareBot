from telegram import InlineKeyboardButton, InlineKeyboardMarkup

QUESTIONS = [
    {"key": "skin_type", "text": "💧 Step 1/11: What is your skin type?", "options": ["Dry", "Oily", "Combination", "Normal", "Sensitive"]},
    {"key": "problems", "text": "🔍 Step 2/11: Main skin concern?", "options": ["Acne/Post-acne", "Wrinkles", "Pigmentation", "Large pores", "Dryness", "Dull complexion"]},
    {"key": "age", "text": "🎂 Step 3/11: Your age?", "options": ["Under 20", "20-30", "30-40", "40+"]},
    {"key": "budget", "text": "💰 Step 4/11: Your budget?", "options": ["Budget", "Mid-range", "Premium"]},
    {"key": "allergies", "text": "⚠️ Step 5/11: Any ingredient allergies?", "options": ["None", "Retinol", "Acids", "Fragrances", "Not sure"]},
    {"key": "climate", "text": "🌍 Step 6/11: Your climate?", "options": ["Dry", "Humid", "Moderate", "Cold"]},
    {"key": "current_products", "text": "🧴 Step 7/11: What do you already use?", "options": ["Nothing", "Cleanser", "Cleanser+moisturizer", "Cleanser+toner+cream", "Cleanser+toner+serum", "Enzyme+toner+serum", "Full routine"]},
    {"key": "sun_exposure", "text": "☀️ Step 8/11: How often are you in the sun?", "options": ["Rarely (indoors)", "Sometimes", "Often outside", "Very often"]},
    {"key": "sleep_stress", "text": "💤 Step 9/11: Sleep & stress?", "options": ["Sleep well, low stress", "Occasionally tired", "Chronic sleep deprivation", "High stress"]},
    {"key": "vitamins", "text": "💊 Step 10/11: Do you take vitamins? (pick multiple, then ✅ Done)", "options": ["None", "Vitamin C", "Vitamin D", "Vitamin E", "Omega-3", "Collagen", "Biotin", "Zinc", "Iron", "Magnesium", "✅ Done"]},
    {"key": "wash_frequency", "text": "🚿 Step 11/11: How often do you cleanse?", "options": ["Once a day", "Morning & evening", "Evening only", "Rarely"]}
]

MULTI_SELECT_QUESTIONS = {"vitamins"}

def get_keyboard(i, selected=None):
    options = QUESTIONS[i]["options"]
    keyboard = []
    for opt in options:
        if opt == "✅ Done":
            keyboard.append([InlineKeyboardButton("✅ Done", callback_data=f"ans_{i}_DONE")])
        else:
            mark = "☑️ " if selected and opt in selected else ""
            keyboard.append([InlineKeyboardButton(f"{mark}{opt}", callback_data=f"ans_{i}_{opt}")])
    return InlineKeyboardMarkup(keyboard)

def get_question_text(i):
    return QUESTIONS[i]["text"]

def is_last_question(i):
    return i >= len(QUESTIONS) - 1

def is_multi_select(i):
    return QUESTIONS[i]["key"] in MULTI_SELECT_QUESTIONS
