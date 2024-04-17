import {Link, router, Stack} from 'expo-router';
import React, {useEffect, useState} from 'react';
import {Theme, YStack} from 'tamagui';
import * as Location from 'expo-location';
import {Arrows} from '../components/Arrows.js';

import {
    Container,
    ButtonText,
    LogOutButton,
    LogOutButtonContainer,
} from '~/tamagui.config';
import AsyncStorage from '@react-native-async-storage/async-storage';

const url = 'http://192.168.1.186:5000';

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
        await fetch(url + '/admin/bus/location', options).then((response) => {
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

    async function logOut() {
        const BusId = await AsyncStorage.getItem('bus-id');
        try {
            const options = {
                method: 'Delete',
                headers: {
                    'Content-Type': 'application/json',
                    Accept: 'application/json',
                    'access-control-allow-origin': '*',
                },
                body: JSON.stringify({
                    busId: JSON.parse(BusId),
                }),
            };
            await fetch(url + '/admin/bus/delete', options).then((response) => {
                if (response.status === 400) {
                    console.log(response.status);
                } else {
                    router.replace('/pages/LoginPage');
                }
            });
        } catch (error) {
            console.error(error);
            return;
        }
    }

    console.log(busId);

    return (
        <Theme name="light">
            <Container style={{flexDirection: 'column', justifyContent: 'flex-end'}}>
                <Stack.Screen options={{headerShown: false}}/>
                <YStack>
                    <LogOutButtonContainer>
                        <LogOutButton onPress={logOut}>
                            <ButtonText>Log out</ButtonText>
                        </LogOutButton>
                    </LogOutButtonContainer>
                </YStack>
            </Container>
        </Theme>
    );
};
export default MainPageLogic;
