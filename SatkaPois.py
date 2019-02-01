"""
Python 3 program for helping reduce smoking.

Members of the project:
    Toni Bomström
    Kasper Eklund
    Joona Kallio

Program implemented as part of university studies in University of Oulu.
2018
"""

# __________ Imports __________
import random
import os
import time
import datetime
import webbrowser
from getpass import getpass


def open_links():
    """
    Opens all hardcoded links with the default web browser.
    """
    global links
    i = 1
    
    for link in links:
        webbrowser.open(link[1], new=i, autoraise=True)
        if i == 1:
            i = 2
            
def daterange(start_date, end_date):
    """
    Counts the date difference.
    """
    for i in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(i)
        
def update_info():
    """
    Updates user info to the user account file (like "X.user").
    """
    global register_date
    global current_date
    global cigarette_count
    global cigarettes
    global goal
    cigarette_list = [] # Helps reformat information in cigarettes-dictionary for writing in file
    
    # Builds a list with items of type [date,cigarette_count]
    for single_date in daterange(register_date, current_date):
        if single_date.strftime("%Y-%m-%d") in cigarettes.keys():
            cigarette_list.append(single_date.strftime("%Y-%m-%d") + ":" + str(cigarettes[single_date.strftime("%Y-%m-%d")]))
    cigarette_list = ";".join(cigarette_list)
    
    # Read the password from user file before overwriting
    with open(user[0]+".user", "r") as source:
        password = source.readline().rstrip("\n")
    
    # Overwrite user's info in the file with all current informations
    with open(user[0]+".user", "w") as source:
        source.write(password + "\n")
        source.write(str(register_date) + "\n")
        source.write(str(cigarettes_per_day) + "\n")
        source.write(cigarette_list + "\n")
        # If goal is set
        if goal != []:
            source.write(goal[0].strftime("%Y-%m-%d")+";"+goal[1].strftime("%Y-%m-%d")+";"+str(goal[2])+"\n")
        # If goal is not set
        else:
            source.write("0;0;0\n")
            
## ------------- "SWITCH CASE" FUNCTIONS -------------

## Input code 1 - Always
def smoking_information():
    """
    Displays information about the dangers of smoking.
    """
    global links
    global information
    answer = ""
    i = 0
    
    while True:
        
        os.system('cls')  # Clear screen on windows
        print("{}\n{}TUPAKOINNIN VAARAT{}\n{}\n".format("="*80, "-"*31, "-"*31,"="*80))
        
        # Information about smoking
        for j, row in enumerate(information):
            print(row)
            if row[-1] == ")":
                input("\n---------- PAINA ENTER JATKAAKSESI TULOSTUSTA ----------")
                print("")

        print("{}\n".format("="*80))
    
        answer = input("\nMitä haluat tehdä?\n\n1 - Tarkista lähteet\n2 - Palaa päävalikkoon\n>")
        
        # Shows references
        if answer == "1":
            print("\n{} LÄHTEET {}\n".format("="*36, "="*35))
            
            i = 0
            # Provides references with links for verifiability
            for link in links:
                print("{}\n{}\n".format(link[0], link[1]))
                if (i+1)%5 == 0 and information[i] != information[-1]:
                    input("\n---------- PAINA ENTER JATKAAKSESI TULOSTUSTA ----------")
                    print("")
                i += 1
            print("\n{}\n".format("="*80))
            answer = ""
            while answer not in ["1","2","Y","N","K","E"]:
                answer = input("Haluatko avata linkit oletusselaimella?\n\n1 - Kyllä\n2 - En\n>")
                
                # Opens the reference links with default browser
                if answer.upper() in ["1","Y","K"]:
                    open_links()
                    print("Linkit avattu!\n")
                    print("\n{}PAINA ENTER JATKAAKSESI{}".format("-"*29, "-"*28))
                    input()
                    
                # User doesn't want to open links
                elif answer in ["2","N","E"]:
                    pass
                
                # Bad input
                else:
                    print("\nKäskyä ei ymmärretty! Yritä uudestaan.\n")
                    print("\n{}PAINA ENTER JATKAAKSESI{}".format("-"*29, "-"*28))
                    input()
                    break
        
        # Return to main menu
        elif answer == "2":
            break
        
        else:
            print("\nKäskyä ei ymmärretty! Yritä uudestaan.\n")
            print("\n{}PAINA ENTER JATKAAKSESI{}".format("-"*29, "-"*28))
            input()
            
    print("\n{}PAINA ENTER JATKAAKSESI{}".format("-"*29, "-"*28))
    input()

