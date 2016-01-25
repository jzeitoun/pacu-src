import Ember from 'ember';

export default Ember.Controller.extend({
  curIndex: 0,
  actions: {
    currentSFrequencyEnumChange: function(_, index) {
      console.log(index);
    }
  },
  refresh: function() {
    window.qwe = this;
    const session = this.get('session');
    session.invoke('condition.extract').then((condition) => {
      this.set('condition', condition.attributes);
      session.invoke('get_grand_trace').gate('busy').then((trace) => {
        this.set('trace', trace);
      });
      session.invoke('get_current_sfrequency').then((value) => {
        this.set('current_sfrequency', value);
      });
    });
  }.observes('session'),
  cleanup: function(transition) {
    this.session.dnit();
    this.session = null;
    this.set('curIndex', 0);
    this.set('current_sfrequency', null);
  }
});
