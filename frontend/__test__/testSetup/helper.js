import { renderRouter } from 'expo-router/testing-library';

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
