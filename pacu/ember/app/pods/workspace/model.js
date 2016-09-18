import Model from 'ember-data/model';
import attr from 'ember-data/attr';
import { belongsTo, hasMany } from 'ember-data/relationships';
import computed  from 'ember-computed-decorators';

export default Model.extend({
  created_at: attr('epoch'),
  name: attr('string'),
  cur_sfreq: attr(),
  baseline_duration: attr(),
  // iopath: attr('string'),
  rois: hasMany('roi'),
  // colormaps: hasMany('colormap'),
  condition: belongsTo('condition'),
  // ecorrs: hasMany('ephys-correlation'),
  activeROIs: Ember.computed.filterBy('rois', 'active', true),
  activeROIBinding: 'activeROIs.firstObject',
  savingROIs: Ember.computed.filterBy('rois', 'isSaving', true),
  loadingROIs: Ember.computed.filterBy('rois', 'isLoading', true),
  busyROIs: Ember.computed.uniq('savingROIs', 'loadingROIs'),
  roisIdle: Ember.computed.empty('busyROIs'),
  roisBusy: Ember.computed.not('roisIdle'),
  // @computed('rois.[]') dtsOverallMean(rois) {
  //   return this.store.query('datatag', { filter: { category: 'overalll' } });
  // },
  appendROI(payload) {
    payload.workspace = this;
    return this.store.createRecord('roi', payload);
  }
});
