const path = require("path");
const { merge } = require("webpack-merge");
const FileManagerPlugin = require("filemanager-webpack-plugin");
const commonConfig = {
  module: {
    mode: "development",
    devtool: false,
    rules: [
      {
        test: /\.(scss)$/,
        use: [
          {
            loader: "style-loader",
          },
          {
            loader: "css-loader",
          },
          {
            loader: "postcss-loader",
            options: {
              postcssOptions: {
                plugins: () => [require("autoprefixer")],
              },
            },
          },
          {
            loader: "sass-loader",
          },
        ],
      },
      {
        test: /\.woff2?$/,
        type: "asset/resource",
      },
    ],
  },
};

module.exports = [
  merge(commonConfig, {
    name: "frontpage",
    entry: {
      bootstrap: { import: path.resolve("assets/js/bootstrap.js") },
      sortable: { import: path.resolve("assets/js/sortable.js") },
      htmx: { import: path.resolve("assets/js/htmx.js") },
      hyperscript: { import: path.resolve("assets/js/hyperscript.js") },
      "crop-update": { import: path.resolve("assets/js/crop-update.js") },
      "crop-models": { import: path.resolve("assets/js/crop-models.js") },
      "location-detail": {
        import: path.resolve("assets/js/location-detail.js"),
      },
      "protocol-manage": {
        import: path.resolve("assets/js/protocol-manage.js"),
      },
    },
    output: {
      path: path.resolve(__dirname, "frontpage", "static", "frontpage"),
      filename: "[name].bundle.js",
    },
  }),
  merge(commonConfig, {
    name: "collect",
    entry: {
      "seedsample-detail": {
        import: path.resolve("assets/js/seedsample-detail.js"),
      },
      "seedsample-form": {
        import: path.resolve("assets/js/seedsample-form.js"),
      },
    },
    output: {
      path: path.resolve(__dirname, "collect", "static", "collect"),
      filename: "[name].bundle.js",
    },
  }),
];
