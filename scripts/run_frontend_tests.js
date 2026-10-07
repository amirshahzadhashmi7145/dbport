const { spawnSync } = require('child_process');
// Ignore Jest-style flags forwarded by `npm test -- --watchAll=false`.
const result = spawnSync('node', ['--test', 'frontend/tests'], { stdio: 'inherit' });
process.exit(result.status === null ? 1 : result.status);
