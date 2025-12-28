# Data Model: Authentication and Access Control System

## Entity: User

**Description**: Represents a registered user with attributes including ID, name, email, password hash, account status, creation date, and last login time

**Fields**:
- `id` (string/UUID): Unique identifier for the user
- `name` (string): User's full name or display name
- `email` (string): User's email address (unique, used for login)
- `password_hash` (string): Securely hashed password using bcrypt
- `is_active` (boolean): Whether the account is active/enabled
- `is_verified` (boolean): Whether the email has been verified
- `created_at` (DateTime): When the account was created
- `updated_at` (DateTime): When the account was last updated
- `last_login_at` (DateTime | null): When the user last logged in
- `profile_picture_url` (string | null): URL to user's profile picture
- `oauth_provider` (string | null): OAuth provider if registered via social login

**Validation Rules**:
- `id` must be unique and follow UUID format
- `email` must be valid email format and unique across all users
- `password_hash` must be present and properly hashed
- `name` must be 2-100 characters
- `is_active` defaults to true
- `is_verified` defaults to false for email verification
- `email` cannot be changed without verification process

**State Transitions**:
- `is_verified: false` → `is_verified: true` after email verification
- `is_active: true` → `is_active: false` when account is deactivated
- `is_active: false` → `is_active: true` when account is reactivated

## Entity: AuthenticationSession

**Description**: Represents an active user session with JWT access token, refresh token, expiration times, and associated user ID

**Fields**:
- `id` (string/UUID): Unique identifier for the session
- `user_id` (string/UUID): Reference to the associated user
- `access_token` (string): JWT access token (stored securely on client)
- `refresh_token_hash` (string): Securely hashed refresh token (stored server-side)
- `access_token_expires_at` (DateTime): When the access token expires
- `refresh_token_expires_at` (DateTime): When the refresh token expires
- `created_at` (DateTime): When the session was created
- `last_used_at` (DateTime): When the session was last used
- `user_agent` (string): Browser/device information
- `ip_address` (string): IP address of the session origin
- `is_active` (boolean): Whether the session is still valid

**Validation Rules**:
- `user_id` must reference an existing active user
- `access_token` must be a valid JWT format
- `refresh_token_hash` must be properly hashed
- `access_token_expires_at` must be in the future
- `refresh_token_expires_at` must be after `access_token_expires_at`
- `is_active` defaults to true

**State Transitions**:
- `is_active: true` → `is_active: false` when session is invalidated/logout
- `is_active: false` → `is_active: true` if session is reactivated (rare)

## Entity: PasswordResetToken

**Description**: Represents a temporary token for password reset functionality with expiration time and associated user

**Fields**:
- `id` (string/UUID): Unique identifier for the reset token
- `user_id` (string/UUID): Reference to the associated user
- `token_hash` (string): Securely hashed reset token
- `expires_at` (DateTime): When the reset token expires
- `used_at` (DateTime | null): When the token was used (null if unused)
- `created_at` (DateTime): When the token was created
- `ip_address` (string): IP address that requested the reset
- `user_agent` (string): Browser/device that requested the reset

**Validation Rules**:
- `user_id` must reference an existing active user
- `token_hash` must be properly hashed and unique
- `expires_at` must be in the future (typically 1 hour from creation)
- `used_at` must be null initially
- Token cannot be used after `expires_at`

**State Transitions**:
- `used_at: null` → `used_at: [timestamp]` when token is used for password reset
- Token becomes invalid after use or expiration

## Entity: OAuthAccount

**Description**: Represents an OAuth connection for a user (Google, GitHub, etc.)

**Fields**:
- `id` (string/UUID): Unique identifier for the OAuth connection
- `user_id` (string/UUID): Reference to the associated user
- `provider` (string): OAuth provider (e.g., "google", "github")
- `provider_account_id` (string): Unique ID from the OAuth provider
- `email` (string): Email from the OAuth provider
- `name` (string): Name from the OAuth provider
- `access_token` (string): OAuth access token (if needed for API calls)
- `refresh_token` (string | null): OAuth refresh token (if applicable)
- `expires_at` (DateTime | null): When the access token expires
- `created_at` (DateTime): When the connection was created
- `updated_at` (DateTime): When the connection was last updated

**Validation Rules**:
- `user_id` must reference an existing user
- `provider` must be one of allowed providers (google, github, etc.)
- `provider_account_id` must be unique per provider
- `email` should match the user's email if linking to existing account

**State Transitions**:
- Connection can be added/removed from user account
- Tokens can be refreshed when they expire