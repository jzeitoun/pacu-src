import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('x-canvas-arraybuffer', 'Integration | Component | x canvas arraybuffer', {
  integration: true
});

test('it renders', function(assert) {
  assert.expect(2);

  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.render(hbs`{{x-canvas-arraybuffer}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:
  this.render(hbs`
    {{#x-canvas-arraybuffer}}
      template block text
    {{/x-canvas-arraybuffer}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
