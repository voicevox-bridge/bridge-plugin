from pathlib import Path
from typing import Any, Dict, Iterable, List, Literal, Optional, Union

import numpy as np
import torch
from espnet2.bin.tts_inference import Text2Speech
from espnet2.text.token_id_converter import TokenIDConverter
from pydantic import BaseModel, Extra, Field

from ..model import Speaker, SpeakerStyle


class TTSInferenceInitArgs(BaseModel):
    """
    espnet2.bin.tts_inference.Text2Speechの初期化時に渡すパラメータ
    """

    train_config: Union[Path, str] = None
    model_file: Union[Path, str] = None
    threshold: float = 0.5
    minlenratio: float = 0.0
    maxlenratio: float = 10.0
    use_teacher_forcing: bool = False
    use_att_constraint: bool = False
    backward_window: int = 1
    forward_window: int = 3
    speed_control_alpha: float = 1.0
    noise_scale: float = 0.667
    noise_scale_dur: float = 0.8
    vocoder_config: Union[Path, str] = None
    vocoder_file: Union[Path, str] = None
    dtype: str = "float32"
    device: str = "cpu"  # use_gpu引数で上書きされる
    seed: int = 777
    always_fix_seed: bool = False


class TTSInferenceCallArgs(BaseModel):
    """
    espnet2.bin.tts_inference.Text2Speechの呼び出し時に渡すパラメータ
    """

    class Config:
        arbitrary_types_allowed = True

    speech: Optional[Union[torch.Tensor, np.ndarray]] = None
    durations: Optional[Union[torch.Tensor, np.ndarray]] = None
    spembs: Optional[Union[torch.Tensor, np.ndarray]] = None
    sids: Optional[Union[torch.Tensor, np.ndarray]] = None
    lids: Optional[Union[torch.Tensor, np.ndarray]] = None
    decode_conf: Optional[Dict[str, Any]] = None


class TokenIDConverterInitArgs(BaseModel):
    """
    espnet2.text.token_id_converter.TokenIDConverterの呼び出し時に渡すパラメータ
    """

    token_list: Union[Path, str, Iterable[str]]
    unk_symbol: str = "<unk>"


class StyleConfig(SpeakerStyle):
    """
    スタイルの設定のフォーマット
    """

    class Config:
        arbitrary_types_allowed = True
        extra = Extra.ignore

    g2p: Literal["pyopenjtalk_accent_with_pause", "pyopenjtalk_prosody"] = Field(
        title="g2pの設定"
    )
    tts_inference_init_args: TTSInferenceInitArgs = Field(
        title="Text2Speechクラス初期化時の引数", default=TTSInferenceInitArgs()
    )
    tts_inference_call_args: TTSInferenceCallArgs = Field(
        title="Text2Speechクラス呼び出し時の引数", default=TTSInferenceCallArgs()
    )
    token_id_converter_init_args: TokenIDConverterInitArgs = Field(
        title="TokenIDConverterクラス初期化時の引数",
    )
    text2speech: Optional[Text2Speech] = Field(
        title="Text2Speechクラスのインスタンス（内部で使用）", default=None
    )
    token_id_converter: Optional[TokenIDConverter] = Field(
        title="TokenIDConverterクラスのインスタンス（内部で使用）", default=None
    )


class SpeakerConfig(Speaker):
    """
    スピーカーの設定のフォーマット
    """

    styles: List[StyleConfig] = Field(title="スタイルの設定")


class BridgeConfig(BaseModel, extra=Extra.ignore):
    """
    エンジンの設定のフォーマット
    """

    host: str = Field(title="エンジンのホスト", default="127.0.0.1")
    port: int = Field(title="エンジンのポート番号", default=50021)
    speakers: List[SpeakerConfig] = Field(title="スピーカー情報")
    engine_version: str = Field(title="エンジンのバージョン")
    sampling_rate: int = Field(title="出力サンプリングレート")
