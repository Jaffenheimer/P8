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

const MainPage = () => {
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
