from repox.repox import Repox
import yaml
from tqdm import tqdm
from emoji import emojize
import requests
import arrow
from lxml import etree
import argparse

settings = yaml.safe_load(open("../config.yml", "r"))
repox_connection = Repox(settings["repox"], settings["username"], settings["password"])
dpla_ingest3_sets = requests.get(
    'https://raw.githubusercontent.com/DigitalLibraryofTennessee/dltn_ingestion3_config_generator/master/sets.yml'
).content
dpla_providers = yaml.safe_load(dpla_ingest3_sets)
in_dpla = []
for key, value in dpla_providers.items():
    for yaml_set in value:
        in_dpla.append(yaml_set)

now = arrow.utcnow().to("US/Eastern").format("YYYY-MM-DD")
generate_total_mods = settings["generate_mods_count"]


class DLTN:
    def __init__(self, aggregator_id):
        self.providers = repox_connection.get_list_of_providers(aggregator_id, True)

    def generate_rst_page_for_each_provider(self):
        """Iterates over providers from Repox and generates individual rst files.
        """
        print(
            emojize(
                "\n\n\t:snake: Generating documentation for Digital Library of Tennessee providers: :snake:\n"
            )
        )
        for provider in tqdm(self.providers):
            self._write_rst_file(provider)
        return

    def generate_rst_page_for_one_provider(self, provider_id):
        """Generate an rst page for one specific provider"""
        for provider in tqdm(self.providers):
            if provider_id == provider['id']:
                print(
                    emojize(
                        f"\n\n\t:snake: Generating documentation for {provider['name']}: :snake:\n"
                    )
                )
                self._write_rst_file(provider)
        return

    @staticmethod
    def __generate_details_section(current_provider):
        """Generates top-level details section about the provider of provider rst files.

        Requires a provider and ruturns a details section based on that provider.

        Args:
            current_provider (dict): a dict of metadata about a provider

        Returns:
            str: a string of text for the details section

        """
        total_records = repox_connection.count_records_from_provider(
            current_provider["id"]
        )
        return (
            f"\n**Email**: {current_provider['email']}\n\n**Description**: {current_provider['description']}\n\n**OAI "
            f"endpoint**: {current_provider['homepage']}\n\n**Total records in Repox**: {total_records}\n\n"
            f"**Page last updated**: {now}"
        )

    @staticmethod
    def __generate_dataset_details_section(provider_id):
        """Generates the datasets details sections of provider rst files.

        Requires a provider_id of a provider and returns markup for all the individual datasets in a provider rst.

        Args:
            provider_id (str): a string id that represents a provider

        Returns:
            str: a string of markup about all datasets of a provider

        """
        dataset_details = ""
        for dataset in repox_connection.get_list_of_sets_from_provider(
            provider_id, True
        ):
            current_set = DataSet(dataset["dataSource"]["id"])
            dataset_details += f"{current_set.generate_rst_for_set()}\n\n"
        return dataset_details

    def _write_rst_file(self, a_provider):
        with open(f"../docs/providers/{a_provider['id']}.rst", "w+") as provider_rst_file:
            provider_rst_file.write(f'{a_provider["name"]}\n')
            provider_rst_file.write("=" * len(a_provider["name"]))
            provider_rst_file.write(f"\n\nDetails\n-------\n\n")
            provider_rst_file.write(self.__generate_details_section(a_provider))
            provider_rst_file.write(f"\n\nDatasets\n--------\n\n")
            provider_rst_file.write(
                self.__generate_dataset_details_section(a_provider["id"])
            )
        return


class DataSet:
    def __init__(self, set_id):
        self.details = repox_connection.get_dataset_details(set_id)
        self.total_records = repox_connection.count_records_in_dataset(set_id)
        self.last_ingest_date = repox_connection.get_last_ingest_date_of_set(set_id)
        self.in_dpla = self.__in_dpla(set_id)

    def generate_rst_for_set(self):
        dataset_details = (
            f"{self.details['name']}\n\n* **Record Total**: {self.total_records}\n"
            f"* **In DPLA?**: {self.in_dpla}\n"
            f"* **Metadata format**: {self.details['dataSource']['metadataFormat']}\n"
            f"* **Last ingest date**: {self.last_ingest_date}\n"
            f"* **Dataset Type**: {self.details['dataSource']['dataSetType']}\n"
        )
        total_mods = 0
        if self.in_dpla is True and generate_total_mods is True:
            counter = OAIMODSCounter(self.details["dataSource"]["id"])
            counter.list_records()
            total_mods = counter.total_records
        if self.details["dataSource"]["dataSetType"] == "DIR":
            dataset_details += f"* **Source Directory**: {self.details['dataSource']['sourcesDirPath']}\n"
        elif self.details["dataSource"]["dataSetType"] == "OAI":
            dataset_details += (
                f"* **OAI Endpoint**: {self.details['dataSource']['oaiSourceURL']}?verb=ListRecords&set="
                f"{self.details['dataSource']['oaiSet']}&metadataPrefix="
                f"{self.details['dataSource']['metadataFormat']}\n"
                f"* **OAI Set**: {self.details['dataSource']['oaiSet']}\n"
            )
        dataset_details += f"* **Records Being Sent to DPLA**: {total_mods}\n\n"
        return dataset_details

    @staticmethod
    def __in_dpla(identifier):
        """Determines if a dataset is in DPLA.

        Args:
            identifier (str): the dataset_id of a dataset

        Returns:
            bool: True if it's in DPLA and False if it's not.

        """
        if identifier in in_dpla:
            return True
        else:
            return False


class OAIMODSCounter:
    def __init__(self, set_name):
        self.set_name = set_name
        self.oai_base = "http://dpla.lib.utk.edu/repox/OAIHandler"
        self.endpoint = (
            f"{self.oai_base}?verb=ListRecords&metadataPrefix=MODS&set={set_name}"
        )
        self.token = ""
        self.status = "In Progress"
        self.total_records = 0

    def process_token(self, token):
        """Modifies self.token and self.status based on a OAI resumption token.

        Args:
            token (list): A list with either a len of 0 or 1.  If len is 1, the value of index 0 should be a
            <Element {http://www.openarchives.org/OAI/2.0/}resumptionToken>

        """
        if len(token) == 1:
            self.token = f"&resumptionToken={token[0].text}"
        else:
            self.status = "Done"
        return

    def list_records(self):
        """Function to process the OAI PMH ListRecords protocol."""
        r = requests.get(f"{self.endpoint}")
        oai_document = etree.fromstring(r.content)
        self.process_token(
            oai_document.findall(
                ".//{http://www.openarchives.org/OAI/2.0/}resumptionToken"
            )
        )
        self.total_records += len(
            oai_document.findall(".//{http://www.openarchives.org/OAI/2.0/}metadata")
        )
        if self.status is not "Done":
            self.endpoint = f"{self.oai_base}?verb=ListRecords{self.token}"
            return self.list_records()
        else:
            return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Provider Reports for DLTN.")
    parser.add_argument(
        "-p", "--provider", dest="provider", required=False
    )
    args = parser.parse_args()
    if args.provider:
        DLTN("TNDPLAr0").generate_rst_page_for_one_provider(args.provider)
    else:
        DLTN("TNDPLAr0").generate_rst_page_for_each_provider()
