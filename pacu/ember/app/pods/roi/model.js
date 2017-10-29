import Ember from 'ember';
import Model from 'ember-data/model';
import attr from 'ember-data/attr';
import { belongsTo, hasMany } from 'ember-data/relationships';
import computed, { observes } from 'ember-computed-decorators';
import { getCentroid } from 'pacu/pods/components/x-layer/roi/centroid';
import { outerPointsByRatio } from 'pacu/pods/components/x-layer/roi/neuropil';

// const SOG_INITIAL_GUESS = {
//   a1min:0  , a1max:1,
//   a2min:0  , a2max:1,
//   sigmin:15, sigmax:60,
//   offmin:0 , offmax:0.01
// }

export default Model.extend({
  didCreate() {
    this._super(...arguments);
    if(Ember.isNone(this.get('params.cell_id'))) {
      const cid = this.get('id');
      const params = this.get('params');
      this.set('params', { ...params, cell_id: cid });
      this.save();
    }
  },
  toast: Ember.inject.service(),
  created_at: attr('epoch'),
  params: attr({ defaultValue: () => ({}) }),
  // active: attr('boolean', { defaultValue: false }),
  polygon: attr({ defaultValue: () => { return []; } }),
  neuropil_ratio: attr({ defaultValue: 4.0 }),
  neuropil_factor: attr({ defaultValue: 0.7 }),
  neuropil_polygon: attr({ defaultValue: () => { return []; } }),
  neuropil_enabled: attr({ defaultValue: false }),
  sog_initial_guess: attr(),
  draw_dtoverallmean: attr({ defaultValue: false }),
  centroid: attr({ defaultValue: () => { return {x: -1, y: -1}; } }),
  workspace: belongsTo('workspace'),

  dtorientationsmeans: hasMany('dtorientationsmean'),
  dtorientationsfits: hasMany('dtorientationsfit'),
  dtanovaeachs: hasMany('dtanovaeach'),
  dtsfreqfits: hasMany('dtsfreqfit'),
  dtorientationbestprefs: hasMany('dtorientationbestpref'),
  dtanovaalls: hasMany('dtanovaall'),
  dtoverallmean: belongsTo('dtoverallmean'),
  // @computed() anova_all() {
  //   const promise = this.get('dtanovaall.promise');
  //   console.log('getting anoval all with ', promise);
  //   return DS.PromiseObject.create({ promise });
  // },
  @observes('polygon.@each.{x,y}') updateCentroid(/*polygon*/) {
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
  unfocus() {
    this.get('workspace.rois').setEach('active', false);
  },
  focus() {
    this.unfocus();
    this.set('active', true);
  },
  enableTrace() {
    this.set('draw_dtoverallmean', true);
    this.save();
  },
  disableTrace() {
    this.set('draw_dtoverallmean', false);
    this.save();
  },
  enableNeuropil() {
    this.set('neuropil_enabled', true);
    return this.save();
  },
  disableNeuropil() {
    this.set('neuropil_enabled', false);
    return this.save();
  },
  askNeuropilRatio() {
    const ratio = prompt("Please enter neuropil ratio amount",
      this.get('neuropil_ratio'));
    const fRatio = parseFloat(ratio);
    if (isNaN(fRatio)) {
      this.get('toast').warning(`Invalid value ${ratio}.`);
    } else {
      this.set('neuropil_ratio', fRatio);
      this.save();
    }
  },
  askNeuropilFactor() {
    const factor = prompt("Please enter neuropil R value",
      this.get('neuropil_factor'));
    const fFactor = parseFloat(factor);
    if (isNaN(fFactor)) {
      this.get('toast').warning(`Invalid value ${factor}.`);
    } else {
      this.set('neuropil_factor', fFactor);
      this.save();
    }
  },
  saveROI() {
    this.save();
  },
  destroyROI() {
    this.destroyRecord();
  },
  refreshAll() {
    if (this.get('inAction')) { return; }
    this.set('inAction', true);
    return this.save().then(() => {
      return this.store.createRecord('action', {
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
  synchronizeDatatags() {
    if (this.get('workspace.condition.imported')) {
      this.get('dtorientationsmeans').reload();
      this.get('dtorientationsfits').reload();
      this.get('dtanovaeachs').reload();
      this.get('dtsfreqfits').reload();
      this.get('dtorientationbestprefs').reload();
      this.get('dtanovaalls').reload();
    } else {
      this.get('workspace.dtoverallmeans').reload();
    }
  },
  clearSoGParam() {
    const dt = this.get('cur_dtorientationsfit');
    dt.set('sog_params', null);
    dt.save();
  },
  overrideSoGParam() {
    const dt = this.get('cur_dtorientationsfit');
    const p = dt.get('sog_params');
    const current = `${p.a1_min}, ${p.a1_max}, ${p.a2_min}, ${p.a2_max}, ${p.sigma_min}, ${p.sigma_max}, ${p.offset_min}, ${p.offset_max}`;
    const toggled = !p.override;
    if (toggled) {
      const params = prompt('Please type new parameters', current);
      if (Ember.isNone(params)) { return; }
      try {
        const [a1_min, a1_max, a2_min, a2_max, sigma_min, sigma_max, offset_min, offset_max] = params.split(',').map(parseFloat);
        const newParams = { a1_min, a1_max, a2_min, a2_max, sigma_min, sigma_max, offset_min, offset_max };
        for (let p in newParams) {
          if (isNaN(newParams[p])) {
            throw 'Parameter error';
          }
        }
        dt.set('sog_params', {...newParams, override: true});
        dt.save();
      } catch(e) {
        this.get('toast').warning(e);
      }
    } else {
        dt.set('sog_params', {override: false});
        dt.save();
    }
  },
  computeSoG() {
    this.get('toast').info('Recompute SoG fit...');
    if (this.get('inAction')) { return; }
    this.set('inAction', true);
    this.store.createRecord('action', {
      model_name: 'ROI',
      model_id: this.id,
      action_name: 'refresh_orientations_fit'
    }).save().then((action) => {
      if (action.get('status_code') === 500) {
        this.get('toast').error(action.get('status_text'));
      } else {
        Ember.run.next(() => {
          this.get('dtorientationsfits').reload();
        });
      }
    }).finally(() => {
      this.set('inAction', false);
    });
  },
  // adding temporal frequency (JZ)
  //@computed('workspace.cur_sfreq', 'workspace.cur_contrast', 'dtorientationsmeans') dtorientationsmeanBySF(sfreq, cont, tfreq, dts) {
  //  return dts.filterBy('trial_sf', sfreq).findBy('trial_contrast', cont);
  //},
  @computed('workspace.cur_sfreq', 'workspace.cur_contrast', 'workspace.cur_tfreq', 'dtorientationsmeans') dtorientationsmeanBySF(sfreq, cont, tfreq, dts) {
    return dts.filterBy('trial_sf', sfreq).filterBy('trial_contrast', cont).findBy('trial_tf', tfreq);
  },
  //@computed('workspace.cur_sfreq', 'workspace.cur_contrast', 'dtorientationsfits') dtorientationsfitBySF(sfreq, cont, dts) {
  //  return dts.filterBy('trial_sf', sfreq).findBy('trial_contrast', cont);
  //},
  @computed('workspace.cur_sfreq', 'workspace.cur_contrast', 'workspace.cur_tfreq', 'dtorientationsfits') dtorientationsfitBySF(sfreq, cont, tfreq, dts) {
    return dts.filterBy('trial_sf', sfreq).filterBy('trial_contrast', cont).findBy('trial_tf', tfreq);
  },
  @computed('workspace.cur_contrast', 'workspace.cur_tfreq', 'dtsfreqfits') dtsfreqfitByCT(cont, tfreq, dts) {
    return dts.filterBy('trial_contrast', cont).findBy('trial_tf', tfreq);
  },
  @computed('workspace.cur_contrast', 'workspace.cur_tfreq', 'dtorientationbestprefs') dtorientationbestprefByCT(cont, tfreq, dts) {
    return dts.filterBy('trial_contrast', cont).findBy('trial_tf', tfreq);
  },
  @computed('workspace.cur_contrast', 'workspace.cur_tfreq', 'dtanovaalls') dtanovaallByCT(cont, tfreq, dts) {
    return dts.filterBy('trial_contrast', cont).findBy('trial_tf', tfreq);
  },
  @computed('workspace.cur_contrast', 'workspace.cur_tfreq', 'dtanovaeachs') dtanovaeachsByCT(cont, tfreq, dts) {
    return dts.filterBy('trial_contrast', cont).filterBy('trial_tf', tfreq);
  },
  @computed('workspace.cur_contrast', 'workspace.cur_tfreq', 'dtorientationsfits') dtorientationsfitsByCT(cont, tfreq, dts) {
    return dts.filterBy('trial_contrast', cont).filterBy('trial_tf', tfreq);
  },
  @computed('workspace.cur_contrast', 'workspace.cur_sfreq', 'dtorientationsfits') cur_dtorientationsfit(ct, sf, dts) {
    return dts.filterBy('trial_contrast', ct).filterBy('trial_sf', sf).get('firstObject');
  },
  setCellId() {
    const params = this.get('params');
    let cid = params.cell_id || '';
    cid = prompt('Please type new cell id. Blank will delete current id.', cid);
    if (cid.trim() === '') {
      cid = null;
    }
    this.set('params', { ...params, cell_id: cid });
    this.save();
  },
  @computed('params.cell_id') reprId(cid) {
    return cid || this.get('id');
  },
  toggleUseSeed() {
    const dtbestprefs = this.get('dtorientationbestprefs');
    const dt = this.get('cur_dtorientationsfit');
    const params = dt.get('sog_params');
    const toggled = !params.use_seed;
    dt.set('sog_params', { ...params, use_seed: toggled });
    if (toggled) {
      Ember.RSVP.all([ dtbestprefs.reload(), dt.save()]).then(() => {
        this.get('toast').info(
          `A seed value will be used for A1_MAX and A2_MAX to get Sog fit.<br>
           This will take precedence over SoG override params.<br>`);
      });
    } else {
      dt.save().then(() => {
        this.get('toast').info(
          `The seed value will not be used. Sog override params will take precedence if any.`);
      });
    }
  }
});
