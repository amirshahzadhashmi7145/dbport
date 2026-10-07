import test from 'node:test'
import assert from 'node:assert/strict'
import fs from 'node:fs'
import path from 'node:path'

const src = fs.readFileSync(path.resolve('frontend/src/DataGrid.tsx'), 'utf8')

test('data grid requests rows and expects 200 OK body fields', () => {
  assert.match(src, /\/tables\/\$\{table\}\/rows/)
  assert.match(src, /status === 200|status \{status\}/)
  assert.match(src, /page_size/)
  assert.match(src, /total_rows/)
  assert.match(src, /next_cursor/)
  assert.match(src, /columns/)
  assert.match(src, /rows/)
})
