import bpy

class LayerPanel(bpy.types.Panel):
    bl_idname = "layer_panel"
    bl_label = "Layers"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"
    bl_context = 'imagepaint'

    def draw(self, context):
        layout = self.layout
        mat = bpy.context.object.active_material
        
        if not mat:
            row = layout.row()
            row.label("Add material to use layers", icon='INFO')
            return
        
        index = mat.layer_index
        
        if not mat.layer_list:
            row = layout.row()
            row.prop(mat.layer_img_data, 'width')
            row = layout.row()
            row.prop(mat.layer_img_data, 'height')
            
            row = layout.row()
            row.prop(mat.layer_img_data, 'color')
            
            row = layout.row()
            row.prop(mat.layer_img_data, 'float')
            
            layout.label(text="Apply and create layer:")
            row = layout.row()
            row.operator('layer_list.new_layer', text="New Layer")
            return

        row = layout.row()
        row.template_list('MATERIAL_UL_layerlist', "", mat, 'layer_list', mat, 'layer_index')
        
        col = row.column(align=True)
        col.operator('layer_list.new_layer', icon='ZOOMIN', text="")
        col.operator('layer_list.delete_layer', icon='ZOOMOUT', text="")
        col.separator()
        
        col.operator('layer_list.move_layer', icon='TRIA_UP', text="").direction = 'UP'
        col.operator('layer_list.move_layer', icon='TRIA_DOWN', text="").direction = 'DOWN'
        
        if index >= 0 and index < len(mat.layer_list) and mat.layer_list:
            layer = mat.layer_list[index]
            
            row = layout.row()
            row.prop(layer, 'name')
            
            row = layout.row()
            try:
                row.prop(mat.node_tree.nodes[layer.mix], 'blend_type', text="")
            except KeyError as e:
                print("Can't find mix node for blend types: " + layer.mix)
                
            row = layout.row()
            try:
                row.prop(mat.node_tree.nodes[layer.multiply].inputs[1], 'default_value',
                        text="Opacity")
            except KeyError as e:
                print("Can't find multiply node for opacity: " + layer.multiply)
        
        space = bpy.context.space_data
        if space.type == 'VIEW_3D' and \
            (space.viewport_shade != 'MATERIAL' and space.viewport_shade != 'RENDERED'):
            row = layout.row()
            row.label("Not in material mode", icon='ERROR')
        