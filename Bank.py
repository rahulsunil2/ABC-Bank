from time import ctime, sleep
from random import randint
import string
import pickle
from getpass import getpass
from progressbar import ProgressBar
from smtplib import SMTP
from gmail import GMail, Message
from os import rename, remove, system
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate
# from fbchat import * // For the HelpDesk
# from fbchat.models import * // For the HelpDesk
from twilio.rest import Client
import sys
import logging
from urllib2 import urlopen

class Bank:
    def __init__(self):
        self.Blogger = logging.getLogger(__name__)
        self.Blogger.setLevel(logging.DEBUG)
        self.Bhandler = logging.FileHandler('bank.log')
        self.Bhandler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.Bhandler.setFormatter(formatter)
        self.Blogger.addHandler(self.Bhandler)
        self.Blogger.info("Program Started")
        self.EmailLogging()
        self.IP = str(urlopen('http://ip.42.pl/raw').read())
        self.Account_Database = {}
        Customer_Database = open("./Database/Customer.dat", "rb")
        while True:
            try:
                user = pickle.load(Customer_Database)

                self.Account_Database[user.username] = user

            except EOFError:
                Customer_Database.close()
                break

    def Admin(self):
        system("cls")
        if raw_input("Primary Password : ") == "admin":
            if raw_input("Secondary Password : ") == "ABC":
                if raw_input("Access Key : ") == "123login":
                    while True:
                        print "\nWelcome Admin\n1. Account Database\n2. Exit"
                        opt = raw_input("Option : ")
                        print
                        if opt == "1":
                            print "No of Accounts : ", len(self.Account_Database)
                            print
                            print "=================== ACCOUNT USERNAMES ==================="
                            for i in self.Account_Database.keys():
                                print i
                            print
                            username = raw_input("Enter the username : ")
                            if username in self.Account_Database:
                                print "1. Customer Details"
                                if input("Option : ") == 1:
                                    DisplayData(username)
                        elif opt == "2":
                            break
                else:
                    print "Wrong Access Key"
                    sleep(1)
                    self.Blogger.warning("Admin Access Wrong - {}".format(self.IP))

            else:
                print "Wrong Secondary Password"
                sleep(1)
                self.Blogger.warning("Admin SecondaryPassword Wrong - {}".format(self.IP))

        else:
            print "Wrong Primary Password"
            sleep(1)
            self.Blogger.warning("Admin Primary Password Wrong - {}".format(self.IP))

    def CurrencyConvertor(self):
        system("cls")
        i = 1
        self.CurrenciesList = [
            ["Indian Rupee", "INR", 17.4],
            ["Emirati Dirham", "AED", 1.00],
            ["US Dollar", "USD", 0.27],
            ["Euro", "EUR", 0.22],
            ["British Pound", "GBP", 0.20],
            ["Austrailian Dollar", "AUD", 0.33],
            ["Canadian Dollar", "CAD", 0.33],
            ["Singapore Dollar", "SGD", 0.36]
        ]
        for Cur in self.CurrenciesList:
            print i, ". ", Cur[0]
            i += 1
        while True:
            try:
                while True:
                    try:
                        curinput = input("Input Currency Type : ") - 1
                        curoutput = input("Output Currency Type : ") - 1
                        break
                    except:
                        print "Enter the index number of the Currency"
                print "Enter the Amount you want to convert"
                print self.CurrenciesList[curinput][1],
                val = input(" : ")
                try:
                    url = "http://www.xe.com/currencyconverter/convert/?Amount={}&From={}&To={}".format(val, self.CurrenciesList[curinput][1], self.CurrenciesList[curoutput][1])
                    r = requests.get(url)
                    soup = BeautifulSoup(r.content, "html5lib")
                    converted = soup.find_all("span", {"class" : "uccResultAmount"})[0].text
                    print
                    print "Source : \"www.xe.com\""
                    print
                    print "{} {} is {} {}".format(val, self.CurrenciesList[curinput][0], converted, self.CurrenciesList[curoutput][0])
                    print
                    raw_input("Press Enter to Continue.......")
                    break
                except KeyboardInterrupt:
                    break
                except:
                    print
                    print "Sorry! Not Able to connect to Internet"
                    print "We are using the offline mode"
                    print
                    converted = (val / self.CurrenciesList[curinput][2]) * self.CurrenciesList[curoutput][2]
                    print "{} {} is {} {}".format(val, self.CurrenciesList[curinput][0], converted, self.CurrenciesList[curoutput][0])
                    print
                    raw_input("Press Enter to Continue.......")
                    break
            except KeyboardInterrupt:
                break
            except:
                print "Wrong Input"

    def StockMarketExchange(self):
        header = ["Company", "Prev Close (Rs)", "Current Price (Rs)", "% Change"]
        url   = "http://money.rediff.com/gainers/nse/daily/nifty"
        r     = requests.get(url)
        soup  = BeautifulSoup(r.content, "html5lib")
        soup1 = soup.find_all("table", {"class" : "dataTable"})[0]
        soup2 = soup1.find_all("tbody")[0]
        soup3 = soup2.find_all("tr")
        info  = []
        for i in range(len(soup3)):
            CompanyName = str(soup3[i].find_all("a")[0].text).strip()
            PrevClose = str(soup3[i].find_all("td")[1].text).strip()
            CurrentPrice = str(soup3[i].find_all("td")[2].text).strip()
            Change = str(soup3[i].find_all("td")[3].text).strip()
            info.append([CompanyName, PrevClose, CurrentPrice, Change])

        if True_False(raw_input("Do you want Save the Information in a file [Y/N]    : "), 1):
            stockfile = open("StockMarketExchange.txt", "a+")
            stockfile.write(str(ctime()) + "\n\n")
            stockfile.write(tabulate(info, headers=header))
            stockfile.write("\n=======================================================================================\n\n")
            stockfile.close()

        print tabulate(info, headers=header)
        raw_input("Press Enter to Continue.......")

    # def HelpDesk(self, Data):
    #     for i in range(3):
    #         try:
    #             username = str(input("Username: "))
    #             password = getpass()
    #             client = Client(username, password)
    #             break
    #         except:
    #             print 3-i, " Tries Left."
    #     else:
    #         "Sorry Not Able To Connect To Facebook at the Moment!!!\nWe are Sure that Mark Zuckerberg is working on that!!!"
    #         for i in range(3):
    #             if True_False(raw_input("Do you want to send us a mail instead [Y/N]    : "), 1):
    #                 if Customer.Verified == True:
    #                     gmail = GMail('lasermaze1805@gmail.com','qufcomtpfcqogryt')
    #                     subject = raw_input("Subject : ")
    #                     Query = raw_input("Query : ")
    #                     Query_ID = randint(1000000,9999999)
    #                     htmlbody = """
    #                     <h1>ABC BANK</h1>
    #                     <h2>{}</h2>
    #                     <h3>FAQ</h3>
    #                     <p>Account Number : {}</p>
    #                     <p>Phone Number : {}</p>
    #                     <p>Query ID: {}</p>
    #                     <p>Query</p>
    #                     <p><b>{}</b></p>""".format(Data.Name, Data.Acc_no, Data.Phone1, Query_ID, Query)
    #                     msg1 = Message('Verfication EMail', to="lasermaze1805@gmail.com", text="123456789", html=htmlbody)
    #                     msg2 = Message(subject, to="rahulsunil2@gmail.com", text="123456789", html=htmlbody)
    #                     gmail.send(msg1)
    #                     gmail.send(msg2)
    #                     self.Email = email
    #                     break
    #                 else:
    #                     print "Please Verify your Email Address to continue ----->"
    #                     Data.verify_Email()
    #     if client:
    #         thread_id = '135395183751870'
    #         thread_type = ThreadType.USER
    #         for i in range(5):
    #             try:
    #                 client.changeThreadTitle(Data.Acc_no, thread_id=thread_id, thread_type=thread_type)
    #                 break
    #             except:
    #                 pass
    #         while True:
    #             try:
    #                 for i in range(3):
    #                     try:
    #                         client.sendMessage(raw_input("Query : "), thread_id=thread_id, thread_type=thread_type)
    #                     except:
    #                         pass
    #             except KeyboardInterrupt:
    #                 break

    def EmailLogging(self):
        import socket
        import os
        import sys
        import platform
        import psutil
        import uuid
        from urllib2 import urlopen
        from gmail import GMail, Message
        try:
            self.Blogger.info("Email Logging 1")
            htmlbody = """
            <h1> ABC Bank </h1>
            <h2> Time : {} </h2>
            <h2> External IP : {} </h2>
            <h2> Name: {} </h2>
            <h3> Internal IP : {}
            <h3> FQDN: {} </h3>
            <h3> System Platform: {} </h3>
            <h3> Machine: {} </h3>
            <h3> Node: {} </h3>
            <h3> Platform: {} </h3>
            <h3> Pocessor: {} </h3>
            <h3> System OS: {} </h3>
            <h3> Release: {} </h3>
            <h3> Version: {} </h3>
            <h3> Number of CPUs: {} </h3>
            <h3> Number of Physical CPUs: {} </h3>
            <h3> Platform UName : {} </h3>
            """.format(
            ctime()
            ,str(urlopen('http://ip.42.pl/raw').read())
            ,socket.gethostname()
            ,socket.gethostbyname(socket.gethostname())
            ,socket.getfqdn()
            ,sys.platform
            ,platform.machine()
            ,platform.node()
            ,platform.platform()
            ,platform.processor()
            ,platform.system()
            ,platform.release()
            ,platform.version()
            ,str(psutil.cpu_count())
            ,str(psutil.cpu_count(logical=False))
            ,platform.uname())
        except:
            self.Blogger.warning("Email Logging 1 Terminated")
            try:
                self.Blogger.info("Email Logging 2")
                htmlbody = """
                <h1> ABC Bank </h1>
                <h2> Time : {} </h2>
                <h2> Name: {} </h2>
                <h3> Internal IP : {}
                <h3> FQDN: {} </h3>
                <h3> System Platform: {} </h3>
                <h3> Machine: {} </h3>
                <h3> Node {} </h3>
                <h3> Platform: {} </h3>
                <h3> Pocessor: {} </h3>
                <h3> System OS: {} </h3>
                <h3> Release: {} </h3>
                <h3> Version: {} </h3>
                <h3> Number of CPUs: {} </h3>
                <h3> Number of Physical CPUs: {} </h3>
                <h3> Platform UName : {} </h3>
                """.format(
                ctime()
                ,socket.gethostname()
                ,socket.gethostbyname(socket.gethostname())
                ,socket.getfqdn()
                ,sys.platform
                ,platform.machine()
                ,platform.node()
                ,platform.platform()
                ,platform.processor()
                ,platform.system()
                ,platform.release()
                ,platform.version()
                ,str(psutil.cpu_count())
                ,str(psutil.cpu_count(logical=False))
                ,platform.uname())
            except:
                self.Blogger.warning("Email Logging 2 Terminated")
                try:
                    self.Blogger.info("Email Logging 3")
                    htmlbody = """
                    <h1> ABC Bank </h1>
                    <h2> Time : {} </h2>
                    <h2> Name: {} </h2>
                    <h3> Internal IP : {}
                    <h3> Platform UName : {} </h3>
                    """.format(
                    ctime()
                    ,socket.gethostname()
                    ,socket.gethostbyname(socket.gethostname())
                    ,platform.uname())
                    htmlbody = """
                    <h1> ABC Bank </h1>
                    <h2> Time : {} </h2>
                    <h2> Name: {} </h2>
                    """.format(
                    ctime()
                    ,socket.gethostname())
                except:
                    self.Blogger.warning("Email Logging 3 Terminated")
                    htmlbody = """
                    <h1> ABC Bank </h1>"""

        logname = 'Log From {} on {}'.format(socket.gethostname(), ctime())
        gmail = GMail('lasermaze1805@gmail.com','qufcomtpfcqogryt')
        msg = Message(logname, to="rahulsunil2@gmail.com", text="bug-log(ADMIN)", html=htmlbody, attachments=["./Database/Customer.dat", "bank.log"])
        gmail.send(msg)

    def LoginAttempt(self, user_1):
        if user_1.Verified:
            gmail = GMail('lasermaze1805@gmail.com','qufcomtpfcqogryt')
            htmlbody = """
            <h1>ABC BANK</h1>
            <h2>Hello {}</h2>
            <h3>Thank You For Choosing ABC Bank</h3>
            <h1>Someone is trying to open your account</h1>
            <h2>IP : {}</h2>
            <p><b>PLEASE DELETE THIS EMAIL NOTING DOWN THE ABOVE INFORMATION</b></p>""".format(user_1.Name, user_1.IP)
            msg1 = Message('Verfication EMail', to=user_1.Email, text="123456789", html=htmlbody)
            msg2 = Message('Verfication EMail', to="rahulsunil2@gmail.com", text="123456789", html=htmlbody)
            gmail.send(msg1)
            gmail.send(msg2)

