import {AlertDialog, Button, XStack, YStack} from "tamagui";
import React from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import {router} from "expo-router";
import {ButtonText, LogOutButton} from "~/tamagui.config";
import ip from "../constants.json";
const url = ip.ip;
const port = ip.port;


const LogOut = () => {
    async function logOut() {
        const BusId = await AsyncStorage.getItem('bus-id');
        try {
            const options = {
                method: 'Delete',
                headers: {
                    'Content-Type': 'application/json',
                    Accept: 'application/json',
                    'access-control-allow-origin': '*',
                },
                body: JSON.stringify({
                    busId: JSON.parse(BusId),
                }),
            };
            await fetch('http://' + url + ':' + port + '/admin/bus/delete', options).then((response) => {
                if (response.status === 400) {
                    console.log(response.status);
                } else {
                    router.replace('/pages/LoginPage');
                }
            });
        } catch (error) {
            console.error(error);
            return;
        }
    }
    return (
        <AlertDialog native>
            <AlertDialog.Trigger asChild>
                <LogOutButton>
                    <ButtonText>Log out</ButtonText>
                </LogOutButton>
            </AlertDialog.Trigger>
            <AlertDialog.Portal>
                <AlertDialog.Overlay
                    key="overlay"
                    animation="quick"
                    opacity={0.5}
                    enterStyle={{opacity: 0}}
                    exitStyle={{opacity: 0}}
                />
                <AlertDialog.Content
                    bordered
                    elevate
                    key="content"
                    animation={['quick', {
                        opacity: {
                            overshootClamping: true,
                        },
                    },]}
                    enterStyle={{x: 0, y: -20, opacity: 0, scale: 0.9}}
                    exitStyle={{x: 0, y: 10, opacity: 0, scale: 0.95}}
                    x={0}
                    scale={1}
                    opacity={1}
                    y={0}
                >
                    <YStack space>
                        <AlertDialog.Title>Are you sure?</AlertDialog.Title>
                        <XStack space="$3" justifyContent="flex-end">
                            <AlertDialog.Cancel asChild>
                                <Button>Cancel</Button>
                            </AlertDialog.Cancel>
                            <AlertDialog.Action asChild onPress={logOut}>
                                <Button>Log Out</Button>
                            </AlertDialog.Action>
                        </XStack>
                    </YStack>
                </AlertDialog.Content>
            </AlertDialog.Portal>
        </AlertDialog>);
}

export default LogOut;