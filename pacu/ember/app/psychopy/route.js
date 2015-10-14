import Ember from 'ember';

export default Ember.Route.extend({
  actions: {
    didTransition() {
      this.controllerFor('application').set(
        'current-feature', 'PsychoPy Controller');
    },
    broadcast(payload = {}) {
      const model = this.currentModel;
      const names = 'monitor window stimulus projection clock handler'.split(' ');
      names.forEach(name => {
        const spec = model[name];
        const kwargs = {};
        for (let field of spec.fields) {
          kwargs[field.key] = field.val;
        }
        payload[name] = {
          pkgname: spec.pkgname,
          clsname: spec.clsname,
          kwargs
        };
      });
      Ember.set(model, 'payload', payload);
      this.transitionTo('psychopy.broadcast-onair');
    }
  },
  model() {
    return Ember.$.getJSON('api/service-format/pacu.core.svc.vstim/ember');
  },
  afterModel(model) {
    // debug
    // console.log(model);
    model.monitor_id = 0;
    model.window_id = 0;
    model.stimulus_id = 0;
    model.projection_id = 0;
    model.clock_id = 0;
    model.handler_id = 0;
    model.monitor = model.monitors[0];
    model.window = model.windows[0];
    model.stimulus = model.stimuli[0];
    model.projection = model.projections[0];
    model.clock = model.clocks[0];
    model.handler = model.handlers[0];
  }
});
