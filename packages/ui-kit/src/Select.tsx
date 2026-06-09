import type { SelectHTMLAttributes, ReactNode } from 'react'

interface SelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
  label?: string
  children: ReactNode
}

export function Select({ label, children, className = '', ...props }: SelectProps) {
  return (
    <label style={{ display: 'flex', flexDirection: 'column', gap: '0.35rem', fontSize: '0.875rem' }}>
      {label && <span style={{ fontWeight: 500 }}>{label}</span>}
      <select className={`mui-select ${className}`} {...props}>
        {children}
      </select>
    </label>
  )
}