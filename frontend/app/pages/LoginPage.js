import { Link, Stack } from 'expo-router';
import React from 'react';
import { YStack } from 'tamagui';

import {
    Title,
    Button,
    Container,
    Input,
    ButtonText,
    UserInformationForm,
} from '~/tamagui.config';

const LoginPage = () => {
    return (
        <Container>
            <Stack.Screen options={{ headerShown: false }} />
            <YStack>
                <Title>Login</Title>
                <UserInformationForm>
                    <Input placeholder="Password" testID="input-field" secureTextEntry={true} />
                </UserInformationForm>
                <Link href="/pages/MainPage" asChild>
                    <Button href="/pages/MainPage">
                        <ButtonText>Start Driving</ButtonText>
                    </Button>
                </Link>
            </YStack>
        </Container>
    );
};

export default LoginPage;
