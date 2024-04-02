import React, { useState } from 'react';
import RNPickerSelect from 'react-native-picker-select';
import { Container } from '~/tamagui.config';
import { Stack } from 'expo-router';
import { View, Text } from 'tamagui';

const Select = ({ items, title, onChange }) => {
    const [value, setValue] = useState('');

    function onChangeFunction(itemValue) {
        setValue(itemValue);
        onChange(itemValue);
    }

    return (
        <Container>
            <Stack.Screen />
            <RNPickerSelect
                onValueChange={onChangeFunction}
                items={items.map((item) => ({ label: item, value: item }))}
                touchableWrapperProps={{ testID: 'picker-select' }}
                style={{
                    inputIOS: {
                        fontSize: 16,
                        paddingVertical: 12,
                        paddingHorizontal: 10,
                        borderWidth: 1,
                        borderColor: 'gray',
                        borderRadius: 4,
                        color: 'black',
                        paddingRight: 30, // to ensure the text is never behind the icon
                        backgroundColor: '#6366F1',
                        borderRadius: 10,
                        height: 50,
                    },
                    inputAndroid: {
                        backgroundColor: '#6366F1',
                        color: 'white',
                    },
                }}
                placeholder={{ label: `--- ${title} ---`, value: '' }}
                value={value}
            />
        </Container>
    );
};

export default Select;
