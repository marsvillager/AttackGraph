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
