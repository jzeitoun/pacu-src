import Ember from 'ember';

export default Ember.Component.extend({
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
  }.on('didInsertElement'),
  stop: function() {
    if (this.currentLoop) {
      Ember.run.cancel(this.currentLoop);
      this.currentLoop = null;
      clearInterval(this.curfpsInterval);
      this.set('active', false);
    }
  }.on('willDestroyElement').observes('mmw.url'),
  loop: function() {
    var interval = 16;
    var mmw = this.get('mmw');
    return Ember.run.later(this, () => {
      mmw.nudge();
      var thisFrameFPS = 1000 / ((this.now=new Date) - this.lastUpdate);
      this.fps += (thisFrameFPS - this.fps) / this.fpsFilter;
      this.lastUpdate = this.now * 1 - 1;
      this.currentLoop = this.loop();
    }, interval);
  }
});
