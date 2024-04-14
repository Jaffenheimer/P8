import {Link, router, Stack} from 'expo-router';
import React, {useState} from 'react';
import {YStack} from 'tamagui';

import {
    Container,
    ButtonText,
    LogOutButton,
    LogOutButtonContainer,
    MainPageTitle,
} from '~/tamagui.config';
import AsyncStorage from '@react-native-async-storage/async-storage';

const MainPage = () => {
    const [action, setAction] = useState('Keep Driving'); //speed up, slow down, keep driving
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

    return (
        <Container>
            <Stack.Screen options={{headerShown: false}}/>
            <YStack>
                <LogOutButtonContainer>
                        <LogOutButton onPress={logOut}>
                            <ButtonText>Log out</ButtonText>
                        </LogOutButton>
                </LogOutButtonContainer>
                <MainPageTitle>{action}</MainPageTitle>
            </YStack>
        </Container>
    );
};

export default MainPage;
