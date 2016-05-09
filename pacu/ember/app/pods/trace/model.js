import Model from 'ember-data/model';
import attr from 'ember-data/attr';
import { belongsTo, hasMany } from 'ember-data/relationships';

export default Model.extend({
  created_at: attr('epoch'),
  array: attr(),
  category: attr('string'),
  roi: belongsTo('roi'),
});
