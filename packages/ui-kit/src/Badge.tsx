import type { ReactNode } from 'react'

interface BadgeProps {
  variant?: string
  children: ReactNode
}

export function Badge({ variant = 'default', children }: BadgeProps) {
  return <span className={`mui-badge mui-badge-${variant}`}>{children}</span>
}