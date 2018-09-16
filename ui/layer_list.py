import bpy

class MATERIAL_UL_layerlist(bpy.types.UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):
        self.use_filter_show= False
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align = True)
            row.label(item.name)
            
            hide_icon = 'VISIBLE_IPO_ON'
            if item.hide:
                hide_icon = 'RESTRICT_VIEW_ON'
                    
            
            #row.prop(current_node, "name")
            row.prop(item, "hide", icon=hide_icon, text="", emboss=False)
            
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label("")