#import matplotlib.pyplot as plt

# read in screw_file.txt file data into a list
screw_list = []
data = open('screw_file.txt', 'r')

for line in data:
    if line[0] != '#':
        screw_list.append(line.strip().split(','))

data.close()


# present user with menu options
def menu():
    print('MAIN MENU:')
    print('\t1.Summary Report')
    print('\t2.Total Units Per Length Category')
    print('\t3.Search Stock')
    print('\t4.Edit Stock', )
    print('\t5.Discount', )
    print('\t6.Bar Chart of Stock')
    print('\t7.Quit Program')
    option = input('Enter option: ')

    # execute whichever option was chosen by the user
    if option == '1':
        summary_report()
        total_stock()
    elif option == '2':
        total_units()
    elif option == '3':
        search()
    elif option == '4':
        edit_stock()
    elif option == '5':
        discount()
    elif option == '6':
        chart()
    elif option == '7':
        print('Goodbye.')


# function summary_report outputs the screw data in table format
def summary_report():
    print('-' * 106)
    print('\tMATERIAL', 'HEAD TYPE', 'LENGTH', '50 Unit box', '100 Unit box', '200 Unit box', 'COST PER BOX of 50 (£)',
          sep=' | ')
    print('-' * 106)

    # print out all available stock in table format
    try:
        for each_row in screw_list:
            print('\t{:^8}{:^14}{:^9}{:^14}{:^15}{:^15}{:^23}'.format(each_row[0], each_row[1], each_row[2],
                                                                      each_row[3], each_row[4], each_row[5],
                                                                      each_row[6]))

    except IndexError:
        print()

    # report total stock
    total_stock()

    # allow user to return to main menu
    return_to_menu()


# function total_stock outputs a report giving the total number of units in stock in each length category.
def total_stock():
    # calculates total stock
    print('----------------------------------------------------------------------------------------------------------')
    stock_tally = 0  # total has to initially be set to 0 before calculation
    material = ''
    head = ''
    length = ''
    discount_changed = False

    try:
        # check for unit with discount applied
        for each_row in screw_list:
            if 'Sale: ' in each_row[6]:
                discount_line = each_row[6]
                each_row[6] = discount_line.strip('Sale: ')  # strip string and only leave price for calculation
                # gather all details of screw
                material = each_row[0]
                head = each_row[1]
                length = each_row[2]
                discount_changed = True
    except IndexError:
        print()

    try:
        # calculate total stock price from data
        i = 0  # make sure i is back to 0 position
        for i in range(len(screw_list)):
            stock_price = (int(screw_list[i][3]) + (int(screw_list[i][4]) * 2) + (int(screw_list[i][5]) * 4)) * \
                          float(screw_list[i][6])
            stock_tally = stock_tally + stock_price
    except IndexError:
        print()

    try:
        # after calculation is complete, find the screw that had the sale applied and reapply the string
        each_row = 0
        if discount_changed == True:
            for each_row in screw_list:
                if material in each_row[0] and head in each_row[1] and length in each_row[2]:
                    each_row[6] = 'Sale: ' + each_row[6]
    except IndexError:
        print()

    print('Total price of all stock: £', format(stock_tally, ',.2f'), sep='')  # prints out total price of stock
    print('\t')

    # allow user to return to main menu
    return_to_menu()


def total_units():
    # 1 unit is defined as 50 screws
    units_20 = 0
    units_40 = 0
    units_60 = 0
    unit_count = 0

    try:
        for each_row in screw_list:
            if '20' in each_row[2]:  # checks each sublist in list for value
                unit_count = (int(each_row[3]) + (int(each_row[4]) * 2) + (
                        int(each_row[5]) * 4))  # turns all boxes into 50 unit ones
                units_20 = units_20 + unit_count  # add number of units of this length to variable
            elif '40' in each_row[2]:
                unit_count = (int(each_row[3]) + (int(each_row[4]) * 2) + (int(each_row[5]) * 4))
                units_40 = units_40 + unit_count  # add number of units of this length to variable
            else:
                unit_count = (int(each_row[3]) + (int(each_row[4]) * 2) + (int(each_row[5]) * 4))
                units_60 = units_60 + unit_count  # add number of units of this length to variable
    except IndexError:
        print()

    print('There are', units_20, 'units of 20mm length screws available.')
    print('There are', units_40, 'units of 40mm length screws available.')
    print('There are', units_60, 'units of 60mm length screws available.\n')

    # allow user to return to main menu
    return_to_menu()


