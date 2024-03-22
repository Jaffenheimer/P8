import { Stack, Link } from 'expo-router';
import { YStack, ButtonText } from 'tamagui';

import { Container, Main, Title, Subtitle, Button } from '../tamagui.config';
import LoginPage from './pages/LoginPage';
export default function Page() {
  return (
    <Container>
      <Main>
        <Stack.Screen />
        <LoginPage />
      </Main>
    </Container>
  );
}
