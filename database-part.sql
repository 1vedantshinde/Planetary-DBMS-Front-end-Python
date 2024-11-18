create database projectfinal;
show databases;
use projectfinal;

create table starSystem (
SID int primary key,
StellarName varchar(70),
NoofStars int,
NoofPlanets int,
Distance float,
RA varchar(70),
Declination varchar(70)

);
select *from starSystem;

create table planets(
PID int primary key,
planetname varchar(70),
orbitalperiod float,
eradius float,
Jradius float,
eccentricity float,
equilibriumtemperature float,
SID int,
FOREIGN KEY (SID) REFERENCES starSystem(SID)
);
select *from planets;

create table starCharacteristics(
StarID int primary key,
SID int,
stellarMass float,
stellarRadius float,
surfaceGravity float,
stellarTemp int,
spectralType varchar(40),
FOREIGN KEY (SID) REFERENCES starSystem(SID)
);
select *from starCharacteristics;


create table orbitalPropt(
OPID int primary key,
SID int,
orbitalPeriod float,
eccentricity float,
FOREIGN KEY (SID) REFERENCES starSystem(SID)
);
select *from orbitalPropt;

create table Metallicity(
CompId int primary key,
StarID int,
stellarMetallicity float,
stellarRatio varchar(20),
FOREIGN KEY (StarID) REFERENCES starCharacteristics(StarID)
);
select *from Metallicity;

create table Discovery(
DiscoveryID int primary key,
discoveryMethod varchar(40),
discoveryYear int,
SID int,
FOREIGN KEY (SID) REFERENCES starSystem(SID)
);
select *from Discovery;

create table Facility(
FacilityID int primary key,
facilityname varchar(70)
);
select *from Facility;

create table discoveryFacility(
DiscoveryId int,
FacilityID int,
primary key (DiscoveryID, FacilityID),
FOREIGN KEY (DiscoveryID) REFERENCES Discovery(DiscoveryID),
FOREIGN KEY (FacilityID) REFERENCES Facility(FacilityID)
);
select *from discoveryFacility;


#1. Get Stellar Systems with More Than 3 Planets (Filtering with WHERE)
SELECT * FROM starSystem
WHERE NoofPlanets > 3;

-- 2. Select Stellar Systems Within a Certain Distance Range (Advanced Filtering with BETWEEN)
SELECT * FROM starSystem
WHERE Distance BETWEEN 10.0 AND 50.0;

-- 3. Sort Planets by Orbital Period (ORDER BY)
SELECT * FROM planets
ORDER BY orbitalperiod DESC; 

-- 4. Count the Number of Planets in Each Stellar System (GROUP BY)
SELECT SID, COUNT(*) AS PlanetCount
FROM planets
GROUP BY SID;

-- 5. List Discoveries Made After the Year 2000 (Filtering with WHERE)
SELECT * FROM Discovery
WHERE discoveryYear > 2000;

#Total Number of planets and stars in the system
SELECT
    SID,
    StellarName,
    NoofStars,
    NoofPlanets
FROM starSystem
WHERE NoofPlanets > 3
ORDER BY NoofPlanets DESC;

#planets with high eccentricity
SELECT 
    planetname, 
    orbitalperiod, 
    eccentricity 
FROM planets 
WHERE eccentricity < 0.2
ORDER BY eccentricity DESC;

#Discoveries sorted by year
SELECT 
    DiscoveryID, 
    discoveryMethod, 
    discoveryYear 
FROM Discovery 
ORDER BY discoveryYear DESC;

#Planets by Orbital Period Range
SELECT planetname, orbitalperiod, SID 
FROM planets 
WHERE orbitalperiod BETWEEN %s AND %s;

SELECT stellarMetallicity, stellarRatio, StellarName 
FROM Metallicity 
JOIN starCharacteristics ON Metallicity.StarID = starCharacteristics.StarID 
JOIN starSystem ON starCharacteristics.SID = starSystem.SID 
WHERE stellarMetallicity > %s;

    
#Show all Planets discovered by a specific method
SELECT planetname, discoveryYear, discoveryMethod
FROM planets
JOIN Discovery on planets.SID = Discovery.SID
WHERE discoveryMethod = %s;

#Planets having graceful orbits with high eccentricity and longer orbital period
SELECT starSystem.StellarName, orbitalPropt.orbitalPeriod, orbitalPropt.eccentricity 
FROM starSystem 
JOIN orbitalPropt ON starSystem.SID = orbitalPropt.SID 
WHERE orbitalPropt.eccentricity > 0.5 AND orbitalPropt.orbitalPeriod > 300;

SELECT starSystem.StellarName, starCharacteristics.stellarTemp
FROM starCharacteristics
JOIN starSystem ON starCharacteristics.SID = starSystem.SID
WHERE starCharacteristics.stellarTemp BETWEEN %s AND %s;

DESCRIBE starSystem;




