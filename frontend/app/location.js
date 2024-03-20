import { Stack, Link } from 'expo-router';
import React, { useState, useEffect } from 'react';

import { Container, Main, Subtitle, TopHalf, ButtomHalf, Title } from '../tamagui.config';

import * as Location from 'expo-location';

export default function LocationPage() {
  const [location, setLocation] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    (async () => {
      let { status } = await Location.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        setError('Adgang til placering er nægtet');
        return;
      }

      let currentLocation = await Location.getCurrentPositionAsync();
      setLocation(currentLocation);
    })();
  }, []);

  let text = 'Henter placering...';
  if (error) {
    text = error;
  } else if (location) {
    text = `Breddegrad: ${location.coords.latitude}, Længdegrad: ${location.coords.longitude}`;
  }

  return (
    <Container>
      <Main>
        <Stack.Screen options={{ title: 'Location' }} />
        <TopHalf>
          <Title>Location</Title>
          <Subtitle>Location of Phone</Subtitle>
        </TopHalf>
        <ButtomHalf>
          <Subtitle>{text}</Subtitle>
        </ButtomHalf>
      </Main>
    </Container>
  );
}
