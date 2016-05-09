import Model from 'ember-data/model';
import attr from 'ember-data/attr';
import { belongsTo, hasMany } from 'ember-data/relationships';
import computed  from 'ember-computed-decorators';

export default Model.extend({
  created_at: attr('epoch'),
  name: attr('string'),
  rois: hasMany('roi'),
  ts: function() {
    const entry = [];
    this.get('rois').then(rs => {
      rs.forEach(roi => {
        console.log('roi id', roi.get('id'));
      });
      // rs.getEach('traces').forEach(t => {
      //   t.then(trace => {
      //     console.log(trace);
      //     entry.pushObject(trace);
      //   });
      // });
    });
    return entry;
//     console.log('getting ts');
//     return this.get('rois').then(rs => {
//       return Ember.RSVP.all(rs.map((roi) => {
//         const ts = roi.get('traces');
//         console.log(ts);
//         return ts;
//       }), 'rsmap').then(traces => {
//         return traces;
//       });
//     });
// //     this.get('rois').then(rs => {
//       const prom = Ember.RSVP.all(rs.map((roi) => {
//         const ts = roi.get('traces');
//         console.log(ts);
//         return ts;
//       }), 'rsmap');
//       this.set('fetchedRS', prom);
//       // console.log('total prom', prom);
//     });
  }.property('rois.@each.traces')
});
