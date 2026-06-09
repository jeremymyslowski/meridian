import type { ReactNode } from 'react'

export interface Column<T> {
  key: string
  header: string
  render: (row: T) => ReactNode
}

interface DataTableProps<T> {
  columns: Column<T>[]
  data: T[]
  keyField: keyof T & string
  emptyMessage?: string
}

export function DataTable<T>({ columns, data, keyField, emptyMessage = 'No data' }: DataTableProps<T>) {
  if (data.length === 0) {
    return <div className="mui-empty">{emptyMessage}</div>
  }

  return (
    <table className="mui-table">
      <thead>
        <tr>
          {columns.map((col) => (
            <th key={col.key}>{col.header}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row) => (
          <tr key={String(row[keyField])}>
            {columns.map((col) => (
              <td key={col.key}>{col.render(row)}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  )
}