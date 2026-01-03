import React from 'react'

interface CardProps {
  children: React.ReactNode
  className?: string
  title?: string
  subtitle?: string
  hoverable?: boolean
}

export default function Card({
  children,
  className = '',
  title,
  subtitle,
  hoverable = false,
}: CardProps) {
  return (
    <div
      className={`bg-white rounded-lg shadow-md p-6 border border-gray-200 ${
        hoverable ? 'hover:shadow-lg transition-shadow cursor-pointer' : ''
      } ${className}`}
    >
      {title && (
        <div className="mb-4">
          <h3 className="text-lg font-bold text-gray-900">{title}</h3>
          {subtitle && <p className="text-sm text-gray-600 mt-1">{subtitle}</p>}
        </div>
      )}
      {children}
    </div>
  )
}
