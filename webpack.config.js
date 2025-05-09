const path = require("path");
const { merge } = require("webpack-merge");
const commonConfig = {
    mode: "development",
    devtool: false,
    output: {
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
            {
                test: /\.css$/,
                use: [
                    'style-loader',
                    'css-loader',
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
            main: { import: path.resolve("assets/js/main.js") },
	},
        output: {
            path: path.resolve(__dirname, "frontpage", "static", "frontpage"),
        },
    }),
    merge(commonConfig, {
        name: "calculator",
        entry: {
            "crop-update": { import: path.resolve("assets/js/crop-update.js") },
            "crop-models": { import: path.resolve("assets/js/crop-models.js") },
        },
        output: {
            path: path.resolve(__dirname, "calculator", "static", "calculator"),
        },
    }),
    merge(commonConfig, {
        name: "django_sortable_htmx",
        entry: {
            sortable: { import: path.resolve("assets/js/sortable.js") },
        },
        output: {
            path: path.resolve(__dirname, "django_sortable_htmx", "static", "django_sortable_htmx"),
        },
    }),
];
