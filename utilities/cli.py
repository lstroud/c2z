import csv
import dataclasses
from collections import defaultdict
import click


geo_cache = defaultdict(lambda: defaultdict(list))


@dataclasses.dataclass
class County:
    name: str
    state: str

    def matches(self, oname: str):
        return self.name.lower() in oname.lower() or self.name.lower() == oname.lower()


def load_cache():
    reader = csv.reader(open('ZIP-COUNTY-FIPS_2017-06.csv', 'r'))
    for data in reader:
        state_list = geo_cache[data[2]]
        county_list = state_list[data[1]]
        zip_list = county_list.append(data[0])


def zipcodes_for(county: County):
    state_data = geo_cache[county.state]
    for key in state_data.keys():
        if county.matches(key):
            return state_data[key]
    print(f"ERROR: {county} not found.")


def zipcodes_for_list(counties: [County]):
    zips = []
    for county in counties:
        _zips = zipcodes_for(county)
        if _zips:
            zips.extend(_zips)
    return zips


@click.command()
@click.option("--state", "-s",  type=str, required=True, help="state")
@click.argument("counties", type=str)
def main(state: str, counties: str) -> None:
    """ COUNTIES: comma delimited list of county names """
    load_cache()
    _counties = []
    for county_name in counties.strip().split(','):
        county = County(name=county_name.strip(), state=state.strip())
        _counties.append(county)
    zip_list = zipcodes_for_list(_counties)
    zip_str = ','.join(zip_list)
    print(zip_str)
