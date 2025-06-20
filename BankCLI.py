from prettytable import PrettyTable
import stdiomask
import mysql.connector as sql
import random
import csv
mycon=sql.connect(host='localhost',user='root',passwd='Shubham@2003')
cursor=mycon.cursor()
cursor.execute('create database if not exists bankdb')
cursor.execute('use bankdb')
cursor.execute('create table if not exists login_and_register(username varchar(255) unique     not null,password varchar(255) unique not null)')
cursor.execute('create table if not exists bank(accno int primary key not null,name varchar(50) not null,mobile varchar(10) not null,email varchar(50) not null,address varchar(100) not null,city varchar(20) not null,state varchar(20) not null,country varchar(20) not null,balance float not null)')
cursor.execute('create table if not exists banktrans(accno int,amount float,date_of_trans datetime default now(),trans_desc varchar(50),trans_ref varchar(100),foreign key (accno) references bank(accno) on delete cascade on update cascade)')
mycon.commit()

def login_and_register():
    while True:
        print('1.ADMIN')
        print('2.CUSTOMER')
        print('3.EXIT WINDOW')
        user1=input('Enter your choice:')
        if user1=='1':
            while True:
                try:
                    print('1.LOGIN')
                    print('2.REGISTER')
                    print('3.FORGET PASSWORD')
                    print('4.EXIT')
                    user=input('Enter your choice:')
                    if user=='2':
                        choice=input('Are you a Bank Administrator(Y/N):')
                        if choice=='y' or choice=='Y':
                            username=input('Set username:')
                            password=stdiomask.getpass('Set password:')
                            password1=stdiomask.getpass('Confirm the password:')
                            if password==password1:
                                cursor.execute("insert into login_and_register values(%s, %s)", (username, password))
                                mycon.commit()
                                print('Registerd successfully \n')
                            else:
                                print('Password mismatch \n')
                        elif choice=='n' or choice=='N':
                            print('Registration Denied !! \n')
                            pass
                        else:
                            print('Wrong choice entered \n')

                    elif user=='1':
                        username=input('Enter your username:')
                        password=stdiomask.getpass('Enter your password:')
                        cursor.execute("select password from login_and_register where username=%s", (username,))
                        data=cursor.fetchone()
                        if data and data[0] == password:
                            print('Login successfully \n')
                            print(f'welcome {username} to our bank')
                            while True:
                                menu()
                                ch=input('Enter your Choice:')
                                menu_actions = {
                                    '1': create,
                                    '2': deposit,
                                    '3': withdraw,
                                    '4': balance_enquiry,
                                    '5': mini_statement,
                                    '6': display,
                                    '7': transfer,
                                    '8': modify,
                                    '9': close,
                                    '10': account,
                                    '11': export_,
                                    '12': exporttrans,
                                    '13': lambda: print('Exitting... \n')
                                }

                                action = menu_actions.get(ch)
                                if action:
                                    if ch == '13':
                                        action()
                                        break
                                    else:
                                        action()
                                else:
                                    print('Wrong choice entered \n')
                        else:
                            print('Invalid Username and Password \n')
                            

                    elif user=='3':
                        username =input('Enter the username:')
                        cursor.execute("select * from login_and_register where username='{}'".format(username))
                        data = cursor.fetchall()
                        if cursor.rowcount>=1:
                            for i in data:
                                i=list(i)
                                if i[0]==username:
                                    i[1]=stdiomask.getpass("Set your new password:")
                                    password=stdiomask.getpass("Confirm your new password:")
                                    if i[1]==password:
                                        cursor.execute("update login_and_register set password=%s where username=%s", (i[1], i[0]))
                                        mycon.commit()
                                        print("Password changed sucessfully \n")
                                    else:
                                        print('Password mismatch \n')
                        else:
                            print('Username not found \n')

                    elif user=='4':
                        print('Exitting....\n')
                        break
                    else:
                        print('Wrong choice entered \n')
                except TypeError:
                    print('Invalid Username and Password \n')
                    continue
                except sql.Error:
                    print('Username and Password already taken \n')
                    continue

        elif user1=='2':
            accno=int(input('Enter the account number:'))
            cursor.execute("select name from bank where accno='{}'".format(accno))
            data=cursor.fetchone()
            if cursor.rowcount==1:
                print(f'WELCOME {data[0]} TO OUR BANK')
                while True:
                    menu1()
                    ch = input('Enter your Choice:')
                    customer_menu_actions = {
                        '2': deposit,
                        '3': withdraw,
                        '4': balance_enquiry,
                        '5': mini_statement,
                        '7': transfer,
                        '12': exporttrans,
                        '13': lambda: print('Exitting... \n')
                    }
                    action = customer_menu_actions.get(ch)
                    if action:
                        if ch == '13':
                            action()
                            break
                        else:
                            action()
                    else:
                        print('Wrong choice entered \n')
                        break
            else:
                print('Account not found \n')

        elif user1=='3':
            print('Exiting... \n')
            break

        else:
            print('Wrong choice entered \n')

