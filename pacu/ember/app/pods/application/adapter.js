import JSONAPIAdapter from 'ember-data/adapters/json-api';
import computed from 'ember-computed-decorators';

export default JSONAPIAdapter.extend({
  namespace: 'jsonapi',
  session: Ember.inject.service('session'),
  @computed('session.jsonapi.{moduleName,sessionArgs,baseName'
  ) headers(m, s, b) {
    return {
      PACU_JSONAPI_MODULE_NAME: m,
      PACU_JSONAPI_SESSION_ARGUMENTS: s,
      PACU_JSONAPI_BASE_NAME: b
    };
  }
});