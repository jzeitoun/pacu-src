import Model from 'ember-data/model';
import attr from 'ember-data/attr';
import { belongsTo /*, hasMany */ } from 'ember-data/relationships';

export default Model.extend({
  basename: attr('string', { defaultValue: 'jet' }),
  xmid1: attr('number', { defaultValue: 25 }),
  ymid1: attr('number', { defaultValue: 25 }),
  xmid2: attr('number', { defaultValue: 75 }),
  ymid2: attr('number', { defaultValue: 75 }),
  workspace: belongsTo('workspace')
});
