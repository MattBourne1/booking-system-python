# Matthew Edoimioya
# Assignment 7: Booking System

# import pytest
import math
import os
import csv
import re
from datetime import date
from datetime import datetime

NOW = datetime.now()  # current date and time
DATE_FORMATTED = NOW.strftime("%m/%d/%Y")

# date pattern regex
date_pattern = re.compile(r'^(1[0-2]|0[1-9])/(3[01]|[12][0-9]|0[1-9])/[0-9]{4}$')

# Useful global variable
TOTAL_DAYS = 365  # Number of days in a year
TODAY_DATE = date.today()  # Date
LOADED_CUSTOMERS = False
SAVED_CUSTOMERS = False
NOTHING = '0'
PREVIOUS = "[0] For Previous Menu >>> "
max_length = 30
max_weight = 10
max_volume = 125
file_name = 'booking_quotes.csv'

# this will be our list of shipping packages - list of dictionaries
customer_packages = []

# Choices for menus
ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT = "[0]", "[1]", "[2]", "[3]", "[4]", "[5]", "[6]", "[7]", "[8]"

# This dictionary will help to convert our dates to a day of the year
months = {"1": 0, "2": 31, "3": 31 + 28, "4": 31 + 28 + 31,
          "5": 31 + 28 + 31 + 30, "6": 31 + 28 + 31 + 30 + 31, "7": 31 + 28 + 31 + 30 + 31 + 30,
          "8": 31 + 28 + 31 + 30 + 31 + 30 + 31,
          "9": 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31, "10": 31 + 28 + 31 + 30 + 31 + 30 + 31 + 30,
          "11": 31 + 28 + 31 + 30 + 31 + 30 + 31 + 30 + 31,
          "12": 31 + 28 + 31 + 30 + 31 + 30 + 31 + 30 + 31 + 30}

# User choices for main menu input code readability
LOAD_CUSTOMERS = 1
SAVE_CUSTOMERS = 2
NEW_QUOTE = 3
EDIT_QUOTE = 4
UPCOMING_DELIVERIES = 5
ALL_DELIVERIES = 6
EXIT = 7

# User choices for edit menu input code readability
CUSTOMER_NAME = 1
PACKAGE_DESCRIPTION = 2
DANGEROUS_CONTENTS = 3
PACKAGE_WEIGHT = 4
PACKAGE_VOLUME = 5
DELIVERY_DATE = 6
INTERNATIONAL_DESTINATION = 7
DONE = 8

# keys for accessing dictionary values in customer_packages dictionary
KEY_CUSTOMER_NAME = "name"
KEY_PACKAGE_DESCRIPTION = "package_description"
KEY_DANGEROUS_CONTENTS = "dangerous_contents"
KEY_PACKAGE_WEIGHT = "weight"
KEY_PACKAGE_VOLUME = "volume"
KEY_DELIVERY_DATE = "delivery_date"
KEY_DAYS = "delivery_days"
KEY_URGENT = "urgent"
KEY_INTERNATIONAL_DESTINATION = "international_destination"
KEY_QUOTE = "quote"
KEY_QUOTE_DATE = "quote_date"


# simple helper function
def recorded_response():
    print("Thank you, your response has been recorded.")


# functions to help with each piece of data that needs to be collected
def get_name():
    while True:
        cust_name = input("\nPlease enter the customers name.\n"
                          "(0 to skip) >>> ")
        if cust_name == NOTHING:
            return NOTHING
        elif len(cust_name) > max_length or len(cust_name) < 1:
            print(f"Sorry, you must enter a name between 1 and {max_length} characters.\n")
        elif cust_name.isnumeric():
            print("Sorry, your name must contain letters.\n")
        else:
            break

    recorded_response()
    return cust_name.title()


def get_package_description():
    while True:
        pkg_descr = input("\nPlease enter a description of the package.\n"
                          "(0 to skip) >>> ")
        if pkg_descr == NOTHING:
            return NOTHING
        if len(pkg_descr) > max_length or len(pkg_descr) < 1:
            print(f"Sorry, you must enter a description between 1 and {max_length} characters.\n")
        elif pkg_descr.isnumeric():
            print("Sorry, your description must contain letters.\n")
        else:
            break

    recorded_response()
    return pkg_descr.upper()


