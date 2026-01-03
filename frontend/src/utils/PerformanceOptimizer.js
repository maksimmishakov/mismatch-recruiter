import { useMemo, useCallback } from 'react';
export const useMemoCallback = (deps, fn) => {
    return useMemo(() => fn(deps), deps);
};
export const useDebounce = (callback, delay) => {
    return useCallback((e) => {
        const timeout = setTimeout(() => callback(e), delay);
        return () => clearTimeout(timeout);
    }, [callback, delay]);
};
// Performance measurement utility
export const measurePerformance = (name, fn) => {
    const start = performance.now();
    fn();
    const duration = performance.now() - start;
    console.log(`[PERF] ${name}: ${duration.toFixed(2)}ms`);
};
