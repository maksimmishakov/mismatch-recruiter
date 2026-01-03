import { lazy } from 'react';
// Lazy load component with fallback
export const createLazyComponent = (importFunc, fallback = />) => {
    const Component = lazy(importFunc);
    return (props) => fallback = { fallback } >
        { ...props } /  >
        /Suspense>;
};
// Image lazy loading helper
export const lazyLoadImage = (src, alt = '') => {
    return src;
};
// Script lazy loading
export const lazyLoadScript = (src) => {
    return new Promise((resolve, reject) => {
        if (document.querySelector(`script[src="${src}"]`)) {
            resolve();
            return;
        }
        const script = document.createElement('script');
        script.src = src;
        script.async = true;
        script.onload = () => resolve();
        script.onerror = () => reject(new Error(`Failed to load script: ${src}`));
        document.body.appendChild(script);
    });
};
