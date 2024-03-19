import { Stack, Link } from 'expo-router';

import { Container, Main, Subtitle, TopHalf, ButtomHalf } from '../tamagui.config';

function Layouttest() {
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

export default Layouttest;
