import Ember from 'ember';
import Model from 'ember-data/model';
import attr from 'ember-data/attr';
import { belongsTo, hasMany } from 'ember-data/relationships';

export default Model.extend({
  created_at: attr('epoch'),
  array: attr(),
  color: attr('string'),
  category: attr('string'),
  roi: belongsTo('roi'),
  action(name, ...args) {
    // willAct
    this.actions[name].apply(this, args);
    // didAct
  },
  actions: {
    fetch() {
      window.qwe = this;
      console.log('reload');
      // this.reload();
      console.log('reloaded');
      return true;

      //  return this.get('wsx').invoke('fetch_trace', t.get('id')).gateTo(
      //    t, 'isBusy'
      //  ).then(data => {
      //    t.reload();
      //  }).catch(err => {
      //    this.toast.error(err.title, err.detail);
      //  }).finally(() => {
      //  });
    }
  }
});
