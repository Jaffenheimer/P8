import { Stack } from 'expo-router';
import { Theme } from 'tamagui';

import { Container, Main } from '../tamagui.config';
import LoginPage from './pages/LoginPage';
import React from "react";
import Arrows from './components/Arrows';
import MainPageLogic from "~/app/components/MainPageLogic";

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
