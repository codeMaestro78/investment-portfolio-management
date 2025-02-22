import mysql.connector # type: ignore
from datetime import datetime
import hashlib
import matplotlib.pyplot as plt
from decimal import Decimal
class RealEstate:
    def __init__(self, id, name, location, purchase_price, current_value, rental_income):
        self.id = id
        self.name = name
        self.location = location
        self.purchase_price = purchase_price
        self.current_value = current_value
        self.rental_income = rental_income

    def update_value(self, new_value):
        self.current_value = new_value

    def calculate_return(self):
        return (self.current_value - self.purchase_price) / self.purchase_price

    def calculate_total_return(self):
        return self.calculate_return() + (self.rental_income / self.purchase_price)

    def calculate_monthly_return_real(self):
        today = datetime.today()
        days_in_month = today.day
        monthly_rental_income = (self.rental_income) * (days_in_month / 30)
        return ((self.current_value - self.purchase_price) / self.purchase_price) + ((monthly_rental_income / self.purchase_price))

    def calculate_monthly_return(self):
        today = datetime.today()
        days_in_month = Decimal(today.day)
        monthly_rental_income = Decimal(self.rental_income) * (days_in_month / Decimal(30))
        return ((self.current_value - self.purchase_price) / self.purchase_price) + ((monthly_rental_income / self.purchase_price))

    def calculate_yearly_return(self):
        return (self.current_value - self.purchase_price) / self.purchase_price + (self.rental_income * 12 / self.purchase_price)