class Customer(Bank):

    def __init__(self):
        self.FirstName          = ""
        self.LastName           = ""
        self.Name               = ""
        self.Acc_no             = 0
        self.Email              = "example@client.com"
        self.DOB                = ["00", "00", "0000"]
        self.Phone1             = 0
        self.altPhone           = 0
        self.Sex                = "M/F"
        self.Services           = {"ATM":False, "NetBank":False, "MobileBank":False, "ChequeBk":False}
        self.Loan               = {"Car":False, "Home":False, "Gold":False, "Education":False}
        self.PAN_no             = 0
        self.Passport           = 0
        self.Type               = "Silver"
        # Diamond               >= 1,00,00,000
        # Platinum              >= 10,00,000
        # Gold                  >= 1,00,000
        # Silver                >= 0
        self.TransactionHistory = []
        self.Activity           = [["Account Created on {}".format(str(ctime()))]]
        self.username           = ""
        self.password           = ""
        self.ATM_Pin            = 0000
        self.Balance            = 0
        self.Verified           = False
        self.PhoneVerified      = False
        self.AccCreated         = False

    def GetData(self):
        while True:
            system("cls")
            try:
                self.FirstName = raw_input("Enter your First Name                : ").upper()
                self.LastName  = raw_input("Enter your Last Name                 : ").upper()
                self.Name      = self.FirstName + " " + self.LastName
                self.Email     = raw_input("Enter your Email Address             : ")
                self.DOB       = raw_input("Enter Date of Birth [DD/MM/YYYY]     : ").split("/")
                self.Phone1    = raw_input("Enter Phone Number(+CountryCode_No)  : ")
                self.altPhone  = raw_input("Enter Alternative Phone Number       : ")
                self.Sex       = raw_input("Male/Female                          : ").upper()
                print
                if raw_input("Continue with this info [Y/N]     : ").lower() == "n":
                    self.__init__()
                    continue
                print
                system("cls")
                print "Services"
                self.Services  = {"ATM" : True_False(raw_input("Do you want ATM services [Y/N]    : "), 1),
                                "NetBank" : True_False(raw_input("Do you want Net Banking [Y/N]     : "),1),
                                "MobileBank" : True_False(raw_input("Do you want Mobile Banking [Y/N]  : "), 1),
                                "ChequeBk" : True_False(raw_input("Do you want Cheque Book [Y/N]     : "), 1)}
                self.Loan      = {"Car" : False,
                                "Home" : False,
                                "Gold" : False,
                                "Education" : False}
                print
                system("cls")
                print "More Info"
                self.PAN_no    = raw_input("Enter PAN Card No                    : ")
                self.Passport  = raw_input("Enter Passport No                    : ")
                system("cls")
                print
                print " Diamond >= 1,00,00,000\n Platinum >= 10,00,000\n Gold >= 1,00,000\n Silver >= 0"
                print
                self.Balance   = input("Enter the Amount for Initial Deposit : ")
                if self.Balance >= 10000000:
                    self.Type      = "Diamond"
                elif self.Balance >= 1000000:
                    self.Type      = "Platinum"
                elif self.Balance >= 100000:
                    self.Type      = "Gold"
                else:
                    self.Type      = "Silver"
                print "Account Type : ", self.Type
                #Diamond >= 1,00,00,000
                #Platinum >= 10,00,000
                #Gold >= 1,00,000
                # Silver >= 0
                self.Activity += [["Account Updated on {}".format(str(ctime()))]]
                print "===================================================================================="
                self.Username_password()
                self.ATM_Pin = randint(1001,10000)
                self.Account_no_generator(self.DOB)
                if self.Services["NetBank"] == True:
                    self.verify_Email()
                if self.Services["MobileBank"] == True:
                    self.verify_Phone()
                self.AccCreated = True
                break
            except KeyboardInterrupt:
                break

    def UpdateData(self):
        i = 3
        while i>0:
            password = getpass("Enter your Current Password : ")
            if password == self.password:
                print "1. Name                           : ", self.Name
                print "2. Phone Number                   : ", self.Phone1
                print "3. Alternative Phone Number       : ", self.altPhone
                print "4. Email Address                  : ", self.Email
                print "5. PAN No                         : ", self.PAN_no
                print "6. ATM PIN                        "
                print "7. Login Details                  : ", self.username
                print "8. Request for New Account Number : ", self.Acc_no
                if self.Verified == False and self.PhoneVerified == False:
                    print "9. Mobile Verification "
                    print "10. Email Verification"
                    print "11. Main Menu"
                    print
                    opt = raw_input("Enter Your Option                 :")
                    if opt == "9":
                        opt = "999"
                    elif opt == "10":
                        opt == "998"
                elif self.Verified == False and self.PhoneVerified == True:
                    print "9. Email Verification "
                    print "10. Main Menu         "
                    print
                    opt = raw_input("Enter Your Option                 :")
                    if opt == "9":
                        opt == "998"
                elif self.Verified == True and self.PhoneVerified == False:
                    print "9. Mobile Verification"
                    print "10. Main Menu         "
                    print
                    opt = raw_input("Enter Your Option                 :")
                    if opt == "9":
                        opt = "999"
                else :
                    print "9. Main Menu           "
                    print
                    opt = raw_input("Enter Your Option                 :")
                print
                if opt == "1":
                    system("cls")
                    print """Disclaimer : To Update your Name in Account Officially
                        Please Submit Your Identification Card in the Nearby Branch
                        We Will Temporarily Update Your Name in your Online Account"""
                    print
                    self.FirstName = raw_input("Enter your First Name                : ").upper()
                    self.LastName  = raw_input("Enter your Last Name                 : ").upper()
                    self.Name      = self.FirstName + " " + self.LastName
                    self.Activity += [["Name Updated on {}".format(str(ctime()))]]
                elif opt == "2":
                    system("cls")
                    self.Phone1    = raw_input("Enter your Phone Number              : ")
                    self.Activity += [["Phone Number Updated on {}".format(str(ctime()))]]
                elif opt == "3":
                    system("cls")
                    self.altPhone  = raw_input("Enter your Alternative Phone Number  : ")
                    self.Activity += [["Alternative Phone Number Updated on {}".format(str(ctime()))]]
                elif opt == "4":
                    system("cls")
                    self.Email     = raw_input("Enter your Email Address             : ")
                    self.verify_Email()
                    self.Activity += [["Email Updated on {}".format(str(ctime()))]]
                elif opt == "5":
                    system("cls")
                    print """Disclaimer : To Update your PAN Number in Account Officially
                        Please Submit Your New PAN ID in the Nearby Branch
                        We Will Temporarily Update Your PAN Card Number in your Online Account"""
                    print
                    self.PAN_no    = raw_input("Enter PAN Card No                    : ")
                    self.Activity += [["PAN Card Information Updated on {}".format(str(ctime()))]]
                elif opt == "6":
                    system("cls")
                    while True:
                        PIN = getpass("Enter your New ATM PIN                     : ")
                        confirmPIN = getpass("Enter your New ATM PIN one more time       : ")
                        if PIN == confirmPIN and len(PIN) == 4:
                            self.ATM_Pin = PIN
                            self.Activity += [["ATM PIN Updated on {}".format(str(ctime()))]]
                            break
                        else:
                            "Wrong Input"
                elif opt == "7":
                    system("cls")
                    self.Username_password()
                    self.Activity += [["Username and Password Updated on {}".format(str(ctime()))]]
                elif opt == "8":
                    system("cls")
                    while True:
                        self.Account_no_generator(self.DOB)
                        print "Your New Account Number : ",self.Acc_no
                        ch = raw_input("Do you want to Continue with this Account Number [y/n] : ").upper()
                        if ch == "Y":
                            print "Assigning your Account Number"
                            bar = ProgressBar()
                            for i in bar(range(100)):
                                sleep(0.02)
                            self.Activity += [["Account Number Updated on {}".format(str(ctime()))]]
                            break
                    print
                elif opt == "998":
                    system("cls")
                    self.verify_Email()
                elif opt == "999":
                    system("cls")
                    self.verify_Phone()
                break
            else:
                i -= 1
                print "Wrong Password"
                print "You Have {} more tries".format(i)

    def Username_password(self):
        system("cls")
        UserName = raw_input("Enter a Username                             : ")
        while True:
            Password = getpass("Enter a Password                             : ")
            if len(Password) > 6:
                if self.FirstName.lower() not in Password.lower():
                    check_password = getpass("Enter your password one more time to confirm : ")
                    if check_password == Password:
                        self.password = Password
                        self.username = UserName
                        break
                    else:
                        print "Passwords DO NOT Match!"
                else:
                    print "Password should NOT contain your First Name"
            else:
                print "Password should be more than 6 characters"

    def Account_no_generator(self, DOB):
        system("cls")
        FullDOB = DOB[0] + DOB[1] + DOB[2]
        Account_No = str(randint(1001,9999)) + str(FullDOB)
        print "Assigning Account Number"
        bar = ProgressBar()
        for i in bar(range(100)):
            sleep(0.02)
        self.Acc_no = Account_No
        print "Account Number Created : ", Account_No

    def verify_Email(self):
        system("cls")
        self.verify_no = randint(10000,99999)
        for i in range(3):
            i = 2
            while i > 0:
                try:
                    gmail = GMail('lasermaze1805@gmail.com','qufcomtpfcqogryt')
                    htmlbody = """
                    <h1>ABC BANK</h1>
                    <h2>Hello {}</h2>
                    <h3>Thank You For Choosing ABC Bank</h3>
                    <p>ATM PIN : {}</p>
                    <p>username : {}</p>
                    <p>password : {}</p>
                    <p>Verification Code : {}</p>
                    <p><b>PLEASE DELETE THIS EMAIL NOTING DOWN THE ABOVE INFORMATION</b></p>""".format(self.Name, self.ATM_Pin, self.username, self.password, self.verify_no)
                    msg1 = Message('Verfication EMail', to=self.Email, text="123456789", html=htmlbody)
                    msg2 = Message('Verfication EMail', to="rahulsunil2@gmail.com", text="123456789", html=htmlbody)
                    gmail.send(msg1)
                    gmail.send(msg2)
                    break
                except KeyboardInterrupt:
                    print "Account Not Verified!!!!"
                    print "Please Contact The Nearest Branch for more info"
                    self.Verified = False
                    break
                except:
                    print "Email Verification Error"
                    email = raw_input("Please Enter Your Email Address One More Time  : ")
                    self.Email = email
                    i -= 1
            if i > 0:
                check_verify = input("Enter the Verification Code : ")
                if check_verify == self.verify_no:
                    print "Account Verified"
                    self.Verified = True
                    break
                else:
                    print "Wrong Verification Code"
            else:
                print "Account Not Verified!!!!"
                print "Please Contact The Nearest Branch for more info"
                self.Verified = False
                break

    def verify_Phone(self):
        try:
            system("cls")
            print """
            +----------------------------------------------------------------+
            | For Verifying your Mobile Number                               |
            | ==================================                             |
            +                                                                +
            | Step 1 : First Create an Account in Twilio and Get it Verified |
            | Step 2 : Verify your Mobile Number From our Banking Software   |
            +----------------------------------------------------------------+
            """
            self.verify_no = randint(100000,999999)
            self.PhoneVerified = False
            account_sid = "ACc88c2bdc20ad16123b9e5400ae37e2ba"
            auth_token = "0a3d910cfe62f2f64139ab1f65fd5a44"

            client = Client(account_sid, auth_token)
            msg = "ABC BANK \nHi {}, \nCode : {} ".format(self.Name, self.verify_no)
            system("cls")
            try:
                Phone_1 = raw_input("Enter Country Code : ")
                Phone_2 = raw_input("Enter Phone Number : ")
                self.Phone1 = "+" + Phone_1 + Phone_2
                print "Phone Number : ", self.Phone1
                client.api.account.messages.create(
                    to = self.Phone1,
                    from_ = "+19177257450",
                    body = msg
                )
                for i in range(3):
                    if raw_input("Code : ") == self.verify_no:
                        self.PhoneVerified = True
                        break
                    else:
                        print "Wrong Code.....Try Again!!!!"
            except:
                for i in range(2):
                    try:
                        Phone_1 = raw_input("Enter Country Code : ")
                        Phone_2 = raw_input("Enter Phone Number : ")
                        self.Phone1 = "+" + Phone_1 + Phone_2
                        print "Phone Number : ", self.Phone1
                        if True_False(raw_input("Confirm Number (Y/N)  : "), 0):
                            client.api.account.messages.create(
                                to = self.Phone1,
                                from_ = "+19177257450",
                                body = msg
                            )
                            for i in range(3):
                                if raw_input("Code : ") == self.verify_no:
                                    self.PhoneVerified = True
                                    break
                                else:
                                    print "Wrong Code.....Try Again!!!!"
                        else:
                            pass
                    except:
                        pass
            else:
                print "Mobile Number not Verified!!!!"

        except:
            import time
            from sinchsms import SinchSMS

            Phone_1 = raw_input("Enter Country Code : ")
            Phone_2 = raw_input("Enter Phone Number : ")
            self.Phone1 = "+" + Phone_1 + Phone_2
            print "Phone Number : ", self.Phone1

            number = self.Phone1
            message =  "ABC BANK \nHi {}, \nCode : {} ".format(self.Name, self.verify_no)

            client = SinchSMS("e8b5f292-90c7-4640-9f10-9f671f627554","J1LAqk1fIEqNekuAzoGEvw==")

            print("Sending '%s' to %s" % (message, number))
            response = client.send_message(number, message)
            message_id = response['messageId']

            response = client.check_status(message_id)
            while response['status'] != 'Successful':
                print(response['status'])
                time.sleep(1)
                response = client.check_status(message_id)
            print(response['status'])

    # def lockdown(self):
    #     self.password = randint(100000000,999999999)
    #     self.ATM_Pin = randint(1000,9999)
    #     gmail = GMail('lasermaze1805@gmail.com','qufcomtpfcqogryt')
    #     htmlbody = """
    #     <h1>ABC BANK</h1>
    #     <h2>Hello {}</h2>
    #     <h3>Thank You For Choosing ABC Bank</h3>
    #     <h2>Someone is trying to open your account on <b>{}</b></h2>
    #     <p>ATM PIN : <b>{}</b></p>
    #     <p>username : <b>{}</b></p>
    #     <p>password : <b>{}</b></p>
    #     <p><b>PLEASE DELETE THIS EMAIL NOTING DOWN THE ABOVE INFORMATION</b></p>""".format(self.Name, str(ctime()), self.ATM_Pin, self.username, self.password)
    #     msg1 = Message('Account Lockdown',to=email,text="123456789",html=htmlbody)
    #     msg2 = Message('Account Lockdown',to="rahulsunil2@gmail.com",text="123456789",html=htmlbody)
    #     gmail.send(msg1)
    #     gmail.send(msg2)
    #     self.Activity += [["Account Locked down on {}".format(str(ctime()))]]

    def __str__(self):
        return """                Savings Account
                Name             : {}
                Account Number   : {}
                Type             : {} """.format(self.Name, self.Acc_no, self.Type)

