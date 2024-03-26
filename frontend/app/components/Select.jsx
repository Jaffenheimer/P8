import React, { useState } from 'react';
import { StyleSheet, View } from 'react-native';
import { Picker } from '@react-native-picker/picker';
import { Container } from '~/tamagui.config';
import { Stack } from 'expo-router';
import { YStack } from 'tamagui';

const Select = ({ items, title }) => {
    const [Enable, setEnable] = useState('courses');

    return (
        <Container>
            <Stack.Screen options={{ headerShown: false }} />
            <YStack>
                <View style={styles.container}>
                    <Picker
                        selectedValue={Enable}
                        style={{ height: 50, width: 250 }}
                        mode={'dialog'}
                        onValueChange={(itemValue) => setEnable(itemValue)}
                    >
                        <Picker.Item value="" label={`--- ${title} ---`} enabled={false} />
                        {items.map((item) => (
                            <Picker.Item label={item} value={item} key={item} />
                        ))}
                    </Picker>
                </View>
            </YStack>
        </Container>
    );
};
export default Select;

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
    },
});
