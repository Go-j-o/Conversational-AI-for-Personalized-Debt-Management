import re

class FinancialAdvisorBot:
    def __init__(self):
        self.income = 0
        self.expenses = 0
        self.savings = 0
        self.debt = 0
        self.financial_goals = []
        self.state = 'greeting'


    def start_conversation(self):
        return "Hello! I'm your Financial Advisor Bot 🤖. I can help you manage your finances better. Tell me about your income, expenses, savings, debt, and financial goals!"

    # Main function to process user input and generate response
    def process_message(self, user_message):
        # Convert message to lowercase for easier processing
        message = user_message.lower()
        
        # Update conversation state based on user input
        self.update_state_based_on_input(message)
        
        # Generate appropriate response based on current state
        return self.generate_response()

    # Analyze user input to extract financial information
    def update_state_based_on_input(self, message):
        # Check for debt information
        if any(term in message for term in ['debt', 'loan', 'credit card']):
            self.extract_debt_information(message)
        
        # Check for income information
        if any(term in message for term in ['income', 'salary', 'earn']):
            self.extract_income_information(message)
        
        # Check for expense information
        if any(term in message for term in ['spend', 'expense', 'rent', 'food', 'transportation']):
            self.extract_expense_information(message)
        
        # Check for goals
        if any(term in message for term in ['goal', 'want to', 'debt free', 'saving', 'home']):
            self.extract_goals(message)
        
        # Check for refinancing questions
        if any(term in message for term in ['refinance', 'refinancing']):
            self.conversation_state = 'refinancing'
        
        # Update conversation flow based on what information we have
        self.update_conversation_state()

    # Extract debt information from user message
    def extract_debt_information(self, message):
        # Clear existing debts if this is first debt entry
        if len(self.debts) == 0:
            self.debts = []
        
        # Extract credit card debt
        credit_card_match = re.search(r'credit card.+?(?:rs\.?|₹)\s*([0-9,]+).*?(\d+(?:\.\d+)?)(?:\s*%)', message, re.IGNORECASE)
        if credit_card_match:
            amount = float(credit_card_match.group(1).replace(',', ''))
            interest_rate = float(credit_card_match.group(2))
            self.debts.append({
                'type': 'Credit Card',
                'amount': amount,
                'interest_rate': interest_rate
            })
        
        # Extract personal loan
        personal_loan_match = re.search(r'personal loan.+?(?:rs\.?|₹)\s*([0-9,]+).*?(\d+(?:\.\d+)?)(?:\s*%)', message, re.IGNORECASE)
        if personal_loan_match:
            amount = float(personal_loan_match.group(1).replace(',', ''))
            interest_rate = float(personal_loan_match.group(2))
            self.debts.append({
                'type': 'Personal Loan',
                'amount': amount,
                'interest_rate': interest_rate
            })

    # Extract income information from user message
    def extract_income_information(self, message):
        if self.monthly_income is not None:
            return  # Skip if already set

        # Check for a proper income statement
        income_match = re.search(r'(?:income|salary|earn(?:ing)?(?:s)?)\D*(?:rs\.?|₹)\s*([0-9,]+)', message, re.IGNORECASE)
        if income_match:
            self.monthly_income = float(income_match.group(1).replace(',', ''))


    # Extract expense information from user message
    def extract_expense_information(self, message):
        # Clear existing expenses if this is first expense entry
        if len(self.monthly_expenses) == 0:
            self.monthly_expenses = []
        
        # Extract rent expense
        rent_match = re.search(r'rent.+?(?:rs\.?|₹)\s*([0-9,]+)', message, re.IGNORECASE)
        if rent_match:
            amount = float(rent_match.group(1).replace(',', ''))
            self.monthly_expenses.append({
                'category': 'Rent',
                'amount': amount
            })
        
        # Extract food expense
        food_match = re.search(r'food.+?(?:rs\.?|₹)\s*([0-9,]+)', message, re.IGNORECASE)
        if food_match:
            amount = float(food_match.group(1).replace(',', ''))
            self.monthly_expenses.append({
                'category': 'Food',
                'amount': amount
            })
        
        # Extract transportation expense
        transport_match = re.search(r'transportation.+?(?:rs\.?|₹)\s*([0-9,]+)', message, re.IGNORECASE)
        if transport_match:
            amount = float(transport_match.group(1).replace(',', ''))
            self.monthly_expenses.append({
                'category': 'Transportation',
                'amount': amount
            })
        
        # Extract other expenses
        other_match = re.search(r'other expenses.+?(?:rs\.?|₹)\s*([0-9,]+)', message, re.IGNORECASE)
        if other_match:
            amount = float(other_match.group(1).replace(',', ''))
            self.monthly_expenses.append({
                'category': 'Other',
                'amount': amount
            })

    # Extract financial goals from user message
    def extract_goals(self, message):
        if 'debt free' in message:
            # Extract timeframe for becoming debt free
            year_match = re.search(r'(\d+)\s*years?', message, re.IGNORECASE)
            if year_match:
                years = int(year_match.group(1))
                self.goals.append({
                    'type': 'Debt Free',
                    'timeframe': years
                })
        
        if 'home' in message or 'house' in message:
            self.goals.append({
                'type': 'Home Purchase',
                'description': 'Saving for a home'
            })

    # Update conversation state based on available information
    def update_conversation_state(self):
        if self.conversation_state == 'greeting':
            self.conversation_state = 'collecting_debt'
            return
        
        if len(self.debts) > 0 and not self.monthly_income and self.conversation_state == 'collecting_debt':
            self.conversation_state = 'collecting_income'
            return
        
        if self.monthly_income and len(self.monthly_expenses) == 0 and self.conversation_state == 'collecting_income':
            self.conversation_state = 'collecting_expenses'
            return
        
        if len(self.monthly_expenses) > 0 and len(self.goals) == 0 and self.conversation_state == 'collecting_expenses':
            self.conversation_state = 'collecting_goals'
            return
        
        if len(self.goals) > 0 and self.conversation_state == 'collecting_goals':
            self.conversation_state = 'providing_analysis'
            return

    # Calculate total debt amount
    def calculate_total_debt(self):
        return sum(debt['amount'] for debt in self.debts)

    # Calculate weighted average interest rate
    def calculate_average_interest_rate(self):
        total_debt = self.calculate_total_debt()
        if total_debt == 0:
            return 0
        
        weighted_sum = sum(debt['amount'] * debt['interest_rate'] for debt in self.debts)
        
        return weighted_sum / total_debt

    # Calculate total monthly expenses
    def calculate_total_monthly_expenses(self):
        return sum(expense['amount'] for expense in self.monthly_expenses)

    # Calculate debt-to-income ratio
    def calculate_debt_to_income_ratio(self):
        if not self.monthly_income or self.monthly_income == 0:
            return 0
        return self.calculate_total_debt() / (self.monthly_income * 12)

    # Calculate monthly amount available for debt repayment
    def calculate_available_for_debt_repayment(self):
        total_expenses = self.calculate_total_monthly_expenses()
        return self.monthly_income - total_expenses

    # Calculate time to debt free (in months) based on avalanche method
    def calculate_time_to_debt_free(self):
        available_for_debt = self.calculate_available_for_debt_repayment()
        if available_for_debt <= 0:
            return float('inf')
        
        # Sort debts by interest rate (highest first)
        sorted_debts = sorted(self.debts, key=lambda x: x['interest_rate'], reverse=True)
        
        months = 0
        remaining_debts = [{**debt} for debt in sorted_debts]  # Create deep copy
        
        # Simple simulation of debt repayment
        while remaining_debts and months < 1000:  # Cap at 1000 months to prevent infinite loop
            months += 1
            payment_remaining = available_for_debt
            
            # Make minimum payments (assume 2% of balance)
            for i in range(len(remaining_debts)):
                min_payment = min(remaining_debts[i]['amount'] * 0.02, payment_remaining)
                remaining_debts[i]['amount'] -= min_payment
                payment_remaining -= min_payment
            
            # Apply remaining payment to highest interest debt
            if payment_remaining > 0 and remaining_debts:
                remaining_debts[0]['amount'] -= payment_remaining
            
            # Calculate interest (simplified)
            for i in range(len(remaining_debts)):
                remaining_debts[i]['amount'] *= (1 + (remaining_debts[i]['interest_rate'] / 100 / 12))
            
            # Remove paid off debts
            remaining_debts = [debt for debt in remaining_debts if debt['amount'] > 1]  # Consider <₹1 as paid off
        
        return months

    # Generate response based on conversation state
    def generate_response(self):
        if self.conversation_state == 'greeting':
            return "Hi there! I'm your Financial Advisor Bot. I can help you manage your debt and improve your financial health. How can I assist you today?"
        
        elif self.conversation_state == 'collecting_debt':
            return "Thank you for sharing. Could you please tell me your monthly income after taxes?"
        
        elif self.conversation_state == 'collecting_income':
            return f"Thank you. Your monthly income is ₹{self.monthly_income:,.2f}. Could you share your major monthly expenses (rent, food, transportation, etc.)?"
        
        elif self.conversation_state == 'collecting_expenses':
            return "Thank you for sharing your expenses. What are your financial goals? For example, when would you like to be debt-free or are you saving for something specific?"
        
        elif self.conversation_state == 'collecting_goals':
            return "Thanks for sharing your goals. Based on the information you've provided, I'll create a financial plan for you. Would you like to see your debt repayment strategy or explore refinancing options?"
        
        elif self.conversation_state == 'refinancing':
            return self.generate_refinancing_advice()
        
        elif self.conversation_state == 'providing_analysis':
            return self.generate_financial_analysis()
        
        else:
            return "I'm here to help with your financial questions. What would you like to know?"
        
