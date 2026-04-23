module.exports = {
  apps: [
    {
      name: "week-4-api",
      script: "server.js",

      env_prod: {
        NODE_ENV: "prod",
        PORT: 3001,
        LOG_LEVEL: "info"
      },

      log_date_format: "YYYY-MM-DD HH:mm:ss Z",
    },
  ],
};