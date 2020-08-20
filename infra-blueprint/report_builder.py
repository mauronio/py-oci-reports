def build_compartment_tree(oci_client, compartment_ocid, compartment_tree, parent_compartment_name = None):

    compartment_response = oci_client.identity_service.get_compartment(compartment_id = compartment_ocid)
    compartment = compartment_response.data

    if not parent_compartment_name is None:
        compartment_tree.append(
            [
                compartment.name,
                compartment.description,
                parent_compartment_name
            ]
        )

    child_compartments_response = oci_client.identity_service.list_compartments(compartment_ocid)
    child_compartments = child_compartments_response.data

    for child_compartment in child_compartments:
        build_compartment_tree(oci_client, child_compartment.id, compartment_tree, parent_compartment_name=compartment.name)


def write_table(writers, report_name, title, column_list, row_list):

    for writer in writers:
        writer.write_table(
            report_name,
            title,
            column_list,
            row_list
        )


def process_compartment_tree(report_data, oci_client, writers):

    root_compartment_ocid = report_data['compartment-ocid']

    compartment_tree = []
    build_compartment_tree(oci_client, root_compartment_ocid, compartment_tree)

    title = 'Step 1: Compartments'
    column_list = [
        {   
            'name': 'Compartment name',
            'description': 'Compartment name'
        },
        {   
            'name': 'Description',
            'description': 'Compartment description'
        },
        {   
            'name': 'Parent Compartment',
            'description': 'Parent Compartment name'
        }
    ]
    row_list = compartment_tree

    write_table(
        writers,
        report_data['name'],
        title, 
        column_list, 
        row_list
    )

def process_vcn(report_data, oci_client, writers):

    network_compartment_ocid = report_data['network-compartment-ocid']

    title = 'Step 2: VCN'
    column_list = [
        {   
            'name': 'VCN name',
            'description': 'VCN name'
        },
        {   
            'name': 'CIDR',
            'description': 'CIDR'
        },
        {   
            'name': 'DNS Label',
            'description': 'DNS Label'
        }
    ]

    row_list = []
    vcn_list_response = oci_client.vcn_service.list_vcns(network_compartment_ocid)
    vcn_list = vcn_list_response.data
    for vcn in vcn_list:
        row_list.append(
            [
                vcn.display_name,
                vcn.cidr_block,
                vcn.dns_label
            ]
        )

    write_table(
        writers,
        report_data['name'],
        title, 
        column_list, 
        row_list
    )
