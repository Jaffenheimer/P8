import { Stack } from 'expo-router';
import { Theme } from 'tamagui';

import { Container, Main } from '~/tamagui.config';
import LoginPage from './pages/LoginPage';
import React from "react";
import MainPage from "~/app/pages/MainPage";

export default function Page() {
    return (
        <Theme name="light">
            <Container>
                <Main>
                    <Stack.Screen options={{ headerShown: false }}/>
                    <LoginPage/>
                </Main>
            </Container>
        </Theme>
    );
}