def get_dangerous_contents():
    while True:
        danger = input("\nDoes your package contain dangerous contents? (Y/N)\n"
                       "*required\n" +
                       PREVIOUS)
        if danger == NOTHING:
            return NOTHING
        if danger.upper() == "Y":
            recorded_response()
            return danger.upper()
        elif danger.upper() == "N":
            recorded_response()
            return danger.upper()
        else:
            print("Sorry, please enter 'Y' or 'N'\n")


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def valid_number(attribute_name):
    while True:
        attribute = input(f"\nPlease enter the {attribute_name} of your package.\n"
                          "*required\n" +
                          PREVIOUS)

        if attribute.isnumeric() or isfloat(attribute):
            if float(attribute) > 0:
                return float(attribute)
            if float(attribute) == 0 or int(attribute) == 0:
                return NOTHING
            else:
                print(f"The {attribute_name} entered must be greater than 0.\n")
                continue
        else:
            print("A valid number must be entered.\n")


def get_package_weight():
    while True:
        pkg_weight = valid_number("weight [kg]")
        if pkg_weight == NOTHING:
            return NOTHING
        if pkg_weight > max_weight:
            print(f"Sorry, we are only able to ship packages under {max_weight} kgs.\n")
            continue
        else:
            recorded_response()
            return pkg_weight


def get_package_volume():
    pkg_volume = 0

    print("\nThe size of your package by volume [cubic meters] needs to be determined.")
    while True:
        shape = input("What is the general shape of your package?\n"
                      " [S] Sphere\n"
                      " [C] Cube\n" +
                      PREVIOUS)
        if shape == NOTHING:
            return NOTHING

        if shape.upper() == "S":
            radius = valid_number("radius [m]")
            if radius == NOTHING:
                return NOTHING

            pkg_volume = (4 / 3) * math.pi * math.pow(radius, 3)
            if pkg_volume > max_volume:
                print(f"Sorry, we cannot ship packages that are larger than {max_volume} [cubic meters].\n"
                      f"Your spherical package is " + "{:.5f}".format(pkg_volume) + " [m^3].\n")
                continue

            break
        elif shape.upper() == "C":
            length = valid_number("length [m]")
            if length == NOTHING:
                return NOTHING

            width = valid_number("width [m]")
            if width == NOTHING:
                return NOTHING

            height = valid_number("height [m]")
            if height == NOTHING:
                return NOTHING

            pkg_volume = length * width * height
            if pkg_volume > max_volume:
                print(f"Sorry, we cannot ship packages that are larger than {max_volume} [cubic meters].\n"
                      f"Your cubic package is " + "{:.2f}".format(pkg_volume) + " [m^3].\n")
                continue

            break
        else:
            print("Invalid selection.\n")
            continue

    print(f"Package Volume = " + "{:.2f}".format(pkg_volume) + " [m^3]")
    recorded_response()
    return pkg_volume


def date_verify(date_input):
    if re.fullmatch(date_pattern, date_input):
        return True
    else:
        return False


# converting date to a day of year
def date_to_doy(date_input):
    month_day_year = date_input.split('/')
    month = str(month_day_year[0]).lstrip('0')
    day = int(month_day_year[1])
    year = int(month_day_year[2])

    doy = int(months.get(month)) + day

    return doy, year


def get_delivery_date():
    pkg_urgent = 'N'

    while True:
        delivery_date = input("\nWhat date would you like your package delivered? (mm/dd/yyyy)\n"
                              "*required\n" +
                              PREVIOUS)
        if delivery_date == NOTHING:
            return NOTHING
        if date_verify(delivery_date):
            # we will also need to make sure that the user has entered a future date
            delivery_doy, delivery_year = date_to_doy(delivery_date)
            current_doy = months.get(str(TODAY_DATE.month)) + TODAY_DATE.day

            day_difference = (delivery_doy - current_doy) + ((delivery_year - TODAY_DATE.year) * TOTAL_DAYS)

            if day_difference < 1:
                print("Please enter a future date for delivery.\n")
                continue
            elif day_difference > 365:
                print("Sorry, we can only process delivery dates within the next 365 days.\n")
                continue
            elif day_difference <= 3:
                print("Your package will be marked as Urgent.\n" +
                      f"Your package will arrive in {day_difference} day(s).")
                pkg_urgent = 'Y'
                recorded_response()
                break
            else:
                print(f"Your package will arrive in {day_difference} days.")
                recorded_response()
                break
        else:
            print("Sorry, start date entered is invalid! Try again!\n")

    return delivery_date, day_difference, pkg_urgent


