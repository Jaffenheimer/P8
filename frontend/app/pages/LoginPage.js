import React from 'react';
import { YStack, ButtonText, SizableText } from 'tamagui';

import { Title, Button, Container } from '~/tamagui.config';

import InputField from '../components/InputField';

const LoginPage = () => {
  return (
    <Container>
      <YStack>
        <Title>Login</Title>
        <InputField label="Username" />
        <InputField label="Password" />
        <Button>
          <SizableText>Login</SizableText>
        </Button>
        <Button>
          <SizableText>Create Account</SizableText>
        </Button>
      </YStack>
    </Container>
  );
};

export default LoginPage;
