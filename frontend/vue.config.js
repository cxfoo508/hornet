// vue.config.js 配置

module.exports = {
    runtimeCompiler: true,
    publicPath: "./", // 设置打包文件相对路径
    outputDir: "dist", // 构建时输出的目录根路径
    // assetsDir: 'static',  // 放置静态资源的目录
    // indexPath: 'index.html', // HTML输出的路径
    devServer: {
        // proxy: "http://localhost:8000",
        host: "0.0.0.0",
        port: "8080",
        proxy: {
            "/api": {
                // 配置到接口包含api使用该代理
                target: "http://hornet:8000/api", // 定义后端的接口
                changeOrigin: true,
                ws: true,
                pathRewrite: {
                    "^/api": "",
                },
            },
            static: {
                target: "http://hornet:8000/static", // 定义后端的接口
                changeOrigin: true,
                ws: true,
                pathRewrite: {
                    "^/static": "",
                },
            },
        },
    },
};
