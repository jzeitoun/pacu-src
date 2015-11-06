import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  state: '',
  @computed('state') stateStr(s) {
    return s===''   ? 'Initial' :
           s===null ? 'Released':
           s===true ? 'Acquired':
                      'Unavailable'
  },
  @computed('state') stateCss(s) { return s===true ? 'block': 'none' },
  actions: {
    acquire: function() {
      const self = this;
      this.wsx.invoke('acquire').then(function(data) {
        if (data.error) {
          alert(data.detail);
        } else {
          self.wsx.mirror('state');
          self.wsx.mirror('features');
        }
      });
    },
    release: function() {
      const self = this;
      this.wsx.invoke('release').then(function(data) {
        self.set('state', null);
        self.set('features', []);
      });
    }
  },
  socket: Ember.inject.service(),
  initWS: function() {
    window.asd = this;
    const self = this;
    this.wsx = this.get('socket').create(
      this, 'pacu.core.svc.andor', 'AndorBindingService', this.getAttr('src')
    );
    this.$('.tabular.menu .item').tab({
      onLoad: function(tabPath, parameterArray, historyEvent) {
      }
    });
  }.on('didInsertElement'),
  dnitWS: function() { this.wsx.dnit(); }.on('willDestroyElement'),
});
