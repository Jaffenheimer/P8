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
import {
    Pusher,
    PusherMember,
    PusherChannel,
    PusherEvent,
} from '@pusher/pusher-websocket-react-native';
const appConfig = require('../app.json');

const MainPage = async () => {
    const pusher = Pusher.getInstance();

    await pusher.init({
        appId: appConfig.pusher.appId,
        key: appConfig.pusher.key,
        secret: appConfig.pusher.secret,
        cluster: appConfig.pusher.cluster,
    });

    await pusher.connect();
    await pusher.subscribe({
        channelName: 'action',
        onEvent: (event) => {
            console.log('Event received:, ${event}');
            setAction(event.message);
        },
    });
    
    const [action, setAction] = useState('Keep Driving'); //speed up, slow down, keep driving
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