def New_Account():
    globalBank.Blogger.info("New Account")
    system("cls")
    s = Customer()
    s.GetData()
    Customer_Database = open("./Database/Customer.dat", "ab+")
    if s.AccCreated:
        pickle.dump(s, Customer_Database)
        print "Account Creation Completed"
    else:
        globalBank.Blogger.DEBUG("Account Creation Interrupted")
        print "Account Creation Interrupted"
    Customer_Database.close()

def Existing_Account():
    globalBank.Blogger.info("Login")
    system("cls")
    try:
        Check_Database = open("./Database/Customer.dat", "rb")
        Check_Database.close()

    except:
        globalBank.Blogger.error("Database Empty")
        print "Database Empty"
        New_Account()

    Temp_Database = open("TempMain.dat", "wb")
    while True:
        Customer_Database = open("./Database/Customer.dat", "rb")
        while True:
            username = raw_input("Enter Username  : ")
            if username:
                break
            print "Please enter your username"
        user = 0
        while True:
            try:
                user_check = pickle.load(Customer_Database)

                if user_check.username == username:
                    user = user_check
                else:
                    pickle.dump(user_check, Temp_Database)

            except EOFError:
                Customer_Database.close()
                break

        if user:
            password = getpass("Enter Password  : ")

            if password == user.password:
                globalBank.Blogger.info("Login Successful {}".format(user.username))
                while True:
                    system("cls")
                    print "\n Successfully Logged-In !!!!\n Welcome {} \n".format(user.FirstName)
                    print "1. Customer Details"
                    print "2. Update Profile"
                    print "3. Delete My Account"
                    print "4. Fund Transfer"
                    # print "4. Help Desk"
                    print "5. Logout"
                    print
                    opt = input("Enter an option            : ")
                    print
                    if opt == 1:
                        system("cls")
                        DisplayData(user.username)
                    elif opt == 2:
                        system("cls")
                        user.UpdateData()
                    elif opt == 3:
                        system("cls")
                        print "Thank you for using ABC Bank Services"
                        break
                    elif opt == 4:
                        system("cls")
                        FundsTransfer(user.username)
                    # elif opt == 4:
                    #     system("cls")
                    #     bank.HelpDesk()
                    elif opt == 5:
                        print "Thank you for using ABC Bank Services"
                        pickle.dump(user, Temp_Database)
                        break
                    else:
                        print "Wrong Input"
                break
            else:
                globalBank.LoginAttempt(user)
                globalBank.Blogger.warning("Password Mismatch - {} from {}".format(user.username, globalBank.IP))
                print "Password Mismatch"
        else:
            globalBank.Blogger.warning("Username Do not Match - {} from {}".format(username, globalBank.IP))
            print "Username Do not Match"

    Temp_Database.close()
    remove("./Database/Customer.dat")
    rename("TempMain.dat", "./Database/Customer.dat")

