# IMPORTING NECESSARY MODULES
import mysql.connector
from datetime import datetime
# GLOBAL VARIABLES DECLARATION
myConnnection =""
cursor=""
userName=""
password =""
cid=""
#TO CHECK MYSQL CONNECTIVITY
def MYSQLconnectionCheck ():
    global myConnection
    global userName
    global password
    userName = input("\n ENTER MYSQL SERVER'S USERNAME : ")
    password = input("\n ENTER MYSQL SERVER'S PASSWORD : ")

    myConnection=mysql.connector.connect(host="localhost",user=userName,passwd=password ,auth_plugin='mysql_native_password' )
    if myConnection:
        print("\n CONGRATULATIONS ! YOUR MYSQL CONNECTION HAS BEEN ESTABLISHED !")
        cursor=myConnection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ATM")
        cursor.execute("COMMIT")
        cursor.close()
        return myConnection
    else:
        print("\nERROR ESTABLISHING MYSQL CONNECTION CHECK USERNAME AND PASSWORD !")

# TO ESTABLISHED MYSQL CONNECTION
def MYSQLconnection ():

  global userName
  global password
  global myConnection

  myConnection=mysql.connector.connect(host="localhost",user=userName,passwd=password ,database="ATM" , auth_plugin='mysql_native_password' )
  if myConnection:
      return myConnection
  else:
      print("\nERROR ESTABLISHING MYSQL CONNECTION !")
      myConnection.close()
# TO CREATE NEW CUSATOMER
def newCustomer():
  global cid
  if myConnection:
     cursor=myConnection.cursor()
     createTable ="""CREATE TABLE IF NOT EXISTS CUSTOMER(CID VARCHAR(10) PRIMARY KEY,CNAME VARCHAR(30) NOT NULL,ADDRESS VARCHAR(30)NOT NULL ,PHONE VARCHAR(12) NOT NULL)"""
     cursor.execute(createTable)
     print("\nPlease Fill All The Information Carefully !")
     cid=input("Please Enter Customer ID : ")
     cname=input("Please Enter Customer Name : ")
     address=input("Please Enter Customer Address : ")
     phone=input("Please Enter Customer Contact No. : ")
     sql='INSERT INTO CUSTOMER(cid,cname,address,phone) values(%s,%s,%s,%s)'
     values=(cid,cname,address,phone)
     cursor.execute(sql,values)
     cursor.execute("COMMIT")
     cursor.close()
     print("\nNew Customer Added Successfully !")

# TO DISPLAY CUSTOMER INFORMATION :
def displayAllCustomer():
   if myConnection:
      cursor=myConnection.cursor()
      cursor.execute("SELECT * FROM CUSTOMER")
      data = cursor.fetchall()
      if data:
         print("\n*****DETAILS OF ALL CUSTOMER*****")
         print(data)
      else:
        print("Sorry ! No Record Found , Please Try Again ! ")
   else:
      print("\nERROR ESTABLISHING MYSQL CONNECTION !")

# TO SEARCH A CUSTOMER
def searchCustomer():
   global cid
   if myConnection:
       cursor=myConnection.cursor()
       cid=input("Please Enter Customer ID : ")
       sql="SELECT * FROM CUSTOMER WHERE CID = %s"
       values=(cid,)
       data=cursor.execute(sql,values)
       data = cursor.fetchall()
       if data:
          print("\n*****CUSTOMER DETAILS*****")
          print(data)
       else:
          print("Sorry ! Customer NOT Found , Please Try Again ! ")
   else:
       print("\nSomething Went Wrong ,Please Try Again !")

# TO OPEN A NEW ACCOUNT
def newAccount():
   global cid
   if myConnection:
      cursor=myConnection.cursor()
      cid=input("Please Enter Customer ID : ")
      createTable ="""
                    CREATE TABLE IF NOT EXISTS ACCOUNT(
                        CID VARCHAR(10),
                        ACCOUNT_NO INT(15) PRIMARY KEY,
                        ACCOUNT_TYPE VARCHAR(20) NOT NULL ,
                        AMOUNT INT(10) NOT NULL ,
                        PIN INT(4) NOT NULL UNIQUE  ) """
      cursor.execute(createTable)
      account_no=int(input("PLEASE ENTER THE ACCOUNT NUMBER [0-9]: "))
      account_type=input("PLEASE ENTER THE ACCOUNT TYPE [ S-SAVING / C - CURRENT ]: ")
      amount=int(input("PLEASE ENTER THE AMOUNT TO DEPOSIT : "))
      ATM_pin=int(input("PLEASE ENTER THE ATM PIN [ FOUR DIGITIS ONLY ] : "))
      sql='INSERT INTO ACCOUNT (cid,account_no,account_type,amount ,pin) VALUES (%s,%s,%s,%s,%s)'
      values1=(cid,account_no,account_type,amount,ATM_pin)
      cursor.execute(sql,values1)
      cursor.execute("COMMIT")
      print("\nNew Account Opened Successfully !") 

   else:
      print("\nSomething Went Wrong ,Please Try Again !")
