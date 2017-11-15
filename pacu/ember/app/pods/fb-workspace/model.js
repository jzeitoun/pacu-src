import DS from 'ember-data';

export default DS.Model.extend({
  name: DS.attr('string'),
  //roi_count: DS.attr('number', { defaultValue: 0 }),
  rois: DS.hasMany('fb-roi', { async: true })
});