class RealEstatePortfolio:
    def __init__(self):
        try:
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="investiq"
            )
            self.cursor = self.db_connection.cursor()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def add_property(self, property):
        try:
            sql_query = "INSERT INTO real_estate (name, location, purchase_price, current_value, rental_income, return_per_month, return_per_year) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            monthly_return = property.calculate_monthly_return_real()
            yearly_return = property.calculate_yearly_return()
            property_data = (property.name, property.location, property.purchase_price, property.current_value, property.rental_income, monthly_return, yearly_return)
            self.cursor.execute(sql_query, property_data)
            self.db_connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def remove_property(self, property_id):
        try:
            sql_query = "DELETE FROM real_estate WHERE id = %s"
            property_id = (property_id,)
            self.cursor.execute(sql_query, property_id)
            self.db_connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def update_property_value(self, property_id, new_value):
        try:
            sql_query = "UPDATE real_estate SET current_value = %s WHERE id = %s"
            property_data = (new_value, property_id)
            self.cursor.execute(sql_query, property_data)
            self.db_connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def generate_report(self):
        try:
            sql_query = "SELECT id, name, location, purchase_price, current_value, rental_income FROM real_estate"
            self.cursor.execute(sql_query)
            properties = self.cursor.fetchall()

            total_return = 0
            names = []
            total_returns = []
            for prop in properties:
                property_object = RealEstate(prop[0], prop[1], prop[2], prop[3], prop[4], prop[5])
                monthly_return = property_object.calculate_monthly_return()
                yearly_return = property_object.calculate_yearly_return()
                total_return += property_object.calculate_total_return()
                names.append(property_object.name)
                total_returns.append(property_object.calculate_total_return())

                sql_query_update = "UPDATE real_estate SET return_per_month = %s, return_per_year = %s WHERE id = %s"
                return_data = (monthly_return, yearly_return, prop[0])
                self.cursor.execute(sql_query_update, return_data)
                self.db_connection.commit()

            plt.figure(figsize=(10, 6))
            plt.bar(names, total_returns, color='skyblue')
            plt.xlabel('Property Name')
            plt.ylabel('Total Return')
            plt.title('Total Return on Real Estate Properties')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

            print(f"Total Portfolio Return: {total_return}")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        
    def generate_report_save(self, filename):
        try:
            sql_query = "SELECT * FROM real_estate"
            self.cursor.execute(sql_query)
            properties = self.cursor.fetchall()

            with open(filename, 'w') as file:
                file.write("Name, Location, Purchase Price, Current Value, Rental Income, Return per Month, Return per Year\n")
                for prop in properties:
                    file.write(f"{prop[1]}, {prop[2]}, {prop[3]}, {prop[4]}, {prop[5]}, {prop[6]}, {prop[7]}\n")
            print(f"Report saved to {filename}.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    
    def print_properties(self):
        try:
            sql_query = "SELECT * FROM real_estate"
            self.cursor.execute(sql_query)
            properties = self.cursor.fetchall()

            print("Real Estate Properties:")
            for prop in properties:
                print(f"ID: {prop[0]}, Name: {prop[1]}, Location: {prop[2]}, Purchase Price: {prop[3]}, Current Value: {prop[4]}, Rental Income: {prop[5]}, Monthly Return: {prop[6]}, Yearly Return: {prop[7]}")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    
    

    def __del__(self):
        self.cursor.close()
        self.db_connection.close()

class Stock:
    def __init__(self, id, symbol, purchase_price, current_price, quantity):
        self.id = id
        self.symbol = symbol
        self.purchase_price = purchase_price
        self.current_price = current_price
        self.quantity = quantity

    def update_price(self, new_price):
        self.current_price = new_price

    def calculate_return(self):
        return (self.current_price - self.purchase_price) * self.quantity
    
    def calculate_roi(self):
        if self.purchase_price == 0:
            return None
        return ((self.current_price - self.purchase_price) / self.purchase_price) * 100

class StockPortfolio:
    def __init__(self):
        try:
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="investiq"
            )
            self.cursor = self.db_connection.cursor()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def add_stock(self, stock):
        try:
            sql_query = "INSERT INTO stocks (symbol, purchase_price, current_price, quantity) VALUES (%s, %s, %s, %s)"
            stock_data = (stock.symbol, stock.purchase_price, stock.current_price, stock.quantity)
            self.cursor.execute(sql_query, stock_data)
            self.db_connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def remove_stock(self, stock_id):
        try:
            sql_query = "DELETE FROM stocks WHERE id = %s"
            stock_id = (stock_id,)
            self.cursor.execute(sql_query, stock_id)
            self.db_connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def update_stock_price(self, stock_id, new_price):
        try:
            sql_query = "UPDATE stocks SET current_price = %s WHERE id = %s"
            stock_data = (new_price, stock_id)
            self.cursor.execute(sql_query, stock_data)
            self.db_connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def generate_report(self):
        try:
            sql_query = "SELECT id, symbol, purchase_price, current_price, quantity FROM stocks"
            self.cursor.execute(sql_query)
            stocks = self.cursor.fetchall()

            total_return = 0
            total_roi = 0
            symbols = []
            total_returns = []
            for stock_data in stocks:
                stock_object = Stock(stock_data[0], stock_data[1], stock_data[2], stock_data[3], stock_data[4])
                total_return += stock_object.calculate_return()
                total_roi += stock_object.calculate_roi()
                symbols.append(stock_object.symbol)
                total_returns.append(stock_object.calculate_return())

            plt.figure(figsize=(10, 6))
            plt.subplot(1, 2, 1)
            plt.bar(symbols, total_returns, color='skyblue')
            plt.xlabel('Stock Symbol')
            plt.ylabel('Total Return')
            plt.title('Total Return on Stocks')
            plt.xticks(rotation=45)

            plt.subplot(1, 2, 2)
            plt.bar(symbols, total_roi, color='lightgreen')
            plt.xlabel('Stock Symbol')
            plt.ylabel('ROI (%)')
            plt.title('ROI on Stocks')
            plt.xticks(rotation=45)

            plt.tight_layout()
            plt.show()

            print(f"Total Portfolio Return: {total_return}")
            print(f"Total Portfolio ROI: {total_roi}%")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    
    def sell_stock(self, stock_id, quantity):
        try:
            sql_query = "SELECT * FROM stocks WHERE id = %s"
            stock_id_data = (stock_id,)
            self.cursor.execute(sql_query, stock_id_data)
            stock = self.cursor.fetchone()

            if stock:
                current_quantity = stock[4]  
                if current_quantity >= quantity:
                    new_quantity = current_quantity - quantity
                    sql_update_query = "UPDATE stocks SET quantity = %s WHERE id = %s"
                    stock_data = (new_quantity, stock_id)
                    self.cursor.execute(sql_update_query, stock_data)
                    self.db_connection.commit()
                    print(f"{quantity} shares of stock with ID {stock_id} sold successfully.")
                else:
                     print("Insufficient quantity of stocks to sell.")
            else:
             print("Stock not found.")
        except mysql.connector.Error as err:
         print(f"Error: {err}")

    def print_stocks(self):
        try:
            sql_query = "SELECT * FROM stocks"
            self.cursor.execute(sql_query)
            stocks = self.cursor.fetchall()

            print("Stocks:")
            for stock_data in stocks:
                print(f"ID: {stock_data[0]}, Symbol: {stock_data[1]}, Purchase Price: {stock_data[2]}, Current Price: {stock_data[3]}, Quantity: {stock_data[4]}")
        except mysql.connector.Error as err:
            print(f"Error: {err}")


    def close_connection(self):
        self.cursor.close()
        self.db_connection.close()

