var gulp = require('gulp');
var fs = require('fs');
var sass = require('gulp-sass');
var sassGlob = require('gulp-sass-glob');
var postcss = require('gulp-postcss');
var autoprefixer = require('autoprefixer');
var cssvariables = require('postcss-css-variables');
var calc = require('postcss-calc');
var concat = require('gulp-concat');
var rename = require('gulp-rename');
var uglify = require('gulp-uglify');
var gzip = require('gulp-gzip');

var browserSync = require('browser-sync');
var reload = browserSync.reload;

// var through = require('through2');
var svg = require("./svg_sprites")

// js file paths
var utilJsPath = 'src/js'; // util.js path - you may need to update this if including the framework as external node module
var componentsJsPath = 'src/js/components/*.js'; // component js files
var scriptsJsPath = 'public/js'; //folder for final scripts.js/scripts.min.js files

// css file paths
var cssFolder = 'public/css'; // folder for final style.css/style-custom-prop-fallbac.css files
var scssFilesPath = 'src/scss/**/*.scss'; // scss files to watch
var htmlFilesPath = 'view/**/*.html'; // scss files to watch


gulp.task('sass', function () {
  return gulp.src(scssFilesPath)
    .pipe(sassGlob())
    .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
    .pipe(postcss([autoprefixer()]))
    .pipe(gulp.dest(cssFolder))
    .pipe(rename('style-fallback.css'))
    .pipe(postcss([cssvariables(), calc()]))
    .pipe(gzip())
    .pipe(gulp.dest(cssFolder));
});

gulp.task('scripts', function () {
  return gulp.src([utilJsPath + '/util.js', componentsJsPath])
    .pipe(concat('scripts.js'))
    .pipe(gulp.dest(scriptsJsPath))
    .pipe(rename('scripts.min.js'))
    .pipe(uglify())
    // .pipe(gzip())
    .pipe(gulp.dest(scriptsJsPath))
});

gulp.task('svg', function () {
  var icons = {
    "wrench": true,
    "newspaper": true,
    "file-alt": true,
  }
  return gulp.src(htmlFilesPath)
    .pipe(svg.count(icons))
    .on('end', svg.build('src/sprites/icons.svg', 'public/sprites/icons.svg', icons));
});

gulp.task('codyframe', gulp.parallel(['sass', 'scripts', 'svg']));

gulp.task('watch', gulp.series(['codyframe'], function () {
  gulp.watch(scssFilesPath, gulp.series(['sass'])).on('change', reload);
  gulp.watch(componentsJsPath, gulp.series(['scripts'])).on('change', reload);

  gulp.watch(htmlFilesPath, gulp.series(['svg'])).on('change', reload);

  gulp.watch(["db/db.sqlite3", '**/*.py']).on('change', reload);
}));


gulp.task('browser-sync', gulp.series(function () {
  browserSync({
    notify: false,
    proxy: "127.0.0.1:8080",
  })
}));

gulp.task('default', gulp.parallel(['watch', 'browser-sync']));