def search():
    # initialise again as true to allow user to search at least once
    again = True

    while again:
        search_length = input('Enter the screw length to search for: ')

        if search_length != '20' and search_length != '40' and search_length != '60':  # validates input before next statement
            print('ERROR: Invalid length entered. Please enter a valid length. (20, 40, 60)')
            search()  # allows the user to try again if input is incorrect

        else:  # if input is valid this sequence executes
            print('------------------------------------- INFO ON', search_length,
                  'MM SCREWS ---------------------------------------')
            print('MATERIAL', 'HEAD TYPE', 'LENGTH', '50 Unit box', '100 Unit box', '200 Unit box',
                  'COST PER BOX of 50 (£)', sep=' | ')
            print('--------------------------------------------------------------------------------------------------')

            try:
                # print out all stock of the specified length in table format
                for each_row in screw_list:
                    if search_length in each_row[2]:
                        print('{:^8}{:^14}{:^9}{:^14}{:^15}{:^15}{:^23}'.format(each_row[0], each_row[1], each_row[2],
                                                                                each_row[3], each_row[4], each_row[5],
                                                                                each_row[6]))
            except IndexError:
                print()

            # allow user to search for another length
            keep_searching = input('Would you like to search again? (y/n) ')
            if keep_searching == 'y':
                again = True
            else:
                again = False
                # allow user to return to main menu
                return_to_menu()