#TO DISPLAY ALL ACCOUNTS
def displayAllAccounts():

   if myConnection:
      cursor=myConnection.cursor()
      cursor.execute("SELECT * FROM ACCOUNT")
      data = cursor.fetchall()
      if data:
         print("\n*****DETAILS OF ALL ACCOUNTS*****")
         print(data)
      else:
         print("Sorry ! No Account Information , Please Try Again ! ")
   else:
      print("\nERROR ESTABLISHING MYSQL CONNECTION !")


# TO SEARCH AN ACCOUNT
def searchAccount():
   global cid
   if myConnection:
      cursor=myConnection.cursor()
      cid=input("PLEASE ENTER CUSTOMER ID : ")
      account_no=int(input("PLEASE ENTER THE ACCOUNT NUMBER [0-9]: "))
      sql="SELECT * FROM ACCOUNT WHERE CID = %s AND ACCOUNT_NO =%s"
      values=(cid,account_no)
      data=cursor.execute(sql,values)
      data = cursor.fetchall()
      if data:
          print("\n*****CUSTOMER ACCOUNT DETAILS*****")
          print(data)
      else:
          print("Sorry ! Account Information NOT Found , Please Try Again ! ")
   else:
       print("Something Went Wrong ,Please Try Again !")
# TO WITHDRAW AMOUNT
def withdrawAmount():
   count =3
   if myConnection:
       cursor=myConnection.cursor()
       account_no=int(input("PLEASE ENTER THE ACCOUNT NUMBER [0-9]: "))
       cid=int(input(" PLEASE ENTER THE CUSTOMER ID : "))
       sql="SELECT * FROM ACCOUNT WHERE ACCOUNT_NO =%s"
       values=(account_no,)
       data=cursor.execute(sql,values)
       data = cursor.fetchall()
       if data:
           while True:
              ATM_PIN=int(input("PLEASE ENTER THE ATM PIN - ONLY 3 ATTEMPTS ARE ALLOWED : "))
              sql='SELECT * FROM ACCOUNT WHERE PIN = %s'
              values=(ATM_PIN,)
              cursor.execute(sql,values)
              currentdate=datetime.now()
              data = cursor.fetchall()
              if data:
                  amount=int(input("PLEASE ENTER AMOUNT TO WITHDRAW : "))
                  sql='UPDATE ACCOUNT SET AMOUNT = AMOUNT - %s'
                  cursor.execute(sql ,(amount,))
                  cursor.execute("COMMIT")
                  withdrawaltable = """
                          CREATE TABLE IF NOT EXISTS WITHDRAWALS(
                          CID VARCHAR(10),
                          ACCOUNT_NO INT(15),
                          WITHDRAWN_AMOUNT INT(10) NOT NULL ,
                          DATE_OF_WITHDRAWAL DATE) """
                  cursor.execute(withdrawaltable)
                  sql1='INSERT INTO WITHDRAWALS (CID,ACCOUNT_NO,WITHDRAWN_AMOUNT,DATE_OF_WITHDRAWAL) VALUES (%s,%s,%s,%s)'
                  values2=(cid, account_no,amount,currentdate)
                  cursor.execute(sql1, values2)
                  cursor.execute("COMMIT")
                  print("******* TRANSACTION SUCCESSFULLY COMPLETED ! *******")
                  print("***** PLEASE REMOVE YOUR CARD ! *****")
                  break
              else:
                  print("Wrong Pin ! Please enter a Valid PIN")
                  count=count-1
                  print("You are left with only ",count ,"Attempts")
              if count == 0:
                  print("Your Card has been Blocked , Please Visit the Branch to activate it")
                  break
       else:
            print("Sorry ! Account Information NOT Found , Please Try Again ! ")
# TO DEPOSIT AMOUNT
def depositAmount():
    count=3
    if myConnection:
       cursor=myConnection.cursor()
       account_no=int(input("PLEASE ENTER THE ACCOUNT NUMBER [0-9]: "))
       cid=int(input(" PLEASE ENTER THE CUSTOMER ID : "))
       sql="SELECT * FROM ACCOUNT WHERE ACCOUNT_NO =%s"
       values=(account_no,)
       data=cursor.execute(sql,values)
       data = cursor.fetchall()
       if data:
           while True:
              ATM_PIN=int(input("PLEASE ENTER THE ATM PIN - ONLY 3 ATTEMPTS ARE ALLOWED : "))
              sql='SELECT * FROM ACCOUNT WHERE PIN = %s'
              values=(ATM_PIN,)
              cursor.execute(sql,values)
              currentdate=datetime.now()
              data = cursor.fetchall()
              
              if data:
                  Damount=int(input("PLEASE ENTER AMOUNT TO DEPOSIT : "))
                  sql='UPDATE ACCOUNT SET AMOUNT = AMOUNT + %s'
                  cursor.execute(sql ,(Damount,))
                  cursor.execute("COMMIT")
                  depositiontable = """
                    CREATE TABLE IF NOT EXISTS DEPOSITS(
                    CID VARCHAR(10),
                    ACCOUNT_NO INT(15),
                    DEPOSITED_AMOUNT INT(10) NOT NULL ,
                    DATE_OF_DEPOSITION DATE) """
                  cursor.execute(depositiontable)
                  sql2='INSERT INTO DEPOSITS (CID,ACCOUNT_NO,DEPOSITED_AMOUNT,DATE_OF_DEPOSITION) VALUES (%s,%s,%s,%s)'
                  values3=(cid, account_no,Damount,currentdate)
                  cursor.execute(sql2, values3)
                  cursor.execute("COMMIT")
                  print("******* TRANSACTION SUCCESSFULLY COMPLETED ! *******")
                  print("***** PLEASE REMOVE YOUR CARD ! *****")
                  break
              else:
                print("Wrong Pin ! Please enter a Valid PIN")
                count=count-1
                print("You are left with only ",count ,"Attempts")
                if count == 0:
                   print("Your Card has been Blocked , Please Visit the Branch to activate it")
                   break
    else:
       print("Sorry ! Account Information NOT Found , Please Try Again ! ")
