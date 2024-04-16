import {Theme} from 'tamagui';

import {Container, Main, MainPageTitle} from '~/tamagui.config';
import MainPageLogic from "../components/MainPageLogic";
import Arrows from "../components/Arrows";
import React, {useEffect, useState} from "react";
import {Stack} from "expo-router";
import AsyncStorage from "@react-native-async-storage/async-storage";



export default function MainPage() {
    const [currentAction, setCurrentAction] = useState(); // Add this line

    useEffect(() => {
        async function fetchCurrentAction() {
            const action = await AsyncStorage.getItem('action');
            setCurrentAction(action);
        }
        fetchCurrentAction();
    }, []);
    return (
        <Container>
            <Main>
                <Stack.Screen options={{headerShown: false}}/>
                <MainPageLogic/>
                <Arrows/>
            </Main>
        </Container>
    );
}