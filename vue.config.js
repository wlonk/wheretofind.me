module.exports = {
  lintOnSave: false,
  filenameHashing: false,
  devServer: {
    proxy: "http://localhost:8000",
    writeToDisk: true
  },
  configureWebpack: {
    output: {
      filename: "js/[name].js"
    }
  }
};
