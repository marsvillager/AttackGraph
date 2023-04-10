import getpass

from db.attack_process import insert_json_to_neo4j, delete_duplicate_node, delete_all
from tools.prepare import update_attack, update_d3fend, connect_to_neo4j
from tools.config import Config


if __name__ == '__main__':
    # Update data source.
    update_attack()
    update_d3fend()

    # Prompt the user for the password without showing the input.
    # ⚠️：Try to use an actual terminal, or will don't work.
    password = getpass.getpass("Please input the password of neo4j: ")

    # Call the function to connect to Neo4j.
    driver = connect_to_neo4j(Config.NEO4J_URL, "neo4j", password)

    # Use the driver to execute queries.
    # with driver.session() as session:
    #     result = session.run("MATCH (n) RETURN count(n) as count")
    #     print(result.single()["count"])

    delete_all(driver)

    # Call the function to insert JSON data into Neo4j
    insert_json_to_neo4j(driver, "./data/attack/ics-attack/ics-attack.json",
                         Config.CREATE_NODE["basic"], Config.CREATE_REL["basic"])
    delete_duplicate_node(driver, "./data/attack/ics-attack/ics-attack.json")

    insert_json_to_neo4j(driver, "./data/attack/mobile-attack/mobile-attack.json",
                         Config.CREATE_NODE["basic"], Config.CREATE_REL["basic"])
    delete_duplicate_node(driver, "./data/attack/mobile-attack/mobile-attack.json")

    insert_json_to_neo4j(driver, "./data/attack/enterprise-attack/enterprise-attack.json",
                         Config.CREATE_NODE["basic"], Config.CREATE_REL["basic"])
    delete_duplicate_node(driver, "./data/attack/enterprise-attack/enterprise-attack.json")
