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
		if match := re.match('.*minecraft/worldgen/biome/([a-z0-9_]+).json$', file):
			biome_id = match[1]
			zip.extract(file, path='tmp')
			with open(f'tmp/mcmeta-{version}-data-json/data/minecraft/worldgen/biome/{biome_id}.json', 'r') as f:
				biome = json.load(f)

			for i in range(0, len(biome['features'])):
				step_name = STEPS[i]
				placed_features = biome['features'][i]
				biome['features'][i] = f'#minecraft:{step_name}/in_biome/{biome_id}'

				tag_contents = {
					'replace': False,
					'values': placed_features,
				}
				tag_folder = f'data/minecraft/tags/worldgen/placed_feature/{step_name}/in_biome'
				os.makedirs(tag_folder, exist_ok=True)
				with open(f'{tag_folder}/{biome_id}.json', 'w') as f:
					json.dump(tag_contents, f, indent=2)

			for carver_step in biome['carvers']:
				carvers = biome['carvers'][carver_step]
				biome['carvers'][carver_step] = f'#minecraft:{carver_step}/in_biome/{biome_id}'

				tag_contents = {
					'replace': False,
					'values': carvers,
				}
				tag_folder = f'data/minecraft/tags/worldgen/configured_carver/{carver_step}/in_biome'
				os.makedirs(tag_folder, exist_ok=True)
				with open(f'{tag_folder}/{biome_id}.json', 'w') as f:
					json.dump(tag_contents, f, indent=2)

			biome_folder = f'data/minecraft/worldgen/biome'
			os.makedirs(biome_folder, exist_ok=True)
			with open(f'{biome_folder}/{biome_id}.json', 'w') as f:
				json.dump(biome, f, indent=2)

if __name__ == '__main__':
	main()
