import Ember from 'ember';

// vectors: [
//   {index: 100, x:13, y:-36},
// ]

export default Ember.Component.extend({
  actions: {
    removeVector(vector) {
      const roi = this.get('roi');
      this.get('roi.vectors').removeObject(vector);
      this.sendAction('invalidateTrajectory', roi);
    },
    insertVector(index, x, y) {
      const roi = this.get('roi');
      if (roi && index && x && y) {
        const i = parseInt(index);
        const px = parseInt(x);
        const py = parseInt(y);
        const vectors = this.get('roi.vectors');
        vectors.pushObject({index:i, x:px, y:py});
        this.set('roi.vectors', vectors.sortBy('index'));
        this.set('index', null);
        this.set('x', null);
        this.set('y', null);
        this.sendAction('invalidateTrajectory', roi);
      }
    },
    activateInteractive() {
      const roi = this.get('roi');
      if (roi) {
        this.set('pointLocatorActive', true);
      }
    }
  },
  updateIndex: function() {
    const index = this.get('curIndex');
    this.set('index', index);
  }.observes('curIndex'),
  updateX: function() {
    const x = this.get('curX');
    this.set('x', x);
  }.observes('curX'),
  updateY: function() {
    const y = this.get('curY');
    this.set('y', y);
  }.observes('curY'),
});
