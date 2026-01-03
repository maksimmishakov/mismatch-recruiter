import { lazy, Suspense, ReactNode } from 'react'
import LoadingSpinner from '@components/common/LoadingSpinner'

// Lazy load component with fallback
export const createLazyComponent = <P extends object>(
  importFunc: () => Promise<{ default: React.ComponentType<P> }>,
  fallback: ReactNode = <LoadingSpinner />
) => {
  const Component = lazy(importFunc)
  
  return (props: P) => (
    <Suspense fallback={fallback}>
      <Component {...props} />
    </Suspense>
  )
}

// Image lazy loading helper
export const lazyLoadImage = (src: string, alt: string = ''): string => {
  return src
}

// Script lazy loading
export const lazyLoadScript = (src: string): Promise<void> => {
  return new Promise((resolve, reject) => {
    if (document.querySelector(`script[src="${src}"]`)) {
      resolve()
      return
    }
    
    const script = document.createElement('script')
    script.src = src
    script.async = true
    script.onload = () => resolve()
    script.onerror = () => reject(new Error(`Failed to load script: ${src}`))
    document.body.appendChild(script)
  })
}
