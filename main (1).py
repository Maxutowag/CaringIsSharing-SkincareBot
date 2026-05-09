import nest_asyncio
nest_asyncio.apply()
import json, os, logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from survey import get_keyboard, get_question_text, is_last_question, is_multi_select, QUESTIONS
from recommender import build_routine
from database import save_routine, get_routine

BOT_TOKEN = "8638382652:AAHhc0qR2__xGFgOhup3BLd4IEqLmh5AXNk"
WHATSAPP_NUMBER = "77055130486"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["answers"] = {}
    context.user_data["q"] = 0
    context.user_data["multi_selected"] = []
    await update.message.reply_text(
    "👋 Hi! I will create a personalized skincare routine just for you. Let's go! 🚀\n\n"
    "📌 Available commands:\n"
    "/start — Take the survey\n"
    "/myroutine — View your saved routine\n"
    "/ingredient [name] — Learn about an ingredient\n"
    "   Example: /ingredient niacinamide\n"
    "/sos — Quick help for skin emergencies 🆘"
)
    await update.message.reply_text(get_question_text(0), reply_markup=get_keyboard(0))

async def my_routine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    saved = get_routine(update.effective_user.id)
    if saved:
        await update.message.reply_text("📋 Your saved routine:\n\n" + saved["routine"])
    else:
        await update.message.reply_text("No routine saved yet. Take the survey: /start")

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy_yes":
        url = f"https://wa.me/{WHATSAPP_NUMBER}?text=Hi!+I+want+to+order+my+skincare+routine"
        await query.message.reply_text(f"🛍 Amazing! Contact us on WhatsApp:\n{url}")
        return
    elif query.data == "buy_maybe":
        await query.message.reply_text("🤔 No worries! Your routine is saved. Come back anytime — /myroutine 💾")
        return
    elif query.data == "buy_no":
        await query.message.reply_text("👌 Routine saved. Come back whenever you're ready! 😊")
        return

    try:
        _, q_str, answer = query.data.split("_", 2)
        q = int(q_str)
    except Exception:
        return

    if q != context.user_data.get("q", 0):
        return

    if is_multi_select(q):
        if answer == "DONE":
            selected = context.user_data.get("multi_selected", [])
            if not selected:
                selected = ["None"]
            context.user_data["answers"][QUESTIONS[q]["key"]] = ", ".join(selected)
            await query.edit_message_text(f"✅ {get_question_text(q)}\n→ {', '.join(selected)}")
            context.user_data["multi_selected"] = []
            next_q = q + 1
            context.user_data["q"] = next_q
            if is_last_question(q):
                await finish(query, context)
            else:
                await query.message.reply_text(get_question_text(next_q), reply_markup=get_keyboard(next_q))
        else:
            selected = context.user_data.get("multi_selected", [])
            if answer in selected:
                selected.remove(answer)
            else:
                selected.append(answer)
            context.user_data["multi_selected"] = selected
            try:
                await query.edit_message_reply_markup(reply_markup=get_keyboard(q, selected))
            except Exception:
                pass
        return

    context.user_data["answers"][QUESTIONS[q]["key"]] = answer
    await query.edit_message_text(f"✅ {get_question_text(q)}\n→ {answer}")
    next_q = q + 1
    context.user_data["q"] = next_q

    if is_last_question(q):
        await finish(query, context)
    else:
        await query.message.reply_text(get_question_text(next_q), reply_markup=get_keyboard(next_q))

async def finish(query, context):
    routine = build_routine(context.user_data["answers"])
    save_routine(query.from_user.id, context.user_data["answers"], routine)
    await query.message.reply_text("🎉 Your personalized skincare routine:\n\n" + routine)
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Ready to buy!", callback_data="buy_yes")],
        [InlineKeyboardButton("🤔 I'll think about it", callback_data="buy_maybe")],
        [InlineKeyboardButton("❌ Not right now", callback_data="buy_no")]
    ])
    await query.message.reply_text("🛒 Would you like to order these products?", reply_markup=keyboard)

async def error_handler(update, context):
    logging.error(f"Error: {context.error}")

