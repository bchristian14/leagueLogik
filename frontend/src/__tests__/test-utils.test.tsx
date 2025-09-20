/**
 * Test suite for test utilities
 * Validates that our testing infrastructure is working correctly
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { QueryClient } from '@tanstack/react-query'
import {
  renderWithProviders,
  mockAuthHook,
  createMockUser,
  createMockApiResponse,
  createMockApiError,
  clearAllMocks,
  mockNavigate,
  mockApiClient,
  mockTokenStorage
} from '../test-utils'

// Simple test component
const TestComponent = () => {
  return (
    <div>
      <h1>Test Component</h1>
      <button>Test Button</button>
    </div>
  )
}

describe('Test Utils', () => {
  beforeEach(() => {
    clearAllMocks()
  })

  describe('renderWithProviders', () => {
    it('renders component with default providers', () => {
      const { getByText, queryClient } = renderWithProviders(<TestComponent />)

      expect(getByText('Test Component')).toBeInTheDocument()
      expect(queryClient).toBeInstanceOf(QueryClient)
    })

    it('renders component without router when withRouter is false', () => {
      const { getByText } = renderWithProviders(<TestComponent />, {
        withRouter: false
      })

      expect(getByText('Test Component')).toBeInTheDocument()
    })

    it('accepts custom query client', () => {
      const customQueryClient = new QueryClient()
      const { queryClient } = renderWithProviders(<TestComponent />, {
        queryClient: customQueryClient
      })

      expect(queryClient).toBe(customQueryClient)
    })
  })

  describe('mockAuthHook', () => {
    it('creates default auth mock', () => {
      const authMock = mockAuthHook()

      expect(authMock).toMatchObject({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
        login: expect.any(Function),
        logout: expect.any(Function),
        clearError: expect.any(Function),
      })
    })

    it('accepts custom overrides', () => {
      const authMock = mockAuthHook({
        isAuthenticated: true,
        user: createMockUser({ email: 'test@example.com' }),
        isLoading: true,
      })

      expect(authMock.isAuthenticated).toBe(true)
      expect(authMock.user).toMatchObject({ email: 'test@example.com' })
      expect(authMock.isLoading).toBe(true)
    })
  })

  describe('createMockUser', () => {
    it('creates user with default values', () => {
      const user = createMockUser()

      expect(user).toMatchObject({
        member_id: 'TEST001',
        email: 'test@example.com',
        first_name: 'Test',
        last_name: 'User',
        member_status: 'active',
        member_type: 'full',
        is_admin: false,
        member_balance: 0.00,
      })
    })

    it('accepts custom overrides', () => {
      const user = createMockUser({
        member_id: 'ADMIN99',
        email: 'admin@example.com',
        is_admin: true,
        first_name: 'Admin',
      })

      expect(user).toMatchObject({
        member_id: 'ADMIN99',
        email: 'admin@example.com',
        first_name: 'Admin',
        last_name: 'User', // default value
        is_admin: true,
        member_status: 'active', // default value
      })
    })
  })

  describe('createMockApiResponse', () => {
    it('creates response with default status', () => {
      const response = createMockApiResponse({ message: 'success' })

      expect(response).toMatchObject({
        data: { message: 'success' },
        status: 200,
        statusText: 'OK',
      })
    })

    it('accepts custom status', () => {
      const response = createMockApiResponse({ id: 1 }, 201)

      expect(response.status).toBe(201)
      expect(response.data).toEqual({ id: 1 })
    })
  })

  describe('createMockApiError', () => {
    it('creates error with default values', () => {
      const error = createMockApiError()

      expect(error.message).toBe('API Error')
      expect(error.response?.status).toBe(400)
      expect(error.response?.statusText).toBe('Bad Request')
      expect(error.isAxiosError).toBe(true)
    })

    it('accepts custom message and status', () => {
      const error = createMockApiError('Not Found', 404)

      expect(error.message).toBe('Not Found')
      expect(error.response?.status).toBe(404)
      expect(error.response?.statusText).toBe('Error')
    })
  })

  describe('Mock Functions', () => {
    it('provides mocked navigate function', () => {
      expect(mockNavigate).toBeDefined()
      expect(vi.isMockFunction(mockNavigate)).toBe(true)
    })

    it('provides mocked API client', () => {
      expect(mockApiClient.get).toBeDefined()
      expect(mockApiClient.post).toBeDefined()
      expect(mockApiClient.put).toBeDefined()
      expect(mockApiClient.delete).toBeDefined()
      expect(mockApiClient.patch).toBeDefined()

      Object.values(mockApiClient).forEach(mockFn => {
        expect(vi.isMockFunction(mockFn)).toBe(true)
      })
    })

    it('provides mocked token storage', () => {
      expect(mockTokenStorage.set).toBeDefined()
      expect(mockTokenStorage.get).toBeDefined()
      expect(mockTokenStorage.remove).toBeDefined()
      expect(mockTokenStorage.getAccessToken).toBeDefined()
      expect(mockTokenStorage.getRefreshToken).toBeDefined()
      expect(mockTokenStorage.isTokenExpired).toBeDefined()

      Object.values(mockTokenStorage).forEach(mockFn => {
        expect(vi.isMockFunction(mockFn)).toBe(true)
      })
    })
  })

  describe('clearAllMocks', () => {
    it('clears all mock functions', () => {
      // Setup some mock calls
      mockNavigate()
      mockApiClient.get()
      mockTokenStorage.set()

      // Verify mocks were called
      expect(mockNavigate).toHaveBeenCalledTimes(1)
      expect(mockApiClient.get).toHaveBeenCalledTimes(1)
      expect(mockTokenStorage.set).toHaveBeenCalledTimes(1)

      // Clear all mocks
      clearAllMocks()

      // Verify mocks were cleared
      expect(mockNavigate).not.toHaveBeenCalled()
      expect(mockApiClient.get).not.toHaveBeenCalled()
      expect(mockTokenStorage.set).not.toHaveBeenCalled()
    })
  })

  describe('Global Test Environment', () => {
    it('has jsdom environment available', () => {
      expect(document).toBeDefined()
      expect(window).toBeDefined()
      expect(HTMLElement).toBeDefined()
    })

    it('has mocked browser APIs', () => {
      expect(window.matchMedia).toBeDefined()
      expect(window.scrollTo).toBeDefined()
      expect(global.IntersectionObserver).toBeDefined()
      expect(global.ResizeObserver).toBeDefined()
    })

    it('has vitest globals available', () => {
      expect(describe).toBeDefined()
      expect(it).toBeDefined()
      expect(expect).toBeDefined()
      expect(vi).toBeDefined()
      expect(beforeEach).toBeDefined()
    })
  })
})