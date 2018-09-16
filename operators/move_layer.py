import bpy
from .. import layer_utils


class LAYER_OT_movelayer(bpy.types.Operator):
    """Move a layer in the list."""
    
    bl_idname = 'layer_list.move_layer'
    bl_label = 'Move a layer in the list'
    
    direction = bpy.props.EnumProperty(items=(('UP', 'Up', ""), ('DOWN', 'Down', ""),))
    
    
    @classmethod
    def poll(cls, context):
        return bpy.context.object.active_material.layer_list
        
    
    def swap_loc(self, layer1, layer2):
        nodes = bpy.context.object.active_material.node_tree.nodes
        
        layer1_pos = nodes[layer1.mix].location.x
        layer2_pos = nodes[layer2.mix].location.x
        
        nodes[layer1.mix].location.x = layer2_pos
        nodes[layer2.mix].location.x = layer1_pos
        nodes[layer1.multiply].location.x = layer2_pos
        nodes[layer2.multiply].location.x = layer1_pos
        nodes[layer1.img_tex].location.x = layer2_pos
        nodes[layer2.img_tex].location.x = layer1_pos
        nodes[layer1.add].location.x = layer2_pos
        nodes[layer2.add].location.x = layer1_pos
        
    
    def move_nodes(self, index, neighbor):
        """Move nodes that correspond to layer."""
        
        list = bpy.context.object.active_material.layer_list
        tree = bpy.context.object.active_material.node_tree
        nodes = tree.nodes
        
        if neighbor < 0 or neighbor >= len(list):
            return
        
        higher_index = index
        lower_index = neighbor
        if neighbor > index:
            higher_index = neighbor
            lower_index = index
            
        # Make references and remove links
        to_higher = list[lower_index]
        to_lower = list[higher_index]
        to_higher_node = nodes[to_higher.mix]
        to_lower_node = nodes[to_lower.mix]
        high_low_link = nodes[to_lower.mix].outputs[0].links[0]
        tree.links.remove(high_low_link)
        tree.links.remove(nodes[to_higher.add].outputs[0].links[0])
        tree.links.remove(nodes[to_lower.add].outputs[0].links[0])
        
        higher = layer_utils.get_input_node(to_lower)
        lower = layer_utils.get_output_node(to_higher)
        higher_add = None
        try:
            higher_add = nodes[to_lower.add].inputs[0].links[0].from_node
        except IndexError:
            higher_add = None
        
        self.swap_loc(to_higher, to_lower)
        
        # Make new links
        if higher is not None:
            col_input = layer_utils.get_input_of_type(to_higher_node, 'RGBA')
            tree.links.new(higher.outputs[0], to_higher_node.inputs[col_input], True)
        col_input = layer_utils.get_input_of_type(lower, 'RGBA')
        tree.links.new(to_lower_node.outputs[0], lower.inputs[col_input], True)
        tree.links.new(to_higher_node.outputs[0], to_lower_node.inputs[1], True)
        
        list.move(neighbor, index)
        self.link_add_nodes(lower_index, higher_index, higher_add)
        
    
    def link_add_nodes(self, low_index, high_index, higher):
        tree = bpy.context.object.active_material.node_tree
        nodes = tree.nodes
        layer_list = bpy.context.object.active_material.layer_list
        
        low_out = layer_utils.get_alpha_output(bpy.context, low_index)
        high_out = layer_utils.get_alpha_output(bpy.context, high_index)
        low_index_node = nodes[layer_list[low_index].add]
        high_index_node = nodes[layer_list[high_index].add]
        
        tree.links.new(low_index_node.outputs[0], low_out, True)
        tree.links.new(high_index_node.outputs[0], high_out, True)
        if higher is not None:
            tree.links.new(higher.outputs[0], high_index_node.inputs[0], True)
    
    
    def move_index(self, index):
        """Move index of a layer render que while clamping it."""
        
        list = bpy.context.object.active_material.layer_list
        
        list_length = len(list) - 1 # (index starts at 0)
        new_index = index + (-1 if self.direction == 'UP' else 1)
        
        bpy.context.object.active_material.layer_index = max(0, min(new_index, list_length))
        
        
    def execute(self, context):
        
        index = bpy.context.object.active_material.layer_index
        list = bpy.context.object.active_material.layer_list  
        
        neighbor = index + (-1 if self.direction == 'UP' else 1)
        self.move_nodes(index, neighbor)
        self.move_index(index)
        
        return {'FINISHED'}
    