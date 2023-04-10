import json


def extract_values(data, keys: list):
    """
    Recursively extract values from a nested dictionary using a list of keys.

    :param data: a nested dictionary
    :param keys: e.g. ["external_references", "list", "external_id"],
                 "list" means the type of second layer in data is list
    :return: value correspond with keys
    """
    if len(keys) == 1:
        return data.get(keys[0])
    else:
        if isinstance(data, dict) and keys[0] in data:
            return extract_values(data[keys[0]], keys[1:])
        elif isinstance(data, list):
            # if type(data) == list, it will be unable to traverse the list
            # so need to add extra key to indicate that this layer is list
            # add extra key at will, e.g.list, it will not really be used because in code `keys[1:0]` it will be passed
            result: list = [extract_values(item, keys[1:]) for item in data]
            return next(item for item in result if item is not None)
        else:
            return None


def delete_all(driver) -> None:
    """
    Delete all nodes and relationships in neo4j.

    :param driver: connect to neo4j
    :return: none
    """
    # Start a session.
    with driver.session() as session:
        session.run('MATCH (n) DETACH DELETE (n)')


def insert_json_to_neo4j(driver, json_file_path: str, properties: list[list], relationships: list[list]) -> None:
    """
    Define function to insert JSON data into Neo4j.

    :param driver: connect to neo4j
    :param json_file_path: location of json file
    :param properties: properties that will be used to compose a whole node
    :param relationships: properties that will be used to build the relationship between node A and node B
    :return: none
    """
    # Open JSON file.
    with open(json_file_path) as f:
        data = json.load(f)['objects']

    # Start a session.
    with driver.session() as session:
        # Insert each node into Neo4j.
        for node in data:
            if 'x_mitre_deprecated' in node and node['x_mitre_deprecated'] is True:
                continue
            if node['type'] == 'relationship':
                continue

            command: str = "CREATE (n"
            domains: list[str] = extract_values(node, properties[0])
            if domains is not None:
                for domain in domains:
                    command += ":" + domain.replace('-', '_')

            command += "{"

            for item in properties[1:]:
                value: str = extract_values(node, item)
                if value is not None:
                    if command[-1] != '{':
                        command += ","
                    command += item[-1] + ':"' + value.replace('"', "'").replace('\\', '\\\\') + '"'

            command += "})"
            print(command)
            session.run(command)

        # Insert each relationship into Neo4j.
        for rel in data:
            if 'x_mitre_deprecated' in rel and rel['x_mitre_deprecated'] is True:
                continue

            if rel['type'] == 'relationship':
                command: str = 'MATCH (a),(b) WHERE a.id = "' + extract_values(rel, relationships[0]) + \
                               '" AND b.id = "' + extract_values(rel, relationships[1]) + \
                               '" CREATE (a)-[r:' + extract_values(rel, relationships[2]).replace('-', '_') + '{'

                for relationship in relationships[3:]:
                    val: str = extract_values(rel, relationship)
                    if val is not None:
                        if command[-1] != '{':
                            command += ","
                        command += relationship[0] + ':"' + val.replace('"', "'").replace('\\', '\\\\') + '"'

                # desc: str = extract_values(rel, relationships[3])
                # if desc is not None:
                #     command += '{' + relationships[3][0] + ':"' + desc.replace('"', "'") + '"}'

                command += '}]->(b)'
                print(command)
                session.run(command)

    # Close the driver connection.
    driver.close()


def delete_duplicate_node(driver, json_file_path: str):
    """
    Delete duplicate nodes in Neo4j.

    :param driver: connect to neo4j
    :param json_file_path: location of json file
    """
    # Open JSON file.
    with open(json_file_path) as f:
        data = json.load(f)['objects']

    # Start a session.
    with driver.session() as session:
        for item in data:
            if 'x_mitre_deprecated' in item and item['x_mitre_deprecated'] is True:
                continue
            if item['type'] == 'relationship':
                continue

            id: str = extract_values(item, ["id"])

            res: list = session.run('MATCH (n{id:"' + id + '"}) RETURN count(n)').data()
            if res[0]['count(n)'] > 1:
                # Find the most import node.(decide by relationships)
                node_list: list = session.run('MATCH (n{id:"' + id + '"}) RETURN id(n)').data()
                rel: list = []
                for node in node_list:
                    tmp: list = session.run('MATCH (n)-[r]-(m) WHERE id(n) = ' +
                                            str(node['id(n)']) + ' RETURN id(n),count(m)').data()
                    if len(tmp) == 0:
                        tmp = [{'id(n)': node['id(n)'], 'count(m)': 0}]
                    rel.append(tmp[0])
                rel.sort(key=lambda x: x['count(m)'], reverse=True)  # sort by count(relationships)
                delete_nodes: list[int] = [node['id(n)'] for node in rel[1:]]
                # Delete nodes.
                for node in delete_nodes:
                    # with relationship
                    session.run('MATCH (n)-[r]-(m) WHERE id(n) = ' + str(node) + ' DELETE n,r')
                    # single node
                    session.run('MATCH (n) WHERE id(n) = ' + str(node) + ' DELETE n')
