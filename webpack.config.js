const path = require("path");
module.exports = {
  mode: "development",
  devtool: false,
  entry: {
    bootstrap: { import: path.resolve("assets/js/bootstrap.js") },
    sortable: { import: path.resolve("assets/js/sortable.js") },
    htmx: { import: path.resolve("assets/js/htmx.js") },
    hyperscript: { import: path.resolve("assets/js/hyperscript.js") },
    "crop-update": { import: path.resolve("assets/js/crop-update.js") },
    "crop-models": { import: path.resolve("assets/js/crop-models.js") },
  },
  output: {
    path: path.resolve(__dirname, "frontpage", "static", "frontpage"),
    filename: "[name].bundle.js",
  },
  module: {
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
    ],
  },
};
