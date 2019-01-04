from repox.repox import Repox
import yaml

settings = yaml.load(open("config.yml", "r"))
repox_connection = Repox(settings["repox"], settings["username"], settings["password"])


class DLTN:
    def __init__(self, aggregator_id):
        self.providers = repox_connection.get_list_of_providers(aggregator_id, True)

    def generate_rst_page_for_each_provider(self):
        for provider in self.providers:
            with open(f"temp_docs/{provider['id']}.rst", "w+") as provider_rst_file:
                provider_rst_file.write(f'{provider["name"]}\n')
                provider_rst_file.write("=" * len(provider["name"]))
                provider_rst_file.write(f"\n\nDetails\n-------\n\n")
                provider_rst_file.write(
                    f"\nEmail: {provider['email']}\n\nDescription: {provider['description']}\n\nOAI endpoint: "
                    f"{provider['homepage']}"
                )


if __name__ == "__main__":
    DLTN("TNDPLAr0").generate_rst_page_for_each_provider()