INGREDIENTS = {
    "niacinamide": "💊 Niacinamide (Vitamin B3)\n✅ Minimizes pores, brightens skin, reduces redness\n⚠️ Don't mix with: Vitamin C (use at different times)\n👍 Good for: oily, combination, acne-prone skin",
    "retinol": "💊 Retinol (Vitamin A)\n✅ Reduces wrinkles, boosts collagen, fights acne\n⚠️ Don't mix with: AHA/BHA, Vitamin C\n👍 Good for: aging, acne, pigmentation\n🌙 Use only at night!",
    "vitamin c": "💊 Vitamin C (Ascorbic Acid)\n✅ Brightens, fades dark spots, antioxidant\n⚠️ Don't mix with: Retinol, Niacinamide\n👍 Good for: dull skin, pigmentation\n☀️ Use in the morning!",
    "hyaluronic acid": "💊 Hyaluronic Acid\n✅ Deep hydration, plumps skin, holds moisture\n⚠️ Apply on damp skin for best results\n👍 Good for: all skin types especially dry",
    "salicylic acid": "💊 Salicylic Acid (BHA)\n✅ Unclogs pores, fights acne, exfoliates\n⚠️ Don't mix with: Retinol\n👍 Good for: oily, acne-prone, large pores\n🌙 Use 2-3x per week",
    "glycolic acid": "💊 Glycolic Acid (AHA)\n✅ Exfoliates dead skin, brightens, smooths texture\n⚠️ Don't mix with: Retinol, Vitamin C\n👍 Good for: dull skin, uneven texture\n🌙 Use 2-3x per week at night",
    "ceramides": "💊 Ceramides\n✅ Restores skin barrier, locks in moisture\n⚠️ Safe to mix with everything!\n👍 Good for: dry, sensitive, damaged skin",
    "spf": "💊 SPF (Sunscreen)\n✅ Protects from UV damage, prevents aging & pigmentation\n⚠️ Must reapply every 2 hours outdoors\n👍 Good for: everyone, every single day! ☀️",
    "peptides": "💊 Peptides\n✅ Boosts collagen, firms skin, reduces wrinkles\n⚠️ Safe to mix with most ingredients\n👍 Good for: aging skin, loss of elasticity",
    "azelaic acid": "💊 Azelaic Acid\n✅ Fades dark spots, fights acne, reduces redness\n⚠️ Safe to mix with most ingredients\n👍 Good for: rosacea, pigmentation, acne",
    "squalane": "💊 Squalane\n✅ Deep moisturizing, anti-aging, non-comedogenic\n⚠️ Safe to mix with everything!\n👍 Good for: all skin types especially dry & sensitive",
    "zinc": "💊 Zinc\n✅ Controls oil, fights acne, soothes inflammation\n⚠️ Safe to mix with most ingredients\n👍 Good for: oily, acne-prone skin"
}

async def ingredient(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Niacinamide", callback_data="ing_niacinamide"),
         InlineKeyboardButton("Retinol", callback_data="ing_retinol")],
        [InlineKeyboardButton("Vitamin C", callback_data="ing_vitamin c"),
         InlineKeyboardButton("Hyaluronic Acid", callback_data="ing_hyaluronic acid")],
        [InlineKeyboardButton("Salicylic Acid", callback_data="ing_salicylic acid"),
         InlineKeyboardButton("Glycolic Acid", callback_data="ing_glycolic acid")],
        [InlineKeyboardButton("Ceramides", callback_data="ing_ceramides"),
         InlineKeyboardButton("Peptides", callback_data="ing_peptides")],
        [InlineKeyboardButton("Azelaic Acid", callback_data="ing_azelaic acid"),
         InlineKeyboardButton("Squalane", callback_data="ing_squalane")],
        [InlineKeyboardButton("SPF", callback_data="ing_spf"),
         InlineKeyboardButton("Zinc", callback_data="ing_zinc")]
    ])
    await update.message.reply_text("🔍 Choose an ingredient to learn about:", reply_markup=keyboard)