def handle_message(self, message):
    self.update_conversation_state(message)
    
    # If expecting income and user sends a number — accept it
    if self.conversation_state == 'collecting_income':
        income_value = re.search(r'([0-9,]+)', message)
        if income_value:
            self.monthly_income = float(income_value.group(1).replace(',', ''))
            self.conversation_state = 'collecting_expenses'
            return "Got it. Could you now share your monthly expenses?"
        else:
            return "Please provide your monthly income in numbers."

    # Now handle other states normally...
    self.extract_debt_information(message)
    self.extract_income_information(message)
    self.extract_expense_information(message)
    self.extract_savings_information(message)
    self.extract_goal_information(message)
    
    self.update_conversation_state(message)
    return self.generate_response()


    # Generate comprehensive financial analysis
def generate_financial_analysis(self):
        total_debt = self.calculate_total_debt()
        available_for_debt = self.calculate_available_for_debt_repayment()
        debt_to_income_ratio = self.calculate_debt_to_income_ratio()
        avg_interest_rate = self.calculate_average_interest_rate()
        time_to_debt_free = self.calculate_time_to_debt_free()
        total_expenses = self.calculate_total_monthly_expenses()
        
        sorted_debts = sorted(self.debts, key=lambda d: d['interest_rate'], reverse=True)
        
        analysis = f"""📊 **Your Financial Overview** 📊
        
🔸 Total Debt: ₹{total_debt:,.2f}
🔸 Average Interest Rate: {avg_interest_rate:.2f}%
🔸 Monthly Income: ₹{self.monthly_income:,.2f}
🔸 Total Monthly Expenses: ₹{total_expenses:,.2f}
🔸 Monthly Available for Debt Repayment: ₹{available_for_debt:,.2f}
🔸 Debt-to-Income Ratio: {debt_to_income_ratio:.2%}
🔸 Estimated Time to Become Debt-Free (using Avalanche Method): {int(time_to_debt_free)} months (~{int(time_to_debt_free / 12)} years)

🔹 **Debt Breakdown (Sorted by Interest Rate):**
"""
        for debt in sorted_debts:
            analysis += f"   - {debt['type']}: ₹{debt['amount']:,.2f} at {debt['interest_rate']}%\n"

        if time_to_debt_free == float('inf'):
            analysis += "\n⚠️ Warning: Your current income may not be sufficient to cover both expenses and debt repayments."
        
        analysis += "\n\nWould you like a more detailed monthly payment plan or suggestions on refinancing options?"

        return analysis

    # Generate advice on refinancing options
