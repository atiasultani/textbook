# Quickstart: Professional Chatbot UI-UX

## Overview
This guide will help you set up and run the professional chatbot UI/UX component in the existing Docusaurus textbook project.

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Access to backend API (FastAPI) with chat capabilities
- API keys for OpenAI or compatible service (if required)

## Installation

1. **Navigate to the Docusaurus directory**:
   ```bash
   cd frontend/docusaurus
   ```

2. **Install dependencies** (if any new ones are needed):
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Environment configuration**:
   Create or update `.env` file with API endpoint:
   ```env
   REACT_APP_CHAT_API_ENDPOINT=https://your-backend-api.com/chat
   REACT_APP_OPENAI_API_KEY=your_api_key_here  # if needed client-side
   ```

## Running the Development Server

1. **Start the Docusaurus development server**:
   ```bash
   npm run start
   # or
   yarn start
   ```

2. **Access the chat interface**:
   The chatbot component should be available on the relevant textbook pages or at `/chat` if a dedicated page exists.

## Key Components

The chatbot UI consists of these main React components:

- `Chatbot.jsx`: Main container component
- `ChatMessage.jsx`: Individual message display
- `ChatInput.jsx`: Message input field with typing indicators
- `ChatHistory.jsx`: Scrollable message history container

## Integration with Existing Textbook

The chatbot component can be embedded in textbook pages by importing and using the `Chatbot` component:

```jsx
import Chatbot from '../components/Chatbot';

// In your page component
<Chatbot />
```

## Configuration

The chatbot can be configured with props:

```jsx
<Chatbot
  apiEndpoint={process.env.REACT_APP_CHAT_API_ENDPOINT}
  conversationContext="textbook-chapter-1"
  showOnLoad={true}
/>
```

## Building for Production

1. **Build the Docusaurus site**:
   ```bash
   npm run build
   # or
   yarn build
   ```

2. **Serve the built site**:
   ```bash
   npm run serve
   # or
   yarn serve
   ```

## Troubleshooting

- **API Connection Issues**: Verify that the API endpoint is correctly configured and accessible
- **CORS Errors**: Ensure the backend allows requests from your frontend origin
- **Typing Indicators Not Showing**: Check WebSocket connections or polling intervals
- **Message Formatting Issues**: Verify that the backend returns properly formatted responses