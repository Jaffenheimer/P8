import { renderRouter } from 'expo-router/testing-library';
import AsyncStorageMock from '@react-native-async-storage/async-storage/jest/async-storage-mock';

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

export { render };
