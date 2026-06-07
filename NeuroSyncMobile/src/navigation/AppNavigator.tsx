import React from 'react';
import {NavigationContainer} from '@react-navigation/native';
import {createNativeStackNavigator} from '@react-navigation/native-stack';
import SplashScreen from '../screens/SplashScreen';
import DevicesScreen from '../screens/DevicesScreen';
import DeviceDetailsScreen from '../screens/DeviceDetailsScreen';
import RemoteDashboardScreen from '../screens/RemoteDashboardScreen';

const Stack = createNativeStackNavigator();

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{headerShown: false}}>
        <Stack.Screen name="Splash" component={SplashScreen} />
        <Stack.Screen name="Devices" component={DevicesScreen} />
        <Stack.Screen name="DeviceDetails" component={DeviceDetailsScreen} />
        <Stack.Screen name="RemoteDashboard" component={RemoteDashboardScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}