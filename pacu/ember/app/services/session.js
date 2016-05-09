import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Service.extend({
  @computed() jsonapi() {
    return Ember.Object.create({
      moduleName:'',
      sessionArgs: [],
      baseName: ''
    });
  }
});
