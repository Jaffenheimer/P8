import React, {useEffect, useState} from 'react';
import {Animated, StyleSheet, Text, View} from 'react-native';
import {Entypo} from 'react-native-vector-icons';
import Pusher from 'pusher-js';
import AsyncStorage from "@react-native-async-storage/async-storage";


let secrets = require('../secrets.json');

const pusher = new Pusher(secrets.Pusher.AppKey, {
    cluster: 'eu',
    forceTLS: true,
});

const Arrows = () => {
    const [currentAction, setAction] = useState(null);
    const [busId, setBusId] = useState(null);
    const animatedValue = new Animated.Value(0);
    const animatedValue2 = new Animated.Value(0);
    const animatedValue3 = new Animated.Value(0);
    useEffect(() => {
        async function fetchBusId() {
            const id = await AsyncStorage.getItem('bus-id');
            setBusId(id);
        }

        async function fetchAction() {
            setAction(await AsyncStorage.getItem('action'));
        }

        fetchAction();
        fetchBusId();
    }, []);


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

    let pusherFunction = async () => {
        await pusher.connect();
        const channel = await pusher.subscribe('action');
        channel.bind('test_event', function (data) {
            if (typeof data === 'string') {
                data = JSON.parse(data);
            }
            Object.keys(data.Actions).forEach((key) => {
                if (JSON.parse(busId) === key) {
                    const actionValue = Object.values(data.Actions)[0];
                    if (actionValue === 0) {
                        setAction('Default');
                    } else if (actionValue === 1) {
                        setAction('Maintain Speed');
                    } else if (actionValue === 2) {
                        setAction('Speed Up');
                    } else if (actionValue === 3) {
                        setAction('Slow Down');
                    }
                }
            });
        });
    };
    pusherFunction();
    return (
        <View style={styles.container}>
            <Text style={styles.text}>{currentAction === null ? "Default" : currentAction}</Text>
            {currentAction === 'Speed Up' ?
                <View style={styles.arrow}>
                    <Animated.View style={[animatedStyle, {marginBottom: -70}]}>
                        <Entypo
                            name="chevron-right"
                            size={124}
                            color="black"
                            style={{transform: [{rotate: '-90deg'}]}}
                        />
                    </Animated.View>
                    <Animated.View style={[animatedStyle2, {marginBottom: -70}]}>
                        <Entypo
                            name="chevron-right"
                            size={124}
                            color="black"
                            style={{transform: [{rotate: '-90deg'}]}}
                        />
                    </Animated.View>
                    <Animated.View style={[animatedStyle3]}>
                        <Entypo
                            name="chevron-right"
                            size={124}
                            color="black"
                            style={{transform: [{rotate: '-90deg'}]}}
                        />
                    </Animated.View>
                </View> : currentAction === 'Slow Down' ?
                    <View style={styles.arrowFlipped}>
                        <Animated.View style={[animatedStyle, {marginBottom: -70}]}>
                            <Entypo
                                name="chevron-right"
                                size={124}
                                color="black"
                                style={{transform: [{rotate: '-90deg'}]}}
                            />
                        </Animated.View>
                        <Animated.View style={[animatedStyle2, {marginBottom: -70}]}>
                            <Entypo
                                name="chevron-right"
                                size={124}
                                color="black"
                                style={{transform: [{rotate: '-90deg'}]}}
                            />
                        </Animated.View>
                        <Animated.View style={[animatedStyle3]}>
                            <Entypo
                                name="chevron-right"
                                size={124}
                                color="black"
                                style={{transform: [{rotate: '-90deg'}]}}
                            />
                        </Animated.View>
                    </View> : null}
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        position: 'absolute',
        marginTop: '75%',
    },
    arrow: {
        justifyContent: 'center',
        alignItems: 'center',
    },
    arrowFlipped: {
        justifyContent: 'center',
        alignItems: 'center',
        transform: [{rotate: '180deg'}],
    },
    text: {
        fontSize: 50,
        textAlign: 'center',
        color: 'black',
        marginRight: '15%',
    },
});

export default Arrows;
