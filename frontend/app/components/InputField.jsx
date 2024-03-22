import React from 'react';
import { YStack, ButtonText, SizableText } from 'tamagui';

import { Title, Button, Container, Input} from '~/tamagui.config';

const inputField = ({ label }) => {
  return (
    <Container>
      <YStack>
        <SizableText>{label}</SizableText>
        <Input type="text" placeholder={label} />
      </YStack>
    </Container>
  );
};

export default inputField;
