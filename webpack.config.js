const path = require('path');
const webpack = require('webpack');
const merge = require('webpack-merge');
const validate = require('webpack-validator');
const parts = require('./webpack.parts');
const CopyWebpackPlugin = require('copy-webpack-plugin');

const PATHS = {
    app: path.join(__dirname, 'app', 'static', 'src'),
    style: path.join(__dirname, 'app', 'static', 'src', 'styles', 'main.scss'),
    build: path.join(__dirname, 'app', 'build'),
    dev: path.join(__dirname, 'app', 'static', 'dev')
};

const TARGET = process.argv.slice(2)[0].includes('build') ? 'BUILD' : 'DEV'; // webpack --build || webpack --dev

var config;

switch(TARGET) {
    case 'BUILD':
        config = merge({
            devtool:'source-map',
            cache: false,
            entry: {
                app: PATHS.app,
                style: PATHS.style
            },
            output: {
                path: PATHS.build,
                publicPath: '/',
                filename: 'js/[name].[chunkhash].js',
                // chunkFilename: '[chunkhash].js'
            },
            plugins: [],
            resolve: {
                extensions: ['', '.js', '.jsx'],
                // alias: {
                //     'react': 'react-lite',
                //     'react-dom': 'react-lite'
                // }
            }
        },
            parts.clean(PATHS.build),

            parts.babelLoader(),

            parts.staticLoader(TARGET),

            parts.copyFiles(PATHS.build),

            parts.extractBundle({
                name: 'vendor',
                entries: ['react', 'react-dom', 'react-redux']
            }),

            parts.minify(),

            parts.extractCSS(PATHS.style, TARGET),

            parts.assetsJson()
        );
        break;
    default:
        config = merge({
            devtool: 'source-map',
            watch: true,
            cache: true,
            entry: {
                app: PATHS.app,
                style: PATHS.style
            },
            output: {
                path: PATHS.dev,
                publicPath: '/',
                filename: 'js/[name].js',
            },
            plugins: [
                new CopyWebpackPlugin([
                    {
                        from: 'app/static/src/favicon.png',
                        to: PATHS.dev,
                    }
                ])
            ],
            resolve: {
                extensions: ['', '.js', '.jsx'],
                // alias: {
                //     'react': 'react-lite',
                //     'react-dom': 'react-lite'
                // }
            }
        },
            parts.clean(PATHS.dev),

            parts.babelLoader(),

            parts.staticLoader(TARGET),

            parts.extractBundle({
                name: 'vendor',
                entries: ['react', 'react-dom', 'react-redux']
            }),

            parts.extractCSS(PATHS.style, TARGET)
        );
        break;
}

// Run validator in quiet mode to avoid output in stats
module.exports = validate(config, {
    quiet: true
});
