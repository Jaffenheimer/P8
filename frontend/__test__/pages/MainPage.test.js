import { screen } from 'expo-router/testing-library';
import MainPage from '../../app/pages/MainPage';
import { render } from '../testSetup/helper';

beforeEach(() => {
    render(<MainPage />);
});

test('renders all components on load', () => {
    expect(screen.getByText(/Log out/)).toBeTruthy();
    expect(screen.getByText(/Keep Driving/)).toBeTruthy();
});
