const path = require('path');
const webpack = require('webpack');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const AssetsPlugin = require('assets-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');


exports.staticLoader = function (target) {
    var filename = '[name].[ext]';

    if (target === 'BUILD') {
        filename = '[name].[hash].[ext]';
    }

    return {
        module: {
            loaders: [
                {
                    test: /\.(jpg|png|gif)$/,
                    loader: 'url?limit=25000&digest=hex&size=16&name=images/' + filename,
                },
                {
                    test: /\.svg/,
                    loader: 'svg-url-loader?limit=25000&digest=hex&size=16&name=images/' + filename
                },
                {
                    test: /\.(woff|woff2|ttf|eot)$/i,
                    loader: 'file',
                    query: {
                        name: 'fonts/' + filename
                    },
                }
                // Load css via js
                // {
                //     test: /\.(css|scss|sass)$/,
                //     loader: 'css'
                //     // loaders: ["style", "css", "sass"],
                //     // include: 'app/static/src/styles'
                // }
            ]
        }
    }
}

exports.assetsJson = function () {
    return {
        plugins: [
            new AssetsPlugin({
                filename: 'app/build/assets.json',
                prettyPrint: true,
            })
        ]
    }
}

exports.babelLoader = function() {
    return {
        module: {
            loaders: [
                {
                    test: /\.(js|jsx)$/,
                    exclude: /(node_modules|bower_components)/,
                    loader: 'babel',
                    query: {
                        presets: ['es2015','react'],
                    }
                }
            ]
        }
    };
}

exports.minify = function() {
    return {
        plugins: [
            new webpack.optimize.DedupePlugin(),
            new webpack.DefinePlugin({
              'process.env.NODE_ENV': '"production"'
            }),
            new webpack.optimize.UglifyJsPlugin({
                compress: {
                    warnings: false
                }
            }),
            new webpack.optimize.OccurenceOrderPlugin(),
            new webpack.optimize.AggressiveMergingPlugin(),
            new webpack.NoErrorsPlugin()
        ]
    };
}

exports.extractBundle = function(options) {
    const entry = {};
    entry[options.name] = options.entries;

    return {
        entry: entry, // Define an entry point needed for splitting.
            plugins: [
            new webpack.optimize.CommonsChunkPlugin({
                names: [options.name, 'manifest'] // Extract bundle and manifest files. Manifest is needed for reliable caching.
            })
        ]
    };
}

exports.clean = function(path) {
    return {
        plugins: [
            new CleanWebpackPlugin([path], {
                root: process.cwd()
            })
        ]
    };
}

exports.extractCSS = function(path, target) {
    var filename = '[name].css';

    if (target === 'BUILD') {
        filename = '[name].[chunkhash].css';
    }

    return {
        module: {
            loaders: [
                {
                    test: /\.(css|scss|sass)$/i,
                    loader: ExtractTextPlugin.extract('style', 'css?sourceMap', 'sass?sourceMap'),
                    include: path
                }
            ]
        },
        plugins: [
            new ExtractTextPlugin(filename, {
                allChunks: true
            })
        ]
    };
}

exports.copyFiles = function (destination) {
    return {
        plugins: [
            new CopyWebpackPlugin([
                {
                    context: 'app/templates',
                    from: '**/*.html',
                    to: destination
                },
                {
                    from: 'app/static/src/robots.txt',
                    to: destination,
                },
                {
                    from: 'app/static/src/favicon.png',
                    to: destination,
                }
            ])
        ]
    }
}
