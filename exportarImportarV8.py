bl_info = {
    "name": "Addon-exportarImportar",
    "description": "este Addon exporta e importa objetos",
    "author": "Manuel Santos",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "View3D > Tool",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Export and import Mesh"
}

import bpy
from bpy.props import StringProperty, EnumProperty, PointerProperty
from bpy.types import Panel, Operator, PropertyGroup
import os


class MyExportOperator(bpy.types.Operator):
    
    bl_idname = "object.export_fbx"    
    bl_label = "Exportar FBX"
    
    def execute(self, context):
        
        # Selecciona el objeto a exportar
        obj = bpy.context.active_object
        
        # export options configuration
        fbx_options = {
            #'filepath': output_path,
            'object_types': {'MESH'},
            'use_mesh_modifiers': True,
            'mesh_smooth_type': 'FACE',
            'use_subsurf': False,
            'use_custom_props': False,
            'apply_scale_options': 'FBX_SCALE_ALL',
            'use_mesh_edges': False,
            'use_tspace': False,
            'add_leaf_bones': False,
            'primary_bone_axis': 'Y',
            'secondary_bone_axis': 'X',
            'use_armature_deform_only': False,
            'armature_nodetype': 'NULL',
            'batch_mode': 'OFF',
            'use_batch_own_dir': True,
            'use_metadata': True,
            'axis_forward': '-Z',
            'axis_up': 'Y'
        }
        
        filepath = os.path.join(context.scene.layama_tool.exportPath, obj.name + ".fbx")
        bpy.ops.export_scene.fbx(filepath=filepath, **fbx_options)
        
        #Put the name of original object in the var
        object_name = bpy.context.active_object.name
        
        bpy.data.objects.remove(bpy.context.active_object)

        # Importa el objeto en formato FBX
        bpy.ops.import_scene.fbx(filepath=filepath)
        
        bpy.context.selected_objects[0].name = original_name

        return {'FINISHED'}

class EIProperties(PropertyGroup):

    def GetLayamaCollections(self, context):
        camNames = []
        camNames.append("Scene Collection")
        for collection in bpy.data.collections:
            camNames.append(collection.name)
        collectionNames = [(name, "CAMERAS FROM: " + name, "")
                           for name in camNames]
        return collectionNames

    exportPath: StringProperty(
        name="Output path",
        description="Choose a path to be used as render and .lym file output.",
        default=os.path.expanduser('~\\Documents\\'),
        maxlen=1024,
        subtype='DIR_PATH'
    )
    


class SelectedObjectOperator(bpy.types.Operator):
    bl_idname = "object.mod_obj"
    bl_label = "Save Selected Object"
    
    def execute(self, context):
        selected_object = context.active_object
        return {'FINISHED'}


class CopyMaterials:
    def execute(self, context):
        dest_obj =  bpy.context.active_object

        dest_obj.data.materials.clear()
        for mMaterial in mod_obj.data.materials:
            dest_obj.data.materials.append(mMaterial)
            

class MyPanel(bpy.types.Panel):
    
    bl_idname = "VIEW_3D_PT_TestPanel"
    bl_label = "Mi panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layamaTool = scene.layama_tool
        
        row = layout.row()
        row.operator("object.export_fbx", text="Export")
        
        row = layout.row()
        layout.prop(layamaTool, "exportPath")        

classes = (
    EIProperties,
    MyExportOperator,
    MyPanel
    )


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.layama_tool = PointerProperty(type=EIProperties)
    
    
def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.layama_tool
    
    
if __name__ == "__main__":
    register()