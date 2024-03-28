import React, { useState } from 'react';
import RNPickerSelect from 'react-native-picker-select';
import { Container } from '~/tamagui.config';
import { Stack } from 'expo-router';

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
                        backgroundColor: '#6366F1',
                        color: 'white',
                    },
                    inputAndroid: {
                        backgroundColor: '#6366F1',
                        color: 'white',
                    },
                }}
                placeholder={{ label: `--- ${title} ---`, value: null }}
                value={value}
            />
        </Container>
    );
};

export default Select;
