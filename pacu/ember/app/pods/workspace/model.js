import Model from 'ember-data/model';
import attr from 'ember-data/attr';
import { belongsTo, hasMany } from 'ember-data/relationships';
import computed  from 'ember-computed-decorators';

export default Model.extend({
  created_at: attr('epoch'),
  name: attr('string'),
  rois: hasMany('roi'),
  traces: function() {
    const entry = [];
    const interim = [];
    this.get('rois').then(rs => {
      const proms = rs.map(roi => {
        return roi.get('traces').then(ts => {
          ts.forEach(t => {
            interim.pushObject(t);
          });
        });
      });
      Ember.RSVP.all(proms).then(() => {
        entry.pushObjects(interim);
      });
    });
    return entry;
  }.property('rois')
});
