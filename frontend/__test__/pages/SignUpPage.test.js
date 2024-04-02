import { screen } from 'expo-router/testing-library';
import SignUpPage from '../../app/pages/SignUpPage';
import { render } from '../testSetup/helper';

beforeEach(() => {
    render(<SignUpPage />);
});

test('renders all components on load', () => {
    expect(screen.getAllByTestId('input-field')).toHaveLength(4);
    expect(screen.getByPlaceholderText('Username')).toBeTruthy();
    expect(screen.getByPlaceholderText('Email')).toBeTruthy();
    expect(screen.getByPlaceholderText('Password')).toBeTruthy();
    expect(screen.getByPlaceholderText('Confirm Password')).toBeTruthy();
    expect(screen.getByText('Sign Up')).toBeTruthy();
    expect(screen.getByText(/Already have an account?/)).toBeTruthy();
    expect(screen.getByText(/Back to Login/)).toBeTruthy();
});
