import click
import json
import os
import re
import requests
import shutil
import zipfile

STEPS = [
	'raw_generation',
	'lakes',
	'local_modifications',
	'underground_structures',
	'surface_structures',
	'strongholds',
	'underground_ores',
	'underground_decoration',
	'fluid_springs',
	'vegetal_decoration',
	'top_layer_modification',
]

NETHER_BIOMES = ['basalt_deltas', 'crimson_forest', 'nether_wastes', 'soul_sand_valley', 'warped_forest']
END_BIOMES = ['end_barrens', 'end_highlands', 'end_midlands', 'small_end_islands', 'the_end']
MISC_BIOMES = ['the_void']

@click.command()
@click.option('--version', '-v')
def main(version: str):
	shutil.rmtree('tmp', ignore_errors=True)
	shutil.rmtree('data', ignore_errors=True)
	os.makedirs('tmp', exist_ok=True)
	os.makedirs('data', exist_ok=True)

	content = requests.get(f'https://github.com/misode/mcmeta/archive/refs/tags/{version}-data-json.zip').content
	with open('tmp/data-json.zip', 'wb') as f:
		f.write(content)
	zip = zipfile.ZipFile('tmp/data-json.zip')

	for file in zip.namelist():
		if match := re.match(f'mcmeta-{version}-data-json/data/minecraft/worldgen/biome/([a-z0-9_]+).json$', file):
			biome_id = match[1]
			zip.extract(file, path='tmp')
			with open(f'tmp/mcmeta-{version}-data-json/data/minecraft/worldgen/biome/{biome_id}.json', 'r') as f:
				biome = json.load(f)

			dimension_id = get_dimension(biome_id)

			for i, step_name in enumerate(STEPS):
				if len(biome['features']) < len(STEPS):
					biome['features'] += [[] for _ in range(len(STEPS) - len(biome['features']))]
				features: list = biome['features'][i]
				if type(features) == str:
					features = [features]
				if dimension_id is not None:
					features.insert(0, { "id": f'#minecraft:{step_name}/in_{dimension_id}', "required": False })

				write_json(f'tags/worldgen/placed_feature/{step_name}/in_biome/{biome_id}', {
					'replace': False,
					'values': features,
				})
				biome['features'][i] = f'#minecraft:{step_name}/in_biome/{biome_id}'

			for carver_step in ['air', 'liquid']:
				carvers = biome['carvers'].get(carver_step, [])
				if type(carvers) == str:
					carvers = [carvers]
				if dimension_id is not None:
					carvers.insert(0, { "id": f'#minecraft:{carver_step}/in_{dimension_id}', "required": False })
				write_json(f'tags/worldgen/configured_carver/{carver_step}/in_biome/{biome_id}', {
					'replace': False,
					'values': carvers,
				})
				biome['carvers'][carver_step] = f'#minecraft:{carver_step}/in_biome/{biome_id}'

			write_json(f'worldgen/biome/{biome_id}', biome)


def write_json(path: str, contents):
	dir = path[:path.rindex('/')]
	os.makedirs(f'data/minecraft/{dir}', exist_ok=True)
	with open(f'data/minecraft/{path}.json', 'w') as f:
		json.dump(contents, f, indent=2)
		f.write('\n')


def get_dimension(biome_id: str):
	if biome_id in NETHER_BIOMES:
		return 'nether'
	elif biome_id in END_BIOMES:
		return 'end'
	elif biome_id not in MISC_BIOMES:
		return 'overworld'
	else:
		return None


if __name__ == '__main__':
	main()
