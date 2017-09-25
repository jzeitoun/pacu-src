import Ember from 'ember';

export default Ember.Component.extend({
  actions: {
    updateSoGInitialGuessForThisSF(roi, p, sfreq) {
      const params = [[p.p1, p.p2], [p.p3, p.p4], [p.p5, p.p6], [p.p7, p.p8]];
      this.$().parent().parent().find('.cancel').click();
      return this.attrs.updateSoGInitialGuessForThisSF(roi, params, sfreq);
    },
    updateSoGInitialGuessForAllSF(roi, p) {
      const params = [[p.p1, p.p2], [p.p3, p.p4], [p.p5, p.p6], [p.p7, p.p8]];
      this.$().parent().parent().find('.cancel').click();
      return this.attrs.updateSoGInitialGuessForAllSF(roi, params);
    }
  },
  classNames: 'ui inverted segment',
  sfResponse: function() {
    const sr = this.get('roi.sortedResponses');
    const index = this.get('model.sfrequencyIndex');
    if (Ember.isPresent(sr) && Ember.isPresent(index)) {
      return sr[index];
    }
  }.property('roi', 'model'),
  sfInitialGuess: function() {
    const g = this.get('sfResponse.sog_initial_guess');
    if (Ember.isPresent(g)) {
      return {
        p1: g[0][0], p2: g[0][1], p3: g[1][0], p4: g[1][1],
        p5: g[2][0], p6: g[2][1], p7: g[3][0], p8: g[3][1],
      }
    } else {
      return {
        p1: null, p2: null, p3: null, p4: null,
        p5: null, p6: null, p7: null, p8: null,
      }
    }
  }.property('sfResponse')
}).reopenClass({
  positionalParams: ['roi']
});