## Input code 2 - Logged in
def input_data():
    """
    Asks the user to input the number of smoked cigarettes for the days that
    haven't been assigned a cigarette count.
    """
    global register_date
    global current_date
    global cigarettes
    cigarette_count = -1
    
    os.system('cls')  # Clear screen on windows
    print("{}\n{}SAVUKKEIDEN MÄÄRIEN KIRJAAMINEN{}\n{}\n\n".format("="*80, "-"*25, "-"*24,"="*80))

    for single_date in daterange(register_date, current_date):
        # If date doesn't have inputted cigarette count
        if single_date.strftime("%Y-%m-%d") not in cigarettes.keys():
            # Ask for cigarette count
            while cigarette_count < 0 or cigarette_count > 10000:
                print("Syötä {} polttamiesi savukkeiden lukumäärä >".format(single_date.strftime("%d.%m.%Y")), end="")
                try:
                    cigarette_count = int(input())
                    if cigarette_count < 0: # Cannot be negative
                        print("Savukkeiden lukumäärä ei saa olla negatiivinen! Yritä uudestaan.\n")
                    if cigarette_count > 10000: # Limited to 10 000 cigarettes a day (User has to be a unbelievable chain smoker to top this)
                        print("Savukkeiden lukumäärä ei saa olla yli 10 000! Yritä uudestaan.\n")
                except ValueError:
                    print("Syötä savukkeiden lukumäärä kokonaislukuna! Yritä uudestaan.\n")
            cigarettes[single_date.strftime("%Y-%m-%d")] = cigarette_count
        cigarette_count = -1 # Resets cigarette_count for the next iteration
    update_info()
    print("Kaikki tiedot ajantasalla, tarkista huomenna uudelleen!\n")
    print("\n{}PAINA ENTER JATKAAKSESI{}".format("-"*29, "-"*28))
    input()

