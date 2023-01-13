import sys
import traceback
from typing import Dict

from ..bridge_config import BridgeConfigLoader
from .synthesis_engine_base import SynthesisEngineBase
from .synthesis_engine_espnet import SynthesisEngineESPNet


def make_synthesis_engines(
    use_gpu: bool,
    bridge_config_loader: BridgeConfigLoader,
    enable_mock: bool = True,
    load_all_models: bool = False,
) -> Dict[str, SynthesisEngineBase]:
    """
    音声ライブラリをロードして、音声合成エンジンを生成

    Parameters
    ----------
    use_gpu: bool
        音声ライブラリに GPU を使わせるか否か
    bridge_config_loader: BridgeConfigLoader
        BridgeConfigLoader
    enable_mock: bool, optional, default=True
        コア読み込みに失敗したとき、代わりにmockを使用するかどうか
    load_all_models: bool, optional, default=False
        起動時に全てのモデルを読み込むかどうか
    """
    synthesis_engines = {}
    try:
        _synthesis_engine = SynthesisEngineESPNet(
            bridge_config_loader=bridge_config_loader,
            use_gpu=use_gpu,
            load_all_models=load_all_models,
        )
        synthesis_engines[_synthesis_engine.engine_version] = _synthesis_engine
    except Exception:
        if not enable_mock:
            raise
        traceback.print_exc()
        print(
            "Notice: mock-library will be used.",
            file=sys.stderr,
        )

        from ..dev.core import metas as mock_metas
        from ..dev.core import supported_devices as mock_supported_devices
        from ..dev.synthesis_engine import MockSynthesisEngine

        if "0.0.0" not in synthesis_engines:
            synthesis_engines["0.0.0"] = MockSynthesisEngine(
                speakers=mock_metas(), supported_devices=mock_supported_devices()
            )

    return synthesis_engines
