# Biome Extensions
> Standard that modifies the vanilla biome definitions to use tags for placed features and carvers. This allows multiple data packs to add features to a vanilla biome and maintain compatibility.

*Currently targeting: 1.19*

## Usage
1. Download or clone this repository
2. Copy and merge the `data` folder with your project, or use it to start a new project.
3. You SHOULD NOT make any changes to the `minecraft/worldgen/biome` files, otherwise you risk breaking compatibility.
4. You SHOULD NOT delete entries from the `minecraft/tags/worldgen` files, since another data pack using this standard would cause the entries to be re-added. To remove or disable a feature/carver you SHOULD overwrite it with an empty feature/carver.
5. You MAY add entries to the `minecraft/tags/worldgen` files to add a feature/carver to a biome.
6. You MAY add extra files to the `minecraft/tags/worldgen` folders, as indicated by the optional tag entries (eg. `minecraft/tags/worldgen/placed_feature/vegetal_decoration/in_overworld.json`).

### Adding your own biome
1. Add your own biome to your custom namespace. To allow other data packs to add features, use one of the vanilla biome files as a template.
2. Add the corresponding tags for features and carvers to your own namespace (eg. `mypack/tags/worldgen/placed_feature/vegetal_decoration/in_biome/mybiome.json`).
3. Include the optional tag entry `{"id": "#minecraft:vegetal_decoration/in_overworld", "required": false}` at the start.
4. Add any number of vanilla or custom features afterwards.

### Adding features to existing biomes
1. Add your feature to your custom namespace.
2. If you want to add the feature to a whole dimension create a tag `minecraft/tags/worldgen/placed_feature/vegetal_decoration/in_overworld.json` and add your feature's ID to it.
3. If you want to add the feature to one or more individual biomes, locate the corresponding files in `minecraft/tags/worldgen/placed_feature` and add your feature's ID to the bottom.

## Credits
This standard came forward after much debate and feedback from the Minecraft Configs community.
