import { useQuery } from '@tanstack/react-query'
import { useAuth } from '../context/AuthContext'

export function usePermissions(teamId?: string) {
  const { client } = useAuth()

  const { data: teams } = useQuery({
    queryKey: ['my-teams'],
    queryFn: () => client.listMyTeams(),
  })

  const membership = teamId
    ? teams?.find((t) => t.team_id === teamId)
    : undefined

  const role = membership?.role

  return {
    teams: teams ?? [],
    role,
    canWrite: role === 'owner' || role === 'member',
    canAdmin: role === 'owner',
    isViewer: role === 'viewer',
  }
}