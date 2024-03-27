import React, { useState } from 'react';
import { View } from 'react-native';
import RNPickerSelect from 'react-native-picker-select';
import { Container } from '~/tamagui.config';
import { Stack } from 'expo-router';
import { YStack } from 'tamagui';

const Select = ({ items, title, onChange }) => {
    const [value, setValue] = useState('');

    function onChangeFunction(itemValue) {
        setValue(itemValue);
        onChange(itemValue);
    }

    return (
        <Container>
            <Stack.Screen />
            <View>
                <RNPickerSelect
                    onValueChange={onChangeFunction}
                    items={items.map((item) => ({ label: item, value: item }))}
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
            </View>
        </Container>
    );
};

export default Select;