## Input code 3 - Logged in
def manage_goal():
    """
    """
    global goal
    global current_date
    global cigarettes
    global days_missed
    global rewards
    cigarette_count = 0
    answer = ""
    goal_length = -1
    loop = True
    reward = random.randint(0,1) # Randomly determine which reward picture to show
    goal_complete = False
    
    os.system('cls')  # Clear screen on windows
    print("{}\n{}OMA TAVOITTEESI{}\n{}\n\n".format("="*80, "-"*33, "-"*32,"="*80))
    
    # Days without cigarette counts exist
    if days_missed != 0:
        print("Et ole ilmoittanut {} päivän savukemääriä.\nIlmoita kyseisten päivien savukemäärät tarkastellaksesi tavoitettasi.\n".format(days_missed))
    
    # Goal exists
    elif goal != []:
        # Counts inputted cigarette counts up to current date 
        if goal[1] > current_date:
            for single_date in daterange(goal[0], current_date):
                if single_date.strftime("%Y-%m-%d") in cigarettes.keys():
                    cigarette_count += int(cigarettes[single_date.strftime("%Y-%m-%d")])
        
        # Counts inputted cigarette counts up to goal end date
        else:
            for single_date in daterange(goal[0], goal[1]):
                if single_date.strftime("%Y-%m-%d") in cigarettes.keys():
                    cigarette_count += int(cigarettes[single_date.strftime("%Y-%m-%d")])
        
        print("{} -- {}\n{}/{} savuketta".format(goal[0].strftime("%d.%m.%Y"), goal[1].strftime("%d.%m.%Y"), cigarette_count, goal[2]))
        
        # Goal has not been achieved nor failed
        if (goal[1]-current_date).days > 0 and cigarette_count <= int(goal[2]):
            print("{} päivä(ä) jäljellä\n".format(str((goal[1]-current_date).days)))
            print("\n{}\n".format("="*80))
            while answer.upper() not in ["1","Y","K","2","N","E"]:
                answer = ""
                answer = input("Haluatko resetoida tavoitteen?\n\n1 - Kyllä\n2 - En\n>")
                if answer in ["1","Y","K"]:
                    goal = []
                    update_info()
                    print("\nTavoite resetoitu!\n")
        
        # Goal has been achieved or failed
        else:
            # Success
            if cigarette_count <= int(goal[2]):
                print("\nOnnistuit tavoitteessasi!\n")
                for row in rewards[reward]:
                    print(row[0])
                goal_complete = True
                print("\n{}PAINA ENTER JATKAAKSESI{}".format("-"*29, "-"*28))
                input()
            # Failure
            else:
                print("\nNoh, aina ei voi onnistua. Tämä ottelu hävittiin, mutta sota ei ole vielä ohi!\nSeuraavalla kerralla sinä pystyt siihen!\n")
                goal_complete = True
                print("\n{}PAINA ENTER JATKAAKSESI{}".format("-"*29, "-"*28))
                input()
    
    # No active goal
    else:
        while loop:
            answer = input("Sinulla ei vaikuttaisi olevan aktiivista tavoitetta.\nHaluatko asettaa tavoitteen?\n\n1 - Kyllä\n2 - En\n>")
            
            # Set a goal
            if answer.upper() in ["1","Y","K"]:
                answer = ""
                while loop:
                    print("\nVoit keskeyttää tavoitteen asettamisen milloin vain syöttämällä arvon 0.")
                    answer = input("\nKuinka pitkän aikavälin tavoitteen haluat asettaa?\n\n0 - Keskeytä\n1 - Viikko\n2 - 2 Viikkoa\n3 - 3 Viikkoa\n4 - 1 Kuukausi\n>")
                    
                    # Goal setting interrupted
                    if answer == "0":
                        print("Tavoitteen asettaminen keskeytetty!\n")
                        loop = False
                        break
                    
                    # Length for goal given received
                    elif answer in ["1","2","3","4"]:
                        goal_length = int(answer)
                        answer = ""
                        
                        # Asking for cigarette goal
                        while loop:
                            print("\nVoit keskeyttää tavoitteen asettamisen milloin vain syöttämällä arvon 0.")
                            answer = input("Syötä savukemäärätavoite (savukkeiden lukumäärä) >")
                            try:
                                if int(answer) < 0: # Cannot be negative value for cigarette count
                                    print("Savukemäärä ei saa olla negatiivinen! Yritä uudestaan.\n")
                                elif int(answer) > 100000: # Avoiding OverflowError by limiting goal maximum
                                    print("Savukemäärä ei saa ylittää 100 000! Yritä uudestaan.\n")
                                elif int(answer) == 0: # Goal setting interrupted by user
                                    print("Tavoitteen asettaminen keskeytetty!\n")
                                    loop = False
                                    break
                                else:
                                    goal.append(current_date)
                                    goal.append(current_date + datetime.timedelta(days=7*goal_length))
                                    goal.append(int(answer))
                                    update_info()
                                    print("\nTavoite asetettu!\n")
                                    loop = False
                            except ValueError:
                                print("Savukemäärän tulee olla kokonaisluku. Yritä uudestaan.\n")
                    else:
                        print("\nKäskyä ei ymmärretty! Yritä uudestaan.\n")
                        print("\n{}PAINA ENTER JATKAAKSESI{}".format("-"*29, "-"*28))
                        input()
            
            # Don't set a goal
            elif answer.upper() in ["2","N","E"]:
                break
            
            # Bad input
            else:
                print("\nKäskyä ei ymmärretty! Yritä uudestaan.\n")
                print("\n{}PAINA ENTER JATKAAKSESI{}".format("-"*29, "-"*28))
                input()
                
    # If goal is achieved or failed
    if goal_complete:
        print("\nAktiivinen tavoitteesi on saapunut päätökseen.\n")
        while True:
            answer = input("Haluatko resetoida tavoitteen (jotta voit asettaa uuden)?\n\n1 - Kyllä\n2 - En\n>")
            
            # Reset goal
            if answer.upper() in ["1","Y","K"]:
                goal = []
                update_info()
                print("\nTavoite resetoitu!\n")
                break
            
            # No changes to be made
            elif answer.upper() in ["2","N","E"]:
                break
            
            # Bad input
            else:
                print("\nKäskyä ei ymmärretty! Yritä uudestaan.\n")
                print("\n{}PAINA ENTER JATKAAKSESI{}".format("-"*29, "-"*28))
                input()
                
    print("\n{}PAINA ENTER JATKAAKSESI{}".format("-"*29, "-"*28))
    input()

