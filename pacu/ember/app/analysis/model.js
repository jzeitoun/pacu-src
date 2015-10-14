import DS from 'ember-data';

export default DS.Model.extend({
  title: DS.attr('string'),
  src: DS.attr('string'),
  host: DS.attr('string'),
  desc: DS.attr('string'),
  type: DS.attr('string'),
  user: DS.attr('string'),
  index: DS.attr('number', {defaultValue: 0}),
});