def menu():
    print('MAIN MENU')
    print('1.CREATE ACCOUNT')
    print('2.DEPOSIT ACCOUNT')
    print('3.WITHDRAW ACCOUNT')
    print('4.BALANCE ENQUIRY')
    print('5.MINI STATEMENT')
    print('6.DISPLAY ACCOUNT')
    print('7.TRANSFER ACCOUNT')
    print('8.MODIFY ACCOUNT DETAILS')
    print('9.CLOSE ACCOUNT')
    print('10.ACCOUNT HOLDERS')
    print('11.EXPORT ACCOUNTS')
    print('12.EXPORT TRANSCATION DETAILS')
    print('13.LOGOUT \n')
    
def menu1():
    print('MAIN MENU')
    print('2.DEPOSIT ACCOUNT')
    print('3.WITHDRAW ACCOUNT')
    print('4.BALANCE ENQUIRY')
    print('5.MINI STATEMENT')
    print('7.TRANSFER ACCOUNT')
    print('12.EXPORT TRANSCATION DETAILS')
    print('13.LOGOUT \n')
    

def create():
    while True:
        print('All required fields are mandatory')
        accno=random.randint(100,999999)
        name=input('Enter name:').upper()
        mobile=int(input('Enter mobile number:'))
        email=input('Enter email:')
        address=input('Enter address:').upper()
        city=input('Enter city:').upper()
        state=input('Enter state:').upper()
        country=input('Enter country:').upper()
        balance=float(input('Enter balance:'))
        query = "insert into bank(accno,name,mobile,email,address,city,state,country,balance) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (accno, name, mobile, email, address, city, state, country, balance))
        mycon.commit()
        print('Your account number is :',accno)
        print('Account created successfully \n')
        ch=input('Do you want to enter more records?(Y/N)')
        if ch=='n' or ch=='N':
            break

def deposit():
    try:
        accno = int(input('Enter the account number to be deposited:'))
        cursor.execute("select balance from bank where accno=%s", (accno,))
        if cursor.fetchone():
            balance = float(input('Enter the amount to be deposited:'))
            if balance <= 0:
                print('Deposit amount must be positive.\n')
                return
            trans_desc = 'deposited'
            cursor.execute("insert into banktrans(accno,amount,trans_desc) values (%s, %s, %s)", (accno, balance, trans_desc))
            cursor.execute("update bank set balance=balance+%s where accno=%s", (balance, accno))
            mycon.commit()
            print('Amount deposited successfully \n')
            cursor.execute("select balance from bank where accno=%s", (accno,))
            data = cursor.fetchone()
            if data:
                print('Your New Balance:', data[0])
                print('\n')
        else:
            print('Account not found \n')
    except Exception as e:
        print('Error:', e)

