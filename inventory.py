# Python tabulate module import. You first need to install using `pip install tabulate`
from tabulate import tabulate


# Shoe class with initialized variables
class Shoe:

    # Initialize variables
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    # Method to return cost of shoe
    def get_cost(self):
        return self.cost

    # Method to return quantity of the shoes
    def get_quantity(self):
        return self.quantity

    # Method to return a string representation of this class
    def __str__(self):
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}"


# List will be used to store shoe objects
shoe_list = []


# Function to read external text file in read mode, using try and except blocks to handle errors
def read_file(file_name):

    try:
        # Open the file in read mode
        with open(file_name, 'r') as file:
            return file.readlines()

    except (FileNotFoundError, PermissionError) as error:
        print("Something went wrong!", error)


# Function to write list of items with heading to external file
def write_file(file_name, csv_heading, list_items):

    # Open the file in write mode
    with open(file_name, 'w') as file:

        # Create a list of strings, each string reps a line in the file
        lines = [f"{item}\n" for item in list_items]

        # Write the heading to file
        file.write(f"{csv_heading} \n")

        # Write the lines to file
        file.writelines(lines)


# Function to get integer inputs from user, using try and except blocks to check for valid inputs
def get_integer_input(prompt):

    while True:
        try:
            value = int(input(prompt))
            return value

        except (TypeError, ValueError):
            print("Wrong input! Integer expected. Try again...")


# Function to create shoe objects
def read_shoes_data():

    # Always start with an empty shoe_list before reading the inventory data to create shoe objects
    shoe_list.clear()

    # Call read_file function to read the lines in the inventory file and store in a variable
    inventory = read_file('inventory.txt')

    # If there's valid data in inventory, create shoe objects from inventory and append to shoe_list
    # Skip the heading on the csv file
    if inventory:
        for count, line in enumerate(inventory):
            if count == 0:
                continue
            else:
                show_attributes = line.split(',')
                new_shoe = Shoe(show_attributes[0], show_attributes[1], show_attributes[2], int(show_attributes[3]),
                                int(show_attributes[4].replace('\n', '')))
                shoe_list.append(new_shoe)


# Function to create new shoe object from user input and append to shoe_list
def capture_shoes():

    # Get shoe attributes for a new shoe object from user
    # Call the get_integer_input function to get product cost and quantity from user
    product_country = input("Enter the country: \n")
    product_code = input("Enter the SKU: \n").upper()
    product_name = input("Enter the product name: \n")
    product_cost = get_integer_input("Enter the cost: \n")
    product_quantity = get_integer_input("Enter the quantity: \n")

    # Create new shoe object from user input and append to shoe list
    new_shoe = Shoe(product_country, product_code, product_name, product_cost, product_quantity)
    shoe_list.append(new_shoe)

    # Call write_file function to overwrite the inventory.txt file with updated object strings in shoe_list
    write_file("inventory.txt", "Country,Code,Product,Cost,Quantity", shoe_list)

    # Print feedback
    print("New shoe record added!")


# Function to print a list of all shoes in the inventory
def view_all():

    # Extract the data attributes from each of the shoe objects and store in the list
    # Use enumerate function to log count starting from 1
    shoe_data = [[count, shoe.country, shoe.code, shoe.product, shoe.get_cost(), shoe.get_quantity()]
                 for count, shoe in enumerate(shoe_list, 1)]

    # Create the products table using the imported tabulate module
    table = tabulate(shoe_data, headers=["S/N", "Country", "Code", "Product", "Cost", "Quantity"])

    # Print the formatted table
    print(table)


# Function to print a particular item in the inventory by the index
def view_single(index):

    # Extract the data attributes from each of the shoe objects and store in the list
    shoe_data = [[shoe.country, shoe.code, shoe.product, shoe.get_cost(), shoe.get_quantity()]
                 for count, shoe in enumerate(shoe_list) if count == index]

    # Create the products table using the imported tabulate module
    table = tabulate(shoe_data, headers=["Country", "Code", "Product", "Cost", "Quantity"])

    # Print the formatted table
    print(table)


