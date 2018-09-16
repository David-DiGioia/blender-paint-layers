'''
Copyright (C) 2018 DAVID DIGIOIA
DAVIDOFJOY@GMAIL.com

Created by DAVID DIGIOIA

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Layers",
    "description": "Layer functionality using nodes for texture paint",
    "author": "David DiGioia",
    "version": (0, 0, 1),
    "blender": (2, 79, 0),
    "location": "View3D > Tools > Layers",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Paint" }


import bpy


# load and reload submodules
##################################

import importlib
from . import developer_utils
importlib.reload(developer_utils)
modules = developer_utils.setup_addon_modules(__path__, __name__, "bpy" in locals())



# register
##################################

import traceback

def register():
    try: bpy.utils.register_module(__name__)
    except: traceback.print_exc()
    
    #<David>
    def get_index(self):
        return self.layer_private_index
    
    def set_index(self, index):
        layer_list = bpy.context.object.active_material.layer_list
        
        if index < 0 or index >= len(layer_list):
            self.layer_private_index = index
            return
        
        layer = bpy.context.object.active_material.layer_list[index]
        img_name = layer.texture
        
        # Need to update scene in order for slots to update in time
        bpy.context.scene.update()
        
        slots = bpy.context.object.active_material.texture_paint_images
        slot_index = None
        for i, slot in enumerate(slots):
            if slot.name == img_name:
                slot_index = i    
        try:
            bpy.context.object.active_material.paint_active_slot = slot_index
        except TypeError as e:
            print("No slot names match layer name. There are probably missing slots")
            print("Error: " + str(e))
        self.layer_private_index= index
    
    bpy.types.Material.layer_list = bpy.props.CollectionProperty(type = bpy.types.Layer)
    bpy.types.Material.layer_index = bpy.props.IntProperty(name = "Index for layer list", default = 0, \
                                                            get=get_index, set=set_index)
    bpy.types.Material.layer_private_index = bpy.props.IntProperty(name = "PRIVATE layer index", default = 0)
    bpy.types.Material.layer_shaders = bpy.props.PointerProperty(type = bpy.types.LayerShaders)
    bpy.types.Material.layer_img_data = bpy.props.PointerProperty(type = bpy.types.LayerImgData)
    #</David>
    
    print("Registered {} with {} modules".format(bl_info["name"], len(modules)))

def unregister():
    try: bpy.utils.unregister_module(__name__)
    except: traceback.print_exc()

    #<David>
    del bpy.types.Material.layer_list
    del bpy.types.Material.layer_index
    del bpy.types.Material.layer_private_index
    del bpy.types.Material.layer_shaders
    del bpy.types.Material.layer_img_data
    #</David>

    print("Unregistered {}".format(bl_info["name"]))
