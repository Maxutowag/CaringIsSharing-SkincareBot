# Skincare Bot by Caring is Sharing

A Telegram bot that asks 11 questions about your skin and generates a personalized skincare routine.

## Features
- 11-step inline survey
- Personalized morning and evening routines
- Products across 3 budget tiers (Budget / Mid-range / Premium)
- Prices in KZT for every product + total cost
- Save and retrieve routine with /myroutine
- Ingredient encyclopedia with /ingredient
- SOS emergency skin help with /sos
- WhatsApp order button at the end of survey

## Project Structure
- main.py — Bot entry point, all handlers
- survey.py — Survey questions and inline keyboards
- recommender.py — Routine building logic and products
- database.py — JSON-based data persistence
- README.md — This file

## How to Run
1. Open Google Colab: colab.research.google.com
2. Install dependencies: pip install python-telegram-bot==20.7 nest_asyncio
3. Add your bot token in main.py
4. Run: python main.py

## Commands
- /start — Take the 11-step skin survey
- /myroutine — View your saved routine
- /ingredient — Learn about skincare ingredients
- /sos — Emergency skin help

## Budget Tiers
- Budget: 7,000 - 9,000 KZT per product
- Mid-range: 15,000 - 20,000 KZT per product
- Premium: 60,000 - 120,000 KZT per product

## Team
Caring is Sharing
| Name | Module |
| Demegen Amina  |
| Maxutova Gulden|
| Rakhman Aidana|
| Talap Akbota |
