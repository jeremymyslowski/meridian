import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link, useParams } from 'react-router-dom'
import { Badge, Button, DataTable, Select, Spinner, type Column } from '@meridian/ui-kit'
import type { Task } from '@meridian/api-client'
import { useAuth } from '../context/AuthContext'
import { usePermissions } from '../hooks/usePermissions'

export default function TaskListPage() {
  const { projectId } = useParams<{ projectId: string }>()
  const { client } = useAuth()
  const [page, setPage] = useState(1)
  const [statusFilter, setStatusFilter] = useState<string>('')

  const { data: project } = useQuery({
    queryKey: ['project', projectId],
    queryFn: () => client.getProject(projectId!),
    enabled: !!projectId,
  })

  const { canWrite } = usePermissions(project?.team_id)

  const { data, isLoading } = useQuery({
    queryKey: ['tasks-paginated', projectId, page, statusFilter],
    queryFn: () =>
      client.listTasks(projectId!, {
        page,
        page_size: 10,
        status: statusFilter ? (statusFilter as Task['status']) : undefined,
      }),
    enabled: !!projectId,
  })

  const columns: Column<Task>[] = [
    {
      key: 'title',
      header: 'Title',
      render: (row) => <Link to={`/tasks/${row.id}`}>{row.title}</Link>,
    },
    {
      key: 'status',
      header: 'Status',
      render: (row) => <Badge variant={row.status}>{row.status.replace('_', ' ')}</Badge>,
    },
    {
      key: 'updated',
      header: 'Updated',
      render: (row) => new Date(row.updated_at).toLocaleDateString(),
    },
  ]

  if (isLoading) return <Spinner />

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <div>
          <Link to={`/projects/${projectId}`} style={{ fontSize: '0.875rem', color: '#6b7280' }}>
            &larr; Board view
          </Link>
          <h1 style={{ margin: '0.5rem 0 0' }}>{project?.name} — Task List</h1>
        </div>
        <Select
          label="Filter status"
          value={statusFilter}
          onChange={(e) => { setStatusFilter(e.target.value); setPage(1) }}
          style={{ width: 160 }}
        >
          <option value="">All</option>
          <option value="todo">To Do</option>
          <option value="in_progress">In Progress</option>
          <option value="done">Done</option>
        </Select>
      </div>

      {!canWrite && (
        <p style={{ color: '#6b7280', fontSize: '0.875rem', marginBottom: '1rem' }}>
          View-only access — you cannot edit tasks or comments.
        </p>
      )}

      <DataTable columns={columns} data={data?.items ?? []} keyField="id" emptyMessage="No tasks found" />

      {data && data.meta.total_pages > 1 && (
        <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem', alignItems: 'center' }}>
          <Button variant="secondary" disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>
            Previous
          </Button>
          <span style={{ fontSize: '0.875rem' }}>
            Page {data.meta.page} of {data.meta.total_pages} ({data.meta.total} tasks)
          </span>
          <Button
            variant="secondary"
            disabled={page >= data.meta.total_pages}
            onClick={() => setPage((p) => p + 1)}
          >
            Next
          </Button>
        </div>
      )}
    </div>
  )
}