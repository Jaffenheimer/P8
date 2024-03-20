import { renderRouter, screen} from 'expo-router/testing-library';
import Layouttest from '../app/layouttest';


it('Does it render correct path', async () => {
  const MockComponent = jest.fn(() => <Layouttest />);

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

  expect(screen).toHavePathname('/directory/a');
});

it('Does it render the correct view', async () => {
  const MockComponent = jest.fn(() => <Layouttest />);

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

  expect(screen.getByText('This is the Top')).toBeTruthy();
  expect(screen.getByText('This is the Buttom')).toBeTruthy();
});

it('Does it render the id correct', async () => {
  const MockComponent = jest.fn(() => <Layouttest />);

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

  expect(screen.getByTestId("layout")).toBeTruthy();
});

