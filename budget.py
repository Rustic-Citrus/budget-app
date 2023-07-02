# Complete the Category class in budget.py. It should be able to instantiate 
# objects based on different budget categories like food, clothing, and 
# entertainment. When objects are created, they are passed in the name of the 
# category. The class should have an instance variable called ledger that is a
# list.

categories = []

class Category:
    def __init__(self, category):
        self.ledger = []
        self.__name__ = category

    def __str__(self):
        lines = []
        asterisks = "*" * round((30 - len(self.__name__)) / 2)
        title = f"{asterisks}{self.__name__}{asterisks}"
        lines.append(title)
        balance_str = format(self.get_balance(), ".2f")
        for transaction in self.ledger:
            description_str = transaction["description"][:23]
            amount_str = format(round(transaction["amount"], 2), ".2f")
            left = description_str + (" " * (23 - len(description_str)))
            right = (" " * (7 - len(amount_str))) + amount_str
            lines.append(left + right)
        lines.append(f"Total: {balance_str}")
        output_str = "\n".join(lines)
        return output_str

    def deposit(self, amount, description=""):
        """A deposit method that accepts an amount and description. If no description is given, it should default to an empty string. The method should append an object to the ledger list in the form of {"amount": amount, "description": description}."""
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        """A withdraw method that is similar to the deposit method, but the amount passed in should be stored in the ledger as a negative number. If there are not enough funds, nothing should be added to the ledger. This method should return True if the withdrawal took place, and False otherwise."""
        transaction = {"amount": -abs(amount), "description": description}
        if self.check_funds(amount):
            self.ledger.append(transaction)
            return True
        else:
            return False

    def get_balance(self):
        """A get_balance method that returns the current balance of the budget category based on the deposits and withdrawals that have occurred."""
        balance = 0
        for transaction in self.ledger:
            balance += transaction["amount"]
        return balance

    def transfer(self, amount, category):
        """A transfer method that accepts an amount and another budget category as arguments. The method should add a withdrawal with the amount and the description "Transfer to [Destination Budget Category]". The method should then add a deposit to the other budget category with the amount and the description "Transfer from [Source Budget Category]". If there are not enough funds, nothing should be added to either ledgers. This method should return True if the transfer took place, and False otherwise."""
        description_withdraw = f"Transfer to {category.__name__}"
        description_deposit = f"Transfer from {self.__name__}"
        try:
            if self.check_funds(amount):
                self.withdraw(amount, description_withdraw)
                category.deposit(amount, description_deposit)
                return True
            else:
                return False
        except:
            return False

    def check_funds(self, amount):
        """A check_funds method that accepts an amount as an argument. It returns False if the amount is greater than the balance of the budget category and returns True otherwise. This method should be used by both the withdraw method and transfer method."""
        if (self.get_balance() - amount) < 0:
            return False
        elif (self.get_balance() - amount) >= 0:
            return True 


def create_spend_chart(categories):
    # Create the list of output lines.
    output = []

    # Assign the names of the categories to a list.
    category_names = [category.__name__ for category in categories]

    # Find the subtotal of withdrawals for each category and append the 
    # subtotals to a list.
    subtotals = []
    for category in categories:
        subtotal = 0
        for transaction in category.ledger:
            if transaction["amount"] < 0:
                subtotal += abs(transaction["amount"])
        subtotals.append(subtotal)
    
    # Find the sum of the subtotals and assign to a variable.
    total = sum(subtotals)

    # Convert the subtotals to percentages of the total expenses.
    subtotal_pcts = [round((subtotal / total), 1) * 100 for subtotal in subtotals]

    # Add the plot title to the output.
    output.append("Percentage spent by category")

    # Create the plot and the y-axis labels.
    y_axis = [list(((3 - len(str(n))) * " ") + str(n) + "|" + (" " * (len(subtotal_pcts) * 3)) + (" " * 3)) for n in range(100, -10, -10)]
    plot = [list(((3 - len(str(n))) * " ") + str(n) + "|" + (" " * (len(subtotal_pcts) * 3)) + (" " * 3)) for n in range(100, -10, -10)]

    # Plot the percentages as bar graphs of 'o' symbols.
    offset = 5
    for pct in subtotal_pcts:
        for y in y_axis:
            if pct == int("".join(y[:3])):
                for row in y_axis[y_axis.index(y):]:
                    plot[y_axis.index(row)][offset + (subtotal_pcts.index(pct) * 3)] = "o"

    # Add the rows of the plot to the output.
    for row in plot:
        output.append("".join(row))

    # Create the separator string and add it to the output.
    separator = "    " + ("---" * len(category_names)) + "-"
    output.append(separator)

    # Convert the category names into lists of characters.
    letters = [list(category) for category in category_names]

    # Find the length of each word.
    word_lengths = [len(category) for category in category_names]

    # Find the longest word and fill the difference in each word with spaces.
    for word in letters:
        while len(word) < max(word_lengths):
            word.append(" ")

    # Convert the category names into vertical labels.
    lines = list()
    for index in range(max(word_lengths)):
        line = "   "
        for word in letters:
            line += ("  " + word[index])
        lines.append(line)

    # Add the vertical label rows to the output
    for line in lines:
        output.append(line)

    # Convert the output to a string and join on a line break.
    output = "\n".join(output)

    return output
