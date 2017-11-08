import FirebaseAdapter from 'emberfire/adapters/firebase';

export default FirebaseAdapter.extend({
  pathForType(modelName) {
    if (modelName.includes('workspace')) {
      modelName = modelName.split('-')[1];
    };
    var camelized = Ember.String.camelize(modelName);
    return Ember.String.pluralize(camelized);
  },
});
