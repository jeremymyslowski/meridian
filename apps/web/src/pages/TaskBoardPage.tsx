import { useQuery } from '@tanstack/react-query'
import { Link, useParams } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import type { Task } from '@meridian/api-client'
import './TaskBoardPage.css'

const COLUMNS: { status: Task['status']; label: string }[] = [
  { status: 'todo', label: 'To Do' },
  { status: 'in_progress', label: 'In Progress' },
  { status: 'done', label: 'Done' },
]

export default function TaskBoardPage() {
  const { projectId } = useParams<{ projectId: string }>()
  const { client } = useAuth()

  const { data: project } = useQuery({
    queryKey: ['project', projectId],
    queryFn: () => client.getProject(projectId!),
    enabled: !!projectId,
  })

  const { data: tasks, isLoading } = useQuery({
    queryKey: ['tasks', projectId],
    queryFn: () => client.listTasks(projectId!),
    enabled: !!projectId,
  })

  if (isLoading) return <p>Loading board...</p>

  return (
    <div className="task-board">
      <div className="task-board-header">
        <Link to="/" className="back-link">&larr; Projects</Link>
        <h1>{project?.name ?? 'Task Board'}</h1>
      </div>

      <div className="kanban">
        {COLUMNS.map((col) => (
          <div key={col.status} className="kanban-column">
            <h3>{col.label}</h3>
            <div className="kanban-cards">
              {tasks
                ?.filter((t) => t.status === col.status)
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