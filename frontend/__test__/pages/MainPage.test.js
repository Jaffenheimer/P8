import { screen } from 'expo-router/testing-library';
import MainPage from '../../app/pages/MainPage';
import { asyncStorageMock, render } from '../testSetup/helper';

asyncStorageMock();

beforeEach(() => {
    render(<MainPage />);
});

test('renders all components on load', () => {
    expect(screen.getByText(/Log out/)).toBeTruthy();
    expect(screen.getByText(/Default/)).toBeTruthy();
});
