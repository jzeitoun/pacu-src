import Ember from 'ember';
import computed from 'ember-computed-decorators';
import mat from 'pacu/utils/matrix';

export function getCentroid(polygon) {
  const closed = polygon.concat(polygon.get('firstObject'));
  const pointXs = closed.getEach('x');
  const pointYs = closed.getEach('y');
  const area1 = mat.mul(pointXs.slice(0, -1), pointYs.slice(1));
  const area2 = mat.mul(pointYs.slice(0, -1), pointXs.slice(1));
  const areaDiff = mat.sub(area1, area2);
  const area = mat.sum(areaDiff) / 2;
  const cx = mat.add(pointXs.slice(0, -1), pointXs.slice(1));
  const cy = mat.add(pointYs.slice(0, -1), pointYs.slice(1));
  const x = mat.sum(mat.mul(cx, areaDiff)) / (6 * area);
  const y = mat.sum(mat.mul(cy, areaDiff)) / (6 * area);
  return { x:parseInt(x), y:parseInt(y) };
}
export default Ember.Mixin.create({
  @computed('polygon.@each.{x,y}') centroid: {
    get(polygon) {
      if (Ember.isNone(polygon)) { return; }
      return getCentroid(polygon);
    },
    set(value, polygon) {}
  }
});
