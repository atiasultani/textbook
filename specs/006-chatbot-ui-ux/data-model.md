# Data Model: Professional Chatbot UI-UX

## Entity: ChatMessage

**Description**: Represents a single message in the conversation

**Fields**:
- `id` (string): Unique identifier for the message
- `content` (string): The actual message text/content
- `sender` (enum: "user" | "bot"): Indicates whether the message was sent by user or bot
- `timestamp` (Date): When the message was sent/received
- `status` (enum: "sent" | "delivered" | "error"): Current status of the message
- `type` (enum: "text" | "code" | "list" | "error"): Type of content in the message
- `metadata` (object): Additional data for special message types (e.g., language for code blocks)

**Validation Rules**:
- `id` must be unique within the conversation
- `content` must not be empty
- `sender` must be either "user" or "bot"
- `timestamp` must be a valid date/time
- `status` must be one of the defined values

**State Transitions**:
- `sent` → `delivered` when message is confirmed received by backend
- `sent` → `error` when message fails to send
- `delivered` → `error` if backend reports error

## Entity: Conversation

**Description**: Represents a session of messages between user and bot

**Fields**:
- `id` (string): Unique identifier for the conversation
- `createdAt` (Date): When the conversation was started
- `lastActiveAt` (Date): When the last message was sent/received
- `messages` (array of ChatMessage): List of messages in the conversation
- `context` (object): Additional context for the conversation (e.g., topic, user preferences)
- `isActive` (boolean): Whether the conversation is currently active

**Validation Rules**:
- `id` must be unique across all conversations
- `createdAt` must be a valid date/time
- `messages` must be an array of ChatMessage objects
- `isActive` must be a boolean value

**State Transitions**:
- `isActive: true` → `isActive: false` after 30 minutes of inactivity
- New conversation starts with `isActive: true`

## Entity: ChatSession

**Description**: Represents the user's current chat session state

**Fields**:
- `conversationId` (string): ID of the current conversation
- `isTyping` (boolean): Whether the bot is currently typing
- `inputText` (string): Current text in the input field
- `error` (string | null): Any error message to display
- `connectionStatus` (enum: "connected" | "connecting" | "disconnected"): Status of connection to backend

**Validation Rules**:
- `conversationId` must reference an existing Conversation
- `connectionStatus` must be one of the defined values
- `inputText` length must be within reasonable limits

**State Transitions**:
- `connectionStatus` changes based on WebSocket/API connection status
- `isTyping` toggles when bot starts/stops processing