def verify_future_date(customer_info):
    customer_dd = customer_info.get(KEY_DELIVERY_DATE)
    verified = True
    if not date_verify(customer_dd):
        return (not verified), NOTHING

    delivery_doy, delivery_year = date_to_doy(customer_dd)
    current_doy = months.get(str(TODAY_DATE.month)) + TODAY_DATE.day

    day_difference = ((delivery_doy - current_doy) + ((delivery_year - TODAY_DATE.year) * TOTAL_DAYS))
    if day_difference > 0:
        return verified, day_difference
    else:
        return not verified, NOTHING


def get_international_destination():
    while True:
        danger = input("\nIs your package being shipped internationally? (Y/N)\n"
                       "*required\n" +
                       PREVIOUS)
        if danger == NOTHING:
            return NOTHING
        if danger.upper() == "Y":
            recorded_response()
            return danger.upper()
        elif danger.upper() == "N":
            recorded_response()
            return danger.upper()
        else:
            print("Sorry, please enter 'Y' or 'N'")


def main_menu():
    """
    Print the menu for the user and return the choice
    :return: <int>
    """
    while True:
        choice = input("\n" + "{:-^40}".format("Main Menu") + "\n"
                                                              " Please choose an option below:\n"
                                                              f"    {ONE} Load Customers\n"
                                                              f"    {TWO} Save Customers\n"
                                                              f"    {THREE} Get New Quote\n"
                                                              f"    {FOUR} Look Up Customer\n"
                                                              f"    {FIVE} Report of Upcoming Deliveries\n"
                                                              f"    {SIX} Report of All Deliveries\n"
                                                              f"    {SEVEN} EXIT\n"
                                                              " Your selection >>> ")
        if not choice.isnumeric():
            print("Please enter a number only.")
            continue
        elif int(choice) not in [1, 2, 3, 4, 5, 6, 7]:
            print("Please enter a valid choice [1-7]")
            continue
        else:
            return int(choice)


def save_menu():
    """
    Print the save menu for the user and return the choice
    :return: <int>
    """
    while True:
        choice = input("\n" + "{:-^36}".format("Save Menu") + "\n"
                                                              " Please choose a save option below:\n"
                                                              f"    {ONE} APPEND\n"
                                                              f"    {TWO} OVERWRITE\n"
                                                              f"    {ZERO} CONTINUE\n"
                                                              f">>> ")
        if choice == NOTHING:
            return NOTHING
        if not choice.isnumeric():
            print("Please enter a number only.")
            continue
        elif int(choice) not in [1, 2]:
            print("Please enter a valid choice [1-2]")
            continue
        else:
            return int(choice)


def delete_menu():
    """
    Print the delete menu for the user and return the choice
    :return: <int>
    """
    while True:
        choice = input("\n" + "{:-^36}".format("Delete Menu") + "\n"
                       " Please choose an option below:\n"
                       f"   {ONE} EDIT\n"
                       f"   {TWO} DELETE\n"
                       f"   {ZERO} CONTINUE\n"
                       f">>> ")
        if choice == NOTHING:
            return NOTHING
        if not choice.isnumeric():
            print("Please enter a number only.")
            continue
        elif int(choice) not in [1, 2]:
            print("Please enter a valid choice [1-2]")
            continue
        else:
            return int(choice)


