import { createAnimations } from '@tamagui/animations-react-native';
import { createInterFont } from '@tamagui/font-inter';
import { createMedia } from '@tamagui/react-native-media-driver';
import { shorthands } from '@tamagui/shorthands';
import { size, themes, tokens } from '@tamagui/themes';
import { TextInput } from 'react-native';
import { createTamagui, styled, SizableText, H1, YStack } from 'tamagui';

const animations = createAnimations({
    bouncy: {
        damping: 10,
        mass: 0.9,
        stiffness: 100,
        type: 'spring',
    },
    lazy: {
        damping: 20,
        type: 'spring',
        stiffness: 60,
    },
    quick: {
        damping: 20,
        mass: 1.2,
        stiffness: 250,
        type: 'spring',
    },
});

const headingFont = createInterFont();

const bodyFont = createInterFont();

export const Container = styled(YStack, {
    flex: 1,
    padding: 24,
    backgroundColor: '$backgroundColor',
});

export const Main = styled(YStack, {
    flex: 1,
    justifyContent: 'space-between',
    alignContent: 'center',
    maxWidth: 960,
});

export const Input = styled(TextInput, {
    backgroundColor: '#F8F8F8',
    borderRadius: 8,
    color: '$color',
    fontSize: 16,
    padding: 16,
    width: '100%',
    marginTop: 10,
});

export const UserInformationForm = styled(YStack, {
    marginTop: 20,
    marginBottom: 20,
});

export const InputLabel = styled(SizableText, {
    color: '$color',
    fontSize: 14,
    marginTop: 14,
    textAlign: 'left',
});

export const Title = styled(H1, {
    size: '$12',
    fontSize: 44,
    fontStyle: 'normal',
    fontWeight: '700',
    lineHeight: 53,
    textAlign: 'center',
    marginTop: 30,
});

export const MainPageTitle = styled(Title, {
    marginTop: '100%',
    position: 'absolute',
    marginLeft: '10%',
});


export const Button = styled(YStack, {
    alignItems: 'center',
    backgroundColor: '#6366F1',
    borderRadius: 28,
    hoverStyle: {
        backgroundColor: '#5a5fcf',
    },
    maxWidth: 500,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: {
        height: 2,
        width: 0,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    marginTop: 16,
});

export const ButtonText = styled(SizableText, {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
    textAlign: 'center',
});

export const LogOutButton = styled(Button, {
    width: '30%',
    marginTop: '10%',
    marginLeft: '70%',
});

export const LogOutButtonContainer = styled(YStack, {
    width: '100%',
    height: '50%',
});

const config = createTamagui({
    themes: {
        light: {
            color: 'black',
            background: 'white',
            backgroundColor: '',
        },
    },
    backgroundColor: 'white',
    defaultFont: 'body',
    animations,
    shouldAddPrefersColorThemes: true,
    themeClassNameOnRoot: true,
    shorthands,
    fonts: {
        body: bodyFont,
        heading: headingFont,
    },
    tokens,
    media: createMedia({
        xs: { maxWidth: 660 },
        sm: { maxWidth: 800 },
        md: { maxWidth: 1020 },
        lg: { maxWidth: 1280 },
        xl: { maxWidth: 1420 },
        xxl: { maxWidth: 1600 },
        gtXs: { minWidth: 660 + 1 },
        gtSm: { minWidth: 800 + 1 },
        gtMd: { minWidth: 1020 + 1 },
        gtLg: { minWidth: 1280 + 1 },
        short: { maxHeight: 820 },
        tall: { minHeight: 820 },
        hoverNone: { hover: 'none' },
        pointerCoarse: { pointer: 'coarse' },
    }),
});

type AppConfig = typeof config;

// Enable auto-completion of props shorthand (ex: jc="center") for Tamagui templates.
// Docs: https://tamagui.dev/docs/core/configuration

declare module 'tamagui' {
    interface TamaguiCustomConfig extends AppConfig {}
}

export default config;
