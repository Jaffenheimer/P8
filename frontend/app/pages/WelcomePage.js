import React from 'react';
import { Title, Container } from '~/tamagui.config';
import { useState } from 'react';
import { Stack } from 'expo-router';
import { YStack } from 'tamagui';
import Select from '../components/Select';

const WelcomePage = () => {
    const [country, setCountry] = useState('');

    const countries = ['Chile', 'Peru'];
    const citiesChile = ['Santiago', 'Valparaiso'];
    const citiesPeru = ['Lima', 'Arequipa'];
    const busRoutesSantiago = ['Route 1', 'Route 2'];
    const busRoutesValparaiso = ['Route 1', 'Route 2'];
    const busRoutesLima = ['Route 1', 'Route 2'];
    const busRoutesArequipa = ['Route 1', 'Route 2'];

    return (
        <Container>
            <Stack.Screen options={{ headerShown: false }} />
            <YStack>
                <Title>Welcome</Title>

                <Select items={countries} title={'Select a country'} />
                
                
            </YStack>
        </Container>
    );
};

export default WelcomePage;
