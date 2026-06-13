import React, {useEffect, useState} from 'react';
import {ActivityIndicator, View} from 'react-native';
import AppNavigator from './src/navigation/AppNavigator';
import {restoreSession} from './src/services/authService';

export default function App() {
  const [ready, setReady] = useState(false);

  useEffect(() => {
    restoreSession().finally(() => setReady(true));
  }, []);

  if (!ready) {
    return (
      <View style={{flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#000'}}>
        <ActivityIndicator color="#00ffff" />
      </View>
    );
  }

  return <AppNavigator />;
}