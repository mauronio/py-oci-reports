import oci

def get_signer_from_config(config):
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

class OCIClient:

    def __init__(self, config_filename = "~/.oci/config", profile_name = "DEFAULT"):

        config = oci.config.from_file(config_filename, profile_name)
        signer = get_signer_from_config(config)

        self.identity_service = oci.identity.IdentityClient(config, signer=signer)
        self.vcn_service = oci.core.VirtualNetworkClient(config, signer=signer)

        self.tenancy_compartment = self.identity_service.get_compartment(compartment_id=config["tenancy"])
        