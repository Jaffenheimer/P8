import React from 'react';
import { Stack, Link } from 'expo-router';
import { YStack, SizableText, Anchor } from 'tamagui';

import {
    Title,
    Container,
    Input,
    UserInformationForm,
    Button,
    ButtonText,
    LinkText,
    LinkContainer,
} from '~/tamagui.config';

const SignUpPage = () => {
    return (
        <Container>
            <Stack.Screen options={{ headerShown: false }} />
            <YStack>
                <Title>Sign Up</Title>
                <UserInformationForm>
                    <Input placeholder="Username" />
                    <Input placeholder="Email" />
                    <Input placeholder="Password" />
                    <Input placeholder="Confirm Password" />
                </UserInformationForm>
                <Button>
                    <ButtonText>Sign Up</ButtonText>
                </Button>
                <LinkContainer>
                    <Link href="/pages/LoginPage">
                        Already have an account? <LinkText>Back to Login</LinkText>
                    </Link>
                </LinkContainer>
            </YStack>
        </Container>
    );
};

export default SignUpPage;