def edit_stock():
    # allow user to either increase or decrease the number of boxes of a specified item by a specified amount
    # set up check variables
    stock = False
    size = False

    # ask questions to search for specific stock
    # ask for length
    correct = False
    while correct == False:
        length = input('Specify length (20, 40, 60): ')
        if length == '20' or length == '40' or length == '60':
            correct = True
        else:
            print('ERROR: Please answer with either 20, 40 or 60.')

    # ask for material
    correct = False
    while correct == False:
        material = input('Specify material (brass or steel): ')
        if material == 'brass' or material == 'steel':
            correct = True
        else:
            print('ERROR:  Please answer with either brass or steel.')

    # ask for head type
    correct = False
    while correct == False:
        head = input('Specify head type (slot, star, pozidriv): ')
        if head == 'slot' or head == 'star' or head == 'pozidriv':
            correct = True
        else:
            print('ERROR: Please answer with either slot, star or pozidriv.')

    # once all user input has been validated, find the specified item in stock
    try:
        try:
            for each_row in screw_list:
                if length in each_row[2] and material in each_row[0] and head in each_row[1]:  # validates input to search for
                    print('There are', int(each_row[3]), 'of 50 unit boxes,', int(each_row[4]), 'of 100 unit boxes and',
                          int(each_row[5]), 'of 200 unit boxes available.')

                    # asks user how they'd want to modify the stock number
                    while stock == False:
                        change_stock = input('Would you like to increase or decrease the stock level? ')
                        if change_stock == 'increase' or change_stock == 'decrease':
                            stock = True
                        else:
                            print("Error: You must either answer increase or decrease.")

                    # asks user which box size they'd like to modify
                    while size == False:
                        box_size = input('Which box size would you like to affect? (50, 100, 200) ')
                        if box_size == '50' or box_size == '100' or box_size == '200':
                            size = True
                        else:
                            print('Error: You must choose 50, 100, or 200.')

                    # asks user for a value to increase/decrease the stock by
                    user_value = int(input('By what value would you like to affect the stock by? '))

                    # increase the specified item by value specified by user
                    if change_stock == 'increase' or change_stock == 'Increase':  # if increased user_value is added
                        if box_size == '50':
                            each_row[3] = int(each_row[3]) + user_value
                            print('Total price: £', user_value * float(each_row[6]))
                        elif box_size == '100':
                            each_row[4] = int(each_row[4]) + user_value
                            print('Total price: £', user_value * float(each_row[6]))
                        elif box_size == '200':
                            each_row[5] = int(each_row[5]) + user_value
                            print('Total price: £', user_value * float(each_row[6]))

                    # decrease the specified item by value specified by user
                    if change_stock == 'decrease' or change_stock == 'Decrease':  # if decrease user_value is subtracted
                        if box_size == '50':
                            # check whether there is enough units stock
                            if user_value < int(each_row[3]):
                                each_row[3] = int(each_row[3]) - user_value
                                print('Total price: £', user_value * float(each_row[6]))
                            else:
                                print('There is not enough stock available to complete this order and thus it can only be completed partially.')  # if there is not enough stock user is alerted
                                print('You can only decrease the stock by', each_row[3], 'units.')
                                # if not, ask user if they would like to decrease the stock to 0
                                order = input('Would you still like to decrease the stock? This will set the stock to 0 (y/n) ')  # allows user to cancel order
                                if order == 'y' or order == 'Y':
                                    print('Total price: £', int(each_row[3]) * float(each_row[6]))
                                    each_row[3] = int(each_row[3]) - int(each_row[3])


                        elif box_size == '100':
                            # check whether there is enough units stock
                            if user_value < int(each_row[4]):
                                each_row[4] = int(each_row[4]) - user_value
                                print('Total price: £', user_value * float(each_row[6]))
                            else:
                                print('There is not enough stock available to complete this order and thus it can only be completed partially.')
                                print('You can only decrease the stock by', each_row[4], 'units.')
                                # if not, ask user if they would like to decrease the stock to 0
                                order = input('Would you still like to decrease the stock? (y/n) ')
                                if order == 'y' or order == 'Y':
                                    print('Total price: £', int(each_row[4]) * float(each_row[6]))
                                    each_row[4] = int(each_row[4]) - int(each_row[4])


                        elif box_size == '200':
                            # check whether there is enough units stock
                            if user_value < int(each_row[5]):
                                each_row[5] = int(each_row[5]) - user_value
                                print('Total price: £', user_value * float(each_row[6]))
                            else:
                                print(
                                    'There is not enough stock available to complete this order and thus it can only be completed partially.')
                                print('You can only decrease the stock by', each_row[5], 'units.')
                                # if not, ask user if they would like to decrease the stock to 0
                                order = input('Would you still like to decrease the stock? (y/n) ')
                                if order == 'y' or order == 'Y':
                                    print('Total price: £', int(each_row[5]) * float(each_row[6]))
                                    each_row[5] = int(each_row[5]) - int(each_row[5])

        except ValueError:
            print()
    except IndexError:
        print()

    # allow user to return to main menu
    return_to_menu()


