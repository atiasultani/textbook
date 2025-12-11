import React, { useEffect } from 'react';

const TextSelection = ({ onTextSelected }) => {
  useEffect(() => {
    const handleSelection = () => {
      const selectedText = window.getSelection().toString().trim();
      if (selectedText) {
        onTextSelected(selectedText);
      }
    };

    // Add event listeners for text selection
    document.addEventListener('mouseup', handleSelection);

    // Cleanup function to remove event listeners
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, [onTextSelected]);

  return null; // This component doesn't render anything itself
};

export default TextSelection;