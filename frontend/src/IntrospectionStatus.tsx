import React, { useEffect, useState } from 'react'

type Props = { connectionId: string }

export function IntrospectionStatus({ connectionId }: Props) {
  const [status, setStatus] = useState<number | null>(null)
  const [body, setBody] = useState<any>(null)

  useEffect(() => {
    let cancelled = false
    ;(async () => {
      const response = await fetch(`/connections/${connectionId}/introspection`)
      if (cancelled) return
      setStatus(response.status)
      if (response.status === 200) setBody(await response.json())
    })()
    return () => {
      cancelled = true
    }
  }, [connectionId])

  if (status === null) return <p>Loading introspection…</p>
  return (
    <section aria-label="introspection-status">
      <p data-testid="introspection-http">status {status}</p>
      {body ? (
        <p data-testid="introspection-body">
          {body.status} tables {body.table_count} at {body.completed_at} ({body.duration_ms}ms)
        </p>
      ) : null}
    </section>
  )
}
