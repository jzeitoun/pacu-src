var EmberApp = require('ember-cli/lib/broccoli/ember-app');

module.exports = function(defaults) {
  var app = new EmberApp(defaults, {
    babel: {
      optional: ['es7.decorators', 'es7.comprehensions'],
    }
  });
  app.import('bower_components/sweetalert/dist/sweetalert.min.js');
  app.import('bower_components/sweetalert/dist/sweetalert.css');
  return app.toTree();
};
