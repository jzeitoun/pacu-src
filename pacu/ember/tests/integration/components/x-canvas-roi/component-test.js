import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('x-canvas-roi', 'Integration | Component | x canvas roi', {
  integration: true
});

test('it renders', function(assert) {
  assert.expect(2);

  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.render(hbs`{{x-canvas-roi}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:
  this.render(hbs`
    {{#x-canvas-roi}}
      template block text
    {{/x-canvas-roi}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
