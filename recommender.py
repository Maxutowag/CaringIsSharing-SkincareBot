PRODUCTS = {
    "Budget": {
        "cleanser": ("CeraVe Foaming Cleanser", 7500),
        "toner": ("Pyunkang Yul Toner", 7000),
        "serum": ("The Ordinary Niacinamide 10%", 7500),
        "moisturizer": ("Neutrogena Hydro Boost", 8000),
        "spf": ("Garnier Ambre Solaire SPF50", 7500),
        "oil_cleanser": ("Garnier Micellar Water", 7000),
        "exfoliant": ("The Ordinary AHA+BHA", 8000),
        "retinol": ("The Ordinary Retinol 0.5%", 7500)
    },
    "Mid-range": {
        "cleanser": ("La Roche-Posay Toleriane", 15000),
        "toner": ("Paula's Choice Toner", 16000),
        "serum": ("Paula's Choice Niacinamide", 17000),
        "moisturizer": ("Kiehl's Ultra Facial Cream", 19000),
        "spf": ("La Roche-Posay Anthelios", 16000),
        "oil_cleanser": ("Clinique Take The Day Off", 18000),
        "exfoliant": ("Paula's Choice BHA Liquid", 17000),
        "retinol": ("RoC Retinol Correxion", 15000)
    },
    "Premium": {
        "cleanser": ("Tatcha The Rice Wash", 65000),
        "toner": ("SK-II Facial Treatment Essence", 95000),
        "serum": ("Skinceuticals C E Ferulic", 110000),
        "moisturizer": ("La Mer Creme de la Mer", 120000),
        "spf": ("Supergoop! Unseen Sunscreen SPF40", 70000),
        "oil_cleanser": ("Shu Uemura Cleansing Oil", 75000),
        "exfoliant": ("Drunk Elephant T.L.C. Framboos", 85000),
        "retinol": ("Drunk Elephant A-Passioni Retinol", 90000)
    }
}

def build_routine(answers):
    budget = answers.get("budget", "Budget")
    p = PRODUCTS.get(budget, PRODUCTS["Budget"])
    allergy = answers.get("allergies", "None")

    morning_items = [
        ("Cleanser", p['cleanser']),
        ("Toner", p['toner']),
        ("Serum", p['serum']),
        ("Moisturizer", p['moisturizer']),
        ("SPF", p['spf'])
    ]

    retinol = p['retinol'] if allergy != "Retinol" else ("Niacinamide Serum (retinol excluded)", 0)
    evening_items = [
        ("Makeup remover", p['oil_cleanser']),
        ("Cleanser", p['cleanser']),
        ("Exfoliant (2-3x/week)", p['exfoliant']),
        ("Actives", retinol),
        ("Moisturizer", p['moisturizer'])
    ]

    morning_text = ""
    for i, (step, (name, price)) in enumerate(morning_items, 1):
        morning_text += f"{i}️⃣ {step}: {name} — {price:,} KZT\n"

    evening_text = ""
    for i, (step, (name, price)) in enumerate(evening_items, 1):
        evening_text += f"{i}️⃣ {step}: {name} — {price:,} KZT\n"

    seen = set()
    unique_items = []
    total = 0
    for _, (name, price) in morning_items + evening_items:
        if name not in seen:
            seen.add(name)
            unique_items.append((name, price))
            total += price

    products_list = "\n".join([f"• {name} — {price:,} KZT" for name, price in unique_items])

    routine = (
        f"☀️ MORNING ROUTINE:\n{morning_text}\n"
        f"🌙 EVENING ROUTINE:\n{evening_text}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🛒 All products & prices:\n{products_list}\n\n"
        f"💰 Total: ~{total:,} KZT"
    )
    return routine
