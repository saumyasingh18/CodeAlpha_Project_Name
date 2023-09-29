# TASK 1 - Password generator
# DATE - 01/09/2023 
# PROGRAMMER- Saumya singh (saumyasingh635@gmail.com)
import random
import string
# defining class for password generation
class password_gen:
    
    # defining function to generate random password
    def random_pass():
       sym=['@','#','?','$']
       #setting default value for the variables
       dig=upper=lower=symbol=''
       for i in range(2):
          dig=dig+random.choice(string.digits)
          upper=upper+random.choice(string.ascii_uppercase)
          lower=lower+random.choice(string.ascii_lowercase)
          symbol=symbol+random.choice(sym)
       #generating password by combining different parts i.e. letter,alphabet and symbols
       temp_pass=upper+dig+symbol+lower
       #retuning the password to calling part
       return temp_pass
    
    # defining function to generate customized password
    def custom_pass():
       # defining function to generate customized password
       dig=''
       sym=['@','#','?','$']
      # accepting keywords for generating customized password
       keyword1=input("Enter first keyword (eg. name,item)")
       keyword2=input("Enter second keyword (eg. name,item)")
       upper=keyword1[0]+keyword1[1]+keyword1[2]
       lower=keyword2[0]+keyword2[1]
       for i in range(2):
         dig=dig+random.choice(string.digits)
         symbol=random.choice(sym)
      #generating password by combining different parts i.e. letter,alphabet and symbols
       temp_password=upper.upper()+dig+symbol+lower
       #retuning the password to calling part
       return(temp_password)
    #exiting the functions and calling the above functions
    #creating a menu option for user
    print("\t\tPassword Generator\t\t\n\t\tMENU\t\t\nPRESS")
    print("1.Generate random password\n2.Generate customised password\n3.Exit")
    #accepting users choice
    ch=int(input('Enter your choice\n'))
    # running loop till option 3 ie. EXIT is selected
    while ch!=3:
         #runs if option 1 ie. random password generation is selected
         if ch==1:
             print('Password:\n',random_pass())
             next=int(input('Press\n4.Generate next random password\nPress any number key to go back'))
             while next==4:
                print('Password:\n',random_pass())
                next=int(input('Press\n4.Generate next random password\nPress any number key to go back'))
         #runs if option 2 ie. customized password generation is selected
         elif ch==2:
            print('Password:',custom_pass())
            next=int(input('Press\n4.Generate next custom password\nPress any number key to go back'))
            while next==4:
                print('Password:',custom_pass())
                next=int(input('Press\n4.Generate next custom password\nPress any number key to go back'))
         #runs if any number except 1,2 or 3 is selected
         else:
            print('INVALID CHOICE')
         print("1.Generate random password\n2.Generate customised password\n3.Exit")
         ch=int(input('Enter your option\n'))
      #while loop ends is option 3 ie. EXIT is selected
   