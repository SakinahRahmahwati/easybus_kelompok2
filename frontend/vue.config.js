const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://localhost:8081',  // NGINX address
        changeOrigin: true,
        logLevel: 'debug',
      },
    },
  },
});
