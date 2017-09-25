import Model from 'ember-data/model';
import attr from 'ember-data/attr';
import { hasMany } from 'ember-data/relationships';

export default Model.extend({
  workspaces: hasMany('workspace'),
  trials: hasMany('trial'),
  info: attr(),
  imported: attr(),
  message: attr(),
  pixel_x: attr(),
  pixel_y: attr(),
  focal_pane: attr(),
  dist: attr(),
  width: attr(),
  height: attr(),
  contrast: attr(),
  gamma: attr(),
  on_duration: attr(),
  off_duration: attr(),
  orientations: attr(),
  sfrequencies: attr(),
  tfrequencies: attr(),
  contrasts: attr(),
  repetition: attr(),
  projection: attr(),
  stimulus: attr(),
  handler: attr(),
  keyword: attr(),
  trial_list: attr(),
});
