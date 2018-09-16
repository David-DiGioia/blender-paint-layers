import bpy

class LayerShaders(bpy.types.PropertyGroup):
    """References to all shaders that layers depends on."""

    diffuse = bpy.props.StringProperty(
                name="Diffuse",
                description = "Diffuse Shader Node")
            
    transparent = bpy.props.StringProperty(
                    name="Transparent",
                    description = "Transparent Shader Node")
            
    mix = bpy.props.StringProperty(
            name="mix",
            description = "Mix Shader Node")
