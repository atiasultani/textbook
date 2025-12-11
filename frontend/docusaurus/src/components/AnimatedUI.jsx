import React from 'react';
import './AnimatedUI.css';

// A higher-order component that adds animation capabilities to any element
const withAnimation = (WrappedComponent, animationType = 'fade') => {
  return function AnimatedComponent(props) {
    const [isVisible, setIsVisible] = React.useState(false);

    React.useEffect(() => {
      // Simple intersection observer to trigger animations when component comes into view
      const observer = new IntersectionObserver(
        ([entry]) => {
          if (entry.isIntersecting) {
            setIsVisible(true);
            observer.unobserve(entry.target);
          }
        },
        { threshold: 0.1 }
      );

      const element = document.getElementById(`animated-element-${props.id || 'default'}`);
      if (element) {
        observer.observe(element);
      }

      return () => {
        if (element) {
          observer.unobserve(element);
        }
      };
    }, []);

    const animationClass = isVisible ? `animate-${animationType}` : `animate-${animationType}-hidden`;

    return (
      <div
        id={`animated-element-${props.id || 'default'}`}
        className={`animated-wrapper ${animationClass}`}
      >
        <WrappedComponent {...props} />
      </div>
    );
  };
};

// Basic animated elements
const AnimatedDiv = ({ children, animationType = 'fade', className = '', ...props }) => {
  const [isVisible, setIsVisible] = React.useState(false);

  React.useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.unobserve(entry.target);
        }
      },
      { threshold: 0.1 }
    );

    const element = document.getElementById(`animated-div-${props.id || 'default'}`);
    if (element) {
      observer.observe(element);
    }

    return () => {
      if (element) {
        observer.unobserve(element);
      }
    };
  }, []);

  const animationClass = isVisible ? `animate-${animationType}` : `animate-${animationType}-hidden`;

  return (
    <div
      id={`animated-div-${props.id || 'default'}`}
      className={`animated-div ${animationClass} ${className}`}
      style={{
        opacity: isVisible ? 1 : 0,
        transform: isVisible ? 'translateY(0)' : 'translateY(20px)',
        transition: 'opacity 0.5s ease, transform 0.5s ease'
      }}
    >
      {children}
    </div>
  );
};

const AnimatedButton = ({ children, animationType = 'bounce', onClick, ...props }) => {
  const [isHovered, setIsHovered] = React.useState(false);

  return (
    <button
      className={`animated-button ${isHovered ? 'animate-bounce' : ''}`}
      style={{
        transform: isHovered ? 'scale(1.05)' : 'scale(1)',
        transition: 'transform 0.2s ease, box-shadow 0.2s ease',
        cursor: 'pointer',
        padding: '10px 20px',
        border: 'none',
        borderRadius: '5px',
        backgroundColor: '#007cba',
        color: 'white',
        fontSize: '16px'
      }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onClick={onClick}
      {...props}
    >
      {children}
    </button>
  );
};

// Export the components
export { withAnimation, AnimatedDiv, AnimatedButton };

// Default export for a simple animated wrapper
const AnimatedUI = ({ children, animationType = 'fade', delay = 0 }) => {
  const [isVisible, setIsVisible] = React.useState(false);

  React.useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(true);
    }, delay);

    return () => clearTimeout(timer);
  }, [delay]);

  return (
    <div
      style={{
        opacity: isVisible ? 1 : 0,
        transform: isVisible ? 'translateY(0)' : 'translateY(20px)',
        transition: `opacity 0.6s ease, transform 0.6s ease`,
        transitionDelay: `${delay}ms`
      }}
    >
      {children}
    </div>
  );
};

export default AnimatedUI;