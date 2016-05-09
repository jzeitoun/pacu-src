import DS from 'ember-data';
import computed from 'ember-computed-decorators';

export default DS.Model.extend({
  name: DS.attr('string'),
  numberoftrials: DS.attr('number'),
  hasimported: DS.attr('boolean'),
  @computed('numberoftrials') ntrials(n) {
    return `${n} trial(s)`
  },
});
