import { Stack, router } from 'expo-router';
import React, { useState } from 'react';

import { YStack, Text } from 'tamagui';
import { Title, Button, Container, Input, ButtonText } from '~/tamagui.config';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Location from 'expo-location';
const url = 'http://192.168.1.182:5000';
const LoginPage = () => {
    const [password, setPassword] = useState('');
    const [showWrongPasswordText, setShowWrongPasswordText] = useState(false);

    async function requestLocation() {
        let { status } = await Location.requestForegroundPermissionsAsync();
        if (status !== 'granted') {
            setError('Adgang til placering er nægtet');
            return;
        }
    }
    async function login() {
        requestLocation();
        try {
            const options = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Accept: 'application/json',
                    'access-control-allow-origin': '*',
                },
                body: JSON.stringify({
                    password: password,
                    latitude: 0,
                    longitude: 0,
                }),
            };
            await fetch(url + '/admin/bus', options).then((response) => {
                if (response.status === 400) {
                    setShowWrongPasswordText(true);
                } else {
                    response.json().then(async (data) => {
                        await AsyncStorage.setItem('bus-id', JSON.stringify(data));
                        router.replace('/pages/MainPage');
                    });
                }
            });
        } catch (error) {
            console.error(error);
            return;
        }
    }
    return (
        <Container>
            <Stack.Screen options={{ headerShown: false }} />
            <YStack>
                <Title>Login</Title>
                <Input
                    placeholder="Password"
                    testID="input-field"
                    secureTextEntry={true}
                    value={password}
                    onChangeText={(text) => setPassword(text)}
                />
                {showWrongPasswordText && (
                    <Text style={{ color: 'red' }}>Password does not match any route</Text>
                )}
                <Button onPress={login}>
                    <ButtonText>Start Driving</ButtonText>
                </Button>
            </YStack>
        </Container>
    );
};

export default LoginPage;