## Input code 4 - Logged in
def user_information():
    """
    Displays user's
        account name,
        registration date,
        their own set average for cigarettes per week,
        calculation of cigarettes per month,
        number of cigarettes smoked,
        number of days since registration,
        average smokes per day,
        and reminder if user hasn't submitted cigarette counts for all days passed.
    User can also check all cigarette smoking data collected.
    """
    global register_date
    global current_date
    global cigarettes_per_day
    global days_missed
    global ask_for_update
    answer = ""
    password = ""
    cigarette_count = 0 # Cigarettes inputted as smoked
    day_count = 0 # Days since registration
    i = 0
    
    for single_date in daterange(register_date, current_date):
        if single_date.strftime("%Y-%m-%d") in cigarettes.keys():
            cigarette_count += int(cigarettes[single_date.strftime("%Y-%m-%d")])
        day_count += 1
    
    while True:
        os.system('cls')  # Clear screen on windows
        print("{}\n{}OMAT TIEDOT{}\n{}\n\n".format("="*80, "-"*35, "-"*34,"="*80))
        print("Käyttäjätili \"{}\" rekisteröitiin {}.{}.{}.\n".format(user[0], register_date.day, register_date.month, register_date.year))
        
        if cigarettes_per_day == -1:
            print("Oma arviosi viikottaisista savukemääristä: Ei määritetty")
        else:
            print("Oma arviosi viikottaisista savukemääristä: " + str(cigarettes_per_day))
            print("Oma arviosi kuukausittaisista savukemääristä: " + str(cigarettes_per_day*4))
        
        print("\nYhteensä {} savuketta poltettu {} päivässä.".format(cigarette_count, day_count))
        if day_count != 0:
            print("Keskimäärin {:.2f} savuketta poltettu päivässä.".format(float(cigarette_count)/float(day_count)))
        else: # Avoiding DivisionByZero error when it's registration date
            print("Keskimäärin {} savuketta poltettu päivässä.".format(float(cigarette_count)/1))
        if days_missed > 0:
            print("\nEt ole ilmoittanut {} päivän savukemääriä.".format(days_missed))
        
        # Ask for approximation of weekly cigarette usage
        if cigarettes_per_day == -1 and ask_for_update:
            while answer.upper() not in ["Y","N","K","E","1","2"]:
                answer = input("\nHaluatko asettaa arvion viikottaisista savukekulutuksista?\n1 - Kyllä\n2 - Ei nyt\n>")
                if answer.upper() in ["Y","K","1"]:
                    while cigarettes_per_day < 0 or cigarettes_per_day > 10000:
                        try:
                            cigarettes_per_day = int(input("Syötä kuinka monta savuketta poltat viikossa keskiarvoisesti >"))
                            if cigarettes_per_day < 0:
                                print("Poltettujen savukkeiden lukumäärän on oltava positiivinen. Yritä uudelleen.\n")
                            if cigarettes_per_day > 10000:
                                print("Savukkeiden lukumäärä ei saa olla yli 10 000! Yritä uudestaan.\n")
                        except ValueError:
                            print("Varmista, että syöttämäsi arvo on kokonaisluku. Yritä uudelleen.\n")
                    print("Arvo päivitetty!\n")
                    update_info()
                elif answer.upper() in ["N","E","2"]:
                    ask_for_update = False
                    break
                else:
                    print("\nKäskyä ei ymmärretty! Yritä uudestaan.\n")
            print("\n{}PAINA ENTER JATKAAKSESI{}".format("-"*29, "-"*28))
            input()
            continue
            
        answer = input("\n\nMitä haluat tehdä?\n\n1 - Tarkastella savukemääriä päivämäärittäin\n2 - Muuttaa viikottaista arvioita savukemääristä\n3 - Palata päävalikkoon\n>")
        
        # Check inputted cigarette counts paired with dates
        if answer == "1":
            i = 0
            print("\n\nPÄIVÄMÄÄRÄ - POLTETUT SAVUKKEET\n")
            for single_date in daterange(register_date, current_date):
                if single_date.strftime("%Y-%m-%d") in cigarettes.keys():
                    print("{} ----- {}".format(single_date.strftime("%d.%m.%Y"), cigarettes[single_date.strftime("%Y-%m-%d")]))
                if (i+1)%5 == 0 and single_date.strftime("%Y-%m-%d") != (current_date-datetime.timedelta(days=1)).strftime("%Y-%m-%d"):
                    input("\n---------- PAINA ENTER JATKAAKSESI TULOSTUSTA ----------")
                    print("")
                i += 1
                
        # Asking for approximation of weekly cigarette usage
        elif answer == "2":
            cigarettes_per_day = -1
            while cigarettes_per_day < 0:
                try:
                    cigarettes_per_day = int(input("\nSyötä kuinka monta savuketta poltat viikossa keskiarvoisesti >"))
                    if cigarettes_per_day < 0:
                        print("Poltettujen savukkeiden lukumäärä ei saa olla negatiivinen. Yritä uudelleen.\n")
                except ValueError:
                    print("Varmista, että syöttämäsi arvo on kokonaisluku. Yritä uudelleen.\n")
            print("Arvo päivitetty!\n")
            update_info()
        
        # Return to main menu    
        elif answer == "3":
            break
        
        # Bad input
        else:
            print("\nKäskyä ei ymmärretty! Yritä uudestaan.\n")
            time.sleep(2)
            continue
        print("\n{}PAINA ENTER JATKAAKSESI{}".format("-"*29, "-"*28))
        input()

