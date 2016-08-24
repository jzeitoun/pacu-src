import Model from 'ember-data/model';
import attr from 'ember-data/attr';
import { belongsTo, hasMany } from 'ember-data/relationships';

export default Model.extend({
  condition: belongsTo('condition'),
  on_time: attr(),
  off_time: attr(),
  ori: attr(),
  sf: attr(),
  tf: attr(),
  sequence: attr(),
  order: attr(),
  ran: attr(),
  flicker: attr(),
  blank: attr(),
});
