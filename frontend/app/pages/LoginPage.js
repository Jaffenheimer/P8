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
            <Stack.Screen options={{ title: 'Login' }} />
            <YStack>
                <UserInformationForm>
                    <Input placeholder="Username" testID="input-field" />
                    <Input placeholder="Password" testID="input-field" secureTextEntry={true} />
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
