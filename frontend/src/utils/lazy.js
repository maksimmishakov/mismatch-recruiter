import React, { Suspense, lazy } from 'react';
// Default loading spinner component
const DefaultLoadingSpinner = () => {
    return React.createElement('div', {
        style: {
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            height: '100vh',
            fontSize: '18px',
            color: '#666'
        }
    }, React.createElement('div', null, 'Loading...'));
};
// Create a lazy loaded component with fallback UI
export const createLazyComponent = (importFunc, fallback) => {
    const LazyComponent = lazy(() => importFunc());
    const Component = (props) => {
        const fallbackElement = fallback || React.createElement(DefaultLoadingSpinner);
        return React.createElement(Suspense, { fallback: fallbackElement }, React.createElement(LazyComponent, props));
    };
    return Component;
};
// Image lazy loading utility
export const lazyLoadImage = (src, alt = '') => {
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
export const lazyLoadScript = (src) => {
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
