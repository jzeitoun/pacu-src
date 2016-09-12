import Ember from 'ember';

export default Ember.Route.extend({
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
    return Ember.Object.create({
      routes: [
        {
          content: 'Andor Camera Controller',
          linkTo: 'andor',
          icon: 'camera',
          color: 'white',
        },
        {
          content: 'Scanimage Data Controller',
          linkTo: 'sci-analyses',
          icon: 'crosshairs',
          color: 'white',
        },
        {
          content: 'Scanbox V1 Data Controller',
          linkTo: 'sbx-analyses',
          icon: 'cube',
          color: 'white',
        },
        {
          content: 'Scanbox V2 Manager',
          linkTo: 'scanbox-manager',
          icon: 'cube',
          color: 'black',
          featureName: 'aergarg',
        },
        {
          content: 'Trajectory Data Controller',
          linkTo: 'trj-analyses',
          icon: 'paw',
          color: 'white',
        },
        {
          content: 'PsychoPy Controller',
          linkTo: 'psychopy',
          icon: 'unhide',
          color: 'white',
        },
      ]
    })
  }
});
