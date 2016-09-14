import Model from 'ember-data/model';
import attr from 'ember-data/attr';
import { belongsTo, hasMany } from 'ember-data/relationships';
import computed, { on, observes } from 'ember-computed-decorators';
import { getCentroid } from 'pacu/pods/components/x-layer/roi/centroid';
import { outerPointsByRatio } from 'pacu/pods/components/x-layer/roi/neuropil';

export default Model.extend({
  toast: Ember.inject.service(),
  created_at: attr('epoch'),
  active: attr('boolean', { defaultValue: false }),
  polygon: attr({ defaultValue: () => { return []; } }),
  neuropil_ratio: attr({ defaultValue: 4.0 }),
  neuropil_factor: attr({ defaultValue: 0.7 }),
  neuropil_polygon: attr({ defaultValue: () => { return []; } }),
  neuropil_enabled: attr({ defaultValue: true }),
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
  @computed('centroid', 'neuropil_ratio', 'neuropil_enabled') neuropil(
  centroid, npRatio, npEnabled) {
    if (!npEnabled) {
      Ember.run.next(this, 'set', 'neuropil_polygon', []);
      return;
    }
    if (npRatio == 2) { return } // double equal for text and float compare
    const polygon = this.get('polygon');
    const npp = outerPointsByRatio(polygon, centroid, npRatio);
    Ember.run.next(this, 'set', 'neuropil_polygon', npp);
    return npp;
  },
  saveROI() {
    this.save();
  },
  destroyROI() {
    this.destroyRecord();
  },
  refreshAll() {
    const self = this;
    if (this.get('inAction')) { return; }
    this.set('inAction', true);
    this.save().then(() => {
      this.store.createRecord('action', {
        model_name: 'ROI',
        model_id: this.id,
        action_name: 'refresh_all'
      }).save().then((action) => {
        if (action.get('status_code') === 500) {
          this.get('toast').error(action.get('status_text'));
        } else {
          this.get('workspace').then(w => w.notifyPropertyChange('dtsOverallMean'));
        }
      }).finally(() => {
        this.set('inAction', false);
      });
    });
  },
  /*@on('didCreate')*/ synchronizeDatatags() {
    const roi_id = this.get('id');
    this.store.query('datatag', { filter: { roi_id } });
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
    return this.store.query('datatag', { filter: {
      roi_id: this.get('id'),
      category: 'orientation',
      method: 'dff0',
      trial_sf: sfreq,
      trial_blank: false,
      trial_flicker: false,
    } });
  },
  @computed('workspace.cur_sfreq') sumofgaussiansBySF(sfreq) {
    return this.store.query('datatag', { filter: {
      roi_id: this.get('id'),
      category: 'fit',
      method: 'sumof',
      trial_sf: sfreq
    } });
  },
  @computed() sfTuningCurve() {
    return this.store.query('datatag', { filter: {
      roi_id: this.get('id'),
      category: 'fit',
      method: 'diffof',
    } });
  },
  @computed() anovaAll() {
    return this.store.query('datatag', { filter: {
      roi_id: this.get('id'),
      category: 'anova',
      method: 'all',
    } });
  },
  @computed() bootstrapSF() {
    return this.store.query('datatag', { filter: {
      roi_id: this.get('id'),
      category: 'bootstrap',
      method: 'sf',
    } });
  },
});
