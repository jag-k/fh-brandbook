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


// js file paths
var utilJsPath = 'src/js'; // util.js path - you may need to update this if including the framework as external node module
var componentsJsPath = 'src/js/components/*.js'; // component js files
var scriptsJsPath = 'public/js'; //folder for final scripts.js/scripts.min.js files

// css file paths
var cssFolder = 'public/css'; // folder for final style.css/style-custom-prop-fallbac.css files
var scssFilesPath = 'src/scss/**/*.scss'; // scss files to watch


gulp.task('sass', function () {
  return gulp.src(scssFilesPath)
    .pipe(sassGlob())
    .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
    .pipe(postcss([autoprefixer()]))
    .pipe(gulp.dest(cssFolder))
    .pipe(gzip())
    .pipe(gulp.dest(cssFolder));
});

gulp.task('sass-fallback', function () {
  return gulp.src(scssFilesPath)
    .pipe(sassGlob())
    .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
    .pipe(postcss([autoprefixer()]))
    .pipe(rename('style-fallback.css'))
    .pipe(postcss([cssvariables(), calc()]))
    .pipe(gulp.dest(cssFolder))
    .pipe(gzip())
    .pipe(gulp.dest(cssFolder));
});

gulp.task('scripts', function () {
  return gulp.src([utilJsPath + '/util.js', componentsJsPath])
    .pipe(concat('scripts.js'))
    .pipe(gulp.dest(scriptsJsPath))
    .pipe(rename('scripts.min.js'))
    .pipe(uglify())
    .pipe(gulp.dest(scriptsJsPath))
    .pipe(gzip())
    .pipe(gulp.dest(scriptsJsPath))
});


gulp.task('codyframe', gulp.parallel(['sass', 'sass-fallback', 'scripts']));

gulp.task('watch', gulp.series(['codyframe'], function () {
  gulp.watch(scssFilesPath, gulp.series(['sass', 'sass-fallback'])).on('change', reload);
  gulp.watch(componentsJsPath, gulp.series(['scripts'])).on('change', reload);

  gulp.watch(["db/db.sqlite3", '**/*.py']).on('change', reload);
}));


gulp.task('browser-sync', gulp.series(function () {
  browserSync({
    notify: false,
    server: '.'
  })
}));

gulp.task('default', gulp.parallel(['watch', 'browser-sync']));