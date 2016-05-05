import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('x-layer/point-locator', 'Integration | Component | x layer/point locator', {
  integration: true
});

test('it renders', function(assert) {
  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });"

  this.render(hbs`{{x-layer/point-locator}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:"
  this.render(hbs`
    {{#x-layer/point-locator}}
      template block text
    {{/x-layer/point-locator}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
