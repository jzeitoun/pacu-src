import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  classNames: 'mmw-control',
  @computed('mmw.length') maxIndex(len) {
    return len - 1;
  },
  actions: {
    play: function() { this.play(); },
    stop: function() { this.stop(); },
  },
  play: function() {
    if (this.currentLoop) {
      return;
    } else {
      var self = this;
      this.fps = 0;
      this.now = null;
      this.fpsFilter = 8;
      this.lastUpdate = (new Date)*1 - 1;
      this.currentLoop = this.loop();
      this.set('active', true);
      this.curfpsInterval = setInterval(function() {
        self.set('curfps', self.fps.toFixed(2));
      }, 1000);
    }
  },
  stop: function() {
    if (this.currentLoop) {
      Ember.run.cancel(this.currentLoop);
      this.currentLoop = null;
      clearInterval(this.curfpsInterval);
      this.set('active', false);
    }
  }.on('willDestroyElement').observes('mmw.url'),
  loop: function() {
    var interval = parseInt(this.get('mmw.interval'));
    var mmw = this.get('mmw');
    var index = this.get('mmw.index');
    var maxIndex = this.get('mmw.length') - 1;
    if (index >= maxIndex) { return; }
    return Ember.run.later(this, () => {

      var nextIndex = mmw.nudge();
      var hasNext = nextIndex < maxIndex;

      var thisFrameFPS = 1000 / ((this.now=new Date) - this.lastUpdate);
      this.fps += (thisFrameFPS - this.fps) / this.fpsFilter;
      this.lastUpdate = this.now * 1 - 1;
      if (hasNext) {
        this.currentLoop = this.loop();
      } else {
        this.currentLoop = null;
      }
    }, interval);
  },
  cmaps: [
    {uid: 'gray', text: 'Gray', colordot: 'black'},
    {uid: 'jet', text: 'Jet', colordot: 'blue'},
    {uid: 'hsv', text: 'HSV', colordot: 'orange'},
    {uid: 'hot', text: 'Hot', colordot: 'red'},
  ],
  setCMap: function() {
    const cmap = this.get('selectedMap');
    const mmw = this.get('mmw');
    mmw.setCMap(cmap);
    if (!this.get('active')) {
      mmw.draw();
    }
  }.observes('selectedMap')
});
