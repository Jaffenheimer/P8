import { Link, Stack } from 'expo-router';
import React, { useState } from 'react';
import { YStack } from 'tamagui';

import {
    Container,
    ButtonText,
    LogOutButton,
    LogOutButtonContainer,
    MainPageTitle,
} from '~/tamagui.config';

// importScripts('https://js.pusher.com/7.0/pusher.worker.min.js');
import Pusher from 'pusher-js';
// import Pusher from '@pusher/pusher-websocket-react-native'
// const pusher = window.Pusher;

let secrets = require('../secrets.json');

const MainPage = () => {
    const [action, setAction] = useState('Keep Driving'); //speed up, slow down, keep driving
    let pusher = new Pusher(secrets.Pusher.AppKey, {
        cluster: 'eu',
        forceTLS: true,
    });
    pusherFunction = async () => {
        await pusher.connect();
        const channel = await pusher.subscribe('action');
        channel.bind('test_event', function (data) {
            console.log('Event received:', data);
            setAction(data.message);
        });
    };
    pusherFunction();
    return (
        <Container>
            <Stack.Screen options={{ headerShown: false }} />
            <YStack>
                <LogOutButtonContainer>
                    <Link href="/pages/LoginPage" asChild>
                        <LogOutButton>
                            <ButtonText>Log out</ButtonText>
                        </LogOutButton>
                    </Link>
                </LogOutButtonContainer>
                <MainPageTitle>{action}</MainPageTitle>
            </YStack>
        </Container>
    );
};

export default MainPage;
