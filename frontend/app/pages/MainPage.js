import {Theme} from 'tamagui';

import {Container, Main, MainPageTitle} from '~/tamagui.config';
import MainPageLogic from "../components/MainPageLogic";
import Arrows from "../components/Arrows";
import React, {useEffect, useState} from "react";



export default function MainPage() {
    return (
        <Container>
            <Main>
                <Arrows/>
                <MainPageLogic/>
            </Main>
        </Container>
    );
}