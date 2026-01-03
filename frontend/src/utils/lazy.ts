import React, { Suspense, lazy, ComponentType, ReactElement, ReactNode } from 'react';

// Default loading spinner component
const DefaultLoadingSpinner = (): ReactElement => {
  return React.createElement(
    'div',
    {
      style: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        fontSize: '18px',
        color: '#666'
      }
    },
    React.createElement('div', null, 'Loading...')
  );
};

// Type definition for lazy component factory function
type LazyComponentFactory<P extends object = {}> = () => Promise<{ default: ComponentType<P> }>;

// Create a lazy loaded component with fallback UI
export const createLazyComponent = <P extends object = {}>(
  importFunc: LazyComponentFactory<P>,
  fallback?: ReactNode
): ((props: P) => ReactElement) => {
  const LazyComponent = lazy(() => importFunc() as Promise<{ default: ComponentType<any> }>);

  const Component = (props: P): ReactElement => {
    const fallbackElement = fallback || React.createElement(DefaultLoadingSpinner);
    return React.createElement(
      Suspense,
      { fallback: fallbackElement },
      React.createElement(LazyComponent, props as any)
    );
  };

  return Component;
};

// Image lazy loading utility
export const lazyLoadImage = (src: string, alt: string = ''): string => {
  if (typeof document !== 'undefined') {
    const selector = `[data-src="${src}"]`;
    const element = document.querySelector(selector);
    if (element && element instanceof HTMLImageElement) {
      element.src = src;
      if (alt) {
        element.alt = alt;
      }
    }
  }
  return src;
};

// Script lazy loading utility
export const lazyLoadScript = (src: string): Promise<void> => {
  return new Promise((resolve, reject) => {
    // Check if script already loaded
    const selector = `script[src="${src}"]`;
    if (document.querySelector(selector)) {
      resolve();
      return;
    }

    // Create and append script tag
    const script = document.createElement('script');
    script.src = src;
    script.async = true;

    script.onload = () => {
      resolve();
    };

    script.onerror = () => {
      reject(new Error(`Failed to load script: ${src}`));
    };

    document.body.appendChild(script);
  });
};

export default createLazyComponent;
