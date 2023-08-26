from pathlib import Path

from platformdirs import user_data_dir

from ..engine_manifest import EngineManifestLoader


def get_save_dir():
    # TODO: ここの挙動が怪しいのできちんと確認する
    try:
        app_name = EngineManifestLoader().load_manifest().name
    except TypeError:
        app_name = EngineManifestLoader.EngineManifestLoader().load_manifest().name
    return Path(user_data_dir(app_name))
