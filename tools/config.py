import os


class Config:
    """
    Variables.
    """
    BASE_DIR: str = os.path.dirname(os.path.dirname(__file__))

    ATTACK_URL: str = "https://github.com/mitre/cti.git"

    MITRE_ATTACK_DATA_PATH: str = BASE_DIR + "/data/attack/"

    D3FEND_URL: str = "https://github.com/d3fend/d3fend.git"

    D3FEND_DATA_PATH: str = BASE_DIR + "/data/d3fend/"

    NEO4J_URL: str = "bolt://localhost:7687"

    CREATE_NODE: dict = {
        "basic": [["x_mitre_domains"], ["type"], ["name"], ["id"],
                  ["external_references", "list", "external_id"], ["description"]]
    }

    CREATE_REL: dict = {
        "basic": [["source_ref"], ["target_ref"], ["relationship_type"], ["id"], ["description"]]
    }