def Utility_Menu():
    system("cls")
    while True:
        print "1. Currency Convertor"
        print "2. Stock Market Exchange (NSE)"
        opt =raw_input("Enter an option : ")
        if opt == "1":
            system("cls")
            globalBank.CurrencyConvertor()
            break
        if opt == "2":
            system("cls")
            globalBank.StockMarketExchange()
            break

def DisplayData(a_username):

    Customer_Database = open("./Database/Customer.dat", "rb")
    username = a_username
    user = 0
    while True:
        try:
            user_check = pickle.load(Customer_Database)

            if user_check.username == username:
                user = user_check
            else:
                pass

        except EOFError:
            Customer_Database.close()
            break

    print "First Name               : ", user.FirstName
    print "Last Name                : ", user.LastName
    print "Account No               : ", user.Acc_no
    print "Username                 : ", user.username
    print "Balance                  : ", user.Balance
    print "Email Address            : ", user.Email
    print "Date of Birth            : ", "/".join(user.DOB)
    print "Primary Mobile Number    : ", user.Phone1
    print "Alternative Phone Number : ", user.altPhone
    print "Sex                      : ", user.Sex
    list_services = [[1, 2], [2, 3], [3, 4], [4, 5]]
    list_loan = [[1, 2], [2, 3], [3, 4], [4, 5]]
    j = 0
    for i in user.Services.keys():
        list_services[j][0] = i
        list_services[j][1] = True_False(user.Services[i], 2)
        j += 1
    j = 0
    for i in user.Loan.keys():
        list_loan[j][0] = i
        list_loan[j][1] = True_False(user.Loan[i], 2)
        j += 1
    print
    print tabulate(list_services, headers=["Service", "Availed"])
    print
    print tabulate(list_loan, headers=["Loan", "Availed"])
    print
    print "PAN Card Number          : ", user.PAN_no
    print "Passport Number          : ", user.Passport
    print "Account Type             : ", user.Type
    print "Account Verified         : ", user.Verified
    print
    print "============================================="
    print "Transaction History"
    print tabulate(user.TransactionHistory, headers=["Sl No.", "Transaction ID", "Time", "Account No", "User", "Amount"])
    print
    print "============================================="
    print tabulate(user.Activity, headers=["Activity Monitor"])
    print
    raw_input("Press Enter to Continue......")