def edit_menu(customer_dictionary):
    """
    Print the menu for the user and return the choice
    :return: <int>
    """
    if not verify_future_date(customer_dictionary)[0]:
        print(f"Sorry, only shipments with future delivery dates can be edited.")
        return customer_dictionary
    while True:
        choice = input("\n" + "{:-^36}".format("Edit Menu") + "\n"
                       " Please choose an option to edit:\n"
                       f"   {ONE} Customer Name\n"
                       f"   {TWO} Package Description\n"
                       f"   {THREE} Package Contents\n"
                       f"   {FOUR} Package Weight\n"
                       f"   {FIVE} Package Volume\n"
                       f"   {SIX} Delivery Date\n"
                       f"   {SEVEN} Delivery Location\n"
                       f"   {EIGHT} DONE\n"
                       " Your selection --> ")
        if not choice.isnumeric():
            print("Please enter a valid choice.")
            continue

        choice = int(choice)
        if choice not in [1, 2, 3, 4, 5, 6, 7, 8]:
            print("Please enter a selection from the list [1-8].")
            continue

        if choice == DONE:
            return customer_dictionary

        elif choice == CUSTOMER_NAME:
            customer_name = get_name()
            if customer_name == NOTHING:
                continue
            print(f"The customer name is now: {customer_name}\n")
            customer_dictionary[KEY_CUSTOMER_NAME] = customer_name
            continue
        elif choice == PACKAGE_DESCRIPTION:
            package_description = get_package_description()
            if package_description == NOTHING:
                continue
            customer_dictionary[KEY_PACKAGE_DESCRIPTION] = package_description
            print(f"The package description is now:\n{package_description}\n")
            continue
        elif choice == DANGEROUS_CONTENTS:
            dangerous = get_dangerous_contents()
            if dangerous == NOTHING:
                continue
            customer_dictionary[KEY_DANGEROUS_CONTENTS] = dangerous
            customer_dictionary[KEY_QUOTE_DATE] = DATE_FORMATTED
            print(f"The dangerous contents specification is now: {dangerous}")
            print(f"Date of quote is now: {DATE_FORMATTED}\n")
            continue
        elif choice == PACKAGE_WEIGHT:
            package_weight = get_package_weight()
            if package_weight == NOTHING:
                continue
            customer_dictionary[KEY_PACKAGE_WEIGHT] = package_weight
            customer_dictionary[KEY_QUOTE_DATE] = DATE_FORMATTED
            print(f"The package weight is now: " + "{:.2f}".format(package_weight) + "[kg]")
            print(f"Date of quote is now: {DATE_FORMATTED}\n")
            continue
        elif choice == PACKAGE_VOLUME:
            package_volume = get_package_volume()
            if package_volume == NOTHING:
                continue
            customer_dictionary[KEY_PACKAGE_VOLUME] = package_volume
            customer_dictionary[KEY_QUOTE_DATE] = DATE_FORMATTED
            print(f"Date of quote is now: {DATE_FORMATTED}\n")
            continue
        elif choice == DELIVERY_DATE:
            delivery_date, delivery_days, delivery_urgency = get_delivery_date()
            if delivery_date == NOTHING:
                continue
            customer_dictionary[KEY_DELIVERY_DATE] = delivery_date
            customer_dictionary[KEY_DAYS] = delivery_days
            customer_dictionary[KEY_URGENT] = delivery_urgency
            customer_dictionary[KEY_QUOTE_DATE] = DATE_FORMATTED
            print(f"The delivery date is now: {delivery_date}")
            print(f"Date of quote is now: {DATE_FORMATTED}\n")
            continue
        elif choice == INTERNATIONAL_DESTINATION:
            delivery_location = get_international_destination()
            if delivery_location == NOTHING:
                continue
            customer_dictionary[KEY_INTERNATIONAL_DESTINATION] = delivery_location
            customer_dictionary[KEY_QUOTE_DATE] = DATE_FORMATTED
            print(f"The international destination specification is now: {delivery_location}")
            print(f"Date of quote is now: {DATE_FORMATTED}\n")
            continue


def exit_menu():
    """
        Print the exit menu for the user and return the choice
        :return: <int>
        """
    while True:
        choice = input("\n" + "{:-^15}".format("Exit Menu") + "\n"
                                                              " Are you sure:\n"
                                                              f" [Y] YES\n"
                                                              f" [N] NO\n"
                                                              f">>> ")
        if choice.upper() not in ['Y', 'N']:
            print("Please enter 'Y' or 'N'")
            continue
        else:
            return choice


# Helper function that will sort our customers by any dictionary key
def sort_customers(list_of_customers, key):
    # add try statement for, for loop
    for customer in list_of_customers:
        customer[KEY_PACKAGE_WEIGHT] = float(customer.get(KEY_PACKAGE_WEIGHT))
        customer[KEY_PACKAGE_VOLUME] = float(customer.get(KEY_PACKAGE_VOLUME))
    return sorted(list_of_customers, key=lambda eid: eid[key])


