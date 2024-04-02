import React, { useEffect } from 'react';
import {
    Container,
    SelectContainer,
    ButtonText,
    NextButton,
    BottomOfWelcomePage,
} from '~/tamagui.config';
import { useState } from 'react';
import { Stack } from 'expo-router';
import { Text } from 'tamagui';
import Select from '../components/Select';

const WelcomePage = () => {
    const [country, setCountry] = useState('');
    const [city, setCity] = useState('');
    const [route, setRoute] = useState('');

    const countriesAndCities = {
        Chile: ['Santiago', 'Valparaiso'],
        Peru: ['Lima', 'Arequipa'],
    };

    const citiesAndRoutes = {
        Santiago: ['Santiago 1', 'Santiago 2'],
        Valparaiso: ['Valparaiso 1', 'Valparaiso 2'],
        Lima: ['Lima 1', 'Lima 2'],
        Arequipa: ['Arequipa 1', 'Arequipa 2'],
    };

    //when resetting country, city and route should be reset as well
    useEffect(() => {
        if (country === '') {
            setCity('');
            setRoute('');
        }
    }, [country]);

    //when resetting city, route should be reset as well
    useEffect(() => {
        if (city === '') {
            setRoute('');
        }
    }, [city]);

    // dynamically set the options for the city select based on the selected country
    function setCitySelect() {
        return countriesAndCities[country] || [];
    }

    // dynamically set the options for the route select based on the selected city
    function setRoutesSelect() {
        return citiesAndRoutes[city] || [];
    }

    return (
        <Container>
            <Stack.Screen options={{ title: 'Welcome' }} />

            <SelectContainer>
                <Select
                    items={Object.keys(countriesAndCities)}
                    title={'Select a country'}
                    onChange={setCountry}
                />
                <Text>{'\n'}</Text>
                {country === '' ? (
                    ''
                ) : (
                    <>
                        <Select
                            items={setCitySelect()}
                            title={'Select a city'}
                            onChange={setCity}
                        />
                        <Text>{'\n'}</Text>
                    </>
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
