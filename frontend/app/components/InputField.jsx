import { Stack } from 'expo-router';
import React from 'react';
import { YStack, SizableText, Text } from 'tamagui';

import {Input, InputLabel } from '~/tamagui.config';

const inputField = ({ label }) => {
  return (
    <YStack>
      <Stack.Screen options={{ headerShown: false }} />
      <InputLabel>
        {label}
      </InputLabel>
      <Input type="text" placeholder={label} />
    </YStack>
  );
};

export default inputField;
