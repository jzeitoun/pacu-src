import Model from 'ember-data/model';
import attr from 'ember-data/attr';
import { belongsTo, hasMany } from 'ember-data/relationships';
import { on, observes } from 'ember-computed-decorators';
import { getCentroid } from 'pacu/pods/components/x-layer/roi/centroid';

export default Model.extend({
  created_at: attr('epoch'),
  active: attr('boolean', { defaultValue: false }),
  polygon: attr({ defaultValue: () => { return []; } }),
  centroid: attr({ defaultValue: () => { return {x: -1, y: -1}; } }),
  workspace: belongsTo('workspace'),
  traces: hasMany('trace'),
  @observes('polygon.@each.{x,y}') updateCentroid(polygon) {
    const old = this.get('centroid');
    const nue = getCentroid(this.get('polygon'));
    const isSame = old.x === nue.x && old.y === nue.y;
    const incomingNaN = isNaN(nue.x) || isNaN(nue.y);
    if (!incomingNaN && !isSame) { this.set('centroid', nue); }
  },
  @on('didCreate') normalizeTraces() {
    if (Ember.isEmpty(this.get('traces'))) {
      const trace = this.store.createRecord('trace', {
        category: 'df/f0', array: [], roi: this
      });
      trace.save();
    }
  },
  actions: {
    foo(t) {
      debugger
    }
  }
});
