import { Stack, Link } from 'expo-router';
import { YStack, ButtonText, Theme } from 'tamagui';


import { Container, Main, Title, Subtitle, Button } from '../tamagui.config';
import LoginPage from './pages/LoginPage';
import SignUpPage from './pages/SignUpPage';
export default function Page() {
    return (
        <Theme name="light">
            <Container>
                <Main>
                    <Stack.Screen options={{ headerShown: false }} />
                    <LoginPage />
                    {/* <SignUpPage /> */}
                </Main>
            </Container>
        </Theme>
    );
}
