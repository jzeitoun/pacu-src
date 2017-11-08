import Ember from 'ember';
import JSONAPIAdapter from 'ember-data/adapters/json-api';
// import computed from 'ember-computed-decorators';

export default JSONAPIAdapter.extend({
  // namespace: 'jsonapi',
  namespace: 'api',
  host: function() {
    const hostname = location.hostname;
    const port = this.get('session.app.port') + 30000;
    return `http://${hostname}:${port}`
  }.property('session.app.port'),
  session: Ember.inject.service('session'),
  // @computed('session.jsonapi.{moduleName,sessionArgs,baseName}'
  // ) headers(m, s, b) {
  //   return {
  //     PACU_JSONAPI_MODULE_NAME: m,
  //     PACU_JSONAPI_SESSION_ARGUMENTS: s,
  //     PACU_JSONAPI_BASE_NAME: b
  //   };
  // },
  headers: function() {
    const m = this.get('session.jsonapi.moduleName');
    const s = this.get('session.jsonapi.sessionArgs');
    const b = this.get('session.jsonapi.baseName');
    return {
      PACU_JSONAPI_MODULE_NAME: m,
      PACU_JSONAPI_SESSION_ARGUMENTS: s,
      PACU_JSONAPI_BASE_NAME: b
    };
  }.property('session.jsonapi.{moduleName,sessionArgs,baseName}').volatile(),
  ajax(url, type, hash) {
    if (url.includes('rois')) { // modify model type to for communication with backend
      if (hash.data.data) {
        hash.data.data.type = 'rois';
      }
    };
    this.set('store.isfetching', true);
    return this._super(url, type, hash).finally(() => {
      this.set('store.isFetching', false);
    });
  },
  pathForType(type) {
    return Ember.String.underscore(this._super(type));
  },
  //buildURL(modelName, id, snapshot, requestType, query) {
  //  // ensures compatibility with backend
  //  var url = this._super(modelName, id, snapshot, requestType, query);
  //  if (url.includes('roi_data')) {
  //    url = url.replace('roi_data','rois');
  //  };
  //  return url
  //}
});
