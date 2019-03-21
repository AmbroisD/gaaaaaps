
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
// const HtmlWebpackPlugin = require('html-webpack-plugin')
const UglifyJsPlugin = require('uglifyjs-webpack-plugin')
const webpack = require('webpack')
const path = require('path')

let extractCssInstance = new MiniCssExtractPlugin({
  filename: 'static/dist/gaps.css'
})

let languageReplacement = new webpack.NormalModuleReplacementPlugin(
  /element-ui[\/\\]lib[\/\\]locale[\/\\]lang[\/\\]zh-CN/,
  'element-ui/lib/locale/lang/en'
)

// let appHtml = new HtmlWebpackPlugin({
//   template: 'templates/app.html',
//   filename: 'templates/app.html',
//   hash: true
// })

module.exports = (env, argv) => {
  let plugins = [
    extractCssInstance,
    languageReplacement
    // appHtml
  ]

  if (argv.mode === 'development') {
    // plugins.push(new BundleAnalyzerPlugin())
  } else {
    plugins.push(new UglifyJsPlugin({ sourceMap: true }))
  }

  return {
    watch: argv.mode === 'development',
    entry: path.resolve('./src/main.js'),
    output: {
      path: path.resolve('.'),
      publicPath: '',
      filename: 'static/dist/gaps.js'
    },
    module: {
      rules: [
        {
          test: /\.css$/,
          use: [
            MiniCssExtractPlugin.loader,
            'css-loader'
          ]
        },
        {
          test: /\.vue$/,
          loader: 'vue-loader',
          options: {
            loaders: {
              // Override the default loaders
            }
          }
        },
        {
          test: /\.(png|jpg|jpeg|gif|eot|ttf|woff|woff2|svg|svgz)(\?.+)?$/,
          use: [{
            loader: 'url-loader',
            options: {
              outputPath: 'static/dist',
              limit: 10000
            }
          }]
        }
      ]
    },
    devtool: argv.mode === 'development' ? "cheap-eval-source-map" : "source-map",
    plugins: plugins,
    resolve: {
      alias: {
        'vue$': 'vue/dist/vue.esm.js'
      }
    }
  }
}

// const path = require('path')
// const UglifyJsPlugin = require('uglifyjs-webpack-plugin')
//
// module.exports = (env, argv) => ({
//   watch: true,
//   entry: path.resolve('./src/main.js'),
//   output: {
//     path: path.resolve('./static/dist'),
//     publicPath: 'static/dist/',
//     filename: 'gaps.js'
//   },
//   module: {
//     rules: [
//       {
//         test: /\.css$/,
//         use: [ 'style-loader', 'css-loader' ]
//       },
//       {
//         test: /\.coffee$/,
//         use: [ 'coffee-loader' ]
//       },
//       {
//         test: /\.vue$/,
//         loader: 'vue-loader',
//         options: {}
//       },
//       {
//         test: /\.(png|jpg|jpeg|gif|eot|ttf|woff|woff2|svg|svgz)(\?.+)?$/,
//         use: [{
//           loader: 'url-loader',
//           options: {
//             limit: 10000
//           }
//         }]
//       }
//     ]
//   },
//   devtool: argv.mode === 'development' ? "cheap-eval-source-map" : "source-map",
//   plugins: argv.mode === 'development' ? [] : [ new UglifyJsPlugin({ sourceMap: true }) ],
//   resolve: {
//     alias: {
//       'vue$': 'vue/dist/vue.esm.js' // 'vue/dist/vue.common.js' for webpack 1
//     }
//   }
// })
