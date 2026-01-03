// Format number as currency
export const formatCurrency = (value: number, currency: string = 'USD'): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(value)
}

// Format number with commas
export const formatNumber = (value: number): string => {
  return new Intl.NumberFormat('en-US').format(value)
}

// Format date
export const formatDate = (date: Date | string, format: string = 'short'): string => {
  const d = typeof date === 'string' ? new Date(date) : date
  
  const options: Intl.DateTimeFormatOptions = {
    short: { year: 'numeric', month: 'short', day: 'numeric' },
    long: { year: 'numeric', month: 'long', day: 'numeric' },
    full: { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' },
  }[format] || { year: 'numeric', month: '2-digit', day: '2-digit' }
  
  return new Intl.DateTimeFormat('en-US', options).format(d)
}

// Format time ago
export const formatTimeAgo = (date: Date | string): string => {
  const d = typeof date === 'string' ? new Date(date) : date
  const now = new Date()
  const seconds = Math.floor((now.getTime() - d.getTime()) / 1000)
  
  const intervals: [string, number][] = [
    ['year', 31536000],
    ['month', 2592000],
    ['week', 604800],
    ['day', 86400],
    ['hour', 3600],
    ['minute', 60],
  ]
  
  for (const [name, sec] of intervals) {
    const interval = Math.floor(seconds / sec)
    if (interval >= 1) return `${interval} ${name}${interval > 1 ? 's' : ''} ago`
  }
  
  return 'just now'
}

// Format email
export const formatEmail = (email: string): string => {
  return email.toLowerCase().trim()
}

// Format percentage
export const formatPercentage = (value: number, decimals: number = 0): string => {
  return `${(value * 100).toFixed(decimals)}%`
}

// Truncate text
export const truncateText = (text: string, length: number = 100): string => {
  if (text.length <= length) return text
  return `${text.substring(0, length)}...`
}
