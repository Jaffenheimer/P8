# P8 Mobility

## Pusher
* Create an account on pusher.com
* Add a section in the appsettings.json file called "Pusher" and add the values to the section in the following format:
"Pusher": {
    "AppId": "",
    "AppKey": "",
    "AppSecret": "",
    "Cluster": ""
  }
* Create a secrets.json file in the "App" folder in the frontend and add the values in the same manner.


## Docker
* Download and install docker locally
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

## Github

### Frontend comitting
* NEVER commit the secrets.json file

### Backend comitting
* NEVER commit the appsettings.json file without removing the "Pusher" Fields

## SUMO
If you want a different person flow run the `generate_person_flow.py` (since the amount of persons is random and change when you run this file) - the output file must be in the SUMO folder, so remember to run that file in the SUMO folder 