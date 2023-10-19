DROP DATABASE IF EXISTS MovieProduction; # drop database for sake of practice and code testing

CREATE DATABASE MovieProduction; # create database
USE MovieProduction;

# creating table PRODUCTION_CENTER
 CREATE TABLE PRODUCTION_CENTER(
	PID int PRIMARY KEY,
    Pname varchar(20),
    Plocation varchar(20),
    PTelephoneNumber int
);

# creating table MOVIE (MID, Mname, MDuration)
CREATE TABLE MOVIE (
	MID int,
    Mname varchar(20),
    MDuration int,
    PRIMARY KEY(MID)
);

# creating table GENRE (MID, Genre)
CREATE TABLE GENRE (
	MID int,
    Genre varchar(20),
    primary key(MID, Genre),
    Foreign key(MID) references MOVIE(MID) ON DELETE CASCADE,
    CHECK (Genre in ('action', 'comedy', 'romance', 'mystery', 'crime'))
);

# adding cascade delete to GENRE table
 ALTER TABLE `genre` ADD CONSTRAINT `g1` FOREIGN KEY (`MID`) REFERENCES `movie` (`MID`) ON DELETE CASCADE;
 
 # creating table CAST_MEMBER(CastID, Castname, CastSurname)
CREATE TABLE CAST_MEMBER(
	CastID int PRIMARY KEY,
    CastName varchar(20),
    CastSurname varchar(20)
    );

# creating table CREW_MEMBER(CrewMID , CrewName, CrewSurname, CrewRole)
CREATE TABLE CREW_MEMBER(
	CrewMID int,
    CrewName varchar(20),
    CrewSurname varchar(20),
    CrewRole varchar(20),
    PRIMARY KEY(CrewMID),
    CHECK (CrewRole in ('Director', 'Assistant Director', 'Camera Operator', 'Set Dresser', 'Make-up Artist'))
    );

# creating table PRODUCED_IN(PID, MID)
 CREATE TABLE PRODUCED_IN(
	PID int,
    MID int,
    PRIMARY KEY (MID),
    FOREIGN KEY (PID) REFERENCES PRODUCTION_CENTER(PID) ON DELETE CASCADE,
    FOREIGN KEY (MID) REFERENCES MOVIE(MID) ON DELETE CASCADE
    );
 
 # adding cascade delete to PRODUCED_IN table
 ALTER TABLE `produced_in`ADD CONSTRAINT `pi1` FOREIGN KEY (`PID`) REFERENCES `production_center` (`PID`) ON DELETE CASCADE;
 ALTER TABLE `produced_in` ADD CONSTRAINT `pi2` FOREIGN KEY (`MID`) REFERENCES `movie` (`MID`) ON DELETE CASCADE;

# # creating table WORKS_IN(CrewMID, PID)
 CREATE TABLE WORKS_IN(
	PID int,
    CrewMID int,
    PRIMARY KEY (CrewMID),
    FOREIGN KEY (PID) REFERENCES PRODUCTION_CENTER(PID) ON DELETE CASCADE,
    FOREIGN KEY (CrewMID) REFERENCES CREW_MEMBER(CrewMID) ON DELETE CASCADE
    );
 
 # adding cascade delete to WORKS_IN table
 ALTER TABLE `works_in` ADD CONSTRAINT `worksinfk1` FOREIGN KEY (`PID`) REFERENCES `production_center` (`PID`) ON DELETE CASCADE;
 ALTER TABLE `works_in` ADD CONSTRAINT `worksinfk2` FOREIGN KEY (`CrewMID`) REFERENCES `crew_member` (`CrewMID`) ON DELETE CASCADE;
      

 # creating table ACTS_IN(CastID, MID, Appearance, Role)
 CREATE TABLE ACTS_IN(
	CastID int,
    MID int,
    Appearance int,
    Role varchar(20),
    PRIMARY KEY (CastID, MID),
    FOREIGN KEY (CastID) REFERENCES CAST_MEMBER(CastID) ON DELETE CASCADE,
    FOREIGN KEY (MID) REFERENCES MOVIE(MID) ON DELETE CASCADE,
    CHECK (Role in ('main actor', 'background actor', 'cameo'))
    );
 
 # adding cascade delete to ACTS_INs table
 ALTER TABLE `acts_in` ADD CONSTRAINT `ai1` FOREIGN KEY (`MID`) REFERENCES `MOVIE` (`MID`) ON DELETE CASCADE;
 ALTER TABLE `acts_in` ADD CONSTRAINT `ai2` FOREIGN KEY (`CastID`) REFERENCES `cast_member` (`CastID`) ON DELETE CASCADE;
      
      
# insert into PRODUCTION_CENTER table
INSERT INTO PRODUCTION_CENTER VALUES( #(PID, Pname, Plocation, PTelephoneNumber)
	1,
     "MRG Center",
     "2345, NewYork",
     0987907891
);
INSERT INTO PRODUCTION_CENTER VALUES(
	2,
     "Unity Center",
     "0972, Los Angelos",
     0897932723
);

INSERT INTO PRODUCTION_CENTER VALUES(
	3,
     "Joint Center",
     "1234, California",
     0282366191
);
 INSERT INTO PRODUCTION_CENTER VALUES(
 	4,
     "GEN Center",
     "7578, NewYork",
     0169007707
 );

INSERT INTO PRODUCTION_CENTER VALUES(
 	5,
     "KING Center",
     "3245, NewYork",
     0987907891
 );


