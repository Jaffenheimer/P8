# How to run app
There are multiple ways to run the application: Expo Go app, Using Simulator or running in browser.

## IMPORTANT: Remeber to Run NPM Install
Should be done every time something is added/changed in package.json
1. Go to into the App folder
2. Run `npm install` / `npm i` 


## Starting Application
`npx expo start`

If this do not work you will need to run it using a tunnel
Shortcut: `npm run startt`
Other Way: `npx expo start --tunnel`

You may have install tunnel first

### Expo Go App
1. Install Expo Go App
2. run `npx expo start` or `npm run startt`
3. Scan QR Code
    - iPhone - Scan QR code 
    - Andriod - Scan QR or insert path in the Expo App

### Others way than Expo Go App
1. run `npx expo start`
2. Follow the guide when staring project


#### If you are offline 
`npx expo start --offline`

### If you get a watchmen error, when running app with tunnel 
* `watchman watch-del 'YOUR LOCATION TO THE P8 PROJECT' `
* `watchman watch-project 'YOUR LOCATION TO THE P8 PROJECT'`