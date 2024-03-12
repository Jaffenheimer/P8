import { Stack, Link } from 'expo-router';

import { Container, Main, Title, Subtitle, TopHalf, ButtomHalf } from '../tamagui.config';

export default function Layout() {
  return (
    <Container>
      <Main>
        <Stack.Screen options={{ title: 'Layout' }} />
        <TopHalf>
          <Subtitle>This is the Top</Subtitle>
        </TopHalf>
        <ButtomHalf>
          <Subtitle>This is the Buttom</Subtitle>
        </ButtomHalf>
      </Main>
    </Container>
  );
}
