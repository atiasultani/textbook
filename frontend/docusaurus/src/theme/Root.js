// src/theme/Root.jsx
import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from '../context/AuthContext';
import ChatbotFloating from '../components/ChatbotFloating';

export default function Root({ children }) {
  return (
    <AuthProvider>
      <BrowserRouter>
        {children}
        <ChatbotFloating />
      </BrowserRouter>
    </AuthProvider>
  );
}
