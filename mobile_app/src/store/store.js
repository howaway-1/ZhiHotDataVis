import { configureStore } from '@reduxjs/toolkit';
import authSlice from './slices/authSlice';
import articlesSlice from './slices/articlesSlice';
import analysisSlice from './slices/analysisSlice';

export const store = configureStore({
  reducer: {
    auth: authSlice,
    articles: articlesSlice,
    analysis: analysisSlice,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
