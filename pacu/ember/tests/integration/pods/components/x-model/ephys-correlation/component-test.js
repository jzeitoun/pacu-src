import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('x-model/ephys-correlation', 'Integration | Component | x model/ephys correlation', {
  integration: true
});

test('it renders', function(assert) {
  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.render(hbs`{{x-model/ephys-correlation}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:
  this.render(hbs`
    {{#x-model/ephys-correlation}}
      template block text
    {{/x-model/ephys-correlation}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
