import Ember from 'ember';
import Routed from 'pacu/mixins/routed';
import computed from 'ember-computed-decorators';
import interaction from 'pacu/utils/interaction';

export default Ember.Component.extend(Routed, {
  tagName: 'circle',
  attributeBindings: ['cx', 'cy', 'style'],
  cx: Ember.computed.alias('point.x'),
  cy: Ember.computed.alias('point.y'),
  @computed('color') style(c) {
    return Ember.String.htmlSafe(`fill: ${c};`);
  },
  mouseDown(e) {
    if (!this.onCircleUpdated) { return true; }
    const $target = this.parentView.$();
    const polygon = this.get('roi.polygon');
    const point = this.get('point');
    return interaction.bindOnce.call(this, $target, e, polygon, point);
  },
  update() {
    const roi = this.get('roi');
    const polygon = this.get('roi.polygon');
    roi.set('polygon', polygon.copy());
    this.get('onCircleUpdated')();
  },
  leaving(origin, offset, polygon, point) {
    polygon.insertAt(polygon.indexOf(point), Ember.copy(point));
  },
  moving(origin, offset, polygon, point) {
    Ember.setProperties(point, {x: offset.x, y: offset.y});
  },
  moved() { this.update(); },
  shot(origin, offset, polygon, point) {
    if (polygon.length <= 3) {
        this.routeAction('toastWarning', 'Hey.', 'Cannot leave points less than 2.');
    } else {
      polygon.removeObject(point);
      this.update();
    }
  },
});