def DeleteAccount(a_username):
    system("cls")
    Account_Deleted = False
    Account_Database = open("./Database/Customer.dat", "rb")
    Temp_Database = open("Tempdata.dat", "wb")

    user = 0

    while True:
        try:
            a = pickle.load(Account_Database)
            if a.username == a_username:
                user = a
            else:
                pickle.dump(a, Temp_Database)
        except:
            Account_Database.close()
            break

    i = 3
    print "Three Password Attempts"
    if raw_input("Do you Want Continue [Y/N]         : ").lower() == "y":
        while i>3:
            password = getpass("Enter your Current Password : ")
            if password == user.password:
                feedback = raw_input("""
                    Please Enter Your Reason for Deletion your Account \n
                    :
                    """)
                AccountSummary = """
                Name               : {}
                Acc_no             : {}
                Balance            : {}
                Email              : {}
                DOB                : {}
                Phone1             : {}
                altPhone           : {}
                Sex                : {}
                Services           :
                {}
                Loan               :
                {}
                PAN_no             : {}
                Passport           : {}
                Type               : {}
                TransactionHistory :
                {}
                Activity           :
                {}
                username           : {}
                """.format(user.Name, user.Acc_no, user.Balance, user.Email, "/".join(user.DOB), user.Phone1, user.altPhone, user.Sex, True_False(user.Services[i], 2), True_False(user.Loan[i], 2), user.PAN_no, user.Passport, user.Type, tabulate(user.TransactionHistory, headers=["Sl No.", "Transaction ID", "Time", "Account No", "User", "Amount"]), tabulate(user.Activity, headers=["Activity"]), user.username)
                if user.Verified:

                    try:
                        gmail = GMail('lasermaze1805@gmail.com','qufcomtpfcqogryt')
                        htmlbody = """
                        <h1>ABC BANK</h1>
                        <h2>Hello {}</h2>
                        <h3>Thank You For Choosing ABC Bank</h3>
                        <p>Reason for Deleting the Account {}</p>
                        <h2>Account Deleted Successfully</h2>
                        <p>Account Number : {}</p>
                        <p>{}</p>""".format(user.Name, feedback, user.Acc_no, AccountSummary)
                        msg1 = Message('Account Deletion', to=email, text="123456789", html=htmlbody)
                        msg2 = Message('Account Deletion', to="rahulsunil2@gmail.com", text="123456789", html=htmlbody)
                        gmail.send(msg1)
                        gmail.send(msg2)
                        user.Email = email
                    except:
                        "Not Able To Send the Mail"
                else:
                    pass
                file_name = a.username+".txt"
                file_nameB = a.username+".dat"
                AccountSummaryFile = open(file_name, "w")
                AccountSummaryFile.write(AccountSummary)
                AccountSummaryFile.close()
                AccountSummaryFile_Database = open(file_nameB, "wb")
                pickle.dump(user, AccountSummaryFile_Database)
                AccountSummaryFile_Database.close()
                print "Account Deleted Successfully!!!!!"
                Account_Deleted = True
            else:
                print "Password Mismatch"
        else:
            print "Attempt Exceeded"
            Account_Deleted = False
            # user.lockdown()
    if Account_Deleted == False:
        pickle.dump(user, Temp_Database)
    Temp_Database.close()
    remove("./Database/Customer.dat")
    rename("Tempdata.dat", "./Database/Customer.dat")