# insert into MOVIE table
  INSERT INTO MOVIE VALUES ( # (MID, Mname, MDuration)
 	1,
     "Beeblo",
     80
  );
  INSERT INTO MOVIE VALUES (
 	2,
     "Koya",
     85
  );

INSERT INTO MOVIE VALUES (
	3,
     "Jackie Chan",
     70
);
  
INSERT INTO MOVIE VALUES (
 	4,
     "Quicy Bibliography",
     76
);

INSERT INTO MOVIE VALUES (
 	5,
     "Poly With Moly",
     76
);

# insert into CAST_MEMBER table
INSERT INTO CAST_MEMBER VALUES( # (CastID, Castname, CastSurname)
 		1,
         'Anna',
         'Dwayn'
        );

INSERT INTO CAST_MEMBER VALUES(
		2,
         'Malaki',
         'Stout'
);
INSERT INTO CAST_MEMBER VALUES(
 		3,
         'Quinn',
         'Ridley'
);
INSERT INTO CAST_MEMBER VALUES(
		4,
         'Mohamed',
         'Gutierrez'
);

INSERT INTO CAST_MEMBER VALUES(
 		5,
         'Alton',
         'Palmer'
);
INSERT INTO CAST_MEMBER VALUES(
 		6,
         'Kevin',
         'Hart'
);
INSERT INTO CAST_MEMBER VALUES(
 		7,
         'Aleeza',
         'Burn'
);

# insert into CREW_MEMBER table
INSERT INTO CREW_MEMBER VALUES( # (CrewMID , CrewName, CrewSurname, CrewRole)
 	1,
     "Maddison",
     "Noble",
     "Director"
);
INSERT INTO CREW_MEMBER VALUES(
	2,
    "Winston",
    "Whitfield",
    'Camera Operator'
);

INSERT INTO CREW_MEMBER VALUES(
 	3,
     "Mara",
     "Mcintosh",
     'Make-up Artist'
);

INSERT INTO CREW_MEMBER VALUES(
 	4,
     "Phillip",
     "Cain",
     'Set Dresser'
);

INSERT INTO CREW_MEMBER VALUES(
 	5,
     "Hallie",
     "William",
     'Director'
);

INSERT INTO CREW_MEMBER VALUES(
	6,
     "Cosmo",
     "Mayo",
     'Camera Operator'
);

INSERT INTO CREW_MEMBER VALUES(
	7,
    "Zayyan",
     "Neal",
     'Assistant Director'
);

INSERT INTO CREW_MEMBER VALUES(
 	8,
     "Colette",
     "Jacobs",
     'Director'
);


# insert into ACTS_IN table
INSERT INTO ACTS_IN VALUES( # (CastID, MID, Appearance, Role)
 	1,
     2,
     80,
     'main actor'
);

INSERT INTO ACTS_IN VALUES(
	1,
     3,
     2,
     'background actor'
);

INSERT INTO ACTS_IN VALUES(
 	2,
     1,
     20,
     'cameo'
);

INSERT INTO ACTS_IN VALUES(
 	3,
     2,
     81,
     'main actor'
);

INSERT INTO ACTS_IN VALUES(
 	3,
     5,
     10,
     'cameo'
);

INSERT INTO ACTS_IN VALUES(
 	4,
     3,
     12,
     'background actor'
);

INSERT INTO ACTS_IN VALUES(
 	5,
     4,
     70,
     'main actor'
);

INSERT INTO ACTS_IN VALUES(
	6,
    5,
    60,
    'main actor'
);
INSERT INTO ACTS_IN VALUES(
 	6,
     1,
    15,
    'cameo'
);

INSERT INTO ACTS_IN VALUES(
	7,
     1,
    83,
     'main actor'
);

# insert into PRODUCED_IN table
INSERT INTO PRODUCED_IN VALUES( # (PID, MID)
 	2,
     1
);

INSERT INTO PRODUCED_IN VALUES(
 	3,
     2
);

INSERT INTO PRODUCED_IN VALUES(
	2,
    3
);

INSERT INTO PRODUCED_IN VALUES(
 	1,
    4
);

INSERT INTO PRODUCED_IN VALUES(
 	5,
    5
);


# insert into WORKS_IN table
INSERT INTO WORKS_IN VALUES( # (CrewMID, PID)
	2,
    1
);

INSERT INTO WORKS_IN VALUES(
 	1,
     2
);

INSERT INTO WORKS_IN VALUES(
 	5,
    3
);

INSERT INTO WORKS_IN VALUES(
	5,
    4
);

INSERT INTO WORKS_IN VALUES(
	3,
    5
);

INSERT INTO WORKS_IN VALUES(
 	1,
    6
);

INSERT INTO WORKS_IN VALUES(
 	4,
    7
);

INSERT INTO WORKS_IN VALUES(
 	4,
    8
);


# insert into GENRE table
INSERT INTO GENRE VALUES( # (MID, Genre)
	1,
    'action'
);

INSERT INTO GENRE VALUES(
	1,
    'crime'
);

INSERT INTO GENRE VALUES(
 	1,
    'mystery'
);

INSERT INTO GENRE VALUES(
 	2,
    'comedy'
);

INSERT INTO GENRE VALUES(
 	3,
    'romance'
);

INSERT INTO GENRE VALUES(
	3,
   'comedy'
);

INSERT INTO GENRE VALUES(
 	4,
    'crime'
);

INSERT INTO GENRE VALUES(
	5,
     'mystery'
);