# Reading csv file and putting that data into a dictionary
def load_quotes():
    """
    Load customers from the file_name and returns a list of dictionaries
    :return: <list>
    """
    # add try statement
    with open(file_name, "r", newline='') as e_file:
        reader = list(csv.DictReader(e_file))
    return sort_customers(reader, KEY_CUSTOMER_NAME)


def save_quotes(quote_list):
    """
    Saves list of customer quotes to csv file
    """
    e_keys = quote_list[0].keys()
    with open(file_name, "w", newline='') as e_file:
        dict_writer = csv.DictWriter(e_file, e_keys)
        dict_writer.writeheader()
        dict_writer.writerows(quote_list)


def append_quotes(quote_list):
    """
    Saves list of customer quotes to csv file
    """
    e_keys = quote_list[0].keys()
    with open(file_name, "a", newline='') as e_file:
        dict_writer = csv.DictWriter(e_file, e_keys)
        dict_writer.writerows(quote_list)


def verified_dictionary(verify_dict):
    # This will help determine if all the required values are in our dictionary
    verified = True

    verify_DC = verify_dict.get(KEY_DANGEROUS_CONTENTS).upper()
    if verify_DC != 'Y' and verify_DC != 'N':
        print("*Invalid Dangerous Contents Selection*")
        verified = False

    verify_weight = verify_dict.get(KEY_PACKAGE_WEIGHT)
    if not isfloat(verify_weight):
        print("*Invalid Weight - No Number*")
        verified = False
    if verify_weight > max_weight:
        print("*Invalid Weight - Too High*")
        verified = False
    if verify_weight <= 0:
        print("*Invalid Weight*")
        verified = False

    verify_volume = verify_dict.get(KEY_PACKAGE_VOLUME)
    if not isfloat(verify_volume):
        print("*Invalid Volume - No Number*")
        verified = False
    if verify_volume > max_volume:
        print("*Invalid Volume - Too High*")
        verified = False
    if verify_volume <= 0:
        print("*Invalid Volume*")
        verified = False

    verify_urgency = verify_dict.get(KEY_URGENT).upper()
    if verify_urgency != 'Y' and verify_urgency != 'N':
        print("*Invalid Urgency Selection*")
        verified = False

    return verified


def get_quote(customer_dictionary):
    # exiting this method in the data in dictionary is no good
    if not verified_dictionary(customer_dictionary):
        return customer_dictionary

    KEY_METHOD = "method"
    KEY_AVAILABLE = "available"
    KEY_COST = "cost"

    air_index = 0
    ground_index = 1
    water_index = 2

    too_large = max_volume * .85
    too_heavy = max_weight * .85

    air_kg = 10 * customer_dictionary.get(KEY_PACKAGE_WEIGHT)
    air_mmm = 20 * customer_dictionary.get(KEY_PACKAGE_VOLUME)
    air_prices = [{KEY_METHOD: "Air [$10/kg]", KEY_AVAILABLE: True, KEY_COST: air_kg},
                  {KEY_METHOD: "Air [$20/m^3]", KEY_AVAILABLE: True, KEY_COST: air_mmm}]

    ground_cost = 25
    air_cost = max(air_prices, key=lambda cost: cost[KEY_COST])
    if customer_dictionary.get(KEY_URGENT) == 'Y':
        ground_cost = 45
    water_cost = 30

    # Declaring a list of dictionary that will hold the final pricing information
    pricing = [air_cost,
               {KEY_METHOD: "Ground", KEY_AVAILABLE: True, KEY_COST: ground_cost},
               {KEY_METHOD: "Water", KEY_AVAILABLE: True, KEY_COST: water_cost}]
    final_options = []

    # Eliminating methods of shipping (Available: False) based on the booking rules
    if customer_dictionary.get(KEY_DANGEROUS_CONTENTS) == 'Y':
        pricing[air_index][KEY_AVAILABLE] = False

    if customer_dictionary.get(KEY_URGENT) == 'Y':
        pricing[water_index][KEY_AVAILABLE] = False

    if customer_dictionary.get(KEY_INTERNATIONAL_DESTINATION) == 'Y':
        pricing[ground_index][KEY_AVAILABLE] = False

    if customer_dictionary.get(KEY_INTERNATIONAL_DESTINATION) == 'N':
        pricing[water_index][KEY_AVAILABLE] = False

    if customer_dictionary.get(KEY_PACKAGE_WEIGHT) > too_heavy or customer_dictionary.get(KEY_PACKAGE_VOLUME) > \
            too_large:
        if customer_dictionary.get(KEY_URGENT) == 'N':
            pricing[air_index][KEY_AVAILABLE] = False

    print("{:-^28}".format("Shipping Options"))
    print("{:<16}".format(" Method") + "| Cost")
    print("{:-^28}".format(""))
    for option in pricing:
        if option.get(KEY_AVAILABLE):
            print(" " + "{:<15}".format(option.get(KEY_METHOD)) + "| $" + "{:.2f}".format(option.get(KEY_COST)))
            final_options.append(option)

    if len(final_options) == 0:
        print("None.\n"
              "Sorry, unable to send package.")
        customer_dictionary[KEY_QUOTE] = NOTHING
        return customer_dictionary

    least_expensive = min(final_options, key=lambda cost: cost[KEY_COST])
    print("\nBest shipping method: " + least_expensive.get(KEY_METHOD) + "\n"
          "Price: $" + "{:.2f}".format(least_expensive.get(KEY_COST)) + "\n")
    customer_dictionary[KEY_QUOTE] = "{:.2f}".format(least_expensive.get(KEY_COST))
    return customer_dictionary


