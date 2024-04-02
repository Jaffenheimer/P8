import { Link, Stack } from 'expo-router';
import React from 'react';
import { YStack } from 'tamagui';

import {
    Title,
    Button,
    Container,
    Input,
    ButtonText,
    LinkContainer,
    LinkText,
    UserInformationForm,
} from '~/tamagui.config';

const LoginPage = () => {
    return (
        <Container>
            <Stack.Screen options={{ headerShown: false }} />
            <YStack>
                <Title>Login</Title>
                <UserInformationForm>
                    <Input placeholder="Username" />
                    <Input placeholder="Password" />
                </UserInformationForm>
                <Button>
                    <ButtonText>Login</ButtonText>
                </Button>
                <LinkContainer>
                    <Link href="/pages/SignUpPage">
                        Don't have an account? <LinkText>Sign Up</LinkText>
                    </Link>
                </LinkContainer>
            </YStack>
        </Container>
    );
};

export default LoginPage;