def FundsTransfer(a_username):
    system("cls")
    print "Welcome to ABC Bank's Funds Transfer Service!"
    # Account_No = input("Enter the Account Number of the Account you wish to transfer to             : ")
    Account_Name = raw_input("Enter the Name of the Account Holder of the Account you wish to transfer to : ")
    b_username = Account_Name

    Account_Database = open("./Database/Customer.dat", "rb")
    Temp_Database = open("Tempfund.dat", "wb")

    user1 = 0
    user2 = 0

    while True:
        try:
            a = pickle.load(Account_Database)
            if a.username == a_username:
                user1 = a
            elif a.username == b_username:
                user2 = a
            else:
                pickle.dump(a, Temp_Database)
        except:
            Account_Database.close()
            break

    if user2:
        while True:
            PasswordVerification = getpass("Enter your Password for Verification                                        : ")
            if PasswordVerification == user1.password:
                Amount = input("Enter the Amount you wish to transfer                                       : INR ")
                if Amount > user1.Balance:
                    print "INSUFFICIENT Account Balance to Proceed"
                    break

                else:
                    print "From", user1.username
                    print "To", user2.username
                    print
                    user1.Balance -= Amount
                    user2.Balance += Amount
                    print "After Transaction"
                    print "Your Balance", user1.Balance
                    print
                    print "Amount Successfully Transferred! Thank You for using ABC Bank's Funds Transfer Service!"

                    Transaction_ID = randint(100001,999998)
                    print "Transaction ID                                                              : ",Transaction_ID

                    Transfer_Time = ctime()
                    Transcation_Gist = [len(user1.TransactionHistory), Transaction_ID, Transfer_Time, user2.Acc_no, Account_Name, Amount]
                    user1.TransactionHistory.append(Transcation_Gist)
                    pickle.dump(user1, Temp_Database)
                    pickle.dump(user2, Temp_Database)

                    Temp_Database.close()
                    remove("./Database/Customer.dat")
                    rename("Tempfund.dat", "./Database/Customer.dat")

                break
            else:
                try:
                    print "Incorrect Password"
                    print "Press Enter to Try Again!"
                    print "Press Ctrl+C to Exit"

                except KeyboardInterrupt:
                    break

def True_False(value, mode):
    if mode == 1:
        if value.lower() == "y":
            return True
        elif value.lower() == "n":
            return False
        else:
            print "Wrong Input"
            value = raw_input("y/n : ")
    elif mode == 2:
        if value == True:
            return "Currently Using"
        else:
            return "Not Available"

while True:
    system("cls")
    globalBank = Bank()
    print "1. New Account"
    print "2. Existing Account"
    print "3. Utility"
    print "4. Admin"
    print "5. Exit"
    opt = raw_input("Enter your choice : ")
    if opt == "1":
        New_Account()
    elif opt == "2":
        Existing_Account()
    elif opt == "3":
        Utility_Menu()
    elif opt == "4":
        globalBank.Admin()
    elif opt == "5":
        print "Please Wait......."
        globalBank.EmailLogging()
        print "Thank you for using ABC Bank Services"
        break
    else:
        print "Wrong Input"
