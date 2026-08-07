# Description (for the extensions.blender.org listing page)

## Short version (use if the platform has a length limit)

Import From Zip adds a single new import option to Blender:
**File > Import > Import From Zip (.zip)**. Point it at any `.zip`
archive and it will find every supported 3D file inside -- including
ones nested in subfolders -- and import them all into your current
scene. Supports FBX, OBJ, and glTF/GLB, with more formats planned.

## Full version

**What it does**

Many 3D assets are distributed as ZIP archives -- asset packs from
marketplaces, exports shared by teammates, or downloads from asset
libraries. Normally you'd have to extract the ZIP somewhere on disk
first, then run the appropriate importer. Import From Zip removes
that extra step.

Once installed, go to **File > Import > Import From Zip (.zip)**,
select any ZIP file, and the add-on will:

1. Extract the ZIP to a temporary folder.
2. Recursively scan every folder inside it for supported files.
3. Import each supported file found into the current scene, using
   Blender's built-in importers.
4. Automatically delete the temporary extraction folder afterwards --
   nothing is left behind on disk.

If the archive contains multiple supported files (for example, a
character plus separate prop files), all of them are imported in one
action.

**Supported formats**

- FBX (`.fbx`)
- OBJ (`.obj`)
- glTF / GLB (`.gltf`, `.glb`)
- More formats (STL, USD, ...) can be added easily -- the add-on is
  built around a small per-extension importer table so new formats
  can be added without changing how the operator works.

**What it does not do**

- It does not modify, repair, or optimize the imported files
  themselves -- it simply automates extraction + import.
- It does not upload, download, or transmit any data. All processing
  happens locally in a temporary directory that Blender itself manages.
- It does not touch or interfere with any other installed add-ons.

**Typical use cases**

- Importing asset-store purchases that are packaged as ZIP files.
- Quickly bringing in exports shared by collaborators without a
  manual extract step.
- Batch-importing multiple files that were zipped together.

**Requirements**

- Blender 4.2 or later (uses the Extensions system).
- No external dependencies -- it only uses Python's standard library
  (`zipfile`, `tempfile`, `os`) plus Blender's built-in importers.

**Permissions**

This add-on only reads the ZIP file you explicitly select through the
file browser and writes to a temporary directory that is cleaned up
automatically. It does not access the network and does not read or
write any other files on your system.
