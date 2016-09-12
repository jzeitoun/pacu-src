import Ember from 'ember';
import Model from 'ember-data/model';
import attr from 'ember-data/attr';
import { belongsTo, hasMany } from 'ember-data/relationships';

export default Model.extend({
  created_at: attr('epoch'),
  updated_at: attr('epoch'),
  value: attr(),
  category: attr('string'),
  method: attr('string'),
  etext: attr('string'),
  etype: attr('string'),
  trial_on_time: attr(),
  trial_off_time: attr(),
  trial_ori: attr(),
  trial_sf: attr(),
  trial_tf: attr(),
  trial_sequence: attr(),
  trial_order: attr(),
  trial_ran: attr(),
  trial_flicker: attr(),
  trial_blank: attr(),
  roi: belongsTo('roi'),
  roi_id: attr(),
  trial: belongsTo('trial'),
  trial_id: attr(),
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
        model_name: 'Datatag',
        model_id: this.id,
        action_name: 'refresh',
      }).save().then((data) => {
        this.reload();
      });
    }
  }
});
