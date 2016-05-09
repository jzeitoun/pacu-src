import Ember from 'ember';

/*global swal*/

export default Ember.Route.extend({
  actions: {
    create(model) {
      const self = this;
      const names = 'mapper metadata'.split(' ');
      const payload = names.map(name => {
        const amodel = model[`${name}Specs`][model[`${name}SpecIndex`]];
        return {
          type: name,
          name: amodel.name,
          keys: amodel.fields.mapBy('name'),
          vals: amodel.fields.mapBy('value')
        };
      });
      Ember.$.post('api/payload/analysis_v1', {payload: JSON.stringify(payload)
      }).then(function(data) {
        swal('OK!', 'Successfully created a session.', 'success');
        self.send('refreshModel');
        self.replaceWith('analysis.session', data.id);
      }, function(reason) {
        swal('Opps...', reason.responseText, 'error');
      });
    }
  },
  model() {
    const pmodel = this.modelFor('analysis');
    return {
      model: {},
      mapperSpecs: pmodel.mapperSpecs,
      mapperSpecIndex: pmodel.mapperSpecIndex,
      metadataSpecs: pmodel.metadataSpecs,
      metadataSpecIndex: pmodel.metadataSpecIndex
    };
  }
});