def print_customer(customer_dict):
    print(f"Today's Date: {DATE_FORMATTED}")
    print(f"Date of Quote: {customer_dict.get(KEY_QUOTE_DATE)}")
    print("{:-^62}".format("Customer Information"))
    print("{:<30}".format(" Name") + "| " + customer_dict.get(KEY_CUSTOMER_NAME) + "\n"
                                                                                   "{:<30}".format(
        " Package Description") + "| " + customer_dict.get(KEY_PACKAGE_DESCRIPTION) + "\n"
                                                                                      "{:<30}".format(
        " Dangerous Contents") + "| " + customer_dict.get(KEY_DANGEROUS_CONTENTS) + "\n"
                                                                                    "{:<30}".format(
        " Package Weight") + "| " + str("{:.2f}".format(customer_dict.get(KEY_PACKAGE_WEIGHT))) +
          " [kg]\n"
          "{:<30}".format(" Package Volume") + "| " + str("{:.2f}".format(customer_dict.get(KEY_PACKAGE_VOLUME))) +
          " [m^3]\n"
          "{:<30}".format(" Delivery Date") + "| " + customer_dict.get(KEY_DELIVERY_DATE) +
          " (in " + str(customer_dict.get(KEY_DAYS)) + " days)\n"
                                                       "{:<30}".format(" Urgent") + "| " + customer_dict.get(
        KEY_URGENT) + "\n"
                      "{:<30}".format(" International Destination") + "| " + customer_dict.get(
        KEY_INTERNATIONAL_DESTINATION) + "\n"
                                         "{:<30}".format(" Quote") + "| $" + str(customer_dict.get(KEY_QUOTE)))


def print_future_deliveries(customer_list):
    space = " "
    bar = "|"

    print("{:*^143}".format("UPCOMING DELIVERIES"))
    print("{:-<143}".format(""))
    print(bar + "{:^35}".format("Name") + bar + "{:^8}".format("Danger") + bar +
          "{:^8}".format("Urgent") + bar + "{:^10}".format("Int Dest") + bar +
          "{:^14}".format("Pckg Wt [kg]") + bar + "{:^16}".format("Pckg Vol [m^3]") + bar + "{:^13}".format(
        "Quote") + bar +
          "{:^14}".format("Quote Date") + bar + "{:^15}".format("Delivery Date") + bar)
    print("{:-<143}".format(""))

    if len(customer_list) == 0:
        print("None")
        return

    for customer_qt in customer_list:
        verified, days_to_delivery = verify_future_date(customer_qt)
        if not verified:
            continue

        customer_qt[KEY_DAYS] = days_to_delivery
        print(bar + "{:^35}".format(customer_qt.get(KEY_CUSTOMER_NAME)) + space +
              "{:^8}".format(customer_qt.get(KEY_DANGEROUS_CONTENTS)) + space +
              "{:^8}".format(customer_qt.get(KEY_URGENT)) + space +
              "{:^10}".format(customer_qt.get(KEY_INTERNATIONAL_DESTINATION)) + space +
              "{:^14}".format(customer_qt.get(KEY_PACKAGE_WEIGHT)) + space +
              "{:^16}".format(customer_qt.get(KEY_PACKAGE_VOLUME)) + space +
              "{:^13}".format(f"${customer_qt.get(KEY_QUOTE)}") + space +
              "{:^14}".format(customer_qt.get(KEY_QUOTE_DATE)) + space +
              "{:^15}".format(customer_qt.get(KEY_DELIVERY_DATE)) + bar)
    print("{:-<143}".format(""))


