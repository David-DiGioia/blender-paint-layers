import bpy


offset = 180


def get_input_of_type(node, type):
    for index, input in enumerate(node.inputs):
        if input.type == type:
            return index


def get_input_node(layer):
    nodes = bpy.context.object.active_material.node_tree.nodes
    layer_input = None
    try:
        l = nodes[layer.mix].inputs[1].links[0]
        layer_input = l.from_node
        bpy.context.object.active_material.node_tree.links.remove(l)
    except IndexError as e:
        layer_input = None
    return layer_input
    
    
def get_output_node(layer):
    nodes = bpy.context.object.active_material.node_tree.nodes
    layer_output = None
    try:
        l = nodes[layer.mix].outputs[0].links[0]
        layer_output = l.to_node
        bpy.context.object.active_material.node_tree.links.remove(l)
    except IndexError as e:
        print("Layer has no output. This should not occur unless user changed nodes directly.")
        print("Error: " + str(e))
    return layer_output


def offset_layer(layer, offset):
    nodes = bpy.context.object.active_material.node_tree.nodes
    nodes[layer.mix].location.x += offset
    nodes[layer.multiply].location.x += offset
    nodes[layer.img_tex].location.x += offset
    try:
        nodes[layer.add].location.x += offset
    except:
        pass

def get_alpha_output(context, index):
    mat = context.object.active_material
    nodes = mat.node_tree.nodes
    valid_layers = [x for i, x in enumerate(mat.layer_list) if i < index]
    for i, lay in reversed(list(enumerate(valid_layers))):
        if lay.add:
            return nodes[lay.add].inputs[0]
    return nodes[mat.layer_shaders.mix].inputs[0]
