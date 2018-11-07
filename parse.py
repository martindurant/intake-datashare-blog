import json
import requests
import yaml


list_url = "https://www.opendataphilly.org/api/3/action/package_list"
pack_url = "https://www.opendataphilly.org/api/action/package_show?id={}"


def get_list():
    r = requests.get(list_url)
    return r.json()['result']


def pack_csv(pack):
    r = requests.get(pack_url.format(pack))
    try:
        j = r.json()
    except (ValueError, TypeError):
        # didn't get JSON back
        return
    if j['success'] is not True or 'result' not in j:
        # didn't get resource back
        return
    res = j['result']
    for part in res.get('resources', []):
        if part['format'] == "CSV":
            metadata = {'license': res['license_title'],
                        'metadata_modified': res['metadata_modified'],
                        'tags': [t['display_name'] for t in
                                 res.get('tags', [])],
                        'groups': [g['name'] for g in res.get('groups', [])],
                        }
            description = '\n'.join([res['title'], res['notes']])
            urlpath = part['url']
            return {'args': {'urlpath': urlpath,
                             'storage_options': {'block_size': 0},
                             'csv_kwargs': {'blocksize': None}},
                    'description': description,
                    'metadata': metadata,
                    'driver': 'csv',
                    'cache': [{'argkey': urlpath,
                               'regex': urlpath,
                               'type': 'file'}]
                    }


def parse_n(outfile, n=50):
    packages = get_list()
    sources = {}
    for p in packages[:n]:
        out = pack_csv(p)
        if out is not None:
            sources[p.replace('-', '_')] = out
    yaml.dump({'sources': sources},
              open(outfile, 'w'), default_flow_style=False)