def print_all_deliveries(customer_list):
    space = " "
    bar = "|"

    print("{:*^143}".format("ALL DELIVERIES"))
    print("{:-<143}".format(""))
    print(bar + "{:^35}".format("Name") + bar + "{:^8}".format("Danger") + bar +
          "{:^8}".format("Urgent") + bar + "{:^10}".format("Int Dest") + bar +
          "{:^14}".format("Pckg Wt [kg]") + bar + "{:^16}".format("Pckg Vol [m^3]") + bar + "{:^13}".format("Quote") + bar +
          "{:^14}".format("Quote Date") + bar + "{:^15}".format("Delivery Date") + bar)
    print("{:-<143}".format(""))

    if len(customer_list) == 0:
        print("None")
        return

    for customer_qt in customer_list:
        print(bar + "{:^35}".format(customer_qt.get(KEY_CUSTOMER_NAME)) + space +
              "{:^8}".format(customer_qt.get(KEY_DANGEROUS_CONTENTS)) + space +
              "{:^8}".format(customer_qt.get(KEY_URGENT)) + space +
              "{:^10}".format(customer_qt.get(KEY_INTERNATIONAL_DESTINATION)) + space +
              "{:^14}".format(customer_qt.get(KEY_PACKAGE_WEIGHT)) + space +
              "{:^16}".format(customer_qt.get(KEY_PACKAGE_VOLUME)) + space +
              "{:^13}".format(f"${customer_qt.get(KEY_QUOTE)}") + space +
              "{:^14}".format(customer_qt.get(KEY_QUOTE_DATE)) + space +
              "{:^15}".format(customer_qt.get(KEY_DELIVERY_DATE)) + bar)
    print("{:-<143}".format(""))


