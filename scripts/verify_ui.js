const assert = require('assert');
const fs = require('fs');
const path = require('path');
assert.ok(fs.existsSync(path.join(__dirname, '..', 'package.json')), 'package.json missing');
const zone = "frontend";
assert.ok(
  fs.existsSync(zone) || fs.existsSync('web') || fs.existsSync('frontend'),
  'frontend zone missing'
);
process.exit(0);
