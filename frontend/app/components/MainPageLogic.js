import {Link, router, Stack} from 'expo-router';
import React, {useEffect, useState} from 'react';
import {Theme, YStack, AlertDialog, XStack, Button} from 'tamagui';
import * as Location from 'expo-location';

import {
    Container,
    ButtonText,
    LogOutButton,
    LogOutButtonContainer,
} from '~/tamagui.config';
import AsyncStorage from '@react-native-async-storage/async-storage';
import ip from '../constants.json';
import LogOut from "./LogOut";

const url = ip.ip;
const port = ip.port;

async function getLocation() {
    let currentLocation = await Location.getCurrentPositionAsync();
    return currentLocation;
}

setInterval(sendLocation, 10000);

async function sendLocation() {
    const location = await getLocation();
    const BusId = await AsyncStorage.getItem('bus-id');
    try {
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Accept: 'application/json',
                'access-control-allow-origin': '*',
            },
            body: JSON.stringify({
                busId: JSON.parse(BusId),
                latitude: JSON.parse(location.coords.latitude),
                longitude: JSON.parse(location.coords.longitude),
            }),
        };
        await fetch('http://' + url + ':' + port + '/admin/bus/location', options).then((response) => {
            if (response.status === 400) {
                console.log(response.status);
            }
        });
    } catch (error) {
        console.error(error);
        return;
    }
}

const MainPageLogic = () => {
    const [busId, setBusId] = useState(null);

    useEffect(() => {
        async function fetchBusId() {
            const id = await AsyncStorage.getItem('bus-id');
            setBusId(id);
        }

        fetchBusId();
    }, []);

    console.log(busId);

    return (
        <Theme name="light">
            <Container style={{flexDirection: 'column', justifyContent: 'flex-end'}}>
                <Stack.Screen options={{headerShown: false}}/>
                <YStack>
                    <LogOutButtonContainer>
                        <LogOut/>
                    </LogOutButtonContainer>
                </YStack>
            </Container>
        </Theme>
    );
};
export default MainPageLogic;
