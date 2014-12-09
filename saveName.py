import bpy

def setNameText(objectName, meshName):
    t = bpy.data.texts
    oText = t.new("proxy_object_name")
    mText = t.new('proxy_mesh_name')
    oText.write(objectName)
    mText.write(meshName)
    return


def setNameObject(): 
    t = bpy.data.texts
    oName = t["proxy_object_name"].as_string()
    mName = t['proxy_mesh_name'].as_string()
    o = bpy.context.object
    o.name = oName
    o.data.name = mName
