import { screen } from 'expo-router/testing-library';
import LoginPage from '../../app/pages/LoginPage';
import { render } from '../testSetup/helper';

beforeEach(() => {
    render(<LoginPage />);
});

test('renders all components on load', () => {
    expect(screen.getAllByTestId('input-field')).toHaveLength(2);
    expect(screen.getByPlaceholderText('Username')).toBeTruthy();
    expect(screen.getByPlaceholderText('Password')).toBeTruthy();
    expect(screen.getByText('Login')).toBeTruthy();
    expect(screen.getByText(/Don't have an account?/)).toBeTruthy();
    expect(screen.getByText(/Sign Up/)).toBeTruthy();
});
