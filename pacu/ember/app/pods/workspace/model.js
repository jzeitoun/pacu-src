import Model from 'ember-data/model';
import attr from 'ember-data/attr';
import { belongsTo, hasMany } from 'ember-data/relationships';
import computed  from 'ember-computed-decorators';

export default Model.extend({
  created_at: attr('epoch'),
  name: attr('string'),
  iopath: attr('string'),
  cur_sfreq: attr(),
  rois: hasMany('roi'),
  colormaps: hasMany('colormap'),
  condition: belongsTo('condition'),
  ecorrs: hasMany('ephys-correlation'),
  // @computed('rois') traces(rois, entry=[]) {
  //   rois.then(rs => {
  //     const ps = rs.map(roi => roi.get('traces').then(ts => ts.map(t => t)));
  //     Ember.RSVP.all(ps).then(nested => {
  //       entry.pushObjects([].concat(...nested));
  //     });
  //   });
  //   return entry;
  // },
  // @computed('rois') meanTraces(rois, entry=[]) {
  //   rois.then(rs => {
  //     const ps = rs.map(roi => roi.get('traces')
  //       .then(ts => ts.filterBy('category', 'mean')));
  //     Ember.RSVP.all(ps).then(nested => {
  //       entry.pushObjects([].concat(...nested));
  //     });
  //   });
  //   return entry;
  // },
  // @computed('rois') oriTraces(rois, entry=[]) {
  //   rois.then(rs => {
  //     const ps = rs.map(roi => roi.get('traces')
  //       .then(ts => ts.filterBy('category', 'orientation')));
  //     Ember.RSVP.all(ps).then(nested => {
  //       entry.pushObjects([].concat(...nested));
  //     });
  //   });
  //   return entry;
  // }
});
