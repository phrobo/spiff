module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    useminPrepare: {
      html: 'app/index.html',
      options: {
        dest: 'dist'
      }
    },
    usemin: {
      html: 'dist/{*,*/}*.html',
      css: 'dist/**/*.css',
      options: {
        dirs: ['dist']
      }
    },
    uglify: {
      options: {
        mangle: false
      }
    },
    htmlmin: {
      dist: {
        files: {
          'dist/index.html': 'app/index.html'
        }
      }
    },
    less: {
      bootstrap: {
        files: {
          'dist/bootstrap.css': 'bower_components/bootstrap/less/bootstrap.less'
        }
      }
    },
    sass: {
      app: {
        files: {
          'dist/app.css': 'app/lib/app.scss',
        },
      }
    },
    watch: {
      index: {
        files: ["app/index.html"],
        tasks: ['build'],
      },
      templates: {
        files: ["app/**/*.html"],
        tasks: ['ngtemplates']
      },
      deps: {
        files: ['bower.js', 'bower_components/**/*'],
        tasks: ['bower', 'concat', 'uglify']
      },
      scripts: {
        files: ['js/**/*.js', 'js/*.js'],
        tasks: ['concat', 'uglify'],
      }
    },
    filerev: {
      js: {
        src: 'dist/**/*.js'
      },
      css: {
        src: 'dist/**/*.css'
      }
    },
    ngtemplates: {
      spiffApp: {
        cwd: 'app',
        src: '**/*.html',
        dest: 'dist/templates.js'
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-angular-templates');
  grunt.loadNpmTasks('grunt-contrib-htmlmin');
  grunt.loadNpmTasks('grunt-filerev');
  grunt.loadNpmTasks('grunt-usemin');

  grunt.registerTask('build', [
    'less',
    'sass',
    'useminPrepare',
    'htmlmin',
    'concat',
    'cssmin',
    'uglify',
    'ngtemplates',
    'usemin'
  ]);

  grunt.registerTask('default', ['build']);

};