## Input code 2 - Logged out
## Input code 5 - Logged in
def dev_information():
    """
    Displays information about the developers of this system.
    """
    os.system('cls')  # Clear screen on windows
    print("{}\n{}KEHITTÄJÄT{}\n{}\n".format("="*80, "-"*35, "-"*35,"="*80))
    print("Ohjelma on toteutettu osana Oulun yliopiston tietojenkäsittelytieteiden opintoja")
    print("Ohjelman kehittäjät ovat kolmannen vuoden opiskelijoita, joilla ei ole vahvaa\nsovellusalueeseen liittyvää koulutusta tai tuntemusta\n\n")
    print("Suunnittelu, Vaatimusmäärittely ja Ohjelmointi\nToni Bomström\n")
    print("Suunnittelu ja Raportointi\nKasper Eklund\n")
    print("Suunnittelu, Raportointi ja Taustatutkimus\nJoona Kallio\n\n")
    print("{}\n".format("="*80))
    
    print("{}PAINA ENTER JATKAAKSESI{}".format("-"*29, "-"*28))
    input()

## Input code 6 - Logged in
def logout():
    """
    Resets the user info effectively logging the user out.
    """
    global register_date
    global cigarettes_per_day
    global cigarettes
    global goal
    user[0] = None
    register_date = 0
    cigarettes = {}
    cigarettes_per_day = -1
    goal = []

## Input code 5 - Logged out
## Input code 7 - Logged in
def exit_application():
    """
    Sets global state variable to False
    effectively exiting from the application's main while-loop.
    """
    global online
    online = False

## Input code 3 - Logged out
def register():
    """
    Guides the user through the process of
    choosing allowed nickname and password.
    Also asks for approximated weekly cigarette usage.
    """
    global cigarettes_per_day
    global register_date
    username = "\\"
    password = "\\"
    password_confirm = "\\\\"
    answer = ""
    continuing = True # If user wants to interrupt registration
    
    while continuing:
        os.system('cls')  # Clear screen on windows
        print("{}\n{}REKISTERÖITYMINEN{}\n{}\n".format("="*80, "-"*30, "-"*30,"="*80))
        print("Syötä luku 0 keskeyttääksesi rekisteröinnin.\n\n")
        
        # Username validation
        while ("\\" in username or len(username) < 5 or len(username) > 32) and continuing:
            username = input("\nSyötä haluamasi käyttäjänimi tilille (syötä 0 keskeyttääksesi) >")
            if username == "0":
                continuing = False
                break
            if "\\" in username:
                print("Käyttäjänimessä ei saa olla \-merkkiä!\n")
                username = "\\"
                continue
            if len(username) < 5 or len(username) > 32:
                print("Käyttäjänimen pituuden on oltava 5-32 merkkiä!\n")
                username = "\\"
                continue
            try:
                with open(username+".user", "r") as source:
                    print("Syöttämäsi käyttäjänimi on varattu!\n")
                    username = "\\"
                    continue
            except IOError:
                print("Käyttäjänimi on vapaana.\n")
        
        # Password validation
        while continuing and ("\\" in password or password != password_confirm or len(password) < 5 or len(password) > 32):
            password = getpass("Syötä tilillesi salasana (syötä 0 keskeyttääksesi) >")
            if password == "0":
                continuing = False
                continue
            if "\\" in password:
                print("Salasanassa ei saa olla \-merkkiä!\n")
                password = "\\"
                continue
            if len(password) < 5 or len(password) > 32:
                print("Salasanan pituuden on oltava 5-32 merkkiä!\n")
                password = "\\"
                continue
                
            else:
                password_confirm = getpass("Varmista salasana >")
                if password_confirm == "0":
                    continuing = False
                elif password == password_confirm:
                    print("Salasana hyväksytty.\n")
                else:
                    print("Salasanat ovat erit!\n")
        
        # Asking for approximated weekly cigarette usage
        if continuing:
            try:
                register_date = datetime.date.today()
                with open(username+".user", "w") as source:
                    source.write(password + "\n" + str(register_date) + "\n")
                print("\nRekisteröityminen onnistui!\n")
                print("\n{}PAINA ENTER JATKAAKSESI{}".format("-"*29, "-"*28))
                input()
                while answer.upper() not in ["Y","N","K","E","1","2"]:
                    answer = input("Haluatko asettaa arvion viikottaisista savukekulutuksista?\n1 - Kyllä\n2 - En\n>")
                    if answer.upper() in ["Y","K","1"]:
                        while cigarettes_per_day < 0 or cigarettes_per_day > 10000:
                            try:
                                cigarettes_per_day = int(input("Syötä kuinka monta savuketta poltat viikossa keskiarvoisesti >"))
                                if cigarettes_per_day < 0:
                                    print("Poltettujen savukkeiden lukumäärän on oltava positiivinen. Yritä uudelleen.\n")
                                if cigarettes_per_day > 10000:
                                    print("Savukkeiden lukumäärä ei saa olla yli 10000! Yritä uudestaan.\n")
                            except ValueError:
                                print("Varmista, että syöttämäsi arvo on kokonaisluku. Yritä uudelleen.\n")
                    elif answer.upper() in ["N","E","2"]:
                        cigarettes_per_day = -1
                        break
                    else:
                        print("\nKäskyä ei ymmärretty! Yritä uudestaan.\n")
                # Add info to user file
                with open(username+".user", "a") as source:
                    source.write(str(cigarettes_per_day) + "\n")
                    source.write("\n")
                    source.write("0;0;0\n")
                    user[0] = username
                return True
            except IOError:
                print("\nRekisteröityminen epäonnistui:\nVirhetilanne!\n")
                print("\n{}PAINA ENTER JATKAAKSESI{}".format("-"*29, "-"*28))
                input()
                return False
        else:
            print("\nRekisteröityminen epäonnistui keskeyttämisen takia!\n")
            print("\n{}PAINA ENTER JATKAAKSESI{}".format("-"*29, "-"*28))
            input()
            return False

