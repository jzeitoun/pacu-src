import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('x-draggable/circle', 'Integration | Component | x draggable/circle', {
  integration: true
});

test('it renders', function(assert) {
  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });"

  this.render(hbs`{{x-draggable/circle}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:"
  this.render(hbs`
    {{#x-draggable/circle}}
      template block text
    {{/x-draggable/circle}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
