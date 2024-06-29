module.exports = {
  apps : [{
    name: 'SeenBot',
    script: 'routine.py',
    interpreter: './venv/bin/python3',


    // Options reference: https://pm2.keymetrics.io/docs/usage/application-declaration/
    args: '-u',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '300M',
    env: {
      NODE_ENV: 'development',
      PM2_KILL_SIGNAL: 'SIGINT'
    }
  }],
};