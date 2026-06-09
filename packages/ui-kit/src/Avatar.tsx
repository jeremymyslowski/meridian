interface AvatarProps {
  name: string
  size?: number
}

export function Avatar({ name, size = 32 }: AvatarProps) {
  const initials = name
    .split(' ')
    .map((n) => n[0])
    .join('')
    .slice(0, 2)
    .toUpperCase()

  return (
    <span className="mui-avatar" style={{ width: size, height: size, fontSize: size * 0.35 }}>
      {initials}
    </span>
  )
}