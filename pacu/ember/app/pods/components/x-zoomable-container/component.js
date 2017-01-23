import Ember from 'ember';
import computed from 'ember-computed-decorators';

/*
  x-zoomable-container is designed to set its height
  automatically based on the dimension of child element.
  CSS zoom property is not standard and does not guarantee to work on
  every modern browsers. But if we try CSS transform and `scale`,
  DOM does not take place when it is overflown.

  Child element must define two attributes in the tag, width, height.
 */

const observeConfig = {
  attributes: true,
  attributeFilter: ['width', 'height']
};
const Child = Ember.Object.extend({
  @computed('height', 'width') aspectRatio(h, w) {
    return parseInt(h) / parseInt(w)
  },
  desiredHeight(width) {
    return this.get('aspectRatio') * width;
  }
});

export default Ember.Component.extend({ //TODO: Simplify
  attributeBindings: ['style'],
  @computed('child.aspectRatio') style(ratio) {
    if (Ember.isNone(this.element)) { return ''; }
    if (Ember.isNone(this.$())) { return ''; }
    const pTop = this.$().css('padding-top');
    const pBtm = this.$().css('padding-bottom');
    const containerWidth = this.$().width();
    const childWidth = this.get('child.width');
    const height = containerWidth * ratio;
    const scale = containerWidth/childWidth;
    const heightPadded = height + parseInt(pTop) + parseInt(pBtm);
    const parallelContainerStyle = Ember.String.htmlSafe(`
      height: ${heightPadded}px; overflow-y: scroll
    `);
    this.element.firstElementChild.style.transform = `scale(${scale})`;
    this.element.firstElementChild.style.transformOrigin = 'left top';
    const d = { height, pTop, pBtm, scale, heightPadded, parallelContainerStyle };
    Ember.run.scheduleOnce('afterRender', this, () => {
      this.set('dimension', d);
    });
    const style = Ember.String.htmlSafe(
      `height: calc(${d.height}px + ${d.pTop} + ${d.pBtm});`
    );
    this.set('containerStyle', style);
    return style;
  },
  @computed() child() { return Child.create(); },
  @computed() observer() {
    return new MutationObserver(mutations => {
      mutations.forEach(mutation => {
        const key = mutation.attributeName;
        const val = mutation.target.getAttribute(mutation.attributeName);
        this.get('child').set(key, val);
      });
    });
  },
  initialize: function() {
    window.ASD = this;
    const child = this.element.firstElementChild;
    if (Ember.isNone(child)) { return; }
    $(window).on(`resize.${this.elementId}`, e => {
      this.notifyPropertyChange('style');
    });
    this.get('observer').observe(child, observeConfig);
  }.on('didInsertElement'),
  dnitialize: function() {
    $(window).off(`resize.${this.elementId}`);
    this.get('observer').disconnect();
  }.on('willDesroyElement')
});
