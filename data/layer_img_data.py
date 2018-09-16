import bpy

class LayerImgData(bpy.types.PropertyGroup):
    """Data to be used each time layer is created."""

    width = bpy.props.IntProperty(
            name="Width",
            description = "Horizontal dimension",
            default=1024)
            
    height = bpy.props.IntProperty(
            name="Height",
            description = "Vertical dimension",
            default=1024)
    
    color = bpy.props.FloatVectorProperty(
            name="BG color",
            description='Color picker',
            subtype='COLOR',
            size=4,
            default=(0.5, 0.5, 0.5, 1),
            min=0.0,
            max=1.0)
                
    float = bpy.props.BoolProperty(
            name="32 bit",
            description="Create image with 32 bit floating point bit depth",
            default=False)
