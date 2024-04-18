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
import {Alert} from "react-native";
import ip from '../constants.json';

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
            await fetch('http://' + url + ':' + port + '/admin/bus/delete', options).then((response) => {
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
                        <AlertDialog native>
                            <AlertDialog.Trigger asChild>
                                <LogOutButton>
                                    <ButtonText>Log out</ButtonText>
                                </LogOutButton>
                            </AlertDialog.Trigger>
                            <AlertDialog.Portal>
                                <AlertDialog.Overlay
                                    key="overlay"
                                    animation="quick"
                                    opacity={0.5}
                                    enterStyle={{opacity: 0}}
                                    exitStyle={{opacity: 0}}
                                />
                                <AlertDialog.Content
                                    bordered
                                    elevate
                                    key="content"
                                    animation={['quick', {
                                        opacity: {
                                            overshootClamping: true,
                                        },
                                    },]}
                                    enterStyle={{x: 0, y: -20, opacity: 0, scale: 0.9}}
                                    exitStyle={{x: 0, y: 10, opacity: 0, scale: 0.95}}
                                    x={0}
                                    scale={1}
                                    opacity={1}
                                    y={0}
                                >
                                    <YStack space>
                                        <AlertDialog.Title>Are you sure?</AlertDialog.Title>
                                        <XStack space="$3" justifyContent="flex-end">
                                            <AlertDialog.Cancel asChild>
                                                <Button>Cancel</Button>
                                            </AlertDialog.Cancel>
                                            <AlertDialog.Action asChild onPress={logOut}>
                                                <Button>Log Out</Button>
                                            </AlertDialog.Action>
                                        </XStack>
                                    </YStack>
                                </AlertDialog.Content>
                            </AlertDialog.Portal>
                        </AlertDialog>
                    </LogOutButtonContainer>
                </YStack>
            </Container>
        </Theme>
    );
};
export default MainPageLogic;
