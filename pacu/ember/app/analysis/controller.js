import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Controller.extend({
  curIndex: 0,
  actions: {
    currentSFrequencyEnumChange: function(_, index) {
      console.log(index);
    }
  },
  refresh: function() {
    const session = this.get('session');
    session.invoke('condition.extract').then(condition => {
      this.set('condition', condition.attributes);
      session.invoke('get_grand_trace').gate('busy').then(trace => {
        this.set('trace', trace);
      });
      session.invoke('get_current_sfrequency').then(value => {
        this.set('current_sfrequency', value);
      });
      session.access('dimension').then(img => {
        this.set('img.depth', img.depth);
        this.set('img.width', img.width);
        this.set('img.height', img.height);
        session.invokeAsBinary('request_frame', 0).then(buf => {
          this.set('img.buffer', buf);
        });
      });
    });
  }.observes('session'),
  cleanup: function(transition) {
    this.session.dnit();
    this.session = null;
    this.set('curIndex', null);
    this.set('current_sfrequency', null);
  },
  initialize: function() {
    this.set('img', {width: 0, height: 0, depth: 0, buffer: null});
  }.on('init'),
  @computed('img.depth') maxIndex(d) {
    return d - 1;
  },
  dodo: function() {
    const index = this.get('curIndex');
    if (Ember.isNone(index)) return;
    console.log('~~~~~dhaha', index);
  }.observes('curIndex')
});
