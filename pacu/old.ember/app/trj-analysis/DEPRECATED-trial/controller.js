import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Controller.extend({
  curIndex: 0,
  refresh: function() {
    const session = this.get('session');
    session.access('dimension').then(img => {
      this.set('img.depth', img.depth);
      this.set('img.width', img.width);
      this.set('img.height', img.height);
      this.requestFrame(0);
    });
    session.access('log_aligned_json').then(log => {
      this.set('trajectory', log);
    });
  }.observes('session'),
  cleanup: function(transition) {
    this.send('stop');
    this.set('curIndex', 0);
    this.set('trajectory', []);
    this.session.dnit();
  },
  initialize: function() {
    this.onBuf = this.set.bind(this, 'img.buffer');
    this.set('img', {width: 0, height: 0, depth: 0, buffer: null});
  }.on('init'),
  @computed('img.depth') maxIndex(d) {
    return d - 1;
  },
  @computed('curIndex', 'trajectory') curTrj(i, trj) {
    if (Ember.isNone(trj)) { return; }
    return trj.get(i);
  },
  @computed('curTrj') mouseY(trj) {
    if (Ember.isNone(trj)) { return; }
    const ratio = 512/130;
    const value = (trj.y + 65) * ratio;
    console.log(ratio, value);
    return 512 - value;
  },
  @computed('curTrj') mouseX(trj) {
    if (Ember.isNone(trj)) { return; }
    const ratio = 128/5;
    const value = (trj.x + 2.5) * ratio;
    console.log(ratio, value);
    return 128 - value;
  },
  requestFrame: function(index) {
    const session = this.get('session');
    return session.invokeAsBinary('request_frame', parseInt(index)).then(this.onBuf);
  },
  indexChanged: function() {
    const index = this.get('curIndex');
    if (Ember.isNone(index)) return;
    this.requestFrame(parseInt(index));
  }.observes('curIndex'),
  actions: {
    play() {
      if (this.get('playing')) { return; }
      this.set('playing', true);
      const session = this.get('session');
      const maxIndex = this.get('maxIndex');
      const run = () => {
        if (this.shouldStop) {
          this.set('playing', false);
          this.set('shouldStop', false);
          return;
        }
        if (maxIndex <= this.get('curIndex')) {
          this.set('curIndex', 0);
          this.send('stop');
        }
        session.invokeAsBinary(
          'request_frame', this.incrementProperty('curIndex')
        ).then(buf => {
          requestAnimationFrame(run);
          this.onBuf(buf);
        });
      };
      run();
    },
    stop() {
      if (!this.get('playing')) { return; }
      this.set('shouldStop', true);
    },
    setCmap(which) {
      this.get('session').invoke('set_cmap', which).then(() => {
        if (!this.get('playing')) {
          const index = this.get('curIndex');
          this.requestFrame(index);
        }
      });
    }
  },
  cmapNames: ['jet', 'gray', 'hot', 'hsv']
});
