import Ember from 'ember';
import Model from 'ember-data/model';
import attr from 'ember-data/attr';
import { belongsTo, hasMany } from 'ember-data/relationships';

export default Model.extend({
  created_at: attr('epoch'),
  name: attr('string'),
  cur_sfreq: attr(),
  cur_contrast: attr(),
  cur_pane: attr(),
  baseline_duration: attr(),
  sog_initial_guess: attr(),
  // iopath: attr('string'),
  rois: hasMany('roi'),
  dtoverallmeans: hasMany('dtoverallmean'),
  // colormaps: hasMany('colormap'),
  condition: belongsTo('condition'),
  // ecorrs: hasMany('ephys-correlation'),
  activeROIs: Ember.computed.filterBy('rois', 'active', true),
  activeROI: Ember.computed.alias('activeROIs.firstObject'),
  savingROIs: Ember.computed.filterBy('rois', 'isSaving', true),
  loadingROIs: Ember.computed.filterBy('rois', 'isLoading', true),
  busyROIs: Ember.computed.uniq('savingROIs', 'loadingROIs'),
  roisIdle: Ember.computed.empty('busyROIs'),
  roisBusy: Ember.computed.not('roisIdle'),
  // @computed('rois.[]') dtsOverallMean(rois) {
    // const all = this.store.peekAll('datatag').filterBy('category', 'overall');
    // console.log('dtsOverallMean', all);
    // return all
  // },
  appendROI(payload) {
    payload.workspace = this;
    return this.store.createRecord('roi', payload);
  },
  importROIs(jsonstr) {
    const payloads = JSON.parse(jsonstr);
    for (let polygon of payloads) {
      this.store.createRecord('roi', {
        polygon, workspace: this
      }).save();
    }
  },
  loadedROIs: Ember.computed.filterBy('rois', 'isNew', false)
});
