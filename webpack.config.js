const path = require('path')
const UglifyJsPlugin = require('uglifyjs-webpack-plugin')

module.exports = (env, argv) => ({
  watch: true,
  entry: path.resolve('./src/main.js'),
  output: {
    path: path.resolve('./static/dist'),
    publicPath: 'static/dist/',
    filename: 'gaps.js'
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [ 'style-loader', 'css-loader' ]
      },
      {
        test: /\.coffee$/,
        use: [ 'coffee-loader' ]
      },
      {
        test: /\.vue$/,
        loader: 'vue-loader',
        options: {}
      },
      {
        test: /\.(png|jpg|jpeg|gif|eot|ttf|woff|woff2|svg|svgz)(\?.+)?$/,
        use: [{
          loader: 'url-loader',
          options: {
            limit: 10000
          }
        }]
      }
    ]
  },
  devtool: argv.mode === 'development' ? "cheap-eval-source-map" : "source-map",
  plugins: argv.mode === 'development' ? [] : [ new UglifyJsPlugin({ sourceMap: true }) ],
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js' // 'vue/dist/vue.common.js' for webpack 1
    }
  }
})
