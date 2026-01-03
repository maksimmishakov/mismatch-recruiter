import { useEffect, useState, useRef } from 'react';
// Debounce hook for search, filter inputs
export const useDebounce = (value, delay) => {
    const [debouncedValue, setDebouncedValue] = useState(value);
    useEffect(() => {
        const handler = setTimeout(() => {
            setDebouncedValue(value);
        }, delay);
        return () => clearTimeout(handler);
    }, [value, delay]);
    return debouncedValue;
};
// Throttle hook for scroll, resize events
export const useThrottle = (value, limit) => {
    const [throttledValue, setThrottledValue] = useState(value);
    const lastRan = useRef(Date.now());
    useEffect(() => {
        const handler = setTimeout(() => {
            if (Date.now() - lastRan.current >= limit) {
                setThrottledValue(value);
                lastRan.current = Date.now();
            }
        }, limit - (Date.now() - lastRan.current));
        return () => clearTimeout(handler);
    }, [value, limit]);
    return throttledValue;
};
// Lazy loading hook for images
export const useLazyLoad = (ref) => {
    useEffect(() => {
        if (!ref.current)
            return;
        const observer = new IntersectionObserver(([entry]) => {
            if (entry.isIntersecting) {
                const img = entry.target;
                const src = img.dataset.src;
                if (src) {
                    img.src = src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            }
        }, { rootMargin: '50px' });
        observer.observe(ref.current);
        return () => observer.disconnect();
    }, [ref]);
};
// Infinite scroll hook
export const useInfiniteScroll = (callback, hasMore) => {
    const observerTarget = useRef(null);
    useEffect(() => {
        if (!hasMore)
            return;
        const observer = new IntersectionObserver(([entry]) => {
            if (entry.isIntersecting && hasMore) {
                callback();
            }
        }, { threshold: 0.1 });
        if (observerTarget.current) {
            observer.observe(observerTarget.current);
        }
        return () => observer.disconnect();
    }, [callback, hasMore]);
    return observerTarget;
};
// Local storage hook with SSR support
export const useLocalStorage = (key, initialValue) => {
    const [storedValue, setStoredValue] = useState(() => {
        try {
            if (typeof window === 'undefined')
                return initialValue;
            const item = window.localStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        }
        catch (error) {
            console.error('Error reading localStorage:', error);
            return initialValue;
        }
    });
    const setValue = (value) => {
        try {
            const valueToStore = value instanceof Function ? value(storedValue) : value;
            setStoredValue(valueToStore);
            if (typeof window !== 'undefined') {
                window.localStorage.setItem(key, JSON.stringify(valueToStore));
            }
        }
        catch (error) {
            console.error('Error setting localStorage:', error);
        }
    };
    return [storedValue, setValue];
};
