import Ember from 'ember';

const modname = 'pacu.core.io.trajectory.session';
const clsname = 'TrajectorySessionFetcher'

export default Ember.Route.extend({
  socket: Ember.inject.service(),
  actions: {
    didTransition() {
      this.controllerFor('application').set(
        'current-feature', 'Trajectory Analysis');
    },
  },
});
