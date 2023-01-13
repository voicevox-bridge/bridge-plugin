import yaml

from ..engine_manifest import EngineManifestLoader
from .BridgeConfig import BridgeConfig


class BridgeConfigLoader:
    def __init__(self, config_file_dir) -> None:
        self.config_file_path = config_file_dir / "bridge_config.yaml"

    def load_config_file(self) -> BridgeConfig:
        if self.config_file_path.is_file():
            config = yaml.safe_load(self.config_file_path.read_text(encoding="utf-8"))
        else:
            raise FileNotFoundError

        (
            engine_version,
            port,
            sampling_rate,
        ) = EngineManifestLoader().load_info_for_bridge_config()

        config["port"] = port
        config["engine_version"] = engine_version
        config["sampling_rate"] = sampling_rate

        setting = BridgeConfig(**config)

        return setting