if __name__ == '__main__':
    date = NOW.strftime("%B %d, %Y")
    time = NOW.strftime("%H:%M")
    print(f"Date: {date}\n"
          f"Time: {time}")
    while True:
        user_choice = main_menu()
        if user_choice == EXIT:
            exit_choice = exit_menu()
            if exit_choice.upper() == 'Y':
                print("Goodbye!")
                exit()
            else:
                continue
        elif user_choice == LOAD_CUSTOMERS:
            customer_packages = load_quotes()
            LOADED_CUSTOMERS = True
            print(f"The customers and quotes from the file {file_name} have been loaded successfully.")
        elif user_choice == SAVE_CUSTOMERS:
            if not LOADED_CUSTOMERS or (len(customer_packages) == 0):
                print(f"Sorry, you must first load customers from a file named {file_name}\n"
                      f"or create a new quote!")
                continue
            # if len(customer_packages) != 0:
            save_choice = save_menu()
            if save_choice == NOTHING:
                continue

            OVERWRITE = 2
            APPEND = 1
            if save_choice == OVERWRITE:
                save_quotes(customer_packages)
                print(f"The customers and quotes have been successfully overwritten to the file {file_name}.")
            elif save_choice == APPEND:
                append_quotes(customer_packages)
                print(f"The customers and quotes have been successfully appended to the file {file_name}.")

            SAVED_CUSTOMERS = True

        elif user_choice == NEW_QUOTE:
            print("\nTo get started, we will need to collect your information.")
            name = get_name()
            if name == NOTHING:
                name = "No Name"

            description = get_package_description()
            if description == NOTHING:
                description = "No Description"

            dangerous_content = get_dangerous_contents()
            if dangerous_content == NOTHING:
                continue

            weight = get_package_weight()
            if weight == NOTHING:
                continue

            volume = get_package_volume()
            if volume == NOTHING:
                continue

            date, days, urgent = get_delivery_date()
            if date == NOTHING:
                continue

            destination = get_international_destination()
            if destination == NOTHING:
                continue

            # ask user to edit data
            quote = 'TBD'

            new_customer = {KEY_CUSTOMER_NAME: name,
                            KEY_PACKAGE_DESCRIPTION: description,
                            KEY_DANGEROUS_CONTENTS: dangerous_content,
                            KEY_PACKAGE_WEIGHT: weight,
                            KEY_PACKAGE_VOLUME: volume,
                            KEY_DELIVERY_DATE: date,
                            KEY_DAYS: days,
                            KEY_URGENT: urgent,
                            KEY_INTERNATIONAL_DESTINATION: destination,
                            KEY_QUOTE: quote,
                            KEY_QUOTE_DATE: DATE_FORMATTED}
            print_customer(new_customer)
            edit_customer = input("Would you like to edit this info before calculating a quote?\n"
                                  "Enter 'Y' for yes or hit any other key to continue.\n"
                                  ">>> ")
            if edit_customer.upper() == 'Y':
                new_customer = edit_menu(new_customer)
                # print_customer(new_customer)

            # get quote now that all the information has been collected
            new_customer = get_quote(new_customer)
            print_customer(new_customer)
            customer_packages.append(new_customer)
            LOADED_CUSTOMERS = True

        elif user_choice == EDIT_QUOTE:
            if not LOADED_CUSTOMERS or (len(customer_packages) == 0):
                print(f"Sorry, you must first load customers from a file named {file_name}\n"
                      f"or create a new quote!")
                continue

            edit_quotes = []  # this will keep track of all the search results
            delete_quotes = []  # this list will track which customers we want to delete
            print("We will try searching for a quote by full or partial customer name.")
            cust_name = input("What name would you like to search for?\n"
                              ">>> ")

            EDIT = 1
            DELETE = 2
            tot_matches = 0
            num_matches = 0

            # determining our total number of matches
            for customer in customer_packages:
                compare_name = customer.get(KEY_CUSTOMER_NAME)
                if cust_name.casefold() in compare_name.casefold():
                    tot_matches += 1

            if tot_matches == 1:
                print(f"{tot_matches} MATCH FOUND")
            else:
                print(f"{tot_matches} MATCHES FOUND")
            if tot_matches == 0:
                continue

            for index, customer in enumerate(customer_packages):
                compare_name = customer.get(KEY_CUSTOMER_NAME)
                if cust_name.casefold() in compare_name.casefold():
                    num_matches += 1
                    print(f"\nMatch Number {num_matches} OF {tot_matches} Initial Data")

                    print_customer(customer)
                    verified_date, previous_days_to = verify_future_date(customer)
                    if not verified_date:
                        print(f"Sorry, only shipments with future delivery dates can be edited.\n")
                        continue

                    ed_choice = delete_menu()
                    if ed_choice == NOTHING:
                        continue
                    if ed_choice == EDIT:
                        customer = edit_menu(customer)
                        customer = get_quote(customer)
                        current_days_to = customer.get(KEY_DAYS)

                        print(f"\nMatch Number {num_matches} Final Data")
                        if previous_days_to < current_days_to:
                            print(f"Your delivery date has increased by {current_days_to-previous_days_to} days.")
                        elif previous_days_to > current_days_to:
                            print(f"Your delivery date has decreased by {previous_days_to - current_days_to} days.")
                        print_customer(customer)
                        continue
                    if ed_choice == DELETE:
                        delete_quotes.append(index)
                        print("\nCustomer will be deleted.")
                        continue

            # we will have to delete dictionaries from our list of dictionaries in reverse order to avoid
            # out of bounds errors
            delete_quotes.reverse()
            for number in delete_quotes:
                print(number)
                del customer_packages[number]

        elif user_choice == UPCOMING_DELIVERIES:
            if not LOADED_CUSTOMERS or (len(customer_packages) == 0):
                print(f"Sorry, you must first load customers from a file named {file_name}\n"
                      f"or create a new quote!")
                continue
            print_future_deliveries(customer_packages)

        elif user_choice == ALL_DELIVERIES:
            if not LOADED_CUSTOMERS or (len(customer_packages) == 0):
                print(f"Sorry, you must first load customers from a file named {file_name}\n"
                      f"or create a new quote!")
                continue
            print_all_deliveries(customer_packages)
