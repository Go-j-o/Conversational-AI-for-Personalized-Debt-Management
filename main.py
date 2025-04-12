from financial_advisor_bot_fixed import FinancialAdvisorBot

# Create a bot instance
bot = FinancialAdvisorBot()
print(bot.start_conversation())  # 👈 this sends the initial greeting
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Bot: Goodbye! 👋 Stay financially smart.")
        break
    response = bot.respond(user_input)
    print("Bot:", response)