import React from 'react';
import { StyleSheet, Text, View, Animated, Easing } from 'react-native';
import { Entypo } from 'react-native-vector-icons';

const Arrows = () => {
    const animatedValue = new Animated.Value(0);
    const animatedValue2 = new Animated.Value(0);
    const animatedValue3 = new Animated.Value(0);

    Animated.loop(
        Animated.parallel([
            Animated.timing(animatedValue, {
                toValue: 1,
                duration: 2000,
                useNativeDriver: true,
            }),
            Animated.timing(animatedValue2, {
                toValue: 1,
                duration: 2000,
                useNativeDriver: true,
                delay: 200,
            }),
            Animated.timing(animatedValue3, {
                toValue: 1,
                duration: 2000,
                useNativeDriver: true,
                delay: 400,
            }),
        ])
    ).start();

    const animatedStyle = {
        opacity: animatedValue.interpolate({
            inputRange: [0, 0.5],
            outputRange: [1, 0], // Reverse the output range
        }),
        transform: [
            {
                translateY: animatedValue.interpolate({
                    inputRange: [0, 1],
                    outputRange: [0, -50],
                }),
            },
        ],
    };

    const animatedStyle2 = {
        opacity: animatedValue2.interpolate({
            inputRange: [0, 0.7],
            outputRange: [1, 0], // Reverse the output range
        }),
        transform: [
            {
                translateY: animatedValue2.interpolate({
                    inputRange: [0, 1],
                    outputRange: [0, -85],
                }),
            },
        ],
    };

    const animatedStyle3 = {
        opacity: animatedValue3.interpolate({
            inputRange: [0, 0.9],
            outputRange: [1, 0], // Reverse the output range
        }),
        transform: [
            {
                translateY: animatedValue3.interpolate({
                    inputRange: [0, 1],
                    outputRange: [0, -120],
                }),
            },
        ],
    };
    return (
        <View style={styles.arrow}>
            <Animated.View style={[animatedStyle, { marginBottom: -70 }]}>
                <Entypo
                    name="chevron-right"
                    size={124}
                    color="black"
                    style={{ transform: [{ rotate: '-90deg' }] }}
                />
            </Animated.View>
            <Animated.View style={[animatedStyle2, { marginBottom: -70 }]}>
                <Entypo
                    name="chevron-right"
                    size={124}
                    color="black"
                    style={{ transform: [{ rotate: '-90deg' }] }}
                />
            </Animated.View>
            <Animated.View style={[animatedStyle3]}>
                <Entypo
                    name="chevron-right"
                    size={124}
                    color="black"
                    style={{ transform: [{ rotate: '-90deg' }] }}
                />
            </Animated.View>
        </View>
    );
};

const styles = StyleSheet.create({
    arrow: {
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        justifyContent: 'center',
        alignItems: 'center',
    },
});

export default Arrows;
