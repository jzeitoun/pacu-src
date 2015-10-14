import Ember from 'ember';
import computed from 'ember-computed-decorators';
import d3 from 'd3';

export default Ember.Component.extend({
  tagName: 'svg',
  attributeBindings: ['width', 'height'],
  width: '400px',
  height: '300px',
  interpolate: 'linear',
  @computed('interpolate') dfunc(ip) {
    return d3.svg.line().x((d, i) => i).y(d => d).interpolate(ip);
  },
  @computed('src', 'dfunc') d(data, dfunc) {
    return dfunc(data);
  }
});
