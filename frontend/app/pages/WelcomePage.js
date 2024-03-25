import React from 'react';
import { Title, Container } from '~/tamagui.config';
import { useState} from 'react';
import { Stack } from 'expo-router';
import { YStack } from 'tamagui';
import Select from '../components/Select';

const WelcomePage = () => {
    const [val, setVal] = useState('apple');
    const fruit = [
        "apple",
        "banana",
        "cherry",
        "date",
        "elderberry",
        "fig",
        "grape",
    ];
    return (
        <Container>
            <Stack.Screen options={{ headerShown: false }} />
            <YStack>
                <Title>Welcome</Title>
                <Select items={fruit} />
            </YStack>
        </Container>
    );
};

export default WelcomePage;
