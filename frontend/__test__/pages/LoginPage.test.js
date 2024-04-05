import { screen } from 'expo-router/testing-library';
import LoginPage from '../../app/pages/LoginPage';
import { render } from '../testSetup/helper';

beforeEach(() => {
    render(<LoginPage />);
});

test('renders all components on load', () => {
    expect(screen.getByTestId('input-field')).toBeTruthy();
    expect(screen.getByText('Login')).toBeTruthy();
    expect(screen.getByText(/Start Driving/)).toBeTruthy();
});
