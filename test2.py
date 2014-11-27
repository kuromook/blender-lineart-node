import textwrap

import bpy

from bpy.props import StringProperty, BoolProperty, FloatVectorProperty

bl_info = {
    "name":        "Generic Note Node",
    "description": "A generic note node",
    "author":      "Linus Yng",
    "version":     (0, 1, 0),
    "blender":     (2, 7, 1),
    "location":    "Node Editor",
    "category":    "Node",
    "warning":     "The note will not work for people without this addon"
    }

TEXT_WIDTH = 6

class GenericNotePreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    
    note_node_color = FloatVectorProperty(
                      name="Note Color", description='Default color for note node',
                      size=3, min=0.0, max=1.0,
                      default=(.5, 0.5, .5), subtype='COLOR')
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "note_node_color")
    
def register():
    bpy.utils.register_module(__name__)
    
def unregister():
    bpy.utils.unregister_module(__name__)
    
if __name__ == '__main__':
    register()
