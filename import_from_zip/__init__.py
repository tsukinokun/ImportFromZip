import bpy
import zipfile
import tempfile
import shutil
import os
from bpy_extras.io_utils import ImportHelper


def _import_fbx(filepath):
    bpy.ops.import_scene.fbx(filepath=filepath)


def _import_obj(filepath):
    bpy.ops.wm.obj_import(filepath=filepath)


def _import_glb(filepath):
    bpy.ops.import_scene.gltf(filepath=filepath)


IMPORTERS = {
    ".fbx": _import_fbx,
    ".obj": _import_obj,
    ".glb": _import_glb,
    ".gltf": _import_glb,
}


class IMPORT_OT_from_zip(bpy.types.Operator, ImportHelper):
    """Extract a ZIP archive and import every supported file found inside it"""
    bl_idname = "import_scene.from_zip"
    bl_label = "Import From Zip"
    bl_options = {'REGISTER', 'UNDO'}

    filter_glob: bpy.props.StringProperty(default="*.zip", options={'HIDDEN'})

    keep_extracted_files: bpy.props.BoolProperty(
        name="Keep Extracted Files",
        description=(
            "Extract next to the ZIP and keep the files on disk after import.\n"
            "Needed if you plan to export FBX with Path Mode = Copy (so a .fbm "
            "folder with real texture files can be created).\n"
            "If disabled, files are extracted to a temporary folder, packed "
            "into the .blend, and deleted immediately after import"
        ),
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "keep_extracted_files")

    def execute(self, context):
        if self.keep_extracted_files:
            return self._execute_keep(context)
        else:
            return self._execute_temp(context)

    # -------------------------------------------------------------
    # モード1: 展開したファイルを残す(FBXのCopy/.fbm運用向け)
    # -------------------------------------------------------------
    def _execute_keep(self, context):
        zip_dir = os.path.dirname(self.filepath)
        zip_name = os.path.splitext(os.path.basename(self.filepath))[0]
        extract_dir = os.path.join(zip_dir, f"{zip_name}_extracted")

        # 同名フォルダが既にあれば作り直す(古いファイルの混在を防ぐ)
        if os.path.isdir(extract_dir):
            shutil.rmtree(extract_dir, ignore_errors=True)
        os.makedirs(extract_dir, exist_ok=True)

        try:
            with zipfile.ZipFile(self.filepath, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
        except zipfile.BadZipFile:
            self.report({'ERROR'}, "Selected file is not a valid ZIP archive")
            return {'CANCELLED'}
        except OSError as e:
            self.report({'ERROR'}, f"Could not extract ZIP next to source file: {e}")
            return {'CANCELLED'}

        imported_count = self._import_all(extract_dir)

        if imported_count == 0:
            supported = ", ".join(sorted(IMPORTERS))
            self.report({'WARNING'}, f"No supported files ({supported}) found inside the ZIP")
        else:
            self.report(
                {'INFO'},
                f"Imported {imported_count} file(s). Extracted files kept at: {extract_dir}"
            )
        return {'FINISHED'}

    # -------------------------------------------------------------
    # モード2: 一時フォルダを使い、終わったら消す(従来動作)
    # -------------------------------------------------------------
    def _execute_temp(self, context):
        imported_count = 0
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                try:
                    with zipfile.ZipFile(self.filepath, 'r') as zip_ref:
                        zip_ref.extractall(temp_dir)
                except zipfile.BadZipFile:
                    self.report({'ERROR'}, "Selected file is not a valid ZIP archive")
                    return {'CANCELLED'}

                imported_count = self._import_all(temp_dir)

                # 一時フォルダが消える前に画像データを .blend に埋め込む
                bpy.ops.file.pack_all()
                for img in bpy.data.images:
                    if img.filepath.startswith(temp_dir):
                        img.filepath = ""  # 壊れたパス参照を残さない
        except OSError as e:
            self.report({'ERROR'}, f"Failed to extract ZIP: {e}")
            return {'CANCELLED'}

        if imported_count == 0:
            supported = ", ".join(sorted(IMPORTERS))
            self.report({'WARNING'}, f"No supported files ({supported}) found inside the ZIP")
        else:
            self.report({'INFO'}, f"Imported {imported_count} file(s) from ZIP")
        return {'FINISHED'}

    # -------------------------------------------------------------
    @staticmethod
    def _import_all(root_dir):
        imported_count = 0
        for root, _, files in os.walk(root_dir):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                importer = IMPORTERS.get(ext)
                if importer is not None:
                    importer(os.path.join(root, file))
                    imported_count += 1
        return imported_count


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