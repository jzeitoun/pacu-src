const filename = {
  key        : 'filename',
  type       : 'StringMeta',
  value      : '',
  feature    : 'Filename',
  range      : [0, 256],
  readable   : true,
  readonly   : false,
  writable   : true,
  implemented: true,
  guide      : 'Type without file extension. (alphanumeric and underscore only) When this field is blank and mode is stimulation drive, file name and location will be automatically set.',
};
export const writer = [
  filename,
];
export const bypass = [
];
