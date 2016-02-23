import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  attributeBindings: ['style'],
  @computed('width', 'height') style(w, h) {
    return new Ember.Handlebars.SafeString(`position: relative;
      width: ${w}px; height: ${h}px; padding: 0; margin: 0 auto;`);
  },
});

