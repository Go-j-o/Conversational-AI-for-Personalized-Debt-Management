
import re

class FinancialAdvisorBot:
    def __init__(self):
        self.debts = []
        self.monthly_income = None
        self.monthly_expenses = []
        self.goals = []
        self.state = 'greeting'

    def start_conversation(self):
        return "Hello! I'm your Financial Advisor Bot 🤖. Tell me about your income, expenses, savings, debt, and financial goals!"

    def respond(self, user_input):
        user_input = user_input.lower()

        if self.state == 'greeting':
            self.state = 'collecting_income'
            return "Got it. Can you tell me your monthly income after taxes?"

        elif self.state == 'collecting_income':
            try:
                self.income = float(re.sub(r'[^\d.]', '', user_input))
                self.state = 'collecting_expenses'
                return "Thanks! What are your total monthly expenses?"
            except ValueError:
                return "Please enter a valid income amount."

        elif self.state == 'collecting_expenses':
            try:
                self.expenses = float(re.sub(r'[^\d.]', '', user_input))
                self.state = 'collecting_savings'
                return "Good. How much do you currently have in savings?"
            except ValueError:
                return "Please enter a valid expenses amount."

        elif self.state == 'collecting_savings':
            try:
                self.savings = float(re.sub(r'[^\d.]', '', user_input))
                self.state = 'collecting_debt'
                return "Okay. How much total debt do you have?"
            except ValueError:
                return "Please enter a valid savings amount."

        elif self.state == 'collecting_debt':
            try:
                self.debt = float(re.sub(r'[^\d.]', '', user_input))
                self.state = 'collecting_goals'
                return "Understood. Finally, could you list your financial goals separated by commas?"
            except ValueError:
                return "Please enter a valid debt amount."

        elif self.state == 'collecting_goals':
            self.financial_goals = [goal.strip() for goal in user_input.split(',')]
            self.state = 'providing_advice'
            return self.provide_advice()

        elif self.state == 'providing_advice':
            return "I've already given you the advice. Restart the program if you'd like to go again."

        else:
            return "Sorry, I didn't understand that."

    def provide_advice(self):
        disposable_income = self.income - self.expenses
        advice = f"\nAlright — here’s your financial snapshot:\n"
        advice += f"- Income: ₹{self.income}\n"
        advice += f"- Expenses: ₹{self.expenses}\n"
        advice += f"- Savings: ₹{self.savings}\n"
        advice += f"- Debt: ₹{self.debt}\n"
        advice += f"- Disposable Income: ₹{disposable_income}\n\n"

        if disposable_income > 0:
            months_to_clear_debt = self.debt / disposable_income if self.debt else 0
            advice += f"✅ With your current disposable income, you could be debt-free in {months_to_clear_debt:.1f} months.\n"
        else:
            advice += "⚠️ You have no disposable income. Consider reducing expenses or increasing income.\n"

        if self.financial_goals:
            advice += "\nYour financial goals:\n"
            for goal in self.financial_goals:
                advice += f"- {goal}\n"

        return advice
