import bpy
from .. import layer_utils

class LAYER_OT_newlayer(bpy.types.Operator):
    """Delete selected layer"""
    
    bl_idname = 'layer_list.delete_layer'
    bl_label = "Deletes layer"
    
    @classmethod
    def poll(cls, context):
        mat = bpy.context.object.active_material
        return mat.layer_list and mat.layer_index >= 0 and mat.layer_index < len(mat.layer_list)
    
    def delete_nodes(self, context):
        mat = context.object.active_material
        list = mat.layer_list
        index = mat.layer_index
        layer = list[index]
        nodes = mat.node_tree.nodes
        get_input = layer_utils.get_input_node
        get_output = layer_utils.get_output_node
        
        # Delete links and make references
        try:
            mix_node = nodes[layer.mix]
            higher = get_input(layer)
            lower = get_output(layer)
        except KeyError as e:
            return
        try:
            add_node = nodes[layer.add]
        except KeyError as e:
            add_node = None
        try:
            higher_add = add_node.inputs[0].links[0].from_node
        except IndexError as e:
            higher_add = None
        
        # Delete nodes
        nodes.remove(mix_node)
        nodes.remove(nodes[layer.multiply])
        nodes.remove(nodes[layer.img_tex])
        if add_node is not None:
            nodes.remove(add_node)
        
        for i, lay in enumerate(list):
            if i > index:
                layer_utils.offset_layer(lay, layer_utils.offset)
        
        if higher is not None:
            col_input = layer_utils.get_input_of_type(lower, 'RGBA')
            mat.node_tree.links.new(higher.outputs[0], lower.inputs[col_input], True)
        if higher_add is not None:
            add_out = layer_utils.get_alpha_output(context, index)
            mat.node_tree.links.new(higher_add.outputs[0], add_out, True)
    
    def execute(self, context):
        layer_list = context.object.active_material.layer_list
        index = context.object.active_material.layer_index
        
        self.delete_nodes(context)
        
        layer_list.remove(index)
        bpy.context.object.active_material.layer_index = min(max(0, index - 1), len(layer_list) - 1)
        
        return{'FINISHED'}