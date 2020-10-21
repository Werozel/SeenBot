module.exports = {
  apps : [{
    name: 'SeenBot',
    script: 'routine.py',
    interpreter: 'python3',
    

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

  deploy : {
    production : {
      user : 'node',
      host : '212.83.163.1',
      ref  : 'origin/master',
      repo : 'git@github.com:repo.git',
      path : '/var/www/production',
      'post-deploy' : 'npm install && pm2 reload ecosystem.config.js --env production'
    }
  }
};
