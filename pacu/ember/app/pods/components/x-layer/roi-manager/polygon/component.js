import Ember from 'ember';
import computed from 'ember-computed-decorators';
import Routed from 'pacu/mixins/routed';
import interaction from 'pacu/utils/interaction';

export default Ember.Component.extend({
  tagName: 'polygon',
  classNames: ['focus-responder'],
  attributeBindings: ['points'],
  @computed('roi.polygon.@each.{x,y}') points(pg=[]) {
    return pg.map(p => `${p.x},${p.y}`).join(' ');
  },
  mouseDown(e) {
    const $target = this.parentView.$();
    const polygon = this.get('roi.polygon');
    return interaction.bindOnce.call(this, $target, e, polygon);
  },
  leaving() { this.get('onPolygonDoubled')(); },
  moving(origin, offset, polygon) {
    const dest = polygon.map(p => { return {
      x: p.x - (origin.x - offset.x),
      y: p.y - (origin.y - offset.y)
    };});
    this.set('roi.polygon', dest);
  },
  moved() { this.get('onPolygonUpdated')(); },
  shot() { this.get('onPolygonDeleted')(); },
  poked() { this.get('onPolygonClicked')(this); },
  click() { return false; },
  focusHit() { }
});
