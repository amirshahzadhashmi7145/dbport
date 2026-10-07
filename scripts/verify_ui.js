const { spawnSync } = require('child_process');
const result = spawnSync('node', ['--test', 'frontend/tests'], { stdio: 'inherit' });
process.exit(result.status === null ? 1 : result.status);
