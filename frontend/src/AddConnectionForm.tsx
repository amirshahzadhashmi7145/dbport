import React, { useState } from 'react'

type Props = { onCreated: (id: string) => void }

export function AddConnectionForm({ onCreated }: Props) {
  const [name, setName] = useState('local')
  const [error, setError] = useState<string | null>(null)
  const [lastStatus, setLastStatus] = useState<number | null>(null)

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    const response = await fetch('/connections', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name,
        dialect: 'postgresql',
        host: '127.0.0.1',
        port: 5432,
        database: 'app',
        mode: 'read_only',
        username: 'u',
        password: 'p',
      }),
    })
    setLastStatus(response.status)
    if (response.status !== 201) {
      setError(`Failed with ${response.status}`)
      return
    }
    const body = await response.json()
    onCreated(body.id)
  }

  return (
    <form onSubmit={onSubmit} aria-label="add-connection">
      <label>
        Name
        <input value={name} onChange={(e) => setName(e.target.value)} name="name" />
      </label>
      <button type="submit">Add connection</button>
      {lastStatus !== null ? <p data-testid="create-status">status {lastStatus}</p> : null}
      {error ? <p role="alert">{error}</p> : null}
    </form>
  )
}
