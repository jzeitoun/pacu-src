import Ember from 'ember';

export default Ember.Route.extend({
  session: Ember.inject.service(),
  actions: {
    toggleFullscreen() {
      this.fullscreen.toggle();
    },
    toastInfo(title, detail) {
      this.toast.info(detail, title);
    },
    toastWarning(title, detail) {
      this.toast.warning(detail, title);
    },
    willTransition(transition) {
    }
  },
  model() {

    const app = Ember.$.getJSON('/api/json/application/info');
    // return Ember.Object.create({
    const routes = [
      {
        content: 'Andor Camera Controller',
        linkTo: 'andor',
        icon: 'camera',
        color: 'white',
      },
      {
        content: 'PsychoPy Controller',
        linkTo: 'psychopy',
        icon: 'unhide',
        color: 'white',
      },

      {
        content: 'Scanimage Data Controller',
        linkTo: 'sci-analyses',
        icon: 'crosshairs',
        color: 'black',
      },
      // {
      //   content: 'Scanbox V1 Data Controller',
      //   linkTo: 'sbx-analyses',
      //   icon: 'cube',
      //   color: 'white',
      // },
      {
        content: 'Scanbox V2 Manager',
        linkTo: 'scanbox-manager',
        icon: 'cube',
        color: 'black',
      },
      // {
      //   content: 'Trajectory Data Controller',
      //   linkTo: 'trj-analyses',
      //   icon: 'paw',
      //   color: 'black',
      // },
      {
        content: 'Miniscope Manager',
        linkTo: 'miniscope-manager',
        icon: 'circle notched',
        color: 'black',
      },
    ];
    // })
    return Ember.RSVP.hash({ app, routes });
  },
  afterModel(model /*, transition */) {
    this._super(...arguments);
    this.get('session').set('app', model.app);
  },
});