def withdraw():
    try:
        accno = int(input('Enter the account number:'))
        cursor.execute("select balance from bank where accno=%s", (accno,))
        data = cursor.fetchone()
        if data:
            current_balance = data[0]
            balance = float(input('Enter the amount to be withdrawn:'))
            if balance <= 0:
                print('Withdrawal amount must be positive.\n')
                return
            if balance > current_balance:
                print('Insufficient funds.\n')
                return
            if current_balance - balance < 5000:
                print('Cannot withdraw: minimum balance of 5000 must be maintained.\n')
                return
            trans_desc = 'withdrawn'
            cursor.execute("insert into banktrans(accno,amount,trans_desc) values (%s, %s, %s)", (accno, balance, trans_desc))
            cursor.execute("update bank set balance=balance-%s where accno=%s", (balance, accno))
            mycon.commit()
            print('Amount withdrawn successfully \n')
            cursor.execute("select balance from bank where accno=%s", (accno,))
            new_balance = cursor.fetchone()
            print('Your Remaining Balance:', new_balance[0])
        else:
            print('Account not found \n')
    except Exception as e:
        print('Error:', e)

def balance_enquiry():
    try:
        accno=int(input('Enter the account number:'))
        cursor.execute("select balance from bank where accno=%s", (accno,))
        data=cursor.fetchone()
        for row in data:
            print('Your Current Balance:',row)
            print('\n')
    except:
        print('Account Not Found \n')


def mini_statement():
    try:
        cursor = mycon.cursor(buffered=True)
        accno = int(input('Enter the account number:'))
        query = "select amount,date_of_trans,trans_desc,trans_ref from banktrans where accno=%s"
        cursor.execute(query, (accno,))
        data = cursor.fetchall()
        if data:
            h = PrettyTable(['amount', 'date_of_trans', 'trans_desc', 'trans_ref'])
            for amount, date_of_trans, trans_desc, trans_ref in data:
                h.add_row([amount, date_of_trans, trans_desc, trans_ref])
            print(h)
            print('\n')
        else:
            print('No records found \n')
    except:
        print('Account Not Found \n')

def display():
    def show_accounts(query, param=None):
        cursor.execute(query, param or ())
        data = cursor.fetchall()
        if cursor.rowcount >= 1:
            h = PrettyTable(['accno','name','mobile','email','address','city','state','country','balance'])
            for accno, name, mobile, email, address, city, state, country, balance in data:
                h.add_row([accno, name, mobile, email, address, city, state, country, balance])
            print(h)
        else:
            print('No records found \n')

    while True:
        print('1.ACCOUNT NUMBER')
        print('2.NAME WISE SEARCH')
        print('3.ADDRESS WISE SEARCH')
        print('4.CITY WISE SEARCH')
        print('5.STATE WISE SEARCH')
        print('6.COUNTRY WISE SEARCH')
        print('7.EXIT')
        susi = input('On what context you want to search?:')
        if susi == '1':
            try:
                accno = int(input('Enter the account number to display:'))
                show_accounts('SELECT * FROM bank WHERE accno=%s', (accno,))
            except:
                print('Account Not Found \n')
        elif susi == '2':
            name = input('Enter name:')
            show_accounts("SELECT * FROM bank WHERE name LIKE %s", (f'%{name}%',))
        elif susi == '3':
            address = input('Enter address:')
            show_accounts("SELECT * FROM bank WHERE address LIKE %s", (f'%{address}%',))
        elif susi == '4':
            city = input('Enter city:')
            show_accounts("SELECT * FROM bank WHERE city LIKE %s", (f'%{city}%',))
        elif susi == '5':
            state = input('Enter state:')
            show_accounts("SELECT * FROM bank WHERE state LIKE %s", (f'%{state}%',))
        elif susi == '6':
            country = input('Enter country:')
            show_accounts("SELECT * FROM bank WHERE country LIKE %s", (f'%{country}%',))
        elif susi == '7':
            print('Exitting... \n')
            break
        else:
            print('Wrong choice entered \n')
            break

