import bpy

def setNameText(objectName, meshName):
    text_object_name = "proxy_object_name"
    text_mesh_name = "proxy_mesh_name"

    t = bpy.data.texts
    if text_object_name in [i.name for i in t]:
        oText = t.new(text_object_name)
    else:
        oText = t[text_object_name]
    if text_mesh_name in [i.name for i in t]:
        mText = t.new(text_mesh_name)
    else:
        mText = t[text_mesh_name]
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
    return
