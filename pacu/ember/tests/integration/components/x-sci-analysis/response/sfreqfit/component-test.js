import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('x-sci-analysis/response/sfreqfit', 'Integration | Component | x sci analysis/response/sfreqfit', {
  integration: true
});

test('it renders', function(assert) {
  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });"

  this.render(hbs`{{x-sci-analysis/response/sfreqfit}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:"
  this.render(hbs`
    {{#x-sci-analysis/response/sfreqfit}}
      template block text
    {{/x-sci-analysis/response/sfreqfit}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