# TO VIEW BALANCE
def viewBalance():
    if myConnection:
      cursor=myConnection.cursor()
      cursor.execute("SELECT * FROM ACCOUNT")
      data = cursor.fetchall()
      if data:
          account_no=int(input("PLEASE ENTER THE ACCOUNT NUMBER [0-9]: "))
          cid=int(input(" PLEASE ENTER THE CUSTOMER ID : "))
          sql3="SELECT AMOUNT FROM ACCOUNT WHERE ACCOUNT_NO =%s"
          values4=(account_no,)
          data1=cursor.execute(sql3,values4)
          data1 = cursor.fetchall()
          print("\n*****ACCOUNT BALANCE*****")
          print(str(data1))
      else:
        print("Sorry ! No Record Found , Please Try Again ! ")
    else:
      print("\nERROR ESTABLISHING MYSQL CONNECTION !")
    
# TO PROVIDE HELP FOR USER
def helpMe():
    print("Please, Visit The Official Website of SCS To Download The Manual !!!")
    print(" Kindly visit the front office for further queries")
    print(" THANK YOU!")

# MAIN SCREEN
    print("***************** SUBBIAH CENTRAL  ***************")
    print("**************** SCS - ATM MANAGER ***************")
    print("*****Designed and Maintained By:")
    print("*****NAKSHATRA.R - CLASS XII A ")
    print("*****AMIRTHA VARSHINI.N.J - CLASS XII A ")
    print("*****KARUPPANA HARI.S - CLASS XII A ")
    
#STARTING POINT OF THE SYSTEM
myConnection = MYSQLconnectionCheck ()
if myConnection:
    MYSQLconnection ()
    while(1):
        
        print("***************** SUBBIAH CENTRAL  ***************")
        print("**************** SCS - ATM MANAGER ***************")
        print("*****Designed and Maintained By:")
        print("*****NAKSHATRA.R - CLASS XII A ")
        print("*****AMIRTHA VARSHINI.N.J - CLASS XII A ")
        print("*****KARUPPANA HARI.S - CLASS XII A ")
        print("\n!=========================*************=======================!")
        print("! PLEASE ENTER 1 FOR NEW USER !")
        print("! PLEASE ENTER 2 TO DISPLAY ALL CUSTOMERS !")
        print("! PLEASE ENTER 3 TO SEARCH A CUSTOMER !")
        print("! PLEASE ENTER 4 TO OPEN NEW ACCOUNT !")
        print("! PLEASE ENTER 5 TO DISPLAY ALL ACCOUNTS !")
        print("! PLEASE ENTER 6 TO SEARCH AN ACCOUNT !")
        print("! PLEASE ENTER 7 TO WITHDRAW AMOUNT !")
        print("! PLEASE ENTER 8 TO DEPOSIT AMOUNT !")
        print("! PLEASE ENTER 9 TO VIEW BALANCE !")
        print("! PLEASE ENTER 10 TO EXIT !")
        print("! PLEASE ENTER 0 FOR HELP !")
        print("\n!============================*****END*****====================!")
        choice = int(input("\n Please Enter Your Choice : "))
        if choice == 1:
            newCustomer()
        elif choice == 2:
            displayAllCustomer()
        elif choice == 3:
             searchCustomer()
        elif choice == 4:
             newAccount()
        elif choice==5:
             displayAllAccounts()
        elif choice==6:
             searchAccount()
        elif choice==7:
             withdrawAmount()
        elif choice==8:
            depositAmount()
        elif choice==9:
            viewBalance()
        elif choice==10:
             break
        elif choice==0:
             helpMe()
        else:
             print("Sorry ,kindly enter the correct input, Please Try Again !!! ")
else:
    print("Check Your MYSQL Connection First !!! ")

## END OF THE PROJECT
## THANK YOU
## BY NAKSHATRA.R , AMIRTHA VARSHINI.N.J , KARUPPANA HARI.S OF XII - A

