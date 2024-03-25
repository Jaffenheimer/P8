import { Stack } from 'expo-router';
import { Theme } from 'tamagui';


import { Container, Main } from '../tamagui.config';
import LoginPage from './pages/LoginPage';
import SignUpPage from './pages/SignUpPage';
import WelcomePage from './pages/WelcomePage';

export default function Page() {
    return (
        <Theme name="light">
            <Container>
                <Main>
                    <Stack.Screen options={{ headerShown: false }} />
                    {/* <LoginPage /> */}
                    {/* <SignUpPage /> */}
                    <WelcomePage />
                </Main>
            </Container>
        </Theme>
    );
}
