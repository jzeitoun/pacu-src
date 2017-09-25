import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Controller.extend({
  queryParams: ['dsMonthPrev', 'dsGlob', 'dsDays', 'filter'],
  dsDays: 3650,
  dsGlob: '*',
  dsHops: '',
  filter: '',
  filteredModel: Ember.computed.filterBy('model.ios', 'info.iopath', 'filter'),
  @computed('model.ios', 'filter') filteredIOs(ios, filter) {
    return ios.filter(io => io.info.iopath.includes(filter))
  }
});
