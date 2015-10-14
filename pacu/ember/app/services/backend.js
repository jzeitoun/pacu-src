import Ember from 'ember';

export default Ember.Service.extend({
  getServiceSpec(specName) {
    return new Ember.RSVP.Promise((resolve/*, reject*/) => {
      const url = `api/specs/${specName}`;
      Ember.$.ajax(url, {method: 'HEAD'}).done((data, text, resp) => {
        const specNames = resp.getResponseHeader('X-Pacu-Specs').split(',');
        const specMeta = specNames.map(specName => {
          return JSON.parse(resp.getResponseHeader(`X-Pacu-Spec-${specName}`));
        });
        resolve(specMeta);
      });
    });
  }
});