async def handle_ingredient(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    name = query.data.replace("ing_", "")
    info = INGREDIENTS.get(name)
    if info:
        await query.message.reply_text(info)
    else:
        await query.message.reply_text("❌ Not found.")

async def sos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔴 Pimple before an event", callback_data="sos_pimple")],
        [InlineKeyboardButton("🔥 Skin is red & irritated", callback_data="sos_redness")],
        [InlineKeyboardButton("🏜️ Skin is very dry & flaky", callback_data="sos_dry")],
        [InlineKeyboardButton("💧 Oily & shiny skin", callback_data="sos_oily")],
        [InlineKeyboardButton("😖 Breakout all over face", callback_data="sos_breakout")],
        [InlineKeyboardButton("🌞 Sunburn", callback_data="sos_sunburn")]
    ])
    await update.message.reply_text("🆘 What's your skin emergency?", reply_markup=keyboard)

SOS_ANSWERS = {
    "sos_pimple": (
        "🔴 Pimple before an event:\n\n"
        "1. DON'T squeeze it!\n"
        "2. Apply ice wrapped in cloth for 2 min\n"
        "3. Dab salicylic acid or tea tree oil\n"
        "4. Use a pimple patch overnight\n"
        "5. In the morning — green color corrector under foundation\n\n"
        "⏱ Reduces size in 4-6 hours!"
    ),
    "sos_redness": (
        "🔥 Red & irritated skin:\n\n"
        "1. Stop all actives (acids, retinol) TODAY\n"
        "2. Apply cold aloe vera gel\n"
        "3. Use only gentle cleanser + thick moisturizer\n"
        "4. Avoid hot water when washing face\n"
        "5. No makeup until skin calms down\n\n"
        "⏱ Should calm in 24-48 hours"
    ),
    "sos_dry": (
        "🏜️ Very dry & flaky skin:\n\n"
        "1. Don't exfoliate — it will make it worse!\n"
        "2. Apply hyaluronic acid on damp skin\n"
        "3. Layer a thick cream on top immediately\n"
        "4. Use face oil as last step (squalane, rosehip)\n"
        "5. Drink more water today 💧\n\n"
        "⏱ Visible improvement in a few hours!"
    ),
    "sos_oily": (
        "💧 Oily & shiny skin:\n\n"
        "1. Don't over-wash — it makes more oil!\n"
        "2. Use blotting papers during the day\n"
        "3. Apply niacinamide serum in the morning\n"
        "4. Switch to gel moisturizer (no heavy creams)\n"
        "5. Use mattifying SPF\n\n"
        "💡 Tip: oily skin is often dehydrated — hydrate more!"
    ),
    "sos_breakout": (
        "😖 Breakout all over face:\n\n"
        "1. Check if you changed any product recently — stop it!\n"
        "2. Clean your phone screen & pillowcase today\n"
        "3. Use gentle cleanser only — no harsh scrubs\n"
        "4. Apply niacinamide serum all over face\n"
        "5. Don't touch your face!\n"
        "6. Drink water, reduce sugar & dairy for 3 days\n\n"
        "⏱ Give it 3-5 days to calm down"
    ),
    "sos_sunburn": (
        "🌞 Sunburn:\n\n"
        "1. Cool the skin — cold (not ice) water or cloth\n"
        "2. Apply pure aloe vera gel generously\n"
        "3. Use fragrance-free gentle moisturizer\n"
        "4. NO acids, retinol or actives for 1 week!\n"
        "5. Stay out of sun until fully healed\n"
        "6. Take ibuprofen if painful\n\n"
        "⚠️ If blistering — see a doctor!"
    )
}

async def handle_sos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    answer = SOS_ANSWERS.get(query.data)
    if answer:
        await query.message.reply_text(answer)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("myroutine", my_routine))
app.add_handler(CommandHandler("ingredient", ingredient))
app.add_handler(CallbackQueryHandler(handle_ingredient, pattern=r"^ing_"))
app.add_handler(CommandHandler("sos", sos))
app.add_handler(CallbackQueryHandler(handle_sos, pattern=r"^sos_"))
app.add_handler(CallbackQueryHandler(handle_answer, pattern=r"^ans_"))
app.add_handler(CallbackQueryHandler(handle_answer, pattern=r"^buy_"))
app.add_error_handler(error_handler)
app.run_polling()