class MutualFund:
    def __init__(self, id, symbol, name, purchase_price, current_price, quantity):
        self.id = id
        self.name = name
        self.symbol = symbol
        self.purchase_price = purchase_price
        self.current_price = current_price
        self.quantity = quantity


    def update_price(self, new_price):
        self.current_price = new_price

    def calculate_return(self):
        return (self.current_price - self.purchase_price) / self.purchase_price
    
    def calculate_total_return(self):
        return self.calculate_return() * self.quantity

    def calculate_return_on_investment(self):
        if self.purchase_price == 0:
            return None
        return ((self.current_price - self.purchase_price) / self.purchase_price) * 100

class MutualFundPortfolio:
    def __init__(self):
        try:
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="investiq"
            )
            self.cursor = self.db_connection.cursor()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def add_mutual_fund(self, mutual_fund):
        try:
            sql_query = "INSERT INTO mutual_funds (symbol, purchase_price, current_price, quantity, roi) VALUES (%s, %s, %s, %s, %s)"
            roi = mutual_fund.calculate_return_on_investment()
            mutual_fund_data = (mutual_fund.symbol, mutual_fund.purchase_price, mutual_fund.current_price, mutual_fund.quantity, roi)
            self.cursor.execute(sql_query, mutual_fund_data)
            self.db_connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def update_mutual_fund_price(self, mutual_fund_id, new_price):
        try:
            sql_query = "UPDATE mutual_funds SET current_price = %s WHERE id = %s"
            mutual_fund_data = (new_price, mutual_fund_id)
            self.cursor.execute(sql_query, mutual_fund_data)
            self.db_connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def remove_mutual_fund(self, mutual_fund_id):
        try:
            sql_query = "DELETE FROM mutual_funds WHERE id = %s"
            mutual_fund_id = (mutual_fund_id,)
            self.cursor.execute(sql_query, mutual_fund_id)
            self.db_connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
    
    def print_mutual_funds(self):
        try:
            sql_query = "SELECT * FROM mutual_funds"
            self.cursor.execute(sql_query)
            mutual_funds = self.cursor.fetchall()

            print("Mutual Funds:")
            for mf_data in mutual_funds:
                print(f"ID: {mf_data[0]}, Name: {mf_data[1]}, Purchase Price: {mf_data[2]}, Current Price: {mf_data[3]}, Quantity: {mf_data[4]}")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def generate_report(self):
        try:
            sql_query = "SELECT id, symbol, purchase_price, current_price, quantity, roi FROM mutual_funds"
            self.cursor.execute(sql_query)
            mutual_funds = self.cursor.fetchall()

            total_return = 0
            symbols = []
            total_returns = []
            for mutual_fund_data in mutual_funds:
                mutual_fund_object = MutualFund(mutual_fund_data[0], mutual_fund_data[1], mutual_fund_data[2], mutual_fund_data[3], mutual_fund_data[4], mutual_fund_data[5])
                total_return += mutual_fund_object.calculate_total_return()
                symbols.append(mutual_fund_object.symbol)
                total_returns.append(mutual_fund_object.calculate_total_return())

            # Plotting
            plt.figure(figsize=(10, 6))
            plt.bar(symbols, total_returns, color='skyblue')
            plt.xlabel('Mutual Fund Symbol')
            plt.ylabel('Total Return')
            plt.title('Total Return on Mutual Funds')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

            print(f"Total Portfolio Return: {total_return}")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def generate_report_save(self, filename):
        try:
            sql_query = "SELECT * FROM mutual_funds"  
            self.cursor.execute(sql_query)
            mutual_funds = self.cursor.fetchall()

            with open(filename, 'w') as file:
                file.write("Symbol, Name, Purchase Price, Current Price, Quantity, ROI\n")
                for mutual_fund in mutual_funds:
                    file.write(f"{mutual_fund[1]}, {mutual_fund[2]}, {mutual_fund[3]}, {mutual_fund[4]}, {mutual_fund[5]}\n")
            print(f"Report saved to {filename}.")
        except mysql.connector.Error as err:
             print(f"Error: {err}")



    def close_connection(self):
        self.cursor.close()
        self.db_connection.close()


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = hashlib.sha256(password.encode()).hexdigest()

