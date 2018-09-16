# blender-paint-layers
This addon creates a layering system for Blender's Texture Paint mode. Adding, removing, reordering, and any other operation
upon these layers will update that material's node setup to reflect the changes you make in the layer panel of Texture Paint mode.
<br/><br/>
It should be noted that tampering with nodes generated from the blender-paint-layers addon is currently undefined behavior and will
likely break something if you try to use the layer gui afterwords.

<h2>Current Version Has:</h2>
  <ul>
    <li>Specify layer dimensions and bit depth</li>
    <li>Add/Remove layers</li>
    <li>Reorder layers</li>
    <li>Toggle layer visibility</li>
    <li>Set layer blend mode</li>
    <li>Set layer opacity</li>
  </ul>
  
  <h2>Planned Features:</h2>
  <ul>
    <li>Layer groups</li>
    <li>Alpha inheritance</li>
    <li>Import/Export OpenRaster (.ora)</li>
    <li>Bake layers into single texture</li>
  </ul>
