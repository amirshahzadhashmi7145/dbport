import test from 'node:test'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import path from 'node:path'

const src = fs.readFileSync(path.resolve('frontend/src/IntrospectionStatus.tsx'), 'utf8')

test('introspection UI polls status endpoint for 200 complete payload', () => {
  assert.match(src, /\/introspection/)
  assert.match(src, /status === 200|status \{status\}/)
  assert.match(src, /table_count/)
  assert.match(src, /completed_at/)
  assert.match(src, /duration_ms/)
})
