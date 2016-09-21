import Model from 'ember-data/model';
import attr from 'ember-data/attr';
import { belongsTo, hasMany } from 'ember-data/relationships';

export default Model.extend({
  workspaces: hasMany('workspace'),
  // trials: hasMany('trial'),
  info: attr(),
  imported: attr(),
  pixel_x: attr(),
  pixel_y: attr(),
  dist: attr(),
  width: attr(),
  height: attr(),
  gamma: attr(),
  on_duration: attr(),
  off_duration: attr(),
  orientations: attr(),
  sfrequencies: attr(),
  tfrequencies: attr(),
  repetition: attr(),
  projection: attr(),
  keyword: attr(),
  trial_list: attr(),
});
