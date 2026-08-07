# Contributing

Thanks for considering a contribution!

## Reporting bugs

Please open an issue with:

- Blender version
- Steps to reproduce
- The error message from the System Console
  (`Window > Toggle System Console` on Windows, or run Blender from a
  terminal on macOS/Linux)

## Submitting changes

1. Fork the repo and create a branch from `main`.
2. Make your changes.
3. Test by installing the add-on locally (see README).
4. Open a pull request describing what you changed and why.

## Code style

- Keep it simple — this add-on intentionally has a small surface area.
- Follow standard Blender Python API conventions (`bl_idname`, `bl_label`,
  `execute(self, context)`, etc).

## Adding a new file format

New format support is very welcome. Add a `_import_xxx(filepath)`
function that calls the relevant `bpy.ops.import_scene.*` /
`import_mesh.*` / `import_curve.*` operator, then register it in the
`IMPORTERS` dict at the top of `__init__.py`. No other changes should
be needed.
