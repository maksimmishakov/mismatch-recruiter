import { useEffect, useRef } from 'react';
export const LazyImage = ({ src, placeholder = 'data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22%3E%3C/svg%3E', ...props }) => {
    const imgRef = useRef(null);
    useEffect(() => {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting && imgRef.current) {
                    imgRef.current.src = src;
                    observer.unobserve(entry.target);
                }
            });
        });
        if (imgRef.current)
            observer.observe(imgRef.current);
        return () => observer.disconnect();
    }, [src]);
    return <img ref={imgRef} src={placeholder} {...props}/>;
};
export default LazyImage;
