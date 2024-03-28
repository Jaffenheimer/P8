import { render, renderRouter, screen } from 'expo-router/testing-library';
import Select from '../app/components/Select';

it('renders the correct title', async () => {
    const items = [
        { label: 'Chile', value: 'Chile' },
        { label: 'Peru', value: 'Peru' },
    ];
    const title = 'this is title';
    const onChange = jest.fn();
    

    const MockComponent = jest.fn(() => <Select items={items} title={title} onChange={onChange} />);

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
    

    expect(screen.getByDisplayValue('--- this is title ---')).toBeTruthy();
});


