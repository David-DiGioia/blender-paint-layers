import bpy
from .. import layer_utils


def is_layer_node(node, name):
    return node.name[:len(name)] == name


def setup_output(material, tree, offset):
    mat_output = None
    for node in tree.nodes:
        if node.type == 'OUTPUT_MATERIAL':
            mat_output = node
            break
    if not mat_output:
        mat_output = tree.nodes.new('ShaderNodeOutputMaterial')
    
    # Make shaders
    diffuse = tree.nodes.new('ShaderNodeBsdfDiffuse')
    diffuse.name = "LAYER_DIFFUSE"
    material.layer_shaders.diffuse = diffuse.name
    
    transparent = tree.nodes.new('ShaderNodeBsdfTransparent')
    transparent.name = "LAYER_TRANSPARENT"
    material.layer_shaders.transparent = transparent.name
    
    mix = tree.nodes.new('ShaderNodeMixShader')
    mix.name = "LAYER_MIX"
    mix.inputs[0].default_value = 1
    material.layer_shaders.mix = mix.name
    
    # Link shaders
    tree.links.new(transparent.outputs[0], mix.inputs[1], True)
    tree.links.new(diffuse.outputs[0], mix.inputs[2], True)
    tree.links.new(mix.outputs[0], mat_output.inputs[0], True)
    
    # Position shaders
    mix.location.x = mat_output.location.x - offset
    mix.location.y = mat_output.location.y
    transparent.location.x = mix.location.x - offset
    transparent.location.y = mix.location.y
    diffuse.location.x = transparent.location.x
    diffuse.location.y = transparent.location.y - 75


def make_nodes(operator, context, layer, img):
    tree = bpy.context.object.active_material.node_tree
    offset_x = layer_utils.offset
    
    mat = context.object.active_material
    if not mat.layer_shaders.diffuse \
    or not mat.layer_shaders.transparent \
    or not mat.layer_shaders.mix:
        setup_output(mat, tree, offset_x)
    else:
        try:
            tree.nodes[mat.layer_shaders.diffuse]
        except KeyError as e:
            setup_output(mat, tree, offset_x)
    
    shader = tree.nodes[mat.layer_shaders.diffuse]
    current_node = shader
    
    # Find first node in layer tree that has no connected input
    col_input = 0
    try:
        while current_node.inputs[col_input].is_linked:
            current_node = current_node.inputs[col_input].links[0].from_node
            col_input = layer_utils.get_input_of_type(current_node, 'RGBA')
    except TypeError as e:
        print("Node in chain has no color input. Try deleting extra nodes you've added to the chain.")
        print("Error: " + str(e))
            
    # Mix
    mix_node = tree.nodes.new('ShaderNodeMixRGB')
    mix_node.inputs[1].default_value[3] = 0
    mix_node.name = "LAYER_MIX"
    layer.mix = mix_node.name
    
    tree.links.new(mix_node.outputs[0], current_node.inputs[col_input], True)
    mix_node.location.x = current_node.location.x - offset_x
    mix_node.location.y = current_node.location.y
    
    # Multiply
    mult_node = tree.nodes.new('ShaderNodeMath')
    mult_node.operation = 'MULTIPLY'
    mult_node.inputs[1].default_value = 1
    mult_node.name = "LAYER_MULT"
    layer.multiply = mult_node.name
    
    tree.links.new(mult_node.outputs[0], mix_node.inputs[0], True)
    mult_node.location.x = mix_node.location.x
    mult_node.location.y = mix_node.location.y - 170
    
    # Image Texture
    img_node = tree.nodes.new('ShaderNodeTexImage')
    img_node.name = "LAYER_IMG"
    img_node.image = img
    layer.img_tex = img_node.name
    
    tree.links.new(img_node.outputs[0], mix_node.inputs[2], True)
    tree.links.new(img_node.outputs[1], mult_node.inputs[0], True)
    img_node.location.x = mult_node.location.x
    img_node.location.y = mult_node.location.y - 153
    
    # Add
    add_node = tree.nodes.new('ShaderNodeMath')
    add_node.operation = 'ADD'
    add_node.inputs[0].default_value = 0
    add_node.use_clamp = True
    add_node.name = "LAYER_ADD"
    layer.add = add_node.name
    
    add_output = layer_utils.get_alpha_output(context, len(mat.layer_list) - 1)
    
    tree.links.new(add_node.outputs[0], add_output, True)
    tree.links.new(mult_node.outputs[0], add_node.inputs[1], True)
    add_node.location.x = mix_node.location.x
    add_node.location.y = mix_node.location.y + 155


class LAYER_OT_newlayer(bpy.types.Operator):
    """Add a new layer to the material"""
    
    bl_idname = 'layer_list.new_layer'
    bl_label = "Add a new layer"
    
    @classmethod
    def poll(cls, context):
        return bpy.context.object.active_material
    
    def execute(self, context):        
        layer_list = context.object.active_material.layer_list
        img_data = context.object.active_material.layer_img_data
        
        if not context.object.active_material.use_nodes:
            context.object.active_material.use_nodes = True
        
        col = (0, 0, 0, 0)
        if not layer_list:
            col = img_data.color
        
        img = bpy.data.images.new(name='Layer.000', width=img_data.width, height=img_data.height,
                            alpha=True, float_buffer=img_data.float)
        img.generated_color = col
        
        new_layer = layer_list.add()
        new_layer.name = "Layer " + str(len(layer_list) - 1)
        new_layer.texture = img.name
        make_nodes(self, context, new_layer, img)
        
        layer_index = bpy.context.object.active_material.layer_index
        context.object.active_material.layer_index = len(layer_list) - 1
        
        move_up_count = len(layer_list) - max(layer_index, 0) - 1
        for i in range(move_up_count):
            bpy.ops.layer_list.move_layer(direction='UP')
        
        
        
        
        return {'FINISHED'}
    