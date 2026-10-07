const {spawnSync}=require('child_process');const r=spawnSync('node',['--test','frontend/tests'],{stdio:'inherit'});process.exit(r.status??1);
