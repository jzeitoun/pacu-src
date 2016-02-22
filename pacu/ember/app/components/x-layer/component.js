import Ember from 'ember';
import computed from 'ember-computed-decorators';

export default Ember.Component.extend({
  attributeBindings: ['style'],
  @computed('attrs.width', 'attrs.height') style(w, h) {
    return `position: relative; whdth: ${w}px; height: ${h}px;
            padding: 0; margin: 0 auto;`
  },
});

