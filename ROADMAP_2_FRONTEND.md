# ROADMAP 2: FRONTEND OPTIMIZATION

## Step 1: Setup React optimization
В VS Code: Создать `frontend/src/utils/PerformanceOptimizer.ts`:

```typescript
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
```

**Git коммит**: `git add frontend/src/utils/PerformanceOptimizer.ts && git commit -m "Add React performance optimization utilities"`

---

## Step 2: Implement code splitting
В VS Code: Обновить `frontend/src/App.tsx`:

```typescript
import { lazy, Suspense } from 'react';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const CandidateList = lazy(() => import('./pages/CandidateList'));
const JobMatching = lazy(() => import('./pages/JobMatching'));

export const AppRoutes = () => (
  <Suspense fallback={<LoadingSpinner />}>
    {/* Routes with lazy loading */}
  </Suspense>
);
```

**Git коммит**: `git add frontend/src/App.tsx && git commit -m "Implement code splitting with React lazy loading"`

---

## Step 3: Setup CSS optimization
В VS Code: Создать `frontend/src/styles/optimize.css`:

```css
/* Critical above-the-fold CSS */
@import url('optimize.critical.css');

/* Use will-change for animations */
.resume-card {
  will-change: transform, opacity;
  transform: translateZ(0);
}

/* Optimize images */
img {
  content-visibility: auto;
  contain: layout style paint;
}
```

**Git коммит**: `git add frontend/src/styles/optimize.css && git commit -m "Add CSS performance optimizations"`

---

## Step 4: Implement image lazy loading
В VS Code: Создать `frontend/src/components/LazyImage.tsx`:

```typescript
import { useEffect, useRef, ImgHTMLAttributes } from 'react';

interface LazyImageProps extends ImgHTMLAttributes<HTMLImageElement> {
  src: string;
  placeholder?: string;
}

export const LazyImage: React.FC<LazyImageProps> = ({
  src,
  placeholder = 'data:image/svg+xml,%3Csvg...',
  ...props
}) => {
  const imgRef = useRef<HTMLImageElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && imgRef.current) {
          imgRef.current.src = src;
          observer.unobserve(entry.target);
        }
      });
    });

    if (imgRef.current) observer.observe(imgRef.current);
    return () => observer.disconnect();
  }, [src]);

  return <img ref={imgRef} src={placeholder} {...props} />;
};
```

**Git коммит**: `git add frontend/src/components/LazyImage.tsx && git commit -m "Add lazy image loading component"`

---

## Step 5: Setup bundle analysis
В VS Code: Обновить `frontend/package.json`:

```json
{
  "scripts": {
    "analyze": "react-scripts build && webpack-bundle-analyzer build/static/js/*.js"
  }
}
```

**Git коммит**: `git add frontend/package.json && git commit -m "Add bundle analysis script"`

---

## Step 6: Implement service worker for caching
В VS Code: Создать `frontend/public/service-worker.js`:

```javascript
const CACHE_NAME = 'mismatch-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/static/css/main.css',
  '/static/js/main.js',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(urlsToCache);
    })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
```

**Git коммит**: `git add frontend/public/service-worker.js && git commit -m "Add service worker for offline caching"`

---

## Step 7: Create performance monitoring component
В VS Code: Создать `frontend/src/components/PerformanceMonitor.tsx`:

```typescript
export const PerformanceMonitor = () => {
  useEffect(() => {
    if ('PerformanceObserver' in window) {
      const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          console.log(`${entry.name}: ${entry.duration}ms`);
        }
      });
      observer.observe({ entryTypes: ['measure', 'navigation'] });
    }
  }, []);

  return null;
};
```

**Git коммит**: `git add frontend/src/components/PerformanceMonitor.tsx && git commit -m "Add performance monitoring component"`

---

## Step 8: Optimize API calls with caching
В VS Code: Создать `frontend/src/services/apiCache.ts`:

```typescript
interface CacheEntry<T> {
  data: T;
  timestamp: number;
}

class APICache {
  private cache = new Map<string, CacheEntry<any>>();
  private ttl = 5 * 60 * 1000; // 5 minutes

  get<T>(key: string): T | null {
    const entry = this.cache.get(key);
    if (!entry) return null;

    if (Date.now() - entry.timestamp > this.ttl) {
      this.cache.delete(key);
      return null;
    }

    return entry.data;
  }

  set<T>(key: string, data: T): void {
    this.cache.set(key, { data, timestamp: Date.now() });
  }
}

export default new APICache();
```

**Git коммит**: `git add frontend/src/services/apiCache.ts && git commit -m "Add API response caching layer"`

---

## SUMMARY
Все шаги оптимизируют:
- ✅ React компоненты (useMemo, useCallback)
- ✅ Code splitting с lazy loading
- ✅ CSS optimization
- ✅ Lazy image loading
- ✅ Bundle analysis
- ✅ Service worker кеширование
- ✅ Performance monitoring
- ✅ API caching

РЕЗУЛЬТАТ: FCP < 1s, TTI < 2s, LCP < 2.5s
