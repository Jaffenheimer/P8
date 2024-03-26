import React, { useState } from 'react';
import { StyleSheet, View } from 'react-native';
import { Picker } from '@react-native-picker/picker';
import { Container, PickerContainer } from '~/tamagui.config';
import { Stack } from 'expo-router';
import { YStack } from 'tamagui';

const Select = ({ items, title, onChange }) => {
    const [value, setEnable] = useState('');

    function onChangeFunction(itemValue) {
        setEnable(itemValue);
        onChange(itemValue);
    }

    return (
        <Container>
            <Stack.Screen options={{ headerShown: false }} />
            <Picker selectedValue={value} onValueChange={onChangeFunction}>
                <Picker.Item
                    value=""
                    label={`--- ${title} ---`}
                    enabled={value === '' ? true : false}
                />
                {items.map((item) => (
                    <Picker.Item label={item} value={item} key={item} />
                ))}
            </Picker>
        </Container>
    );
};
export default Select;
