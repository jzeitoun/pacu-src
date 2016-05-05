import DS from 'ember-data';

export default DS.Model.extend({
  title: DS.attr('string'),
  type: DS.attr('number'),
  user: DS.attr('string', {defaultValue: 'Dario'}),
  desc: DS.attr('string'),
  imagesrc: DS.attr('string'),
  conditionid: DS.attr('number'),
  createdat: DS.attr('date'),
  // type: DS.attr('string'),
  // index: DS.attr('number', {defaultValue: 0}),
});
