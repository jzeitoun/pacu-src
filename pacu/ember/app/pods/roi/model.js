import Model from 'ember-data/model';
import attr from 'ember-data/attr';
import { belongsTo, hasMany } from 'ember-data/relationships';
import computed, { on, observes } from 'ember-computed-decorators';
import { getCentroid } from 'pacu/pods/components/x-layer/roi/centroid';

export default Model.extend({
  created_at: attr('epoch'),
  active: attr('boolean', { defaultValue: false }),
  polygon: attr({ defaultValue: () => { return []; } }),
  centroid: attr({ defaultValue: () => { return {x: -1, y: -1}; } }),
  workspace: belongsTo('workspace'),
  datatags: hasMany('datatag'),
  @observes('polygon.@each.{x,y}') updateCentroid(polygon) {
    const old = this.get('centroid');
    const nue = getCentroid(this.get('polygon'));
    const isSame = old.x === nue.x && old.y === nue.y;
    const incomingNaN = isNaN(nue.x) || isNaN(nue.y);
    if (!incomingNaN && !isSame) { this.set('centroid', nue); }
  },
  refreshAll() {
    if (this.get('inAction')) { return; }
    this.set('inAction', true);
    this.store.createRecord('action', {
      model_name: 'ROI',
      model_id: this.id,
      action_name: 'refresh_all'
    }).save().then((action) => {
      const filter = { roi_id: this.id };
      this.store.query('datatag', { filter });
    }).finally(() => {
      this.set('inAction', false);
    });
  },
  @on('didCreate') populateDatatags() {
    const roi = this;
    this.store.createRecord('datatag', {
      roi, category: 'overall', method: 'mean'
    }).save();
    const cond = this.store.peekRecord('condition', 1);
    if (cond) {
      const trials = this.store.peekAll('trial');
      for (let trial of trials.toArray()) {
        this.store.createRecord('datatag', {
          trial, roi, category: 'orientations', method: 'mean'
        }).save();
      }
    }
  },
  @on('didDelete') unpopulateDatatags() {
    const id = this.get('id');
    this.store.peekAll('datatag').map(dt => {
      if (id == dt.get('roi_id')) { // comparing int with string
        this.store.unloadRecord(dt);
      }
    });
  },
  @computed('workspace.cur_sfreq') orientationsBySF(sfreq) {
    const dts = this.get('datatags');
    return dts.filterBy('trial.sf', sfreq).sortBy('trial.ori');
  }
});
