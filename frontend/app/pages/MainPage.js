import {Theme} from 'tamagui';

import {Container, Main} from '~/tamagui.config';
import {MainPageLogic} from "../components/MainPageLogic";
import {Arrows} from "../components/Arrows";
import React, {useEffect, useState} from "react";

export default function MainPage() {
    return (
        <Theme name="light">
            <Container>
                <Main>
                    <MainPageLogic/>
                    <Arrows/>
                </Main>
            </Container>
        </Theme>
    );
}