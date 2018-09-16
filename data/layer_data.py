import bpy

class Layer(bpy.types.PropertyGroup):
    """Group of properties representing a layer in the list."""
    
    # Getters / Setters
    def hide_get(self):
        try:
            nodes = bpy.context.object.active_material.node_tree.nodes
            return nodes[self.mix].mute
        except KeyError as e:
            print("Can't find mix node for getting hide: " + self.mix)
            return True
    
    def hide_set(self, value):
        try:
            nodes = bpy.context.object.active_material.node_tree.nodes
            nodes[self.mix].mute = value
        except KeyError as e:
            print("Can't find mix node for setting hide: " + self.mix)
        
    # Properties
    name = bpy.props.StringProperty(
            name="Name",
            description = "Layer name",
            default="New Layer")
            
    hide = bpy.props.BoolProperty(
                name="Hide",
                description="Toggle layer visibility",
                default=False,
                get=hide_get,
                set=hide_set)
                
    mix = bpy.props.StringProperty(
                name="Mix Node Name",
                description="Node handles mixing between adjacent layers based on opacity")
                
    multiply = bpy.props.StringProperty(
                name="Multiply Node Name",
                description="Multiplies alpha, serves as opacity")
                
    img_tex = bpy.props.StringProperty(
                name="Image Texture Node Name",
                description="Image texture node being stored in the layer")
                
    texture = bpy.props.StringProperty(
                name="Image Texture Name",
                description="Image texture being stored in the layer")
                
    add = bpy.props.StringProperty(
                name="Add Node Name",
                description="Adds alpha to produce final alpha map")
                