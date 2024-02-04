Gateway
For weather 
- Get coordinates of a city, call to the weather api to get that - weather/coordinates/{city}"

![image](https://github.com/Catalin-Tin/Gateway/assets/91093455/d700a14a-797f-4b61-b8d1-a7ad655609f0)

![image](https://github.com/Catalin-Tin/Gateway/assets/91093455/f0113138-f105-4157-b54a-e4d451a5b742)

- Get weather per city for the next 5 days - weather/forecast/{city}  (needs gateway to be active to test)

![image](https://github.com/Catalin-Tin/Gateway/assets/91093455/b9ec56f7-62d5-471c-9623-0fd31f78555a)

- Get weather per city right now - weather/{city}

![image](https://github.com/Catalin-Tin/Gateway/assets/91093455/a1991406-315b-4a9e-81a7-92b3f6ebd448)

- Choose the warmest day without rain in the next 5 days - weather/warmestday/{city}

![image](https://github.com/Catalin-Tin/Gateway/assets/91093455/d4e96d09-0e51-4c8f-8e08-b60a2a90f406)

For football
- Get venues by city - football/venues/{city}

![image](https://github.com/Catalin-Tin/Gateway/assets/91093455/6b7e2cf8-85dc-4207-8dbf-3e27425ef2b4)
  
- Get all the matches in the Premier League on the next 5 days - football/getmatches

![image](https://github.com/Catalin-Tin/Gateway/assets/91093455/4359527a-9e89-464c-9e87-6a5721e08ddf)

- Find a match between 2 teams in the next 5 days - football/getmatch/{home}/{away}

![image](https://github.com/Catalin-Tin/Gateway/assets/91093455/2eb6920b-b36a-4ca6-8f09-d5fa94bc4c28)

- Get all matches on a certain day - football/getmatches/{day}

![image](https://github.com/Catalin-Tin/Gateway/assets/91093455/fbc2eee6-907b-401e-8e22-9ebf0e3f3519)

Combining 
- Combines the match that the user is requesting by teams, and it suggests to the user whether to go to the match based on the weather that day - football/plan/{home}/{away}

![image](https://github.com/Catalin-Tin/Gateway/assets/91093455/e8b0ca83-74c4-4001-adb4-471511f2fcac)

- Get the warmest day in the next 5 days in the specific city and suggest matches taking place in that city, if there are none, suggest other matches in UK on that day. - plan/warmest/{city}

![image](https://github.com/Catalin-Tin/Gateway/assets/91093455/5465447a-2279-4063-9ef8-dc7159553f31)

- Get the day you want, and choose the warmest city and match in that city - plan/{date}

![image](https://github.com/Catalin-Tin/Gateway/assets/91093455/47ba22d5-c774-4da9-9c4f-e3ddfc278127)

Tasks:

- Separated DataBase

1. CREATE TABLE `football`.`Matches` (
  `City` CHAR(36) NOT NULL,
  `Date` DATETIME NOT NULL,
  `Home` VARCHAR(45),
  `Away` VARCHAR(45),
  PRIMARY KEY (`City`, `Date`));

2. CREATE TABLE `weather`.`Cities` (
  `Id` CHAR(36) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `longitude` DOUBLE NOT NULL,
  `latitude` DOUBLE NOT NULL,
  PRIMARY KEY (`Id`));

CREATE TABLE `weather`.`Weather` (
  `Id` CHAR(36) NOT NULL,
  `Temperature` DOUBLE NOT NULL,
  `Date` datetime NOT NULL,
  `City` VARCHAR(45) NOT NULL,
  `Description` VARCHAR(45) NOT NULL,
  `Condition` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`Id`));


  - Status Endpoint
    
![image](https://github.com/Catalin-Tin/Gateway/assets/91093455/3c722d69-eb4b-4139-bd31-c91fc6fc8876)

- Task Timeouts

![image](https://github.com/Catalin-Tin/Gateway/assets/91093455/5441dadd-72b8-4fe1-b96c-773313cd7ee5)

- Concurrent Tasks Limit

Implemented with the method ThreadPool.SetMaxThreads(int workerThreads, int completionPortThreads) which sets the maximum number of worker threads and asynchronous I/O completion threads that the ThreadPool will maintain.

- Gateway

Everything is in the main.py file and all the comments in the code.

- Redis Cache for gateway

Implemented with timeout=30

1. First request

![image](https://github.com/Catalin-Tin/Gateway/assets/91093455/eb506754-ece2-468a-9196-5a163b588049)

2. Second request

![image](https://github.com/Catalin-Tin/Gateway/assets/91093455/b36da0bc-d2ab-4e84-a079-22fa29478f5b)

- Load Balacing Round Robin

football_service_instances = [
    "http://football1:8080",
    "http://football2:8080",
    "http://football3:8080"
]
weather_service_instances = [
    "http://weather1:8080",
    "http://weather2:8080",
    "http://weather3:8080"
]

![image](https://github.com/Catalin-Tin/Gateway/assets/91093455/8a0ec8fd-dbe8-4af4-90ee-115c43fbd235)

- ELK stack + Grafana

Two Indexis

![image](https://github.com/Catalin-Tin/Gateway/assets/91093455/36de61bd-e0e8-4cb5-96eb-0344c621908a)

Kibana

![image](https://github.com/Catalin-Tin/Gateway/assets/91093455/ea10a9d9-bb46-4345-bb10-a26cc042839b)


