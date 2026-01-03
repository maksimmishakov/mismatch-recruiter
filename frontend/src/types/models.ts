// User types
export interface User {
  id: string
  email: string
  firstName: string
  lastName: string
  role: 'admin' | 'recruiter' | 'user'
  avatar?: string
  createdAt: string
  updatedAt: string
}

// Candidate types
export interface Candidate {
  id: string
  firstName: string
  lastName: string
  email: string
  phone?: string
  skills: string[]
  experience: number
  location?: string
  resume?: string
  status: 'active' | 'inactive' | 'hired'
  createdAt: string
  updatedAt: string
}

// Job types
export interface Job {
  id: string
  title: string
  description: string
  skills: string[]
  salary?: {
    min: number
    max: number
    currency: string
  }
  location?: string
  status: 'draft' | 'published' | 'closed'
  createdAt: string
  updatedAt: string
}

// Match types
export interface Match {
  id: string
  candidateId: string
  jobId: string
  score: number // 0-100
  status: 'pending' | 'accepted' | 'rejected'
  createdAt: string
  updatedAt: string
}

// API Response types
export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
  pages: number
}
