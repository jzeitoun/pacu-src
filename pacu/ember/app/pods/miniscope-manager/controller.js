import Ember from 'ember';

export default Ember.Controller.extend({
  queryParams: ['dsMonthPrev', 'dsGlob', 'dsDays'],
  dsDays: 3650,
  dsGlob: '*',
  dsHops: ''
});
