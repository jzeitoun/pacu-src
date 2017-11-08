import FirebaseAdapter from 'emberfire/adapters/firebase';

export default FirebaseAdapter.extend({
  /* redirect path to workspaces instead of fbWorkspaces */
  pathForType(modelName) {
    modelName = modelName.split('-')[1];
    var camelized = Ember.String.camelize(modelName);
    return Ember.String.pluralize(camelized);
  },
});
