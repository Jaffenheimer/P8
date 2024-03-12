import { Stack, Link } from 'expo-router';
import { YStack, active, ButtonText } from 'tamagui';

import { Container, Main, Title, Subtitle, TopHalf, ButtomHalf, Button } from '../tamagui.config';

export default function Page() {
  return (
    <Container>
      <Main>
        <Stack.Screen options={{ title: 'Overview' }} />
        <YStack>
          <Title>Test App</Title>
          <Subtitle>Welcome to this test app</Subtitle>
        </YStack>
        <YStack>
          <Link href={'/layouttest'}>
            <Button style={'padding: 3px'}>
              <ButtonText>Go To Layout</ButtonText>
            </Button>
          </Link>
        </YStack>
      </Main>
    </Container>
  );
}
