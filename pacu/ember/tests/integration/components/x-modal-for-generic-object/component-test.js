import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('x-modal-for-generic-object', 'Integration | Component | x modal for generic object', {
  integration: true
});

test('it renders', function(assert) {
  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });"

  this.render(hbs`{{x-modal-for-generic-object}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:"
  this.render(hbs`
    {{#x-modal-for-generic-object}}
      template block text
    {{/x-modal-for-generic-object}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