class Database:
    def __init__(self):
        try:
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="investiq"
            )
            self.cursor = self.db_connection.cursor()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def create_tables(self):
        try:
            self.cursor.execute("USE investiq")
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                    username VARCHAR(255) UNIQUE,
                                    password VARCHAR(64)
                                )""")
            self.db_connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def insert_user(self, user):
        try:
            self.cursor.execute("USE investiq")
            sql_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            user_data = (user.username, user.password)
            self.cursor.execute(sql_query, user_data)
            self.db_connection.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def verify_user(self, username, password):
        try:
            self.cursor.execute("USE investiq")
            sql_query = "SELECT * FROM users WHERE username = %s AND password = %s"
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            self.cursor.execute(sql_query, (username, hashed_password))
            user = self.cursor.fetchone()
            return user is not None
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def close_connection(self):
        self.cursor.close()
        self.db_connection.close()

if __name__ == "__main__":
    database = Database()
    database.create_tables()

    while True:
        print("1. Login")
        print("2. Register")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            if database.verify_user(username, password):
                print("Login successful!")
                real_estate_portfolio = RealEstatePortfolio()
                stock_portfolio = StockPortfolio()
                mutual_fund_portfolio = MutualFundPortfolio()

                while True:
                    print("1. Add Real Estate Property")
                    print("2. Update Real Estate Property Value")
                    print("3. Remove Real Estate Property")
                    print("4. Generate Real Estate Portfolio Report")
                    print("5. Save Real Estate Portfolio Report")
                    print("6. Display Real Estate data")
                    print("7. Add Stock")
                    print("8. Update Stock Price")
                    print("9. Remove Stock")
                    print("10. Sell Stock")
                    print("11. Generate Stock Portfolio Report")
                    print("12. Display stock data")
                    print("13. Add Mutual Fund") 
                    print("14. Update Mutual Fund Price")  
                    print("15. Remove Mutual Fund")  
                    print("16. Generate Mutual Fund Portfolio Report") 
                    print("17. Save Mutual Fund Portfolio Report")
                    print("18. Display Mutual Fund data")
                    print("19. Logout")

                    choice = input("Enter your choice: ")

                    if choice == "1":
                        name = input("Enter property name: ")
                        location = input("Enter property location: ")
                        purchase_price = float(input("Enter purchase price: "))
                        current_value = float(input("Enter current value: "))
                        rental_income = float(input("Enter rental income: "))
                        property = RealEstate(None, name, location, purchase_price, current_value, rental_income)
                        real_estate_portfolio.add_property(property)

                    elif choice == "2":
                        property_id = int(input("Enter property ID: "))
                        new_value = float(input("Enter new value: "))
                        real_estate_portfolio.update_property_value(property_id, new_value)

                    elif choice == "3":
                        property_id = int(input("Enter property ID: "))
                        real_estate_portfolio.remove_property(property_id)

                    elif choice == "4":
                        real_estate_portfolio.generate_report()
                    elif choice == "5":
                        filename = input("Enter filename to save the report: ")
                        real_estate_portfolio.generate_report_save(filename)

                    elif choice == "6":
                        real_estate_portfolio.print_properties()

                    elif choice == "7":
                        symbol = input("Enter stock symbol: ")
                        purchase_price = float(input("Enter purchase price: "))
                        current_price = float(input("Enter current price: "))
                        quantity = int(input("Enter quantity: "))
                        stock = Stock(None, symbol, purchase_price, current_price, quantity)
                        stock_portfolio.add_stock(stock)

                    elif choice == "8":
                        stock_id = int(input("Enter stock ID: "))
                        new_price = float(input("Enter new price: "))
                        stock_portfolio.update_stock_price(stock_id, new_price)

                    elif choice == "9":
                        stock_id = int(input("Enter stock ID: "))
                        stock_portfolio.remove_stock(stock_id)

                    elif choice == "10":
                        stock_id = int(input("Enter stock ID: "))
                        stock_quantity = int(input("Enter the quantity of stock to sell: "))
                        stock_portfolio.sell_stock(stock_id,stock_quantity)

                    elif choice == "11":
                        stock_portfolio.generate_report()
                    
                    elif choice == "12":
                        stock_portfolio.print_stocks()

                    elif choice == "13":  
                        symbol = input("Enter mutual fund symbol: ")
                        purchase_price = float(input("Enter purchase price: "))
                        current_price = float(input("Enter current price: "))
                        quantity = int(input("Enter quantity: "))
                        roi = ((current_price - purchase_price) / purchase_price) * 100 
                        mutual_fund = MutualFund(None, symbol, purchase_price, current_price, quantity, roi)
                        mutual_fund_portfolio.add_mutual_fund(mutual_fund)
                        print("Mutual fund added successfully")

                    elif choice == "14":  
                        mutual_fund_id = int(input("Enter mutual fund ID: "))
                        new_price = float(input("Enter new price: "))
                        mutual_fund_portfolio.update_mutual_fund_price(mutual_fund_id, new_price)

                    elif choice == "15": 
                        mutual_fund_id = int(input("Enter mutual fund ID: "))
                        mutual_fund_portfolio.remove_mutual_fund(mutual_fund_id)

                    elif choice == "16":  
                        mutual_fund_portfolio.generate_report()
                    
                    elif choice == "17":
                        filename = input("Enter filename to save the report: ")
                        mutual_fund_portfolio.generate_report_save(filename)

                    elif choice == "18":
                        mutual_fund_portfolio.print_mutual_funds()

                    elif choice == "19":
                        real_estate_portfolio.close_connection()
                        stock_portfolio.close_connection()
                        print("Logged out.")
                        break

                    else:
                        print("Invalid choice. Please try again.")
                break
            else:
                print("Invalid username or password. Please try again.")

        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            confirm_password = input("Confirm password: ")
            if password == confirm_password:
                user = User(username, password)
                database.insert_user(user)
                database.verify_user(username, password)
                print("Registration successful! Please login.")
            else:
                print("Passwords do not match. Please try again.")

        elif choice == "3":
            database.close_connection()
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")
