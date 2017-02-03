import Model from 'ember-data/model';
import attr from 'ember-data/attr';
import { belongsTo } from 'ember-data/relationships';
import download from 'pacu/utils/download';

/* global toastr */

export default Model.extend({
  traces: attr({defaultValue: () => [[]]}),
  meantrace: attr({defaultValue: () => []}),
  rmeantrace: attr({defaultValue: () => []}),
  roi_ids: attr({defaultValue: () => []}),
  window: attr('number', {defaultValue: 100}),
  random_count: attr('number', {defaultValue: 100}),
  note: attr('string'),
  workspace: belongsTo('workspace'),
  action(name, ...args) {
    if (this.get('inAction')) { return; }
    this.set('inAction', true);
    const prom = this.actions[name].apply(this, args);
    if (prom) {
      prom.finally(() => {
        this.set('inAction', false);
      });
    } else {
      this.set('inAction', false);
    }
  },
  actions: {
    save() {
      this.save().then(() => {
        toastr.info(`Condition updated succefully.
          Click "Compute" to update plot.`)
      });
    },
    export() {
      return this.store.createRecord('action', {
        model_name: 'EphysCorrelation',
        model_id: this.id,
        action_name: 'export_zip_for_download',
      }).save().then((data) => {
        const meta = data.get('meta');
        download.fromBase64(meta.data, meta.filename, meta.mimetype);
      });
    },
    compute() {
      return this.store.createRecord('action', {
        model_name: 'EphysCorrelation',
        model_id: this.id,
        action_name: 'refresh',
      }).save().then((/*data*/) => {
        this.reload();
      });
    }
  }
});
