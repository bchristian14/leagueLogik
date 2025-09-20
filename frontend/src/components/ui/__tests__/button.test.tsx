/**
 * Test suite for Button component
 * Validates button rendering, variants, sizes, and interactions
 */

import { describe, it, expect, vi } from 'vitest'
import { renderWithProviders, expectElementToBeVisible } from '../../../test-utils'
import userEvent from '@testing-library/user-event'
import { Button } from '../button'

describe('Button Component', () => {
  describe('Rendering', () => {
    it('renders a button with default props', () => {
      const { getByRole } = renderWithProviders(
        <Button>Click me</Button>
      )

      const button = getByRole('button')
      expectElementToBeVisible(button)
      expect(button).toHaveTextContent('Click me')
    })

    it('renders with custom text content', () => {
      const { getByText } = renderWithProviders(
        <Button>Custom Button Text</Button>
      )

      expect(getByText('Custom Button Text')).toBeInTheDocument()
    })

    it('applies custom className', () => {
      const { getByRole } = renderWithProviders(
        <Button className="custom-class">Button</Button>
      )

      expect(getByRole('button')).toHaveClass('custom-class')
    })
  })

  describe('Variants', () => {
    it('renders default variant correctly', () => {
      const { getByRole } = renderWithProviders(
        <Button variant="default">Default</Button>
      )

      const button = getByRole('button')
      expect(button).toHaveClass('bg-blue-600', 'text-white')
    })

    it('renders destructive variant correctly', () => {
      const { getByRole } = renderWithProviders(
        <Button variant="destructive">Delete</Button>
      )

      const button = getByRole('button')
      expect(button).toHaveClass('bg-red-600', 'text-white')
    })

    it('renders outline variant correctly', () => {
      const { getByRole } = renderWithProviders(
        <Button variant="outline">Outline</Button>
      )

      const button = getByRole('button')
      expect(button).toHaveClass('border', 'border-gray-300', 'bg-white')
    })

    it('renders secondary variant correctly', () => {
      const { getByRole } = renderWithProviders(
        <Button variant="secondary">Secondary</Button>
      )

      const button = getByRole('button')
      expect(button).toHaveClass('bg-gray-100', 'text-gray-900')
    })

    it('renders ghost variant correctly', () => {
      const { getByRole } = renderWithProviders(
        <Button variant="ghost">Ghost</Button>
      )

      const button = getByRole('button')
      expect(button).toHaveClass('hover:bg-gray-100')
    })

    it('renders link variant correctly', () => {
      const { getByRole } = renderWithProviders(
        <Button variant="link">Link</Button>
      )

      const button = getByRole('button')
      expect(button).toHaveClass('text-blue-600', 'underline-offset-4')
    })
  })

  describe('Sizes', () => {
    it('renders default size correctly', () => {
      const { getByRole } = renderWithProviders(
        <Button size="default">Default Size</Button>
      )

      const button = getByRole('button')
      expect(button).toHaveClass('h-9', 'px-4', 'py-2')
    })

    it('renders small size correctly', () => {
      const { getByRole } = renderWithProviders(
        <Button size="sm">Small</Button>
      )

      const button = getByRole('button')
      expect(button).toHaveClass('h-8', 'px-3', 'text-xs')
    })

    it('renders large size correctly', () => {
      const { getByRole } = renderWithProviders(
        <Button size="lg">Large</Button>
      )

      const button = getByRole('button')
      expect(button).toHaveClass('h-10', 'px-8')
    })

    it('renders icon size correctly', () => {
      const { getByRole } = renderWithProviders(
        <Button size="icon">🔥</Button>
      )

      const button = getByRole('button')
      expect(button).toHaveClass('h-9', 'w-9')
    })
  })

  describe('Interactions', () => {
    it('calls onClick handler when clicked', async () => {
      const user = userEvent.setup()
      const handleClick = vi.fn()

      const { getByRole } = renderWithProviders(
        <Button onClick={handleClick}>Click me</Button>
      )

      const button = getByRole('button')
      await user.click(button)

      expect(handleClick).toHaveBeenCalledTimes(1)
    })

    it('does not call onClick when disabled', async () => {
      const user = userEvent.setup()
      const handleClick = vi.fn()

      const { getByRole } = renderWithProviders(
        <Button onClick={handleClick} disabled>Disabled Button</Button>
      )

      const button = getByRole('button')
      expect(button).toBeDisabled()

      await user.click(button)
      expect(handleClick).not.toHaveBeenCalled()
    })

    it('has correct disabled styling', () => {
      const { getByRole } = renderWithProviders(
        <Button disabled>Disabled</Button>
      )

      const button = getByRole('button')
      expect(button).toHaveClass('disabled:pointer-events-none', 'disabled:opacity-50')
    })
  })

  describe('Accessibility', () => {
    it('has correct role', () => {
      const { getByRole } = renderWithProviders(
        <Button>Accessible Button</Button>
      )

      expect(getByRole('button')).toBeInTheDocument()
    })

    it('supports custom aria-label', () => {
      const { getByLabelText } = renderWithProviders(
        <Button aria-label="Custom label">Button</Button>
      )

      expect(getByLabelText('Custom label')).toBeInTheDocument()
    })

    it('supports focus with keyboard navigation', async () => {
      const user = userEvent.setup()

      const { getByRole } = renderWithProviders(
        <Button>Focusable Button</Button>
      )

      const button = getByRole('button')
      await user.tab()

      expect(button).toHaveFocus()
    })
  })

  describe('Forward Ref', () => {
    it('forwards ref correctly', () => {
      let buttonRef: HTMLButtonElement | null = null

      renderWithProviders(
        <Button ref={(ref: HTMLButtonElement | null) => { buttonRef = ref }}>Ref Button</Button>
      )

      expect(buttonRef).toBeInstanceOf(HTMLButtonElement)
      expect(buttonRef).not.toBeNull()
      if (buttonRef) {
        expect(buttonRef.tagName).toBe('BUTTON')
      }
    })
  })

  describe('AsChild Prop', () => {
    it('renders as child component when asChild is true', () => {
      const { getByRole } = renderWithProviders(
        <Button asChild>
          <a href="/test">Link Button</a>
        </Button>
      )

      const link = getByRole('link')
      expect(link).toBeInTheDocument()
      expect(link).toHaveAttribute('href', '/test')
      expect(link).toHaveTextContent('Link Button')
    })
  })
})