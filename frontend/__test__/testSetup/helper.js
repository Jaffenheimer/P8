import {renderRouter} from 'expo-router/testing-library';

function render(component) {
    const MockComponent = jest.fn(() => component);
    renderRouter(
        {
            index: MockComponent,
            'directory/a': MockComponent,
            '(group)/b': MockComponent,
        },
        {
            initialUrl: '/directory/a',
        }
    );
}

function asyncStorageMock() {
    jest.mock('@react-native-async-storage/async-storage', () =>
        require('@react-native-async-storage/async-storage/jest/async-storage-mock')
    );
}

export {asyncStorageMock ,render};
