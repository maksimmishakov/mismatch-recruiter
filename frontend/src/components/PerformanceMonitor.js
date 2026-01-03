import { useEffect } from 'react';
export const PerformanceMonitor = () => {
    useEffect(() => {
        if ('PerformanceObserver' in window) {
            try {
                const observer = new PerformanceObserver((list) => {
                    for (const entry of list.getEntries()) {
                        console.log(`[PERF] ${entry.name}: ${entry.duration}ms`);
                    }
                });
                observer.observe({ entryTypes: ['measure', 'navigation'] });
                return () => observer.disconnect();
            }
            catch (e) {
                console.warn('PerformanceObserver not supported');
            }
        }
    }, []);
    return null;
};
export default PerformanceMonitor;
