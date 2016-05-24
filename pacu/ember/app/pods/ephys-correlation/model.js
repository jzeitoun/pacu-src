import Model from 'ember-data/model';
import attr from 'ember-data/attr';
import { belongsTo, hasMany } from 'ember-data/relationships';

export default Model.extend({
  traces: attr({defaultValue: () => [[]]}),
  meantrace: attr({defaultValue: () => []}),
  rmeantrace: attr({defaultValue: () => []}),
  roi_ids: attr({defaultValue: () => []}),
  window: attr('number', {defaultValue: 100}),
  note: attr('string'),
  workspace: belongsTo('workspace'),
  action(name, ...args) {
    if (this.get('inAction')) { return; }
    this.set('inAction', true);
    const prom = this.actions[name].apply(this, args).finally(() => {
      this.set('inAction', false);
    });
  },
  actions: {
    fetch() {
      return this.store.createRecord('action', {
        model_name: 'EphysCorrelation',
        model_id: this.id,
        action_name: 'refresh',
      }).save().then((data) => {
        this.reload();
      });
    }
  }
});
