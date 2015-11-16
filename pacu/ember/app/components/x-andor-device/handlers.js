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
  guide      : 'Type without file extension...(alphanumeric and underscore only)',
};
export const writer = [
  filename,
];
export const bypass = [
];
