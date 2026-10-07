import test from 'node:test'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import path from 'node:path'

const src = fs.readFileSync(path.resolve('frontend/src/AddConnectionForm.tsx'), 'utf8')

test('add connection form expects 201 and FR-001 body fields', () => {
  assert.match(src, /fetch\('\/connections'/)
  assert.match(src, /method:\s*'POST'/)
  assert.match(src, /status !== 201/)
  for (const key of ['id', 'name', 'dialect', 'host', 'port', 'database', 'mode', 'introspection_status', 'created_at', 'status_url']) {
    assert.match(src, new RegExp(key))
  }
})
