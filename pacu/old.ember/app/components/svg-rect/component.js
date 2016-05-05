import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  tagName: 'rect',
  classNameBindings: ['temp:roi-rect-temp', 'active'],
  classNames: ['roi-rect'],
  attributeBindings: ['x', 'y', 'width', 'height'],
  @computed('x1', 'x2') x(x1, x2) { return Math.min(x1, x2); },
  @computed('y1', 'y2') y(y1, y2) { return Math.min(y1, y2); },
  @computed('x1', 'x2') width(x1, x2) { return Math.abs(x2 - x1); },
  @computed('y1', 'y2') height(y1, y2) { return Math.abs(y2 - y1); },
  mouseDown({offsetX, offsetY, button}) {
    if (button === 2) { return false; } // contextMenu
    const [initialX, initialY] = [offsetX, offsetY];
    this.$().parent().one('mousemove', this.onMoveROI.bind(this, {initialX, initialY}));
    Ember.$(document).one('mouseup', this.didMoveROI.bind(this, {initialX, initialY}));
    return false;
  },
  onMoveROI({initialX, initialY}, {offsetX, offsetY}) {
    const deltaX = offsetX - initialX;
    const deltaY = offsetY - initialY;
    this.incrementProperty('x1', deltaX);
    this.incrementProperty('x2', deltaX);
    this.incrementProperty('y1', deltaY);
    this.incrementProperty('y2', deltaY);
    this.$().parent().one('mousemove', this.onMoveROI.bind(this,
          {initialX:offsetX, initialY:offsetY}));
  },
  didMoveROI({initialX, initialY}, {offsetX, offsetY}) {
    this.$().parent().off('mousemove');
    if (initialX==offsetX && initialY==offsetY) {
      this.attrs.onROIClick();
    } else {
      this.attrs.onROIMove();
    }
  },
});
