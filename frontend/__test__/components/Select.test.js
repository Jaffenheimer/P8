import { renderRouter, screen, fireEvent } from 'expo-router/testing-library';
import Select from '../../app/components/Select';
import { render } from '../testSetup/helper';

describe('Select', () => {
    const items = [
        { label: 'Chile', value: 'Chile' },
        { label: 'Peru', value: 'Peru' },
    ];
    const title = 'this is title';
    const onChange = jest.fn();

    beforeEach(() => {
        render(<Select items={items} title={title} onChange={onChange} />)
    });
    
    it('renders the correct title', async () => {
        expect(screen.getByDisplayValue('--- this is title ---')).toBeTruthy();
    });

    test('onChange function is called when onchange is triggered', async () => {
        const picker = await screen.findByTestId('picker-select');
        fireEvent(picker, 'onValueChange', 'Chile');
        expect(onChange).toHaveBeenCalledWith('Chile');
    });
});
