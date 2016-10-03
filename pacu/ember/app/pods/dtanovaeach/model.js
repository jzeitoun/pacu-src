import Model from 'ember-data/model';
import attr from 'ember-data/attr';
import { belongsTo, hasMany } from 'ember-data/relationships';
import Datatag from 'pacu/pods/datatag/model';

export default Datatag.extend({
  f: attr(),
  p: attr(),
  roi: belongsTo('roi'),
});