import React, { useEffect } from 'react';
import { StatusBar, Platform } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { Provider } from 'react-redux';
import SplashScreen from 'react-native-splash-screen';

import { store } from './src/store/store';
import AppNavigator from './src/navigation/AppNavigator';
import { APP_CONFIG } from './src/constants/config';

const App = () => {
  useEffect(() => {
    // 隐藏启动屏
    if (Platform.OS === 'android') {
      SplashScreen.hide();
    }
  }, []);

  return (
    <Provider store={store}>
      <NavigationContainer>
        <StatusBar
          barStyle="dark-content"
          backgroundColor={APP_CONFIG.THEME.PRIMARY_COLOR}
          translucent={false}
        />
        <AppNavigator />
      </NavigationContainer>
    </Provider>
  );
};

export default App;
