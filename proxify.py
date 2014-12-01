import bpy

def proxify():
    ng = bpy.data.groups.new('')
    objs = bpy.context.selected_objects
    for ob in objs:
        bpy.context.scene.objects.active = ob
        print(ob)
        #bpy.ops.object.proxy_make(object="", type='DEFAULT')
        bpy.ops.object.proxy_make()
        ob = bpy.context.object
        ng.objects.link(ob)


################### add on setting section###########################
bl_info = {
    "name": "Proxify ",
    "category": "Object",
}

import bpy


class ProxifyWithGroup(bpy.types.Operator):
    """proxify selected object and assign group"""
    bl_idname = "proxify_with_group.comic"
    bl_label = "proxify with group"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):  
        proxify()
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ProxifyWithGroup)


def unregister():
    bpy.utils.unregister_class(ProxifyWithGroup)


if __name__ == "__main__":
    register()