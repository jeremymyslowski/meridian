import { useQuery } from '@tanstack/react-query'
import { Link, useParams } from 'react-router-dom'
import { Badge } from '@meridian/ui-kit'
import type { Task } from '@meridian/api-client'
import { useAuth } from '../context/AuthContext'
import { useFeatureFlags } from '../hooks/useFeatureFlags'
import { usePermissions } from '../hooks/usePermissions'
import './TaskBoardPage.css'

const COLUMNS: { status: Task['status']; label: string }[] = [
  { status: 'todo', label: 'To Do' },
  { status: 'in_progress', label: 'In Progress' },
  { status: 'done', label: 'Done' },
]

export default function TaskBoardPage() {
  const { projectId } = useParams<{ projectId: string }>()
  const { client } = useAuth()
  const { isEnabled } = useFeatureFlags()

  const { data: project } = useQuery({
    queryKey: ['project', projectId],
    queryFn: () => client.getProject(projectId!),
    enabled: !!projectId,
  })

  const { canWrite, role } = usePermissions(project?.team_id)

  const { data: tasksPage, isLoading } = useQuery({
    queryKey: ['tasks', projectId],
    queryFn: () => client.listTasks(projectId!, { page: 1, page_size: 100 }),
    enabled: !!projectId,
  })

  const tasks = tasksPage?.items ?? []

  if (isLoading) return <p>Loading board...</p>

  return (
    <div className="task-board">
      <div className="task-board-header">
        <Link to="/" className="back-link">&larr; Projects</Link>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginTop: '0.5rem' }}>
          <h1 style={{ margin: 0 }}>{project?.name ?? 'Task Board'}</h1>
          {role && <Badge variant={role}>{role}</Badge>}
        </div>
        <div className="task-board-actions">
          {isEnabled('task_pagination') && (
            <Link to={`/projects/${projectId}/list`} className="view-link">
              List view with pagination
            </Link>
          )}
          {!canWrite && (
            <span className="viewer-notice">View-only — editing disabled</span>
          )}
        </div>
      </div>

      <div className="kanban">
        {COLUMNS.map((col) => (
          <div key={col.status} className="kanban-column">
            <h3>{col.label}</h3>
            <div className="kanban-cards">
              {tasks
                .filter((t) => t.status === col.status)
                .map((task) => (
                  <Link
                    key={task.id}
                    to={`/tasks/${task.id}`}
                    className="task-card"
                  >
                    <span className="task-card-title">{task.title}</span>
                  </Link>
                ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}