# Function to find the shoe object with the lowest quantity
def re_stock():

    # Get index of object with the lowest quantity in the list
    lowest_qty_index = shoe_list.index(min(shoe_list, key=lambda qty: qty.get_quantity()))

    # Print out the entry with the lowest quantity
    view_single(lowest_qty_index)

    # While loop prompts and checks if user wants to restock item
    while True:

        restock = input(f"Do you want to restock the {shoe_list[lowest_qty_index].product}? Enter Yes/No: \n").lower()

        if restock == "yes":

            # Call get_integer_input function to get restock quantity from user
            restock_quantity = get_integer_input(f"Enter the quantity of {shoe_list[lowest_qty_index].product}: \n")

            # Sum the entry's quantity in the shoe_list with user input
            shoe_list[lowest_qty_index].quantity += restock_quantity

            # Call write_file function to overwrite inventory.txt file with updated object strings in shoe_list
            write_file("inventory.txt", "Country,Code,Product,Cost,Quantity", shoe_list)

            # Print feedback
            print(f"Success! Total quantity for {shoe_list[lowest_qty_index].product} "
                  f"({shoe_list[lowest_qty_index].code}) is now "
                  f"{shoe_list[lowest_qty_index].get_quantity()}.")

            break

        elif restock == "no":
            break
        else:
            print("Wrong input! Try again...")


# Function to search for a shoe from the list using the shoe code
def search_shoe():

    while True:

        # Get shoe code from user
        shoe_code = input("Enter the shoe code: \n").upper()

        # Extract the data attributes from each of the shoe objects and store in the list
        shoe_data = [[shoe.country, shoe.code, shoe.product, shoe.get_cost(), shoe.get_quantity()]
                     for shoe in shoe_list if shoe.code == shoe_code]

        # Print table with item if shoe_data is not falsy
        if shoe_data:
            # Create the products table using the imported tabulate module
            table = tabulate(shoe_data, headers=["Country", "Code", "Product", "Cost", "Quantity"])

            # Print the formatted table
            print(table)
            break

        else:
            print(f"Oops! Did you enter the correct SKU code? Try again...")


# Function to calculate the total value of each item in the list
def value_per_item():

    # Extract the data attributes from each of the shoe objects and store in the list
    # Use enumerate function to log count starting from 1
    shoe_data = [[count, shoe.country, shoe.code, shoe.product, shoe.get_cost(), shoe.get_quantity(),
                  shoe.get_cost() * shoe.get_quantity()] for count, shoe in enumerate(shoe_list, 1)]

    # Create the products table using the imported tabulate module
    table = tabulate(shoe_data, headers=["S/N", "Country", "Code", "Product", "Cost £", "Quantity", "Total Value £"])

    # Print the formatted table
    print(table)


def highest_qty():
    # Get index of object with the highest quantity in the list
    highest_qty_index = shoe_list.index(max(shoe_list, key=lambda qty: qty.get_quantity()))

    # Print out the entry with the lowest quantity
    view_single(highest_qty_index)


# ==========Main Menu=============
def main():

    # Heading
    print("SHOE INVENTORY MANAGER v1.0")

    while True:

        # Call the read_shoes_data() function
        read_shoes_data()

        # Menu
        menu = input("Select one of the following options below: \n"
                     "v -   View all shoes in inventory \n"
                     "s -   Search for shoe by SKU code \n"
                     "a -   Add new shoe to inventory \n"
                     "r -   Re-stock shoes \n"
                     "o -   View shoe on sale \n"
                     "t -   View total value of each item in stock \n"
                     "e -   Exit \n"
                     ": ").lower()

        if menu == "v":

            # Heading
            print("ALL SHOES IN INVENTORY")

            # Call the view_all() function to view all shoes
            view_all()

        elif menu == "s":

            # Heading
            print("SEARCH FOR SHOE BY SKU CODE")

            # Call the search_shoe() function
            search_shoe()

        elif menu == "a":

            # Heading
            print("ADD NEW SHOE TO INVENTORY")

            # Call the capture_shoes() function to add new item to inventory
            capture_shoes()

        elif menu == "r":

            # Heading
            print("SHOE WITH THE LOWEST QUANTITY")

            # Call the re_stock() function to add new item to inventory
            re_stock()

        elif menu == "o":

            # Heading
            print("ON SALE - SHOE WITH THE HIGHEST QUANTITY")

            # Call the highest_qty() function to add new item to inventory
            highest_qty()

        elif menu == "t":

            # Heading
            print("TOTAL VALUE OF EACH ITEM IN STOCK")

            # Call the value_per_item function to display sum total of each item in the inventory
            value_per_item()

        elif menu == "e":
            print("Good bye!")
            break
        else:
            print("wrong input! Try again...")


# Call the main function to run the program
main()
