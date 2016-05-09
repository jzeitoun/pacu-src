import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Mixin.create({
  @computed() router() {
    return Ember.getOwner(this).lookup('router:main');
  },
  routeAction(action, ...args) {
    return this.get('router').send(action, ...args);
  }
});
