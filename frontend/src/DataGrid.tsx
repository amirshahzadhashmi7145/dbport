import React, { useEffect, useState } from 'react'

type Props = { connectionId: string; table: string }

export function DataGrid({ connectionId, table }: Props) {
  const [status, setStatus] = useState<number | null>(null)
  const [payload, setPayload] = useState<any>(null)

  useEffect(() => {
    let cancelled = false
    ;(async () => {
      const response = await fetch(
        `/connections/${connectionId}/tables/${table}/rows?page=1&page_size=50`,
      )
      if (cancelled) return
      setStatus(response.status)
      if (response.status === 200) {
        setPayload(await response.json())
      }
    })()
    return () => {
      cancelled = true
    }
  }, [connectionId, table])

  if (status === null) return <p>Loading grid…</p>
  if (status !== 200) return <p role="alert">Grid failed {status}</p>
  return (
    <section aria-label="data-grid">
      <p data-testid="grid-status">status {status}</p>
      <table>
        <thead>
          <tr>
            {(payload?.columns || []).map((c: any) => (
              <th key={c.name}>{c.name}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {(payload?.rows || []).map((row: any, i: number) => (
            <tr key={i}>
              {(payload?.columns || []).map((c: any) => (
                <td key={c.name}>{String(row[c.name])}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <p>
        page {payload.page} size {payload.page_size} total {payload.total_rows} cursor{' '}
        {String(payload.next_cursor)}
      </p>
    </section>
  )
}
