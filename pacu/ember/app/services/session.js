import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Service.extend({
  @computed() jsonapi() {
    console.log('get/set jsonapi session');
    return Ember.Object.create({
      moduleName:'',
      sessionArgs: [],
      baseName: ''
    });
  },
});
