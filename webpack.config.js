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
            bootstrap: { import: path.resolve("assets/js/bootstrap.js") },
            htmx: { import: path.resolve("assets/js/htmx.js") },
	    hyperscript: { import: path.resolve("assets/js/hyperscript.js") },
	},
        output: {
            path: path.resolve(__dirname, "frontpage", "static", "frontpage"),
        },
    }),
    merge(commonConfig, {
        name: "register",
        entry: {
            "plantvariety-form": {
                import: path.resolve("assets/js/plantvariety-form.js"),
            },
            "protocol-manage": {
                import: path.resolve("assets/js/protocol-manage.js"),
            },
        },
        output: {
            path: path.resolve(__dirname, "register", "static", "register"),
        },
    }),
    merge(commonConfig, {
        name: "describe",
        entry: {
            "description-form": {
                import: path.resolve("assets/js/description-form.js"),
            },
        },
        output: {
            path: path.resolve(__dirname, "describe", "static", "describe"),
        },
    }),
    merge(commonConfig, {
        name: "collect",
        entry: {
            "sample-detail": {
                import: path.resolve("assets/js/sample-detail.js"),
            },
            "sample-form": {
                import: path.resolve("assets/js/sample-form.js"),
            },
        },
        output: {
            path: path.resolve(__dirname, "collect", "static", "collect"),
        },
    }),
    merge(commonConfig, {
        name: "spaces",
        entry: {
            "location-detail": {
                import: path.resolve("assets/js/location-detail.js"),
            },
        },
        output: {
            path: path.resolve(__dirname, "spaces", "static", "spaces"),
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