## Input code 4 - Logged out
def login():
    """
    Function for checking whether inputted username and password
    combination matches any account.
    Returns:
        True - Account found and login succesful
        False - Account login unsuccesful
    """
    global register_date
    global current_date
    global cigarettes_per_day
    global cigarettes
    global goal
    cigarette_list = []
    pw_confirm = ""
    username = ""
    password = ""
    
    os.system('cls')  # Clear screen on windows
    print("{}\n{}KIRJAUTUMINEN{}\n{}\n\n".format("="*80, "-"*33, "-"*34,"="*80))
    
    username = input("\nSyötä käyttäjänimi >")
    password = getpass("Syötä salasana >")
    
    try:
        # Try to open user-file with inputted nickname
        with open(username+".user", "r") as source:
            pw_confirm = source.readline().rstrip("\n")
            register_date = source.readline().rstrip("\n").split("-")
            register_date = datetime.date(int(register_date[0]), int(register_date[1]), int(register_date[2])) # Year, month, day
            
            # Check for approximation of weekly cigarette usage
            try:
                cigarettes_per_day = int(source.readline().rstrip("\n"))
            except ValueError:
                cigarettes_per_day = -1
            
            # Check for inputted cigarette counts paired with dates
            try:
                cigarette_list = source.readline().rstrip("\n").split(";")
                for i, cigarette in enumerate(cigarette_list):
                    cigarette_list[i] = cigarette.split(":")
                    cigarettes[cigarette_list[i][0]] = cigarette_list[i][1]
            except IndexError:
                cigarettes = {}
            
            goal = source.readline().rstrip("\n").split(";")
            if goal == ["0","0","0"]: # No goal set
                goal = []
            else:
                # Read data related to set goal
                goal[0] = goal[0].split("-")
                goal[1] = goal[1].split("-")
                goal[0] = datetime.date(int(goal[0][0]), int(goal[0][1]), int(goal[0][2]))
                goal[1] = datetime.date(int(goal[1][0]), int(goal[1][1]), int(goal[1][2]))
        
        if pw_confirm == password:
            user[0] = username

            print("\nSisäänkirjautuminen onnistui!\n")
            print("\n{}PAINA ENTER JATKAAKSESI{}".format("-"*29, "-"*28))
            input()
            return True

        register_date = 0
        cigarettes_per_day = -1
        cigarettes = {}
        goal = []
        print("\nSisäänkirjautuminen epäonnistui:\nVirheellinen käyttäjänimi tai salasana!\n")
        print("\n{}PAINA ENTER JATKAAKSESI{}".format("-"*29, "-"*28))
        input()
        return False
    except IOError:
        register_date = 0
        cigarettes_per_day = -1
        cigarettes = {}
        goal = []
        print("\nSisäänkirjautuminen epäonnistui:\nVirheellinen käyttäjänimi tai salasana!\n")
        print("\n{}PAINA ENTER JATKAAKSESI{}".format("-"*29, "-"*28))
        input()
        return False

