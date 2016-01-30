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
const dirname = {
  key        : 'dirname',
  type       : 'StringMeta',
  value      : 'E:\\data\\Soyun',
  feature    : 'Dirname',
  range      : [0, 512],
  readable   : true,
  readonly   : false,
  writable   : true,
  implemented: true,
  guide      : 'Location of local directory.' // should be `directive` key?
  // examples
};
export const writer = [
  filename,
];
export const writer_by_ttl = [
  dirname,
];
export const bypass = [
];
