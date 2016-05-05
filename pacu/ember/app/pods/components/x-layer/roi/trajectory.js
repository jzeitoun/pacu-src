import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Mixin.create({
  index: 0,
  @computed() vectors() {
    return [
    ];
  },
  @computed('centroid', 'vectors.[]') trajectories(cnt, vecs) {
    const arr = [];
    let curr = cnt;
    for (let next of vecs) {
      arr.pushObject({
        x1: curr.x, y1: curr.y,
        x2: next.x, y2: next.y
      });
      curr = next;
    }
    return arr
  },
  @computed('centroid', 'vectors.[]', 'index') dCnt(cntInit, vecs, index) {
    if (Ember.isEmpty(vecs)) { return [null, null, null]; }
    let curr = {index:0, x:cntInit.x, y:cntInit.y};
    let next;
    for (next of vecs) {
      if ((curr.index <= index) && (index < next.index)) {
        return [curr, next, {x:cntInit.x - curr.x, y:cntInit.y - curr.y}];
      } else {
        curr = next;
      }
    }
    return [curr, next, {x:cntInit.x - curr.x, y:cntInit.y - curr.y}];
  },
  @computed('polygon', 'dCnt', 'index') dPolygon(pg, [curr, next, delta], index) {
    // console.log('computing dPoly!', curr, next, delta);
    if (Ember.isNone(pg) || Ember.isNone(curr) || Ember.isNone(next)) {
      return pg;
    }
    const ratio = Math.min(
      (parseInt(index)-curr.index)/(next.index-curr.index), 1
    ) || 0;
    const x = (next.x-curr.x)*ratio;
    const y = (next.y-curr.y)*ratio;
    return pg.map(point => {
      return {
        x:point.x + x - delta.x,
        y:point.y + y - delta.y
      };
    });
  },
  indexChanged: function(index) {
    this.set('index', index);
  }
});
