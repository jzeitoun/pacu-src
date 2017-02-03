import Ember from 'ember';

export default Ember.Component.extend({
  xmid: 25,
  ymid: 25,
  actions: {
    updateMidPoint(cx, cy/* , altKey */) {
      const cxOK = 0 <= cx && cx <= 100;
      const cyOK = 0 <= cy && cy <= 100;
      return cxOK && cyOK;
    }
  },
  midPointChanged: function() {
    const xmid = this.get('xmid');
    const ymid = this.get('ymid');
    this.attrs.onMidPointChanged(xmid, ymid);
  }.observes('xmid', 'ymid')
});
