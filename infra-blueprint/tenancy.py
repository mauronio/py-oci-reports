import oci
import json

# get the config from file for the DEFAULT profile

config = oci.config.from_file("~/.oci/config", "DEFAULT")

def generate_signer_from_config(config):
    # Generate the signer for the API calls using the info from the config file
    signer = oci.signer.Signer(
        tenancy=config["tenancy"],
        user=config["user"],
        fingerprint=config["fingerprint"],
        private_key_file_location=config.get("key_file"),
        # pass_phrase is optional and can be None
        pass_phrase=oci.config.get_config_value_or_default(
            config, "pass_phrase"),
        # private_key_content is optional and can be None
        private_key_content=config.get("key_content")
    )
    
    return signer

# generate the signer
signer = generate_signer_from_config(config)

### Let's call some APIs ###

# initialize the IdentityClient
identity_client = oci.identity.IdentityClient(config, signer=signer)
functionsmgmt_client = oci.functions.FunctionsManagementClient(config, signer=signer)

applications = functionsmgmt_client.list_applications('ocid1.compartment.oc1..aaaaaaaaeyc6bi6rluu3slsfscrohoc76r74ny233uphrggkeedlvqmvrcla')
for application in applications.data:
    print ('Application', json.dumps(json.loads(str(application)), indent=4))

# get the tenancy info
tenancy_data = identity_client.get_tenancy(config["tenancy"]).data
print("My tenancy name is",  tenancy_data.name)

# get the list of all the regions the tenancy is subscribed to
regions = identity_client.list_region_subscriptions(config["tenancy"]).data
print("These are all the OCI regions I am subscribed to:", regions)
