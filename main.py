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


def zipcodes_for_list(counties: [County]):
    zips = []
    for county in counties:
        zips.extend(zipcodes_for(county))
    return zips


@click.command()
@click.option("--state", "-s",  type=str, required=False, help="state")
@click.option("--counties", "-c", type=str, required=False, help="comma delimited list of counties")
def cli(state: str, counties_str: str) -> None:
    counties = [County]
    for county_name in counties_str.strip().split(','):
        counties.append(County(county_name, state))
    zip_list = zipcodes_for_list(counties)
    zip_str = ', '.join(zip_list)
    print(zip_str)

# if __name__ == '__main__':
#     load_cache()
#     # print(geo_cache)
#     zips = zipcodes_for_list([County('Hampden', 'MA'), County('Hampshire', 'MA')])
#     print(zips)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
