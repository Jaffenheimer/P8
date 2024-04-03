# P8 Mobility

## Docker
* Download docker locally
* Navigate to `db-docker`
* Type and run `docker compose up` 
* Open the database in DB admin tool* Run `npm i` after pulling

## Frontend/App
* Navigate to Frontend
* Run `npm i` after pulling

### Run App
* Run `npx expo start` or `npm run start` to run without tunnel
* Run `npm run startt` to run in tunnel

### Frontend Testing
* Run `npm test` or `npm run test` 

## SUMO
install make if you do not have
cd into Simulation\SUMO\makefile
generate the appropriate xml files with `make run`
    if you do not have all the packages install them with pip
    
Alternatively just run both python files in the SUMO folder (The generated xml files must be in the SUMO folder)

