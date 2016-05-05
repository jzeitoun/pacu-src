import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  attributeBindings: ['style'],
  initialize: function() {
    // window.aaa = this;
    // this.$().dropdown();
    // this.$('input.search').on('blur', () => {
    //   console.log('blurred');
    // });
    // const layerElement = this.get('layer.element');
    // this.$(layerElement).on('x-layer-context-menu', (e, roi) => {
    //   console.log('catch context-menu!');
    //   const {x, y} = roi.get('centroid');
    //   this.setProperties({x, y, roi: roi});
    //   this.$('input.search').click();
    //   this.$('input.search').focus();
    // });
  }.on('didInsertElement'),
  dnitialize: function() {
  }.on('willDestroyElement'),
  @computed('roi') display(roi) {
    return roi ? 'inherit' : 'hidden';
  },
  @computed('display', 'x', 'y') style(v, x=0, y=0) {
    console.log('compute style', v, x, y);
    return Ember.String.htmlSafe(
      `left: ${x}px; top: ${y}px; width: 1px; height: 1px; visibility: ${v}`);
  },
  classNames: 'ui selection dropdown', // took off "search" class.
});
