import React from 'react';
import {
    Title,
    Container,
    SelectContainer,
    Button,
    ButtonText,
    NextButton,
    BottomOfWelcomePage,
} from '~/tamagui.config';
import { useState } from 'react';
import { Stack } from 'expo-router';
import { YStack, Text } from 'tamagui';
import Select from '../components/Select';
import { ArrowLeft } from 'lucide-react-native';

const WelcomePage = () => {
    const [country, setCountry] = useState('');
    const [city, setCity] = useState('');
    const [route, setRoute] = useState('');

    const countries = ['Chile', 'Peru'];
    const citiesChile = ['Santiago', 'Valparaiso'];
    const citiesPeru = ['Lima', 'Arequipa'];
    const busRoutesSantiago = ['Santiago 1', 'Santiago 2'];
    const busRoutesValparaiso = ['Valparaiso 1', 'Valparaiso 2'];
    const busRoutesLima = ['Lima 1', 'Lima 2'];
    const busRoutesArequipa = ['Arequipa 1', 'Arequipa 2'];

    function setCitySelect() {
        switch (country) {
            case 'Chile':
                return citiesChile;
            case 'Peru':
                return citiesPeru;
            default:
                return [];
        }
    }

    function setRoutesSelect() {
        switch (city) {
            case 'Santiago':
                return busRoutesSantiago;
            case 'Valparaiso':
                return busRoutesValparaiso;
            case 'Lima':
                return busRoutesLima;
            case 'Arequipa':
                return busRoutesArequipa;
            default:
                return [];
        }
    }

    return (
        <Container>
            <Stack.Screen options={{title: 'Welcome'}} />

            
            <SelectContainer>
                <Select items={countries} title={'Select a country'} onChange={setCountry} />
                {country === '' ? (
                    ''
                ) : (
                    <Select items={setCitySelect()} title={'Select a city'} onChange={setCity} />
                )}
                {city === '' ? (
                    ''
                ) : (
                    <Select
                        items={setRoutesSelect()}
                        title={'Select a route'}
                        onChange={setRoute}
                    />
                )}
            </SelectContainer>
            <BottomOfWelcomePage>
                <NextButton>
                    <ButtonText>Next</ButtonText>
                </NextButton>
            </BottomOfWelcomePage>
        </Container>
    );
};

export default WelcomePage;
