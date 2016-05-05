import Ember from 'ember';

/*global swal*/

export default Ember.Route.extend({
  model() {
    const model = this.modelFor('psychopy');
    if (Ember.isNone(model.result)) {
      swal('Oops...',
        'You have no result to review yet. Please run a stimulus session.',
        'error');
      this.transitionTo('psychopy.broadcast');
    } else {
      Ember.set(model, 'payload', null);
      console.log(model.result);
      return model.result;
    }
  }
});
