import React, { useEffect, useState } from 'react'
import { AddConnectionForm } from './AddConnectionForm'
import { DataGrid } from './DataGrid'
import { IntrospectionStatus } from './IntrospectionStatus'

export function App() {
  const [connectionId, setConnectionId] = useState<string | null>(null)
  const [table] = useState('users')
  return (
    <main>
      <h1>DBPort</h1>
      <AddConnectionForm onCreated={setConnectionId} />
      {connectionId ? (
        <>
          <IntrospectionStatus connectionId={connectionId} />
          <DataGrid connectionId={connectionId} table={table} />
        </>
      ) : null}
    </main>
  )
}
