from repox.repox import Repox
import yaml
from tqdm import tqdm
from emoji import emojize

settings = yaml.load(open("config.yml", "r"))
repox_connection = Repox(settings["repox"], settings["username"], settings["password"])


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
            f"endpoint: {current_provider['homepage']}\n\nTotal records: {total_records}"
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

    # TODO Add OAI Record Counter
    def generate_rst_for_set(self):
        dataset_details = (
            f"{self.details['name']}\n\n* **Record Total**: {self.total_records}\n"
            f"* **Metadata format**: {self.details['dataSource']['metadataFormat']}\n"
            f"* **Last ingest date**: {self.last_ingest_date}\n"
            f"* **Dataset Type**: {self.details['dataSource']['dataSetType']}\n"
        )
        if self.details["dataSource"]["dataSetType"] == "DIR":
            dataset_details += f"* **Source Directory**: {self.details['dataSource']['sourcesDirPath']}\n\n"
        elif self.details["dataSource"]["dataSetType"] == "OAI":
            dataset_details += (
                f"* **OAI Endpoint**: {self.details['dataSource']['oaiSourceURL']}\n"
                f"* **OAI Set**: {self.details['dataSource']['oaiSet']}\n"
                f"* **OAI MODS Records**: \n\n"
            )
        return dataset_details


if __name__ == "__main__":
    DLTN("TNDPLAr0").generate_rst_page_for_each_provider()
