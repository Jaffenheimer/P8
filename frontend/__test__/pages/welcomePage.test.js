import { screen, fireEvent } from 'expo-router/testing-library';
import WelcomePage from '../../app/pages/WelcomePage';
import { render } from '../testSetup/helper';

beforeEach(() => {
    render(<WelcomePage />);
});

test('renders a single select component on load with correct title and a next button', () => {
    expect(screen.getAllByTestId('picker-select')).toHaveLength(1);
    expect(screen.getByDisplayValue('--- Select a country ---')).toBeTruthy();
    expect(screen.getByText('Next')).toBeTruthy();
});

test('When a country is selected, the city select is rendered', () => {
    const countryPicker = screen.getByDisplayValue('--- Select a country ---');
    fireEvent(countryPicker, 'onValueChange', 'Chile');
    const cityPicker = screen.getByDisplayValue('--- Select a city ---');

    expect(screen.getAllByTestId('picker-select')).toHaveLength(2);
    expect(cityPicker).toBeTruthy();
});

test('When Chile is selected, one can select Santiago as a city',() => {
    const countryPicker = screen.getByDisplayValue('--- Select a country ---');
    fireEvent(countryPicker, 'onValueChange', 'Chile');
    const cityPicker = screen.getByDisplayValue('--- Select a city ---');

    expect(() => fireEvent(cityPicker, 'onValueChange', 'Santiago')).not.toThrow();
});

test('When a country and then a city is selected, the route select is rendered', () => {
    const countryPicker = screen.getByDisplayValue('--- Select a country ---');
    fireEvent(countryPicker, 'onValueChange', 'Chile');
    const cityPicker = screen.getByDisplayValue('--- Select a city ---');
    fireEvent(cityPicker, 'onValueChange', 'Santiago');
    const routePicker = screen.getByDisplayValue('--- Select a route ---');

    expect(screen.getAllByTestId('picker-select')).toHaveLength(3);
    expect(routePicker).toBeTruthy();
});
