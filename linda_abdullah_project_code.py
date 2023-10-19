'''
For this project, I applied 4NF to my tables.

the following relational schema of the database is follows:
MOVIE (MID, Mname, MDuration)
PRODUCTION_CENTER (PID, Pname, Plocation, PTelephoneNumber)
CAST_MEMBER (CastID, Castname, CastSurname)
CREW_MEMBER (CrewMID , CrewName, CrewSurname, CrewRole)

ACTS_IN(CastID, MID, Appearance, Role)
GENRE(MID, Genre)
PRODUCED_IN(PID, MID)
WORKS_IN(CrewMID, PID)

for the delete functionality, I added cascading delete in the acts_in, produced_in, works_in tables

----------> tables are initialy empty 

'''
# asks user for user name and password of the database
username = input("Please enter your database username:")
pw = input("Please enter your database password:")


# importing important libraries to be able to execute sql commands in my Movie Production database
import pymysql.cursors
import os 

# Establishing connection with the database 

# #-------------------------------CREATING DATABASE------------------------#
connection = pymysql.connect(host='localhost', user=username, password=pw, cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
    
    cursor.execute("DROP DATABASE IF EXISTS MovieProduction;") # drop database for sake of practice and code testing

    cursor.execute("CREATE DATABASE MovieProduction;") # create database
    cursor.execute("USE MovieProduction;") # uses the database
    

# #-------------------------CREATING TABLES--------------------------#
with connection.cursor() as cursor:
    
    # creating tabel PRODUCTION_CENTER
    cursor.execute("CREATE TABLE PRODUCTION_CENTER( PID int PRIMARY KEY, Pname varchar(20),Plocation varchar(20), PTelephoneNumber int);")
    
    # creating tabel MOVIE
    cursor.execute("CREATE TABLE MOVIE (MID int, Mname varchar(20), MDuration int,PRIMARY KEY(MID));")
    
    # creating tabel GENRE
    cursor.execute("CREATE TABLE GENRE (MID int, Genre varchar(20), primary key(MID, Genre), Foreign key(MID) references MOVIE(MID) ON DELETE CASCADE, CHECK (Genre in ('action', 'comedy', 'romance', 'mystery', 'crime')));")
    # adding cascade delete to GENRE table
    cursor.execute("ALTER TABLE `genre` ADD CONSTRAINT `g1` FOREIGN KEY (`MID`) REFERENCES `movie` (`MID`) ON DELETE CASCADE;")
    
    # creating tabel CAST_MEMBER
    cursor.execute("CREATE TABLE CAST_MEMBER(CastID int PRIMARY KEY, CastName varchar(20), CastSurname varchar(20));")
    
    # creating tabel CREW_MEMBER
    cursor.execute("CREATE TABLE CREW_MEMBER(CrewMID int, CrewName varchar(20), CrewSurname varchar(20), CrewRole varchar(20), PRIMARY KEY(CrewMID), CHECK (CrewRole in ('Director', 'Assistant Director', 'Camera Operator', 'Set Dresser', 'Make-up Artist')));")

    # creating tabel PRODUCED_IN
    cursor.execute("CREATE TABLE PRODUCED_IN(PID int, MID int, PRIMARY KEY (MID), FOREIGN KEY (PID) REFERENCES PRODUCTION_CENTER(PID) ON DELETE CASCADE, FOREIGN KEY (MID) REFERENCES MOVIE(MID) ON DELETE CASCADE);")
    # adding cascade delete to PRODUCED_IN table
    cursor.execute("ALTER TABLE `produced_in`ADD CONSTRAINT `pi1` FOREIGN KEY (`PID`) REFERENCES `production_center` (`PID`) ON DELETE CASCADE;")
    cursor.execute("ALTER TABLE `produced_in` ADD CONSTRAINT `pi2` FOREIGN KEY (`MID`) REFERENCES `movie` (`MID`) ON DELETE CASCADE;")

    # # creating tabel WORKS_IN
    cursor.execute("CREATE TABLE WORKS_IN(PID int, CrewMID int, PRIMARY KEY (CrewMID), FOREIGN KEY (PID) REFERENCES PRODUCTION_CENTER(PID) ON DELETE CASCADE, FOREIGN KEY (CrewMID) REFERENCES CREW_MEMBER(CrewMID) ON DELETE CASCADE);")
    # adding cascade delete to WORKS_IN table
    cursor.execute("ALTER TABLE `works_in` ADD CONSTRAINT `worksinfk1` FOREIGN KEY (`PID`) REFERENCES `production_center` (`PID`) ON DELETE CASCADE;")
    cursor.execute("ALTER TABLE `works_in` ADD CONSTRAINT `worksinfk2` FOREIGN KEY (`CrewMID`) REFERENCES `crew_member` (`CrewMID`) ON DELETE CASCADE;")
      
    # creating tabel ACTS_IN
    cursor.execute("CREATE TABLE ACTS_IN(CastID int,MID int,Appearance int,Role varchar(20),PRIMARY KEY (CastID, MID),FOREIGN KEY (CastID) REFERENCES CAST_MEMBER(CastID) ON DELETE CASCADE,FOREIGN KEY (MID) REFERENCES MOVIE(MID) ON DELETE CASCADE,CHECK (Role in ('main actor', 'background actor', 'cameo')));")
    # adding cascade delete to ACTS_INs table
    cursor.execute("ALTER TABLE `acts_in` ADD CONSTRAINT `ai1` FOREIGN KEY (`MID`) REFERENCES `MOVIE` (`MID`) ON DELETE CASCADE;")
    cursor.execute("ALTER TABLE `acts_in` ADD CONSTRAINT `ai2` FOREIGN KEY (`CastID`) REFERENCES `cast_member` (`CastID`) ON DELETE CASCADE;")


#---------------------------------defining functions-------------------------#
# Defining functions that are useful to make the code look clean
def print_table(dict_name, ptype): # printing function that requires a dictionary and type of 'dict_name' parameter
    
    if ptype == "<class 'tuple'>": # is useful when a table is empty and when table is empty, the result of the table will be = <class 'tuple'>
        return
    else:    
        # displays column names
        columns = ''.join([str(v).ljust(15) for v in dict_name[0].keys()]) # gives a padding of about 19 char
        print(columns) # shows column names

        for dictn in dict_name:
            # values of a dictionary
            values = ''.join([str(v).ljust(19) for v in dictn.values()]) 
            print(values) # shows values in dictionary

def show_table(table): # returns the specified table 
    command = f"SELECT * FROM {table}" # command to select from a table specified by user
    with connection.cursor() as cursor:
        cursor.execute(command) # will exectue the SQL command provided
        return cursor.fetchall() # will give list of dictionaries of the table entrances

#------------------Inserting into tables functions--------------------#
#----------------------MOVIE------------------------#
def MovieDict(MID, Mname, MDuration): # will form a dictionary of a movie record
    movie_val = { # creates a MOVIE record
        'MID': MID, 
        'Mname': Mname, 
        'MDuration': MDuration
        }
    return movie_val # returns the dictionary as a result of the function 


def InsertIntoMovie(val_dict): # adds record to MOVIE table and takes dictionary of MOVIE record as parameter
    with connection.cursor() as cursor:
        
        cursor.execute(f"INSERT INTO MOVIE VALUES ({val_dict['MID']}, '{val_dict['Mname']}', {val_dict['MDuration']});")  # execute the sql command 
            
#-----------------------CREW_MEMBER-----------------------#
def crew_memeber_record(CrewMID, CrewName, CrewSurname, CrewRole): # will form a dictionary of a CREW_MEMBER record
    crew_dict = { # creates a CREW_MEMBER record
        'CrewMID': CrewMID, 
        'CrewName': CrewName, 
        'CrewSurname': CrewSurname, 
        'CrewRole' : CrewRole
    }
    return crew_dict # returns the dictionary as a result of the function 


def InsertIntoCrewMember(val_dict): # adds record to CREW_MEMBER table and takes dictionary of CREW_MEMBER record as parameter
    with connection.cursor() as cursor:
        
            # SQL command used to insert into CREW_MEMBER table 
        command = f"INSERT INTO CREW_MEMBER VALUES ({val_dict['CrewMID']},'{val_dict['CrewName']}', '{val_dict['CrewSurname']}' , '{val_dict['CrewRole']}')"
            
        cursor.execute(command)  # execute the sql command 

#----------------------CAST_MEMBER--------------------#        
def cast_memeber_record(CastID, CastName, CastSurname): # will form a dictionary of a CAST_MEMBER record
    cast_dict = { # creates a CAST_MEMBER record
        'CastID': CastID, 
        'CastName': CastName, 
        'CastSurname': CastSurname
    }

    return cast_dict # returns the dictionary as a result of the function 

def InsertIntoCastMember(val_dict): # adds record to CAST_MEMBER table and takes dictionary of CAST_MEMBER record as parameter
    with connection.cursor() as cursor:
        
        # SQL command used to insert into CAST_MEMBER table
        command = f"INSERT INTO CAST_MEMBER VALUES ({val_dict['CastID']},'{val_dict['CastName']}', '{val_dict['CastSurname']}') "
            
        cursor.execute(command)  # execute the sql command
            
#----------------------------GENRE---------------------#
def add_genre(movieid, genre): # adds record to GENRE table and takes values of GENRE record as parameter
    
    # SQL command used to insert into GENRE table 
    command = f"INSERT INTO GENRE VALUES({movieid}, '{genre}');"
    with connection.cursor() as cursor:
        cursor.execute(command) 

#--------------show genre-------------------#
def show_genre(movieid): # function that shows user the genre(s) of the movie of their choice
    
    # SQL command used to show genre of a movie    
    command = f"SELECT Mname, Genre FROM MOVIE CROSS JOIN GENRE ON MOVIE.MID=GENRE.MID AND MOVIE.MID={movieid};"
    with connection.cursor() as cursor:
        cursor.execute(command)
        result = cursor.fetchall()
        res = str(type(result)) # gets type of result to check if result is an empty table or a populated table
        
    print_table(result, res) # uses my defined print_table() function then shows result
        
#-------------------------PRODUCTION_CENTER-----------------#
def prod_center_record(PID, Pname, Plocation, PTelephoneNumber): # will form a dictionary of a PRODUCTION_CENTER record
    prod_record = { # creates a PRODUCTION_CENTER record
        'PID': PID,
        'Pname': Pname,
        'Plocation': Plocation,
        'PTelephoneNumber': PTelephoneNumber
    }

    return prod_record # returns the dictionary as a result of the function 

def InsertIntoProductionCenter(val_dict): # adds record to PRODUCTION_CENTER table and takes dictionary of PRODUCTION_CENTER record as parameter
    
    with connection.cursor() as cursor:   

        # SQL command used to insert into PRODUCTION_CENTER table 
        command = f"INSERT INTO PRODUCTION_CENTER VALUES ({val_dict['PID']},'{val_dict['Pname']}', '{val_dict['Plocation']}', {val_dict['PTelephoneNumber']}) "
            
        cursor.execute(command)  # execute the sql command 

# ------------------ACTS_IN-------------------#

def addto_ACTS_IN(castid, movieid, appearance, role): # adds record to ACTS_IN table and takes values of ACTS_IN record as parameter
    
    # SQL command used to insert into ACTS_IN table     
    command = f"INSERT INTO ACTS_IN VALUES ({castid}, {movieid}, '{appearance}', '{role}');"
    with connection.cursor() as cursor:
        cursor.execute(command)

#---------------PRODUCED_IN----------------------#
def addto_PRODUCED_IN(PID, movieid):# adds record to PRODUCED_IN table and takes values of PRODUCED_IN record as parameter

    # SQL command used to insert into PRODUCED_IN table  
    command = f"INSERT INTO PRODUCED_IN VALUES({PID}, {movieid})"
    with connection.cursor() as cursor:
        cursor.execute(command)
    
#-----------------WORKS_IN-----------------#
def addto_WORKS_IN(PID, crewmid): # adds record to WORKS_IN table and takes values of WORKS_IN record as parameter

    # SQL command used to insert into WORKS_IN table  
    command = f"INSERT INTO WORKS_IN VALUES({PID}, {crewmid})"
    with connection.cursor() as cursor:
        cursor.execute(command)

#----------------------------delete from tables------------------------#

#-------------MOVIE---------------------#
def deletefrom_MOVIE(id): # deletes tuple of specificed id from MOVIE table

    # SQL command used to delete from MOVIE table
    command = f"DELETE FROM MOVIE WHERE MID={id}"
    with connection.cursor() as cursor:
        cursor.execute(command)

#-------------PRODUCTION_CENTER---------------------#    
def deletefrom_PRODUCTION_CENTER(id): # deletes tuple of specificed id from PRODUCTION_CENTER table

    # SQL command used to delete from PRODUCTION_CENTER table
    command = f"DELETE FROM PRODUCTION_CENTER WHERE PID={id}"
    with connection.cursor() as cursor:
        cursor.execute(command)

#-------------CREW_MEMBER---------------------#
def deletefrom_CREW_MEMBER(id): # deletes tuple of specificed id from CREW_MEMBER table

    # SQL command used to delete from CREW_MEMBER table
    command = f"DELETE FROM CREW_MEMBER WHERE CrewMID={id}"
    with connection.cursor() as cursor:
        cursor.execute(command)

#-------------CAST_MEMBER---------------------#
def deletefrom_CAST_MEMBER(id):# deletes tuple of specificed id from CAST_MEMBER table

    # SQL command used to delete from CAST_MEMBER table
    command = f"DELETE FROM CAST_MEMBER WHERE CastID={id}"
    with connection.cursor() as cursor:
        cursor.execute(command)

#-------------GENRE---------------------#
def deletefrom_GENRE(mid,genre): # deletes tuple of specificed id from GENRE table

    # SQL command used to delete from GENRE table
    command = f"DELETE FROM GENRE WHERE MID={mid} AND Genre='{genre}'"
    with connection.cursor() as cursor:
        cursor.execute(command)

#-------------ACTS_IN---------------------#
def deletefrom_ACTS_IN(id): # deletes tuple of specificed id from ACTS_IN table

    # SQL command used to delete from ACTS_IN table
    command = f"DELETE FROM ACTS_IN WHERE CastID={id}"
    with connection.cursor() as cursor:
        cursor.execute(command)

#-------------WORKS_IN---------------------#
def deletefrom_WORKS_IN(id): # deletes tuple of specificed id from WORKS_IN table

    # SQL command used to delete from WORKS_IN table
    command = f"DELETE FROM WORKS_IN WHERE CrewMID={id}"
    with connection.cursor() as cursor:
        cursor.execute(command)

#-------------PRODUCED_IN---------------------#
def deletefrom_PRODUCED_IN(id): # deletes tuple of specificed id from PRODUCED_IN table

    # SQL command used to delete from PRODUCED_IN table
    command = f"DELETE FROM PRODUCED_IN WHERE MID={id}"
    with connection.cursor() as cursor:
        cursor.execute(command)


while True:

    # asks input from user for: 
    # adding to table, 
    # showing a specific table, 
    # let user know the genre of their desired movie,
    # save changes, 
    # write a complex sql operation, 
    # assign a record relation between entity entrances that have relations with other entities
    # give a very simplified explanation and visualization of how the database behaves
    # delete from a table

    # user to choose their desired action/operation
    user_input = input("Choose your following operation:" 
    + "\n" + "q: Visualization of Movie Production Database"
    + "\n" + "a: Add record" 
    + "\n" + "b: Show records of a table"
    + "\n" + "g: Know the genre or genres of a movie" 
    + "\n" + "s: Save your changes"  
    + "\n" + "c: Write an SQL command"  
    + "\n" + "r: Assign relation between entrances"
    + "\n" + "d: Delete record from a table"
    + "\n" + ">") 

    if user_input == 'a': # user wants to add a record
        add_input = input("Choose table to add record to:" # ask user which table to add a record to 
        + "\n" + "movie" 
        + "\n" + "crew member"
        + "\n" + "cast member"
        + "\n" + "production center" 
        + "\n" + "genre"
        + "\n" + ">")

        if add_input == "movie": # condition if input is "movie" 
            # MOVIE (MID, Mname, MDuration)
            # user is asked to enter movie id, movie's name and movie's duration
            mid = int(input("enter the movie's ID:" + "\n" + ">"))
            mduration = int(input("enter the movie's duration(in minutes):" + "\n" + ">"))
            mname = input("enter the movie's name:" + "\n" + ">")

            # create a dictionary of record and call function to add record to the table
            movie_record = MovieDict(mid, mname, mduration)
            InsertIntoMovie(movie_record)
            print('\n')

        elif add_input == "crew member": # condition if input is "crew member"

            # CREW_MEMBER(CrewMID , CrewName, CrewSurname, CrewRole)
            # user is asked to enter crew member's id, crew member's name, crew member's surname and the crew member's role
            crewid = int(input("enter the crew member's ID:" + "\n" + ">"))
            crewname = input("enter the crew member's name:" + "\n" + ">")
            crewsurname = input("enter the crew member's surname:" + "\n" + ">")
            crewrole = input("choose one of the crew roles (director', assistant director, camera operator, set dresser, make-up rtist)" + "\n" + ">")
            
            # create a dictionary of record and call function to add record to the table
            crew_record = crew_memeber_record(crewid, crewname, crewsurname, crewrole)
            InsertIntoCrewMember(crew_record)
            print('\n')

        elif add_input == "cast member": # condition if input is "cast member"

            # CAST_MEMBER(CastID, Castname, CastSurname)
            # user is asked to enter cast member's id, cast member's name and cast member's surname
            castid = int(input("enter the cast member's ID:" + "\n" + ">"))
            castname = input("enter the cast member's name:" + "\n" + ">")
            castsurname = input("enter the cast member's surname:" + "\n" + ">")
            
            # create a dictionary of record and call function to add record to the table
            cast_record = cast_memeber_record(castid, castname, castsurname)
            InsertIntoCastMember(cast_record)
            print('\n')

        elif add_input == "production center": # condition if input is "production center"

            # PRODUCTION_CENTER (PID, Pname, Plocation, PTelephoneNumber)
            # user is asked to enter production center's ID, production center's name, production center's location and production center's telephone number
            pid = int(input("enter the production center's ID:" + "\n" + ">"))
            pname = input("enter the production center's name:" + "\n" + ">")
            ploc = input("enter the production center's location:" + "\n" + ">")
            ptel = int(input("enter the production center's telephone number:" + "\n" + ">"))
            
            # create a dictionary of record and call function to add record to the table
            pc_record = prod_center_record(pid, pname, ploc, ptel)
            InsertIntoProductionCenter(pc_record)
            print('\n')

        elif add_input == "genre": # GENRE = (MID, Genre)
            while True:
                # user is asked to enter movie's id and genre
                movieid = int(input("enter the movie's ID which you wish to assign a genre to:" + "\n" + ">"))
                genre = input("enter one of the following genres:" 
                + "\n" + "action" 
                + "\n" + "comedy" 
                + "\n" + "romance" 
                + "\n" + "mystery"
                + "\n" + "crime"
                + "\n" + ">")
                add_genre(movieid, genre) # call function which adds genres to genre table
                option = input("do you wish to add more genres? choose: yes or no" + "\n" + ">") # ask user if they want to add more genres
                if option == "yes": continue
                elif option == "no": break
            print("\n")

    elif user_input == 'b': # here user will ask to show their desired table
        
        # ask user which table to show
        show_input = input("enter the table's name:"
        + "\n" + "movie"
        + "\n" + "production_center"
        + "\n" + "crew_member"
        + "\n" + "cast_member"
        + "\n" + "acts_in"
        + "\n" + "produced_in"
        + "\n" + "works_in"
        + "\n" + "genre"
        + "\n" + ">")

        # calling functions that show the selected table
        result = show_table(show_input)
        res = str(type(result))
        print_table(result, res)
        print('\n')

    elif user_input == 'c': # for user to write complex SQL commands
        complex_input = input("write your SQL command:" + "\n" + ">")
        with connection.cursor() as cursor:
            cursor.execute(complex_input)
            result = cursor.fetchall()  
        res = str(type(result)) # gets type of result to check if table is empty or if the table is populated
        print_table(result, res) # call print_table() function
        print('\n')    

    elif user_input == 's': # for user to save their changes
        with connection.cursor() as cursor:
            connection.commit() # commit changes
        print('\n')   
    
    elif user_input == 'g': # for user to know genres of movie their choice
        # user is asked to enter movie's id
        movieidg = input("enter ID of the movie that you wish to know its genre(s)" + "\n" + ">")
        show_genre(movieidg)
    
    elif user_input == 'q': # shows user a breif explanation of how the entities(MOVIE, CAST_MEMBER, CREW_MEMBER, PRODUCTION_CENTER) are related
        print("CAST_MEMBER -- ACTS_IN -- MOVIE"
        + "\n" + "CREW_MEMBER -- WORKS_IN -- PRODUCTION_CENTER"
        + "\n" + "MOVIE -- PRODUCED_IN -- PRODUCTION_CENTER")
        print("\n")
    
    elif user_input == 'r': # will add records to relationships between entities
        
        relation_rec = input("choose your next action: "
        # asks user to choose an action for adding to the relationship
        + "\n" + "p: assign a cast member to act in which movie"
        + "\n" + "o: assign a movie to be produced in a production center"
        + "\n" + "i: assign a crew member to a production center"
        + "\n" + ">")
        
        if relation_rec == 'p': # if user wishes to assign a cast member to a certain movie
            castid = int(input("enter the cast member's ID: " + "\n" + ">"))
            movieid = int(input("enter the movie's ID: " + "\n" + ">"))
            role = input("enter the cast member's role in the movie (main actor, background actor, cameo): " + "\n" + ">")
            appearance = input("enter the cast member's appearance duration(in minutes) in the movie: " + "\n" + ">")
            addto_ACTS_IN(castid, movieid, appearance, role)
        
        elif relation_rec == 'o': # asks user to assign a production center to a movie
            pid = int(input("enter the production center's ID: " + "\n" + ">"))
            movieid = int(input("enter the movie's ID: " + "\n" + ">"))
            addto_PRODUCED_IN(pid,movieid)

        elif relation_rec == 'i': # assign which crew member will work in which production center
            pid = int(input("enter the production center's ID: " + "\n" + ">"))
            crewmid = int(input("enter the crew member's ID: " + "\n" + ">"))
            addto_WORKS_IN(pid,crewmid)
    
    elif user_input == 'd': # if user wishes to delete records
        d = input("choose table to delete record from:"
        + "\n" + "movie"
        + "\n" + "production center"
        + "\n" + "crew member"
        + "\n" + "cast member"
        + "\n" + "genre"
        + "\n" + "acts_in"
        + "\n" + "produced_in"
        + "\n" + "works_in"
        + "\n" + ">"
        ) 

        if d == "movie":# condition if input is "movie"

            # user needs to input the movie's id to delete a movie tuple
            mid = int(input("choose the id of record you wish to delete:" + "\n" + ">"))
            deletefrom_MOVIE(mid)
        
        elif d == "production center":# condition if input is "production center"

            # user needs to input the production center's id to delete a production center tuple
            pid = int(input("choose the id of record you wish to delete:" + "\n" + ">"))  
            deletefrom_PRODUCTION_CENTER(pid)
        
        elif d == "crew member":# condition if input is "crew member"

            # user needs to input the crew member's id to delete a crew member tuple
            cid = int(input("choose the id of record you wish to delete:" + "\n" + ">"))  
            deletefrom_CREW_MEMBER(cid)
        
        elif d == "cast member":# condition if input is "cast member"

            # user needs to input the cast member's id to delete a cast member tuple
            cid = int(input("choose the id of record you wish to delete:" + "\n" + ">"))  
            deletefrom_CAST_MEMBER(cid)
        
        elif d == "genre":# condition if input is "genre"

            # user needs to input the id of movie and the specific genre they wish to delete
            mid = int(input("choose the id of movie you wish to delete its genre:" + "\n" + ">")) 
            genre = input("choose the genre you want to delete from the movie:")
            deletefrom_GENRE(mid, genre)
        
        elif d == "acts_in":# condition if input is "acts_in"

            # due to many-to-many relationship 
            # several actors may act in one movie and actor may act in different movies
            mid = int(input("choose the movie's id for record you wish to delete:" + "\n" + ">")) 
            castid =int(input("choose the cast member's id for record you wish to delete:" + "\n" + ">"))  
            deletefrom_ACTS_IN(mid)
        
        elif d == "produced_in":# condition if input is "produced_in"

            # due to one-to-many relationship, the user must specify the movie's id
            # a production center may have more than one movie and one movie must be produced in only one production center
            mid = int(input("choose the movie id for record you wish to delete:" + "\n" + ">")) 
            deletefrom_PRODUCED_IN(mid)
        
        elif d == "works_in":# condition if input is "works_in"

            # due to one-to-many relationship, the user must specify the movie's id
            # a production center has many crew members working at it and each crew member is assigned to only one certain production center 
            cid = int(input("choose the crew member's id for record you wish to delete:" + "\n" + ">")) 
            deletefrom_WORKS_IN(cid)
            

    x = input("Please press enter to go back to menu or write exit to exit program" + "\n" + ">")
    # gives the user a better experience and view of the program
    if x == '': # if user presses enter
        # then terminal will be cleard
        os.system('cls' if os.name == 'nt' else 'clear')
    elif x == "exit": # if user write "exit"
        # then the user will exit program
        break
