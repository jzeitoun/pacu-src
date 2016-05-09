import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('x-anlz-session-card', 'Integration | Component | x anlz session card', {
  integration: true
});

test('it renders', function(assert) {
  assert.expect(2);

  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.render(hbs`{{x-anlz-session-card}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:
  this.render(hbs`
    {{#x-anlz-session-card}}
      template block text
    {{/x-anlz-session-card}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
