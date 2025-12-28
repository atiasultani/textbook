// Error handling utilities for API calls
class ErrorHandlingUtils {
  // Handle API errors and return user-friendly messages
  static handleApiError(error, context = '') {
    let userMessage = 'An unexpected error occurred. Please try again.';

    if (error instanceof TypeError && error.message.includes('fetch')) {
      userMessage = 'Network error: Please check your internet connection.';
    } else if (error.message.includes('401')) {
      userMessage = 'Authentication failed. Please check your credentials.';
    } else if (error.message.includes('404')) {
      userMessage = 'The requested resource was not found.';
    } else if (error.message.includes('500')) {
      userMessage = 'Server error. Please try again later.';
    } else if (error.message.includes('429')) {
      userMessage = 'Too many requests. Please wait before trying again.';
    } else if (error.message.includes('timeout')) {
      userMessage = 'Request timed out. Please check your connection and try again.';
    } else if (error.message.includes('NetworkError')) {
      userMessage = 'Network error: Please check your internet connection.';
    }

    const errorDetails = {
      message: userMessage,
      originalError: error.message || error,
      context: context,
      timestamp: new Date().toISOString()
    };

    console.error(`API Error (${context}):`, errorDetails);
    return errorDetails;
  }

  // Format error response from API
  static formatApiErrorResponse(response, error) {
    if (response && response.status) {
      return {
        status: response.status,
        message: this.getStatusMessage(response.status),
        details: error.message || 'Unknown error'
      };
    }

    return {
      status: 'NETWORK_ERROR',
      message: 'Network error occurred',
      details: error.message || 'Unknown network error'
    };
  }

  // Get user-friendly message based on HTTP status code
  static getStatusMessage(statusCode) {
    const statusMessages = {
      400: 'Bad request: The request was invalid.',
      401: 'Unauthorized: Please log in to continue.',
      403: 'Forbidden: You do not have permission to access this resource.',
      404: 'Not found: The requested resource does not exist.',
      429: 'Too many requests: Please wait before trying again.',
      500: 'Server error: Something went wrong on our end.',
      502: 'Bad gateway: The server is temporarily unavailable.',
      503: 'Service unavailable: The server is currently down for maintenance.'
    };

    return statusMessages[statusCode] || `Error: Request failed with status ${statusCode}.`;
  }

  // Create error message for specific error types
  static createErrorMessage(errorType, details = {}) {
    const errorMessages = {
      NETWORK_ERROR: 'Network error: Please check your internet connection and try again.',
      AUTH_ERROR: 'Authentication error: Please log in again.',
      TIMEOUT_ERROR: 'Request timed out: The server is taking too long to respond.',
      VALIDATION_ERROR: `Validation error: ${details.field || 'Input'} is invalid.`,
      RATE_LIMIT_ERROR: 'Rate limit exceeded: Please wait before sending another message.',
      SERVER_ERROR: 'Server error: Please try again later.',
      CONVERSATION_ERROR: 'Conversation error: Please start a new conversation.'
    };

    return errorMessages[errorType] || 'An error occurred. Please try again.';
  }

  // Log error for monitoring
  static logError(error, context = {}) {
    const errorLog = {
      error: error.message || error,
      stack: error.stack,
      context,
      timestamp: new Date().toISOString(),
      userAgent: navigator.userAgent,
      url: window.location.href
    };

    // In a real application, you might send this to an error monitoring service
    console.error('Error Log:', errorLog);
  }

  // Retry failed API calls with exponential backoff
  static async retryAsyncOperation(operation, maxRetries = 3, baseDelay = 1000) {
    let lastError;

    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        return await operation();
      } catch (error) {
        lastError = error;

        if (attempt === maxRetries) {
          break;
        }

        // Calculate delay with exponential backoff and jitter
        const delay = baseDelay * Math.pow(2, attempt - 1) + Math.random() * 1000;
        console.log(`Attempt ${attempt} failed, retrying in ${delay}ms...`);

        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }

    throw lastError;
  }
}

export default ErrorHandlingUtils;