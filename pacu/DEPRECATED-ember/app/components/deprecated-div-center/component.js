import Ember from 'ember';

export default Ember.Component.extend({
  attributeBindings: 'style',
  style: function() {
    const disp = 'display:flex;';
    const just = 'justify-content:center;';
    const wdisp = 'display:-webkit-flex;';
    const wjust = '-webkit-justify-content:center;';
    return `${disp}${just}${wdisp}${wjust}`;
  }.property()
});
