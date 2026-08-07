import bpy
import zipfile
import tempfile
import os
from bpy_extras.io_utils import ImportHelper


def _import_fbx(filepath):
    bpy.ops.import_scene.fbx(filepath=filepath)


def _import_obj(filepath):
    bpy.ops.wm.obj_import(filepath=filepath)


def _import_glb(filepath):
    bpy.ops.import_scene.gltf(filepath=filepath)


# Maps a file extension (lowercase, with dot) to the function that
# imports a single file of that type. Add new entries here to support
# more formats.
IMPORTERS = {
    ".fbx": _import_fbx,
    ".obj": _import_obj,
    ".glb": _import_glb,
    ".gltf": _import_glb,  # same importer handles both glTF variants
}


class IMPORT_OT_from_zip(bpy.types.Operator, ImportHelper):
    """Extract a ZIP archive and import every supported file found inside it"""
    bl_idname = "import_scene.from_zip"
    bl_label = "Import From Zip"
    bl_options = {'REGISTER', 'UNDO'}

    filter_glob: bpy.props.StringProperty(default="*.zip", options={'HIDDEN'})

    def execute(self, context):
        imported_count = 0

        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                with zipfile.ZipFile(self.filepath, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)

                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        ext = os.path.splitext(file)[1].lower()
                        importer = IMPORTERS.get(ext)
                        if importer is not None:
                            importer(os.path.join(root, file))
                            imported_count += 1
        except zipfile.BadZipFile:
            self.report({'ERROR'}, "Selected file is not a valid ZIP archive")
            return {'CANCELLED'}

        if imported_count == 0:
            supported = ", ".join(sorted(IMPORTERS))
            self.report({'WARNING'}, f"No supported files ({supported}) found inside the ZIP")
        else:
            self.report({'INFO'}, f"Imported {imported_count} file(s) from ZIP")

        return {'FINISHED'}


def menu_func_import(self, context):
    self.layout.operator(IMPORT_OT_from_zip.bl_idname, text="Import From Zip (.zip)")


def register():
    bpy.utils.register_class(IMPORT_OT_from_zip)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.utils.unregister_class(IMPORT_OT_from_zip)


if __name__ == "__main__":
    register()