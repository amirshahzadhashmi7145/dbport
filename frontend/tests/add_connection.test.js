import test from 'node:test'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import path from 'node:path'

const root = path.resolve('frontend/src')

test('add connection form posts and expects 201 Created', () => {
  const src = fs.readFileSync(path.join(root, 'AddConnectionForm.tsx'), 'utf8')
  assert.match(src, /fetch\('\/connections'/)
  assert.match(src, /method:\s*'POST'/)
  assert.match(src, /status !== 201|status === 201|201/)
  assert.match(src, /Add connection/)
})
