import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import './ProjectsPage.css'

export default function ProjectsPage() {
  const { client } = useAuth()

  const { data: projects, isLoading, error } = useQuery({
    queryKey: ['projects'],
    queryFn: () => client.listProjects(),
  })

  if (isLoading) return <p>Loading projects...</p>
  if (error) return <p className="error">Failed to load projects</p>

  return (
    <div className="projects-page">
      <h1>Projects</h1>
      <div className="project-grid">
        {projects?.map((project) => (
          <Link
            key={project.id}
            to={`/projects/${project.id}`}
            className="project-card"
          >
            <h2>{project.name}</h2>
            <p>{project.description ?? 'No description'}</p>
            <span className="project-status">{project.status}</span>
          </Link>
        ))}
      </div>
      {projects?.length === 0 && (
        <p className="empty">No projects yet. Seed the database to get started.</p>
      )}
    </div>
  )
}