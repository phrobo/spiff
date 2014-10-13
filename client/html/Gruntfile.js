module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    uglify: {
      options: {
        mangle: false,
        beautify: true,
        sourceMap: true
      },
      deps: {
        files: {
          'app/lib/deps.js': [
            'bower_components/jquery/jquery.js',
            'bower_components/bootstrap/docs/assets/js/bootstrap.js',
            'bower_components/jquery-ui/ui/jquery-ui.js',
            'bower_components/jquery-qrcode/jquery.qrcode.min.js',
            'bower_components/underscore/underscore.js',
            'bower_components/angular/angular.js',
            'bower_components/angular-route/angular-route.js',
            'bower_components/restangular/dist/restangular.js',
            'bower_components/angular-ui-bootstrap-bower/ui-bootstrap.js',
            'bower_components/angular-ui-bootstrap-bower/ui-bootstrap-tpls.js',
            'bower_components/angular-ui-router/release/angular-ui-router.js',
            'bower_components/angular-gravatar/build/md5.js',
            'bower_components/angular-gravatar/build/angular-gravatar.js',
            'bower_components/showdown/src/showdown.js',
            'bower_components/angular-sanitize/angular-sanitize.js',
            'bower_components/angular-markdown-directive/markdown.js'
          ]
        }
      },
      app: {
        files: {
          'app/lib/app.js': [
            'js/**/*.js'
          ]
        }
      }
    },
    less: {
      bootstrap: {
        files: {
          'app/lib/bootstrap.css': 'bower_components/bootstrap/less/bootstrap.less'
        }
      }
    },
    sass: {
      app: {
        files: {
          'app/lib/app.css': 'app/lib/app.scss',
        },
      }
    },
    watch: {
      bower: {
        files: ['bower.js'],
        tasks: ['bower']
      },
      deps: {
        files: ["bower_components/**/*"],
        tasks: ['bower', 'uglify:deps']
      },
      scripts: {
        files: ['js/**/*.js', 'js/*.js'],
        tasks: ['uglify:app'],
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.registerTask('default', ['less', 'sass', 'uglify:deps', 'uglify:app']);

};
