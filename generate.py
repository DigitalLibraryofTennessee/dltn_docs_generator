from repox.repox import Repox
import yaml
from tqdm import tqdm
from emoji import emojize
import requests
import arrow
from lxml import etree

settings = yaml.safe_load(open("config.yml", "r"))
repox_connection = Repox(settings["repox"], settings["username"], settings["password"])
in_dpla = requests.get(
    "https://raw.githubusercontent.com/dpla/ingestion/develop/profiles/tn.pjs"
).json()["sets"]
now = arrow.utcnow().to("US/Eastern").format("YYYY-MM-DD")
generate_total_mods = settings["generate_mods_count"]


class DLTN:
    def __init__(self, aggregator_id):
        self.providers = repox_connection.get_list_of_providers(aggregator_id, True)

    def generate_rst_page_for_each_provider(self):
        print(
            emojize(
                "\n\n\t:snake: Generating documentation for Digital Library of Tennessee providers: :snake:\n"
            )
        )
        for provider in tqdm(self.providers):
            with open(
                f"docs/providers/{provider['id']}.rst", "w+"
            ) as provider_rst_file:
                provider_rst_file.write(f'{provider["name"]}\n')
                provider_rst_file.write("=" * len(provider["name"]))
                provider_rst_file.write(f"\n\nDetails\n-------\n\n")
                provider_rst_file.write(self.__generate_details_section(provider))
                provider_rst_file.write(f"\n\nDatasets\n--------\n\n")
                provider_rst_file.write(
                    self.__generate_dataset_details_section(provider["id"])
                )

    @staticmethod
    def __generate_details_section(current_provider):
        total_records = repox_connection.count_records_from_provider(
            current_provider["id"]
        )
        return (
            f"\nEmail: {current_provider['email']}\n\nDescription: {current_provider['description']}\n\nOAI "
            f"endpoint: {current_provider['homepage']}\n\nTotal records in Repox: {total_records}\n\n"
            f"Page last updated: {now}"
        )

    @staticmethod
    def __generate_dataset_details_section(provider_id):
        dataset_details = ""
        for dataset in repox_connection.get_list_of_sets_from_provider(
            provider_id, True
        ):
            current_set = DataSet(dataset["dataSource"]["id"])
            dataset_details += f"{current_set.generate_rst_for_set()}\n\n"
        return dataset_details


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
            dataset_details += f"* **Source Directory**: {self.details['dataSource']['sourcesDirPath']}\n\n"
        elif self.details["dataSource"]["dataSetType"] == "OAI":
            dataset_details += (
                f"* **OAI Endpoint**: {self.details['dataSource']['oaiSourceURL']}?verb=ListRecords&set="
                f"{self.details['dataSource']['oaiSet']}&metadataPrefix="
                f"{self.details['dataSource']['metadataFormat']}\n"
                f"* **OAI Set**: {self.details['dataSource']['oaiSet']}\n"
                f"* **OAI MODS Records**: {total_mods}\n\n"
            )
        return dataset_details

    @staticmethod
    def __in_dpla(identifier):
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
        if len(token) == 1:
            self.token = f"&resumptionToken={token[0].text}"
            return
        else:
            self.status = "Done"
            return

    def list_records(self):
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
    DLTN("TNDPLAr0").generate_rst_page_for_each_provider()