## ===========================
## ---------MAIN MENU---------
## ===========================
def menu(features, functions):
    """
    Menu structure for the application.
        1. Provides user the possible commands.
        2. Reads user input
        3. Returns user input
    """
    global user_count
    global days_missed
    choice = ""

    os.system('cls')  # Clear screen on windows
    print("{}\n{}PÄÄVALIKKO{}\n{}\n".format("="*80, "-"*35, "-"*35,"="*80))
    
    if user[0] is None:
        user_count = 0

    else:
        user_count = 1
        days_missed = 0
        for single_date in daterange(register_date, current_date):
            if single_date.strftime("%Y-%m-%d") not in cigarettes.keys():
                days_missed += 1
    
    print("{} käyttäjää kirjautuneena tällä hetkellä.\n\n".format(user_count))
    
    ## --------------------- IMPLEMENTATION OF SOCIAL FACILITATION WOULD BE HERE IF WE WERE ABLE TO IMPLEMENT IT ---------------------
    ## This implementation here would be deceptive and hence it's commented away
    """
    if random.randint(0,5) == 4: # 25% chance to change concurrent user_count
        user_count = random.randint(user_count-5, user_count+5)
        if user_count <= 0:
            user_count = 1
    """
    
    # If user is logged in
    if user[0] is not None:
        print("Tervetuloa {}!\n".format(user[0]))
        if days_missed > 0:
            print("Sinulla on ilmoittamatta {} päivän savukemäärät.\nKäy ilmoittamassa ne kohdassa \"2 - Kirjaa tulokset!\n".format(days_missed))
    
    # If user is not logged in
    else:
        print("Et ole kirjautunut sisään!\n")
    
    print("Ole hyvä ja valitse toiminto syöttämällä sitä vastaava numero.\n")
    
    for i, feature in enumerate(features):
        print("{} - {}".format(i+1, feature))
    
    print("")
    choice = input(">")
    return choice
    
## >>>>>>>>>> GLOBAL VARIABLES <<<<<<<<<<
# System variables
app_name = "SätkäPois"
online = True  # Default True: Keep running app, False: close app
user_count = 1
current_date = datetime.date.today()
information = ["Tupakkatuotteet vahingoittavat koko elimistöä.",
               "Suomessa tupakka aiheuttaa joka viidennen kuoleman aikuisiällä, eli vuosittain",
               "noin 5 000 suomalaista kuolee tupakan aiheuttamiin sairauksiin.\n",
               "Joka kolmas syöpäkuolema on tupakan aiheuttama, ja joka viides",
               "sydän- ja verenkiertoelinten sairaus aiheutuu tupakoinnista.\n",
               "Keskimäärin tupakointi lyhentää elämää kahdeksan vuotta.",
               "Tupakointi on monien sairauksien riskitekijä ja pahentaa jo todettuja\nsairauksia.",
               " ",
               "(Perustietoa tupakoinnista)",
               
               "Länsimaissa neljätoista prosenttia kuolemista aiheutuu tupakan aiheuttamista",
               "sairauksista, ja se on yleisin estettävissä oleva kuolleisuuden syy.",
               "Myös Suomessa tupakka on merkittävä sairauksien aiheuttaja.",
               " ",
               "(Tupakan terveysriskit)",
               
               "Kun lopetat tupakoinnin, elimistössäsi tapahtuu nopeasti myönteisiä muutoksia.\n",
               "Heti ensimmäisten päivien aikana veren hiilimonoksiditaso laskee normaaliksi,",
               "nikotiini häviää elimistöstä ja haju- ja makuaisti parantuvat huomattavasti.\n",
               "Jo kahden viikon tupakoimattomuuden jälkeen verenkiertoelinten ja keuhkojen",
               "toiminta ja fyysinen suorituskyky paranevat.\n",
               "Vuoden kuluttua sydänkohtauksen riski on laskenut puolella.",
               "Kymmenen vuoden kuluttua lopettamisesta keuhkosyöpäriski on enää noin puolet",
               "tupakoivan henkilön riskistä.\n",
               "Viisitoista vuotta lopettamisen jälkeen aivohalvauksen riski on vähentynyt",
               "tupakoimattomien tasolle.",
               " ",
               "(Tupakoinnin lopettamisen hyödyt)"
              ]
              
