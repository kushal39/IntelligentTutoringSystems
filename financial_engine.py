from rdflib import Graph, URIRef, Literal

class FinancialEngine:
    def __init__(self, income, expenses, debt, investment, goal_amount, credit_score, debt_repayment_strategy, investment_strategy):
        self.graph = Graph()
        self.graph.parse("data/personalFinance.owl")  # Load the ontology
        self.income = income
        self.expenses = expenses
        self.savings = income - expenses
        self.debt = debt
        self.investment = investment
        self.goal_amount = goal_amount
        self.credit_score = credit_score
        self.debt_repayment_strategy = debt_repayment_strategy
        self.investment_strategy = investment_strategy

    def create_user_data(self):
        user_uri = URIRef("http://example.org/user1")

        # Add user's financial data to the RDF graph
        self.graph.add((user_uri, URIRef("http://example.org/hasIncome"), Literal(self.income)))
        self.graph.add((user_uri, URIRef("http://example.org/hasExpense"), Literal(self.expenses)))
        self.graph.add((user_uri, URIRef("http://example.org/hasSavings"), Literal(self.savings)))
        self.graph.add((user_uri, URIRef("http://example.org/hasDebt"), Literal(self.debt)))
        self.graph.add((user_uri, URIRef("http://example.org/hasInvestment"), Literal(self.investment)))
        self.graph.add((user_uri, URIRef("http://example.org/hasFinancialGoal"), Literal(self.goal_amount)))
        self.graph.add((user_uri, URIRef("http://example.org/hasCreditScore"), Literal(self.credit_score)))
        self.graph.add((user_uri, URIRef("http://example.org/hasDebtRepaymentStrategy"), URIRef(self.debt_repayment_strategy)))
        self.graph.add((user_uri, URIRef("http://example.org/hasInvestmentStrategy"), URIRef(self.investment_strategy)))

    def calculate_savings_plan(self):
        # Calculate monthly savings
        monthly_savings = self.income - self.expenses

        # If no savings, return a message along with default or zero values
        if monthly_savings <= 0:
            return 0, "You need to reduce expenses or increase income to save money.", "", "", ""

        # Calculate time to reach goal (in months)
        time_to_goal = self.goal_amount / monthly_savings if monthly_savings > 0 else "Insufficient savings rate"

        # Personalized savings message based on monthly savings amount
        if monthly_savings > 1000:
            savings_message = "Great job! You're saving a significant amount each month. You could reach your financial goal sooner!"
        elif monthly_savings > 500:
            savings_message = "You are on track with a decent savings rate. Consider increasing savings for quicker goal achievement."
        else:
            savings_message = "Consider adjusting your budget to increase your savings rate."

        # Personalized debt repayment strategy
        debt_message = self.get_debt_strategy()

        # Personalized investment strategy
        investment_message = self.get_investment_strategy()

        # Return values as a consistent tuple
        return monthly_savings, time_to_goal, savings_message, debt_message, investment_message

    def get_debt_strategy(self):
        # Personalized debt repayment strategy
        if self.debt_repayment_strategy == "DebtAvalanche":
            return "With Debt Avalanche, focus on paying off high-interest debts first to save on interest in the long run."
        elif self.debt_repayment_strategy == "DebtSnowball":
            return "With Debt Snowball, focus on paying off your smallest debts first to build momentum and motivation."
        else:
            return "No debt repayment strategy selected. Consider using a strategy like Debt Avalanche or Debt Snowball."

    def get_investment_strategy(self):
        # Personalized investment strategy
        if self.investment_strategy == "LongTermInvestment":
            return "Consider investments with higher long-term returns, such as stocks or real estate."
        elif self.investment_strategy == "ShortTermInvestment":
            return "Consider more liquid, low-risk investments such as bonds or money market funds."
        else:
            return "No investment strategy selected. Consider a strategy like Long-Term Investment or Short-Term Investment."

    def generate_financial_tips(self):
        tips = []

        # High debt to income ratio
        if self.debt > 2 * self.income:
            tips.append("Your debt-to-income ratio is quite high. Consider reviewing your budget or seeking debt consolidation options.")

        # Low savings rate
        if self.income - self.expenses < 100:
            tips.append("Your savings rate is low. Try to reduce non-essential expenses or increase income to accelerate savings.")

        # Credit score below 600
        if self.credit_score < 600:
            tips.append("Your credit score is low. Consider reviewing your credit report for errors and paying off any outstanding balances.")

        return tips

    def track_progress(self):
        # Check if user has saved 50% or 75% of their financial goal
        if self.savings >= 0.5 * self.goal_amount:
            return "Congrats! You've saved 50% of your financial goal. Keep going!"
        elif self.savings >= 0.75 * self.goal_amount:
            return "You're almost there! Just a little more to go."
        else:
            return "Keep up the good work! Every step brings you closer to your goal."

    def get_rdf_data(self):
        return self.graph.serialize(format="turtle")
