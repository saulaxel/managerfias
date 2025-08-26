const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyPlugin = require("copy-webpack-plugin");
const path = require('path');

module.exports = {
  entry: './src/main.ts',
  devtool: 'inline-source-map',
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: {
          loader: 'ts-loader'
        },
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js']
  },
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
    library: 'MyLibrary',
    libraryTarget: 'window',
  },
  plugins: [
    new HtmlWebpackPlugin({
      hash: true,
      title: 'Managerfias',
      header: 'Managerfias',
      metaDesc: 'Búsqueda de códigos de documentos como monografías y esquemas',
      template: './src/index.html',
      filename: 'index.html',
      inject: 'body'
    }),
    new CopyPlugin({
      patterns: [
        { from: './src/img', to: 'img' },
        { from: './src/img/icons', to: 'img/icons' },
        { from: './src/service_workers/', to: '' },
      ]
    }),
  ],
  mode: 'development',
  cache: {
    type: 'filesystem'
  }
};
