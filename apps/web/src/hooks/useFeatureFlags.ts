import { useQuery } from '@tanstack/react-query'
import { useAuth } from '../context/AuthContext'

export function useFeatureFlags() {
  const { client } = useAuth()

  const { data } = useQuery({
    queryKey: ['feature-flags'],
    queryFn: () => client.getFeatureFlags(),
    staleTime: 60_000,
  })

  const flags = data?.flags ?? {}

  return {
    flags,
    isEnabled: (key: string) => Boolean(flags[key]),
  }
}