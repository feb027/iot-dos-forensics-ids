module.exports = {
  apps: [
    {
      name: 'iot-dos-soc-demo-api',
      script: '/home/aqua/iot-dos-forensics-ids/backend/app.py',
      interpreter: 'python3',
      cwd: '/home/aqua/iot-dos-forensics-ids',
      env: {
        PYTHONPATH: '/home/aqua/iot-dos-forensics-ids/backend',
        PYTHONUNBUFFERED: '1'
      },
      max_memory_restart: '300M'
    }
  ]
};
