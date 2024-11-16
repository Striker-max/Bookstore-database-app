### --- Compulsory Task: Capstone Project - Databases --- ###
#=====Importing Required Libraries=====
import sqlite3
from tabulate import tabulate

#=====Function Section=====
# Display book table from database
def book_table():
    col_names = ['id', 'title', 'author', 'qty']
    cursor.execute('''SELECT * FROM book''')
    view_records = cursor.fetchall()
    print(tabulate(view_records, col_names, tablefmt = 'grid'))
    return view_records


# Display single record from book table
def book_record(record):
    col_names = ['id', 'title', 'author', 'qty']
    list_record = [record]
    print(tabulate(list_record, col_names, tablefmt = 'grid'))


# Check for duplicates
def duplicate_check(new_book):
    id_counter = 0
    title_counter = 0
    cursor.execute('''SELECT * FROM book''')
    all_records = cursor.fetchall()
    for record in all_records:
        if new_book[0] == record[0]:
            id_counter +=1
        elif new_book[1] == record[1]:
            title_counter += 1
    if id_counter >= 1 or title_counter >= 1:
        return True
    else:
        return False


# Check if book already exists to be updated
def book_exist(new_book):
    book_counter = 0
    cursor.execute('''SELECT * FROM book''')
    all_records = cursor.fetchall()
    for record in all_records:
        if new_book == record[0]:
            book_counter +=1
    if book_counter >= 1:
        return True
    else:
        return False


# Check that inputs are integers
def integer_check(choice):
    while True:  
        try: 
            return int(choice)
        except ValueError:
            print("Invalid entry. Please enter an integer.")
            sec_choice = input()
            return integer_check(sec_choice)
        

# Check that correct inputs are given for Y/N
def char_check(choice):
    current_choice = choice.upper()
    if current_choice == 'Y' or current_choice == 'N':
        return current_choice
    else:
        new_choice = input("Invalid entry. Please Y or N.\n")
        return char_check(new_choice)
        

# Search results from book table
def search_table(search_result):
    print("See search results below:")
    book_record(search_result)
    db.commit()


#=====Database Section=====
# Create database named 'ebookstore' and table named 'book'
db = sqlite3.connect('ebookstore_db.db')
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS book
               (id INTEGER PRIMARY KEY, title TEXT, author TEXT, 
               qty INTEGER)''')

# Add entries to table in database
book_entries = [(3001,'A Tale of Two Cities', 'Charles Dickens', 30),
                 (3002, 'Harry Potter and the Philosopher''s Stone', 
                  'J.K. Rowling', 40),
                 (3003, 'The Lion, the Witch and the Wardrobe', 
                  'C. S. Lewis', 25),
                 (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37),
                 (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)]
cursor.executemany('''INSERT OR IGNORE INTO book(id, title, author, qty)
               VALUES(?, ?, ?, ?)''', (book_entries))
db.commit()

#=====Menu Section=====
while True:
    menu_choice = int(input('''Please select one of the following options:
1. Enter book
2. Update book
3. Delete book
4. Search books
0. Exit
'''))

# Add new record to book table          
    if menu_choice == 1:
        new_id = input("Please enter new book id: ")
        checked_id = integer_check(new_id)
        new_title = input("Please enter new book title: ")
        new_author = input("Please enter new book author: ") 
        new_qty = input("Please enter quantity of new book available: ")
        checked_qty = integer_check(new_qty)
        new_book = (checked_id, new_title, new_author, checked_qty)
        duplicate = duplicate_check(new_book)
        if duplicate == True:
            print("Sorry. A book with similar information already exists.\n")
            continue
        else:
            cursor.execute('''INSERT INTO book(id, title, author, 
                           qty) VALUES(?, ?, ?, ?)''', (new_book))
            db.commit()
            print("New book added to database.\n")
            continue

# Update record in book table     
    elif menu_choice == 2:
        same_count = 0
        record_table = book_table()
        book_id = input("Please enter id of book that needs to be updated: ")
        update_id = integer_check(book_id)
        update_duplicate = book_exist(update_id)
        if update_duplicate == True:
            for record in record_table:
                if update_id == record[0]:
                    choice_title = input(
                        "Does the title need to change? (Y/N): ")
                    change_title = char_check(choice_title)
                    if change_title == 'Y':
                        update_title = input("Please provide updated title: ")
                    elif change_title == 'N':
                        update_title = record[1] 
                        same_count += 1
                    choice_author = input(
                        "Does the author need to change? (Y/N): ")
                    change_author = char_check(choice_author)
                    if change_author == 'Y':
                        update_author = input(
                            "Please provide updated author: ")
                    elif change_author == 'N':
                        update_author = record[2]
                        same_count += 1
                    choice_qty = input(
                        "Does the quantity need to change? (Y/N): ")
                    change_qty = char_check(choice_qty)
                    if change_qty == 'Y':
                        book_qty = input("Please provide updated quantity: ")
                        update_qty = integer_check(book_qty)
                    elif change_qty == 'N':
                        update_qty = record[3]
                        same_count += 1
                    update_record = [update_title, update_author, update_qty, 
                                     update_id]
                    if same_count == 3:
                        print("No changes made to records.\n")
                    else:
                        cursor.execute('''UPDATE book SET title = ?, 
                                       author = ?, qty = ? WHERE id = ?''', 
                                       (update_record))
                        db.commit()
                        print("Book information updated in database.\n")
        else:
            print("Book id provided does not exist in database.")
        continue

# Delete record from book table   
    elif menu_choice == 3:
        del_table = book_table()
        del_record = input(
"Please enter the id of the book that should be deleted from the database: ")
        del_row = integer_check(del_record)
        for record in del_table:
            if del_row == record[0]:
                cursor.execute('''DELETE FROM book WHERE id = ?''', (del_row,))
                db.commit()
                print("Book deleted from database.\n")
            else:
                print("Book id provided does not exist in database.")
        continue

# Find a specific record in book table 
    elif menu_choice == 4:  
        while True:
            input_par = input(
'''Which parameter would you like to use to find a book?
1. Book id
2. Book title
3. Book author
4. Quantity of book available
''')
            search_par = integer_check(input_par)
            if search_par == 1:
                input_id = input("Please input id: ")
                search_id = integer_check(input_id)
                cursor.execute('''SELECT * FROM book WHERE id = ?''', 
                               (search_id,))
                search_result = cursor.fetchone()
                search_table(search_result)
                break
            if search_par == 2:
                search_title = input("Please input title: ")
                cursor.execute('''SELECT * FROM book WHERE title = ?''', 
                               (search_title,))
                search_result = cursor.fetchone()
                search_table(search_result)
                break
            if search_par == 3:
                search_author = input("Please input author: ")
                cursor.execute('''SELECT * FROM book WHERE author = ?''', 
                               (search_author,))
                search_result = cursor.fetchone()
                search_table(search_result)
                break
            if search_par == 4:
                input_qty = input("Please input quantity: ")
                search_qty = integer_check(input_qty)
                cursor.execute('''SELECT * FROM book WHERE qty = ?''', 
                               (search_qty,))
                search_result = cursor.fetchone()
                search_table(search_result)
                break
            else:
                print("Invalid input. Please try again.")
        continue

# Exit database 
    elif menu_choice == 0:
        print('Thank you!')
        break 

# Restart loop if incorrect input given for menu
    else:
        print("Invalid input. Please try again.")

# Close database
db.close() 

