import Ember from 'ember';

export default Ember.Route.extend({
  actions: {
    didTransition() {
      this.controllerFor('application').set(
        'current-feature', 'Image Stack Analyzer');
    },
    refreshModel() {
      this.refresh();
    }
  },
  model() {
    return {
      sbxSrc: '/api/fs/sbx',
      sbxValue: ''
    }
    // const vstim = 'pacu.core.service.analysis.';
    // const promise = this.backend.getServiceSpec;
    // return Ember.RSVP.hash({
    //   entities: Ember.$.getJSON('api/query/analysis_v1'),
    //   mapperSpecs: promise(vstim + 'mapper'),
    //   metadataSpecs: promise(vstim + 'metadata'),
    // });
  },
  afterModel(model) {
    // model.mapperSpecIndex = 0;
    // model.metadataSpecIndex = 0;
  }
});
