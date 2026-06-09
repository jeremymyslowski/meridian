import type { InputHTMLAttributes } from 'react'

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string
}

export function Input({ label, id, className = '', ...props }: InputProps) {
  return (
    <label style={{ display: 'flex', flexDirection: 'column', gap: '0.35rem', fontSize: '0.875rem' }}>
      {label && <span style={{ fontWeight: 500 }}>{label}</span>}
      <input id={id} className={`mui-input ${className}`} {...props} />
    </label>
  )
}