import Model from 'ember-data/model';
import attr from 'ember-data/attr';
import { belongsTo, hasMany } from 'ember-data/relationships';
import computed  from 'ember-computed-decorators';

export default Model.extend({
  created_at: attr('epoch'),
  name: attr('string'),
  rois: hasMany('roi'),
  @computed('rois') traces(rois, entry=[]) {
    rois.then(rs => {
      const ps = rs.map(roi => roi.get('traces').then(ts => ts.map(t => t)));
      Ember.RSVP.all(ps).then(nested => {
        entry.pushObjects([].concat(...nested));
      });
    });
    return entry;
  }
});
