import Ember from 'ember';
import computed from 'ember-computed-decorators';
import mat from 'pacu/utils/matrix';

export function outerPointsByRatio(polygon, centroid, m, n=2) {
  const pointXs = polygon.getEach('x').map(x => (x*m - n*centroid.x) / (m - n));
  const pointYs = polygon.getEach('y').map(y => (y*m - n*centroid.y) / (m - n));
  return new Array(polygon.length).fill().map((_, index) => { return {
      x: parseInt(pointXs[index]),
      y: parseInt(pointYs[index])
    };
  });
}

export default Ember.Mixin.create({
  npDistRatio: 4,
  npEnabled: true,
  npDisabled: Ember.computed.not('npEnabled'),
  @computed('centroid', 'npDistRatio', 'npEnabled') neuropil: {
    get(centroid, ratio, enabled) {
      if (enabled) {
        const polygon = this.get('polygon');
        return outerPointsByRatio(polygon, centroid, ratio);
      } else {
        return [];
      }
    },
    set(value, centroid, ratio, enabled) { return value; }
  },
});