def generate_refinancing_advice(self):
        high_interest_debts = [debt for debt in self.debts if debt['interest_rate'] > 12]
        total_debt = self.calculate_total_debt()
        debt_to_income_ratio = self.calculate_debt_to_income_ratio()
        
        response = "# Refinancing Options\n\n"
        
        if high_interest_debts:
            response += "Based on your debt profile, you could benefit from refinancing these high-interest debts:\n"
            for debt in high_interest_debts:
                response += f"- {debt['type']}: ₹{debt['amount']:,.2f} at {debt['interest_rate']}% interest\n"
            response += "\n"
        else:
            response += "Your current interest rates are relatively competitive, but you might still benefit from consolidation for simplicity.\n\n"
        
        # Potential options based on debt-to-income ratio
        response += "## Potential Refinancing Options\n"
        
        if debt_to_income_ratio < 0.4:
            response += f"With your debt-to-income ratio of {debt_to_income_ratio * 100:.1f}%, you likely qualify for these options:\n\n"
            
            response += "### 1. Personal Loan Consolidation\n"
            response += "- Potential Interest Rate: 10-12%\n"
            response += "- Best for: Combining all debts into one payment\n"
            response += "- Pros: Single payment, fixed timeline\n"
            response += "- Cons: Might require collateral for large amounts\n\n"
            
            response += "### 2. Balance Transfer Credit Card\n"
            response += "- Potential Interest Rate: 0% introductory (12-18 months), then 14-18%\n"
            response += "- Best for: Credit card debt\n"
            response += "- Pros: Interest-free period to make significant progress\n"
            response += "- Cons: Transfer fees, high interest after promotional period\n\n"
        elif debt_to_income_ratio < 0.6:
            response += f"With your debt-to-income ratio of {debt_to_income_ratio * 100:.1f}%, you may qualify for these options with a good credit score:\n\n"
            
            response += "### 1. Secured Personal Loan\n"
            response += "- Potential Interest Rate: 11-14%\n"
            response += "- Best for: Combining debts with collateral available\n"
            response += "- Pros: Lower rates than unsecured options\n"
            response += "- Cons: Risk to collateral if unable to pay\n\n"
        else:
            response += f"With your debt-to-income ratio of {debt_to_income_ratio * 100:.1f}%, traditional refinancing might be challenging. Consider these options:\n\n"
            
            response += "### 1. Credit Counseling\n"
            response += "- Many non-profit organizations can negotiate with creditors on your behalf\n"
            response += "- May help reduce interest rates and fees\n\n"
            
            response += "### 2. Debt Management Plan\n"
            response += "- Structured repayment plan through a counseling agency\n"
            response += "- Could reduce interest rates and waive fees\n\n"
        
        # Steps to take
        response += "## Steps to Explore Refinancing\n"
        response += "1. Check your credit score - this will determine your refinancing options\n"
        response += "2. Research specific lenders and their current rates\n"
        response += "3. Calculate the total cost of each option (including fees)\n"
        response += "4. Apply to multiple lenders within a 14-day period to minimize credit score impact\n"
        response += "5. Compare offers carefully before accepting\n\n"
        
        response += "Would you like me to calculate potential savings from refinancing based on specific interest rate offers?"
        
        return response


# Example usage:
# bot = FinancialAdvisorBot()
# response = bot.process_message("I have a credit card debt of Rs. 250,000 with 18% interest, and a personal loan of Rs. 500,000 with 12% interest.")
# print(response)