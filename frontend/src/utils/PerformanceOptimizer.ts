import { useMemo, useCallback } from 'react';

export const useMemoCallback = <T, R>(deps: T[], fn: (deps: T[]) => R): R => {
  return useMemo(() => fn(deps), deps);
};

export const useDebounce = (callback: Function, delay: number) => {
  return useCallback((e: any) => {
    const timeout = setTimeout(() => callback(e), delay);
    return () => clearTimeout(timeout);
  }, [callback, delay]);
};

// Performance measurement utility
export const measurePerformance = (name: string, fn: () => void) => {
  const start = performance.now();
  fn();
  const duration = performance.now() - start;
  console.log(`[PERF] ${name}: ${duration.toFixed(2)}ms`);
};