def transfer():
    try:
        accno1=int(input('Enter the account number:'))
        accno2=int(input('Enter the account number to be transferred:'))
        balance=float(input('Enter amount to be transferred:'))
        trans_desc1='to transfer'
        trans_desc2='by transfer'
        cursor.execute("insert into banktrans(accno,amount,trans_desc,trans_ref) values (%s, %s, %s, %s)", (accno1, balance, trans_desc1, f'transfer to {accno2}'))
        cursor.execute("update bank set balance=balance-%s where accno=%s", (balance, accno1))
        cursor.execute("insert into banktrans(accno,amount,trans_desc,trans_ref) values (%s, %s, %s, %s)", (accno2, balance, trans_desc2, f'transfer from {accno1}'))
        cursor.execute("update bank set balance=balance+%s where accno=%s", (balance, accno2))
        mycon.commit()
        print('Amount Transferred Successfully \n')
    except:
        print('Account Not Found \n')

def modify():
    try:
        accno = int(input('Enter The Account Number:'))
        cursor.execute('select * FROM bank WHERE accno=%s', (accno,))
        data = cursor.fetchall()
        if cursor.rowcount >= 1:
            for i in data:
                i = list(i)
                fields = [
                    ("name", 1, str.upper),
                    ("mobile", 2, str),
                    ("email", 3, str),
                    ("address", 4, str.upper),
                    ("city", 5, str.upper),
                    ("state", 6, str.upper),
                    ("country", 7, str.upper)
                ]
                for field_name, idx, transform in fields:
                    s = input(f'Change {field_name.capitalize()} (Y/N): ')
                    if s.lower() == 'y':
                        value = input(f'Enter {field_name.capitalize()}: ')
                        i[idx] = transform(value)
                    elif s.lower() == 'n':
                        pass
                    else:
                        print('Wrong choice entered')
                        break
                cursor.execute("update bank set name=%s, mobile=%s, email=%s, address=%s, city=%s, state=%s, country=%s where accno=%s", (i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[0]))
                mycon.commit()
                print('Account Updated Successfully \n')
                break
        else:
            print('Account Not Found \n')
    except:
        print('Account Not Found \n')       


def close():
    try:
        accno = input('Enter the account number:')
        cursor.execute('select accno from bank where accno=%s', (accno,))
        data = cursor.fetchone()
        if data:
            cursor.execute('select * from bank where accno=%s', (accno,))
            cursor.execute('delete from bank where accno=%s', (accno,))
            mycon.commit()
            print('Account Deleted Successfully \n')
        else:
            print('Account Not Found \n')
    except:
        print('Account Not Found \n')

def account(): 
    cursor=mycon.cursor(buffered=True)       
    cursor.execute('select * from bank;')
    if cursor.rowcount>0:
        data=cursor.fetchall()
        h=PrettyTable(['accno','name','mobile','email','address','city','state','country','balance'])
        for accno,name,mobile,email,address,city,state,country,balance in data:
            h.add_row([accno,name,mobile,email,address,city,state,country,balance])
        print(h)
        print('\n')      
    else:
        print('No records found \n')

def export_():
    print('This file should be in csv or txt, No other file extension should be used')
    filename = input('Enter the filename to be exported:')
    cursor.execute('select * from bank')
    data = cursor.fetchall()
    if cursor.rowcount >= 1:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
            print('File exported successfully \n')
    else:
        print('No results found \n')

def exporttrans():
    accno = input('Enter the account number:')
    filename = input('Enter the filename to be exported:')
    cursor.execute('select * from banktrans where accno=%s', (accno,))
    data = cursor.fetchall()
    if cursor.rowcount >= 1:
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(data)
            print('File exported successfully \n')
    else:
        print('No results found \n')

login_and_register()