def discount():
    # report to user which screw category has the largest number of stock
    # ask user if they wish to place a 10% discount on the category
    # if a different category is currently the one with the discount, ask the user if they wish to continue with it or stio it.
    # only one category is allowed to be on sale at a time
    unit_count = 0
    largest_stock = 0
    material = ''
    head = ''
    length = ''
    discount_applied = False

    # check which screw type has the most units at the time
    # count the number of units per screw type

    try:
        for each_row in screw_list:
            unit_count = int(each_row[3]) + (int(each_row[4]) * 2) + (int(each_row[5]) * 4)
            # check if the screw type has the largest stock
            if unit_count >= largest_stock:
                largest_stock = unit_count
                # record details of the screw
                material = each_row[0]
                head = each_row[1]
                length = each_row[2]
    except IndexError:
        print('')

    # report the screw type with the most amount of stock
    print("The screw with the most amount of stock is the", material.upper(), 'screw with the',
          head.upper(), 'head type, of length', length, 'at', largest_stock, 'units in stock.')

    try:
        # check if there is any other screw that currently has the discount applied to it
        while discount_applied == False:
            for each_row in screw_list:
                while discount_applied == False:
                    if 'Sale:' in each_row[6]:
                        # resets unit count to the unit count of the current screw with the discount applied to it.
                        unit_count = (int(each_row[3]) + (int(each_row[4]) * 2) + (int(each_row[5]) * 4))
                        print('A 10% discount is currently applied to the', str(each_row[0]).upper(),
                              'type screw with the', str(each_row[1]).upper(), 'head type, of length',
                              each_row[2], 'at', unit_count, 'units in stock.')

                        # ask user if they wish to place a 10% discount on the new category
                        print('Type "y" if you would like to remove this discount and apply it to the',
                              material.upper(), 'screw with the', head.upper(), 'head type, of length',
                              each_row[2], 'at', largest_stock, 'units in stock.', '\nOr "n" to leave the discount on the',
                              each_row[0].upper(), 'type screw with the', each_row[1].upper(), 'head type', end='')

                        apply_discount = input(': ')

                        # remove the discount from the previous item and apply it to the new item
                        each_row = 0  # make sure the screws_list is read from index 0
                        if apply_discount == 'y':
                            for each_row in screw_list:
                                if 'Sale: ' in each_row[6]:
                                    discount_line = each_row[6]
                                    each_row[6] = discount_line.strip('Sale: ')
                                    original_cost = int(each_row[6]) / (1 - 0.1)  # calculate the original cost before discount was applied by dividing it by 1 - discount
                                    each_row[6] = str(original_cost)  # set back to original price
                                    print('Discount has been changed.')

                                    # apply the discount to the correct screw type
                                    each_row = 0  # make sure the screws_list is read from index 0
                                    if material in each_row[0] and head in each_row[1] and length in each_row[2]:
                                        discount_price = float(each_row[6]) * 0.9
                                        each_row[6] = 'Sale: ' + str(discount_price)
                                        discount_applied = True
                                        print('The discount has been successfully applied.')

                    # if no discount has been applied to any of the stock
                    else:
                        print('Currently, the discount has not been added to any of the screws in stock.')
                        # ask user if they wish to place a 10% discount on the category
                        apply_discount = input('Type "y" if you would you like to apply a 10% discount to this screw: ')

                        # apply the discount to screw
                        each_row = 0
                        if apply_discount == 'y':
                            for each_row in screw_list:
                                if material in each_row[0] and head in each_row[1] and length in each_row[2]:
                                    discount_price = float(each_row[6]) * 0.9
                                    each_row[6] = 'Sale: ' + str(discount_price)
                                    discount_applied = True
                                    print('The discount has been successfully applied.')


    except IndexError:
        print()

    # allow user to return to main menu
    return_to_menu()


def chart():
    num_units = []
    length_list = [20, 40, 60]
    left_edges = [0, 10, 20]

    units_20 = 0
    units_40 = 0
    units_60 = 0
    unit_count = 0

    # find the number of units in each length category
    try:
        for each_row in screw_list:
            if '20' in each_row[2]:  # checks each sublist in list for value
                unit_count = (int(each_row[3]) + (int(each_row[4]) * 2) + (int(each_row[5]) * 4))  # turns all boxes into 50 unit ones
                units_20 = units_20 + unit_count  # add number of units of this length to variable
            elif '40' in each_row[2]:
                unit_count = (int(each_row[3]) + (int(each_row[4]) * 2) + (int(each_row[5]) * 4))
                units_40 = units_40 + unit_count  # add number of units of this length to variable
            else:
                unit_count = (int(each_row[3]) + (int(each_row[4]) * 2) + (int(each_row[5]) * 4))
                units_60 = units_60 + unit_count  # add number of units of this length to variable

    except IndexError:
        print()

    # add number of units in all length categories into the unit list
    num_units.append(units_20)
    num_units.append(units_40)
    num_units.append(units_60)

    # plot bar chart
    plt.bar(left_edges, num_units, 7, color=('b', 'm', 'c'))

    plt.title('Stocks per Length Category')
    plt.xlabel('Length')
    plt.ylabel('Number of screws')
    plt.xticks(left_edges, length_list)
    # show bar chart
    plt.show()

    # allow user to return to main menu
    return_to_menu()


# function return_to_menu
def return_to_menu():
    to_menu = input('To return to main menu type y/n: ')
    if to_menu.lower() == 'y':
        print('\n')
        menu()
    else:
        print('Goodbye.')


# call menu function
menu()
