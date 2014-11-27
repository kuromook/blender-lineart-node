import bpy
 
class NODE_MT_test_menu(bpy.types.Menu):
    bl_idname = 'NODE_MT_test_menu'
    bl_space_type = 'NODE_EDITOR'
    bl_label = "Test Menu"
    bl_description = "Test Tooltip"
    bl_region_type = 'UI'
    bl_context = "UI" 
    def draw(self, context):
        layout = self.layout
        layout.label(text="Test Menu")
 
 
def register():
    bpy.utils.register_class(NODE_MT_test_menu)
 
def unregister():
    bpy.utils.unregister_class(NODE_MT_test_menu)
 
if __name__ == "__main__":
    register()