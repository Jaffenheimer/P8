import {Link, router, Stack} from 'expo-router';
import React, {useEffect, useState} from 'react';
import {YStack} from 'tamagui';

import {
    Container, ButtonText, LogOutButton, LogOutButtonContainer, MainPageTitle,
} from '~/tamagui.config';
import AsyncStorage from '@react-native-async-storage/async-storage';

// importScripts('https://js.pusher.com/7.0/pusher.worker.min.js');
import Pusher from 'pusher-js';
// import Pusher from '@pusher/pusher-websocket-react-native'
// const pusher = window.Pusher;

let secrets = require('../secrets.json');


const MainPage = () => {
    const [action, setAction] = useState('Keep Driving'); //speed up, slow down, keep driving
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
                method: 'Delete', headers: {
                    'Content-Type': 'application/json', Accept: 'application/json', 'access-control-allow-origin': '*',
                }, body: JSON.stringify({
                    busId: JSON.parse(BusId),
                }),
            };
            await fetch('http://10.0.0.10:5000/admin/bus/delete', options).then((response) => {
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

    let pusher = new Pusher(secrets.Pusher.AppKey, {
        cluster: 'eu', forceTLS: true,
    });
    let pusherFunction = async () => {
        await pusher.connect();
        const channel = await pusher.subscribe('action');
        channel.bind('test_event', function (data) {
            if (typeof data === 'string') {
                data = JSON.parse(data);
            }
            Object.keys(data.Actions).forEach((key) => {
                if (JSON.parse(busId) === key) {
                    const actionValue = Object.values(data.Actions)[0];
                    if (actionValue === 0) {
                        setAction('Default');
                    } else if (actionValue === 1) {
                        setAction('Maintain Speed');
                    } else if (actionValue === 2) {
                        setAction('Speed Up');
                    } else if (actionValue === 3) {
                        setAction('Slow Down');
                    }
                }
            });
        });
    };
    pusherFunction();
    return (<Container>
        <Stack.Screen options={{headerShown: false}}/>
        <YStack>
            <LogOutButtonContainer>
                <LogOutButton onPress={logOut}>
                    <ButtonText>Log out</ButtonText>
                </LogOutButton>
            </LogOutButtonContainer>
            <MainPageTitle>{action}</MainPageTitle>
        </YStack>
    </Container>);
};

export default MainPage;
