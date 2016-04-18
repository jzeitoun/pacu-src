import Ember from 'ember';

export default Ember.Component.extend({
  tagName: 'circle',
  attributeBindings: ['cx', 'cy'],
  mouseDown({offsetX, offsetY, altKey}) {
    const [originX, originY] = [offsetX, offsetY];
    Ember.$(this.parentView.element).on(
      'mousemove.circle', ({offsetX, offsetY}) => {
      if (this.attrs.onCircleMoving(offsetX, offsetY, altKey)) {
        this.set('cx', offsetX);
        this.set('cy', offsetY);
      }
    });
    Ember.$(document).one('mouseup.circle', ({offsetX, offsetY}) => {
      Ember.$(this.parentView.element).off('mousemove.circle');
      if (originX === offsetX && originY === offsetY) {
        // this.attrs.onCircleClicked(this, altKey);
      } else { // point was moved
        // this.attrs.onCircleMoved(this, altKey);
      }
    });
  }
});