links = [["Perustietoa tupakoinnista","https://www.terveyskirjasto.fi/terveyskirjasto/tk.koti?p_artikkeli=dlk01066"],
         ["Tupakan terveysriskit", "https://thl.fi/fi/web/alkoholi-tupakka-ja-riippuvuudet/tupakka/tupakka-ja-terveys"], 
         ["Tupakoinnin lopettamisen hyödyt", "https://thl.fi/fi/web/alkoholi-tupakka-ja-riippuvuudet/tupakka/tupakoinnin-lopettaminen/lopettamisen-hyodyt"],
         ["Tupakkariippuvuus","https://thl.fi/fi/web/alkoholi-tupakka-ja-riippuvuudet/tupakka/tupakoinnin-lopettaminen/mita-on-tupakkariippuvuus"],
         ["Paihdelinkki","https://paihdelinkki.fi/fi/tietopankki/pikatieto/tupakka"],
         ["Tilastoja Suomen tupakoinnista","https://thl.fi/fi/tilastot-ja-data/tilastot-aiheittain/paihteet-ja-riippuvuudet/tupakka"]
        ]
rewards = [[
          [" '._==_==_=_.' "],
          [" .-\:      /-. "],
          ["| (|:.     |) |"],
          [" '-|:.     |-' "],
          ["   \::.    /   "],
          ["    '::. .'    "],
          ["      ) (      "],
          ["    _.' '._    "],
          ["   `\"\"\"\"\"\"\"`   "]],
          
          [
          ["        {}      "],
          ["       /__\     "],
          ["     /|    |\   "],
          ["    (_|    |_)  "],
          ["       \  /     "],
          ["        )(      "],
          ["      _|__|_    "],
          ["    _|______|_  "],
          ["   |__________| "]]

        ]

# User variables
user = [None] # User info: Username
cigarettes_per_day = -1 # User set value: approximation of weekly cigarette count
cigarettes = {} # Dates as keys and cigarette counts as values
register_date = None
days_missed = 0 # Days missing cigarette counts
ask_for_update = True # Determines whether to ask for user's approximation of weekly cigarette count
goal = [] # Personal goal. A list of 3 : Begin_date, End_date, Cigarette_count


## ---------- MAIN FUNCTION ----------
def main():
    """
    Main function for the application.
    1. Welcomes the user
    2. Handles the login if necessary (with the use of login()-function),
    3. Calls menu()
    4. Provides (through the use of menu()-function) user interface for system features
    """
    answer = ""
    username = ""
    password = ""
    os.system('cls')  # Clear screen on windows
    
    # Ask for login
    while True:
        print("Tervetuloa {}-sovellukseen!\n".format(app_name))
        print("Haluatko kirjautua sisään?\n")
        print("1 - Kyllä\n2 - Jatka kirjautumatta\n")
        answer = input(">")
        
        if answer == "1" or answer.upper == "Y" or answer.upper() == "K":
            if login():
                break
            else:
                os.system('cls')  # Clear screen on windows
        elif answer == "2" or answer.upper() == "N" or answer.upper() == "E":
            break
        else:
            print("\nKäskyä ei ymmärretty! Yritä uudestaan.")
            print("\n{}PAINA ENTER JATKAAKSESI{}".format("-"*29, "-"*28))
            input()
            os.system('cls')  # Clear screen on windows
    
    # Main Loop
    while online:
        # Features if logged out
        if user[0] is None:
            features = ["Tietoa tupakoinnista", "Tietoa kehittäjistä", "Rekisteröidy", "Kirjaudu sisään", "Lopeta"]
            functions = {1 : smoking_information,
                         2 : dev_information,
                         3 : register,
                         4 : login,
                         5 : exit_application
            }
        # Features if logged in
        else:
            features = ["Tietoa tupakoinnista", "Kirjaa tulokset", "Oma tavoitteesi", "Tarkastele tietojasi", "Tietoa kehittäjistä", "Kirjaudu ulos", "Lopeta"]
            functions = {1 : smoking_information,
                         2 : input_data,
                         3 : manage_goal,
                         4 : user_information,
                         5 : dev_information,
                         6 : logout,
                         7 : exit_application
            }
        # Loop for getting valid input
        while True:
            answer = menu(features, functions)
            if answer.isdigit():
                if int(answer) in functions.keys() and ((user[0] is None and int(answer) in range(1,6)) or (user[0] is not None and int(answer) in range(1,8))):
                    break
            print("\nKäskyä ei ymmärretty! Yritä uudestaan.\n")
            time.sleep(2)
        
        functions[int(answer)]() # Wanna-be Switch-case
        
    print("\n{}PAINA ENTER JATKAAKSESI{}".format("-"*29, "-"*28))
    input()
    os.system('cls')  # Clear screen on windows
    
if __name__ == "__main__":
    main()


