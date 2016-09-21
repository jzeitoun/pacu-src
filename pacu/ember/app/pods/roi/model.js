import DS from 'ember-data';
import Model from 'ember-data/model';
import attr from 'ember-data/attr';
import { belongsTo, hasMany } from 'ember-data/relationships';
import computed, { on, observes } from 'ember-computed-decorators';
import { getCentroid } from 'pacu/pods/components/x-layer/roi/centroid';
import { outerPointsByRatio } from 'pacu/pods/components/x-layer/roi/neuropil';

export default Model.extend({
  toast: Ember.inject.service(),
  created_at: attr('epoch'),
  // active: attr('boolean', { defaultValue: false }),
  polygon: attr({ defaultValue: () => { return []; } }),
  neuropil_ratio: attr({ defaultValue: 4.0 }),
  neuropil_factor: attr({ defaultValue: 0.7 }),
  neuropil_polygon: attr({ defaultValue: () => { return []; } }),
  neuropil_enabled: attr({ defaultValue: true }),
  draw_dtoverallmean: attr({ defaultValue: true }),
  centroid: attr({ defaultValue: () => { return {x: -1, y: -1}; } }),
  workspace: belongsTo('workspace'),

  dtorientationsmeans: hasMany('dtorientationsmean'),
  dtorientationsfits: hasMany('dtorientationsfit'),
  dtsfreqfit: belongsTo('dtsfreqfit'),
  dtorientationbestpref: belongsTo('dtorientationbestpref'),
  dtanovaall: belongsTo('dtanovaall'),
  dtoverallmean: belongsTo('dtoverallmean'),
  // @computed() anova_all() {
  //   const promise = this.get('dtanovaall.promise');
  //   console.log('getting anoval all with ', promise);
  //   return DS.PromiseObject.create({ promise });
  // },
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
          Ember.run.next(this, 'synchronizeDatatags');
        }
      }).finally(() => {
        this.set('inAction', false);
      });
    });
  },
  // on('didCreate')
  synchronizeDatatags() {
    // console.log('SYNC RELATIONSHIP');
    this.get('workspace.dtoverallmeans').reload();
    this.get('dtorientationsmeans').reload();
    this.get('dtorientationsfits').reload();
    this.store.findRecord('dtsfreqfit', this.get('dtsfreqfit.id'));
    this.store.findRecord('dtorientationbestpref', this.get('dtorientationbestpref.id'));
    this.store.findRecord('dtanovaall', this.get('dtanovaall.id'));
  },
  @computed('workspace.cur_sfreq', 'dtorientationsmeans') dtorientationsmeanBySF(sfreq, dts) {
    return dts.findBy('trial_sf', sfreq);
  },
  @computed('workspace.cur_sfreq', 'dtorientationsfits') dtorientationsfitBySF(sfreq, dts) {
    return dts.findBy('trial_sf', sfreq);
  },
  // @computed('dtsfreqfit.value.plot') sfreqfitplot(plot) {
  //   console.log('UP', plot);
  //   return plot;
  // },
  // @computed('workspace.cur_sfreq') sumofgaussiansBySF(sfreq) {
  //   return this.store.query('datatag', { filter: {
  //     roi_id: this.get('id'),
  //     category: 'fit',
  //     method: 'sumof',
  //     trial_sf: sfreq
  //   } });
  // },
  // @computed() sfTuningCurve() {
  //   return this.store.query('datatag', { filter: {
  //     roi_id: this.get('id'),
  //     category: 'fit',
  //     method: 'diffof',
  //   } });
  // },
  // @computed() anovaAll() {
  //   return this.store.query('datatag', { filter: {
  //     roi_id: this.get('id'),
  //     category: 'anova',
  //     method: 'all',
  //   } });
  // },
  // @computed() bootstrapSF() {
  //   return this.store.query('datatag', { filter: {
  //     roi_id: this.get('id'),
  //     category: 'bootstrap',
  //     method: 'sf',
  //   } });
  // },
});
