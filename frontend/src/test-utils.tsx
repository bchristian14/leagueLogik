import React, { type ReactElement } from 'react'
import { render, type RenderOptions } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter } from 'react-router-dom'
import { vi } from 'vitest'
import type { User, AuthContextType } from './types/auth'
import type { AxiosError, InternalAxiosRequestConfig } from 'axios'

// Create a test query client with optimized settings for testing
const createTestQueryClient = () => new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
      staleTime: Infinity,
      gcTime: Infinity,
    },
    mutations: {
      retry: false,
    },
  },
})

// Custom render function that includes providers
interface CustomRenderOptions extends Omit<RenderOptions, 'wrapper'> {
  queryClient?: QueryClient
  withRouter?: boolean
}

export const renderWithProviders = (
  ui: ReactElement,
  {
    queryClient = createTestQueryClient(),
    withRouter = true,
    ...renderOptions
  }: CustomRenderOptions = {}
) => {
  function Wrapper({ children }: { children: React.ReactNode }) {
    const content = (
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    )

    if (withRouter) {
      return (
        <BrowserRouter>
          {content}
        </BrowserRouter>
      )
    }

    return content
  }

  return {
    ...render(ui, { wrapper: Wrapper, ...renderOptions }),
    queryClient,
  }
}

// Mock utilities for common testing scenarios

// Mock the useAuth hook for testing
export const mockAuthHook = (overrides: Partial<AuthContextType> = {}) => {
  const defaultMock = {
    user: null,
    isAuthenticated: false,
    isLoading: false,
    error: null,
    login: vi.fn(),
    logout: vi.fn(),
    clearError: vi.fn(),
    ...overrides
  }

  vi.doMock('../hooks/useAuth', () => ({
    useAuth: vi.fn(() => defaultMock),
    default: vi.fn(() => defaultMock),
  }))

  return defaultMock
}

/**
 * Mock the React Router navigation
 */
export const mockNavigate = vi.fn()
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom')
  return {
    ...actual,
    useNavigate: () => mockNavigate,
  }
})

/**
 * Mock API client for testing
 */
export const mockApiClient = {
  get: vi.fn(),
  post: vi.fn(),
  put: vi.fn(),
  delete: vi.fn(),
  patch: vi.fn(),
}

vi.mock('../lib/api', () => ({
  default: mockApiClient,
  mapApiError: vi.fn((error) => error.message || 'An error occurred'),
}))

/**
 * Mock token storage
 */
export const mockTokenStorage = {
  set: vi.fn(),
  get: vi.fn(),
  remove: vi.fn(),
  getAccessToken: vi.fn(() => null),
  getRefreshToken: vi.fn(() => null),
  isTokenExpired: vi.fn(() => true),
}

vi.mock('../lib/auth', () => ({
  tokenStorage: mockTokenStorage,
}))

// Helper to create mock user data
export const createMockUser = (overrides: Partial<User> = {}): User => ({
  member_id: 'TEST001',
  email: 'test@example.com',
  first_name: 'Test',
  last_name: 'User',
  phone_number: '555-0123',
  date_of_birth: '1990-01-01',
  member_status: 'active',
  member_type: 'full',
  admin_roles: '',
  GHIN_id: 'GHIN123',
  member_balance: 0.00,
  signup_date: '2024-01-01',
  AGA_membership_expiry: '2024-12-31',
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
  is_admin: false,
  ...overrides
})

// Helper to create mock API responses
interface MockApiResponse<T = unknown> {
  data: T
  status: number
  statusText: string
  headers: Record<string, string>
  config: Record<string, unknown>
}

export const createMockApiResponse = <T,>(data: T, status = 200): MockApiResponse<T> => ({
  data,
  status,
  statusText: 'OK',
  headers: {},
  config: {},
})

// Helper to create mock API errors
export const createMockApiError = (message = 'API Error', status = 400): AxiosError => {
  const error = new Error(message) as AxiosError
  error.response = {
    data: { message },
    status,
    statusText: status === 400 ? 'Bad Request' : 'Error',
    headers: {},
    config: {} as InternalAxiosRequestConfig,
  }
  error.isAxiosError = true
  error.code = 'ERR_BAD_REQUEST'
  return error
}

// Wait for React Query to finish loading
export const waitForQueryToFinish = async (queryClient: QueryClient): Promise<void> => {
  await queryClient.refetchQueries()
}

// Helper to assert that an element is visible and accessible
export const expectElementToBeVisible = (element: HTMLElement): void => {
  expect(element).toBeInTheDocument()
  expect(element).toBeVisible()
}

// Helper to clear all mocks
export const clearAllMocks = (): void => {
  vi.clearAllMocks()
  mockNavigate.mockClear()
  Object.values(mockApiClient).forEach(mock => mock.mockClear())
  Object.values(mockTokenStorage).forEach(mock => mock.mockClear())
}

// Re-export specific testing utilities
export {
  screen,
  waitFor,
  waitForElementToBeRemoved,
  within,
  getByRole,
  getByText,
  getByLabelText,
  getByPlaceholderText,
  getByTestId,
  getByDisplayValue,
  queryByRole,
  queryByText,
  queryByLabelText,
  queryByPlaceholderText,
  queryByTestId,
  queryByDisplayValue,
  findByRole,
  findByText,
  findByLabelText,
  findByPlaceholderText,
  findByTestId,
  findByDisplayValue,
  fireEvent,
  act,
  cleanup,
} from '@testing-library/react'
export { default as userEvent } from '@testing-library/user-event'