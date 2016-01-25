import Ember from 'ember';

export default Ember.Component.extend({
  updateROI: function() {
    const self = this;
    const roi = this.getAttr('roi');
    if (Em.isNone(roi)) {
      self.set('data', null);
      return;
    }
    const session = this.getAttr('session');
    const {x1, x2, y1, y2} = roi.getProperties('x1', 'x2', 'y1', 'y2');
    session.invoke('get_response', x1, x2, y1, y2).then(function(data) {
      self.set('data', data);
    }).catch(function(err) {
      console.error(err.source.join(''));
      self.toast.error(err.detail, err.title);
    });
  }.observes('roi')
});
