import { FormEvent, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Link, useParams } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import './TaskDetailPage.css'

export default function TaskDetailPage() {
  const { taskId } = useParams<{ taskId: string }>()
  const { client } = useAuth()
  const queryClient = useQueryClient()
  const [commentBody, setCommentBody] = useState('')

  const { data: task, isLoading } = useQuery({
    queryKey: ['task', taskId],
    queryFn: () => client.getTask(taskId!),
    enabled: !!taskId,
  })

  const { data: comments } = useQuery({
    queryKey: ['comments', taskId],
    queryFn: () => client.listComments(taskId!),
    enabled: !!taskId,
  })

  const addComment = useMutation({
    mutationFn: (body: string) => client.createComment(taskId!, body),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['comments', taskId] })
      setCommentBody('')
    },
  })

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (!commentBody.trim()) return
    addComment.mutate(commentBody.trim())
  }

  if (isLoading) return <p>Loading task...</p>
  if (!task) return <p>Task not found</p>

  return (
    <div className="task-detail">
      <Link to={`/projects/${task.project_id}`} className="back-link">
        &larr; Back to board
      </Link>

      <div className="task-detail-header">
        <h1>{task.title}</h1>
        <span className={`status-badge status-${task.status}`}>{task.status}</span>
      </div>

      {task.description && (
        <p className="task-description">{task.description}</p>
      )}

      <section className="comments-section">
        <h2>Comments ({comments?.length ?? 0})</h2>

        <form className="comment-form" onSubmit={handleSubmit}>
          <textarea
            value={commentBody}
            onChange={(e) => setCommentBody(e.target.value)}
            placeholder="Add a comment..."
            rows={3}
          />
          <button type="submit" className="btn-primary" disabled={addComment.isPending}>
            {addComment.isPending ? 'Posting...' : 'Post comment'}
          </button>
        </form>

        <div className="comment-list">
          {comments?.map((comment) => (
            <div key={comment.id} className="comment">
              <div className="comment-meta">
                <strong>{comment.author_name}</strong>
                <time>{new Date(comment.created_at).toLocaleString()}</time>
              </div>
              <p>{comment.body}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}