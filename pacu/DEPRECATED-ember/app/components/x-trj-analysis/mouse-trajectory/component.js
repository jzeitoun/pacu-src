import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  tagName: 'svg',
  width: '100%',
  attributeBindings: ['width', 'height'],
  @computed('dimension') height(dim) {
    return dim.height;
  },
  @computed('x') cx(x=0) {
    if (Ember.isNone(this.element)) { return 0; }
    const width = this.element.width.baseVal.value;
    const ratio = width/5;
    const value = (x + 2.5) * ratio;
    return width - value;
  },
  @computed('y') cy(y=0) {
    if (Ember.isNone(this.element)) { return 0; }
    const height = this.element.height.baseVal.value;
    const ratio = height/130;
    const value = (y + 65) * ratio;
    return height - value;
  },
  @computed('activity') fill(act) {
    return `rgba(255, 0, 0, ${act}`;
  }
});
