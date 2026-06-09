import type { ReactNode } from 'react'

interface EmptyStateProps {
  title: string
  description?: string
  action?: ReactNode
}

export function EmptyState({ title, description, action }: EmptyStateProps) {
  return (
    <div className="mui-empty">
      <h3 style={{ margin: '0 0 0.5rem', color: '#374151' }}>{title}</h3>
      {description && <p style={{ margin: '0 0 1rem' }}>{description}</p>}
      {action}
    </div>
  )
}