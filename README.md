# ABC-Bank

**AIM**				*The aim of this project is to provide a small scale simulation of an  e-medium for banking. 
				This project collects  information from the customer, confirms its validity and performs related facilities for
				the user. The admin has access to the functions of creating, updating, etc. The information is stored  to be 
				further used in a binary database.*
	
	
	
	
	
**_Functions_**

    
1 **Bank()**            		        *Contains the basic features such as the login of the admin as well as the customer,
                         		the creation of  the primary database as well as additional features as the 
                         		currency converter and the live stock exchange details.*

  - **Admin ()**				          	*Contains the login features of the admin account.*

                            
  - **CurrencyConvertor ()**		        *Contains the features of the currency converter feature.*
                            
  - **StockMarketExchange()**	            *Contains the features of the Stock Market Exchange feature*


2 **Customer()**                      *Contains the backbone features of the project as the collection, verification,
                                    storage of data, etc. & misc. details like the activity monitor, 
                                    details of currency conversions etc.*

  - **GetData()**				            *To accept information from the customer.*

  - **UpdateData()**			            *To modify information of the customer*

  - **Username_password()**	                *For the creation of a valid customer password.*

  - **Account_no_generator()**	            *For the generation of the customer account no.*

  - **verify_Email()**			            *Contains features for the verification of the customer account like via mail, SMS, etc.*

  - **New_Account()**			            *Appending of a new account into the db.*

  - **Existing_Account()**	                *Verification and features for an existing	account.*


  - **Utility_Menu()**			            *Contains the  redirection menu of the utility features.*
                          
  - **DisplayData()**				        *For displaying the customer	data*

  - **DeleteAccount()**			            *For the deletion of a customer account*

  - **FundsTransfer ()**				    *For the transaction of money between customer	accounts*

  - **#Lockdown ()**			            *To alert the customer of a possible intrusion due to wrong password input via mail.*

  - **#Helpdesk ()**					    *A feedback helpdesk for	the customers*


