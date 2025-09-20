import '@testing-library/jest-dom'
import { vi, beforeEach } from 'vitest'

// Global test setup for Vitest
// This file is automatically loaded before all tests

// Mock IntersectionObserver for components that might use it
if (!global.IntersectionObserver) {
  global.IntersectionObserver = class IntersectionObserver {
    constructor() {}
    observe() { return null }
    disconnect() { return null }
    unobserve() { return null }
  } as unknown as typeof IntersectionObserver
}

// Mock ResizeObserver for components that might use it
if (!global.ResizeObserver) {
  global.ResizeObserver = class ResizeObserver {
    constructor() {}
    observe() { return null }
    disconnect() { return null }
    unobserve() { return null }
  } as unknown as typeof ResizeObserver
}

// Mock matchMedia for responsive components
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(), // deprecated
    removeListener: vi.fn(), // deprecated
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
})

// Mock scroll functions
Object.defineProperty(window, 'scrollTo', {
  writable: true,
  value: vi.fn(),
})

// Extend global with test-specific utilities
declare global {
  // Add any global test utilities here if needed
}

// Setup any global test state here if needed
beforeEach(() => {
  // Clear any mocks between tests
  vi.clearAllMocks()
})