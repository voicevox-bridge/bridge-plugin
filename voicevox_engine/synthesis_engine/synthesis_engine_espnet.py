import json
import os
from pathlib import Path
from typing import List, Optional

import librosa.effects
import numpy as np
import pyworld
import torch
from espnet2.bin.tts_inference import Text2Speech
from espnet2.text.token_id_converter import TokenIDConverter
from fastapi import HTTPException
from scipy.signal import resample

from ..bridge_config import BridgeConfigLoader
from ..model import AccentPhrase, AudioQuery
from .synthesis_engine_base import SynthesisEngineBase


def query2tokens(query: AudioQuery, g2p_type: str):
    tokens = []
    if g2p_type in ["pyopenjtalk_accent_with_pause", "pyopenjtalk_g2p_accent"]:
        for accent_phrase in query.accent_phrases:
            accent = accent_phrase.accent
            for i, mora in enumerate(accent_phrase.moras):
                if mora.consonant is not None:
                    tokens.append(mora.consonant)
                    tokens.append(str(accent))
                    tokens.append(str((i + 1) - accent))
                tokens.append(mora.vowel)
                tokens.append(str(accent))
                tokens.append(str((i + 1) - accent))
            if (
                accent_phrase.pause_mora is not None
                and g2p_type == "pyopenjtalk_accent_with_pause"
            ):
                tokens.append(accent_phrase.pause_mora.vowel)
        return tokens

    elif g2p_type == "pyopenjtalk_prosody":
        # TODO: 有声、無声フラグ
        for i, accent_phrase in enumerate(query.accent_phrases):
            accent = accent_phrase.accent
            for j, mora in enumerate(accent_phrase.moras):
                if mora.consonant is not None:
                    tokens.append(mora.consonant.lower())
                if mora.vowel == "N":
                    tokens.append(mora.vowel)
                else:
                    tokens.append(mora.vowel.lower())
                if accent_phrase.accent == j + 1 or j == 0:
                    if accent_phrase.accent == j + 1 and j == 0:
                        tokens.append("]")
                    elif j == 0:
                        tokens.append("[")
                    else:
                        tokens.append("]")
            if len(query.accent_phrases) > i + 1:
                if accent_phrase.pause_mora:
                    tokens.append("_")
                else:
                    tokens.append("#")
            else:
                if accent_phrase.is_interrogative:
                    # 最後のアクセント句のみ疑問文判定する
                    tokens.append("?")
                else:
                    tokens.append("$")
        return tokens

    else:
        raise RuntimeError(f"不明なG2Pの種類です。: {g2p_type}")


def get_abs_path(_path: Optional[str], config_path: Path) -> Path:
    if _path is None:
        return None
    _path = Path(_path)
    if _path.root == "":
        return (config_path / _path).resolve(strict=True)
    else:
        return _path.resolve(strict=True)


class SynthesisEngineESPNet(SynthesisEngineBase):
    def __init__(
        self,
        bridge_config_loader: BridgeConfigLoader,
        use_gpu: bool,
        load_all_models: bool,
    ):

        # if use_gpu:
        #    self.device = "cuda"
        # else:
        self.device = "cpu"

        self.bridge_config = bridge_config_loader.load_config_file()

        self.engine_version = self.bridge_config.engine_version
        self.default_sampling_rate = self.bridge_config.sampling_rate

        os.chdir(bridge_config_loader.config_file_path.parent)

        # use_gpuの引数で上書きする
        # text2speechとtoken_id_converterを作成する
        for speaker in self.bridge_config.speakers:
            for style in speaker.styles:
                style.tts_inference_init_args.device = self.device
                if load_all_models:
                    style.text2speech = Text2Speech(
                        **style.tts_inference_init_args.dict()
                    )
                    style.token_id_converter = TokenIDConverter(
                        **style.token_id_converter_init_args.dict()
                    )
                else:
                    style.text2speech = None
                    style.token_id_converter = None

    @property
    def speakers(self) -> str:
        return json.dumps(
            [
                {
                    "name": speaker.name,
                    "speaker_uuid": speaker.speaker_uuid,
                    "styles": [
                        {"name": style.name, "id": style.id} for style in speaker.styles
                    ],
                    "version": speaker.version,
                }
                for speaker in self.bridge_config.speakers
            ]
        )

    @property
    def supported_devices(self) -> Optional[str]:
        return json.dumps(
            {
                "cpu": True,
                "cuda": False,
            }
        )

    def _get_style(self, speaker_id):
        for speaker in self.bridge_config.speakers:
            for style in speaker.styles:
                if style.id == speaker_id:
                    _speaker = style
                    break
            else:
                continue
            break
        else:
            raise HTTPException(status_code=404, detail="該当する話者が見つかりません")
        return _speaker

    def initialize_speaker_synthesis(self, speaker_id: int, skip_reinit: bool):
        speaker = self._get_style(speaker_id)
        if speaker.text2speech is None or not skip_reinit:
            speaker.text2speech = Text2Speech(**speaker.tts_inference_init_args.dict())
        if speaker.token_id_converter is None or not skip_reinit:
            speaker.token_id_converter = TokenIDConverter(
                **speaker.token_id_converter_init_args.dict()
            )
            assert speaker.token_id_converter is not None

    def is_initialized_speaker_synthesis(self, speaker_id: int) -> bool:
        speaker = self._get_style(speaker_id)
        return (
            speaker.text2speech is not None and speaker.token_id_converter is not None
        )

    def replace_phoneme_length(
        self, accent_phrases: List[AccentPhrase], speaker_id: int
    ) -> List[AccentPhrase]:
        """
        accent_phrasesの母音・子音の長さを設定する
        Parameters
        ----------
        accent_phrases : List[AccentPhrase]
            アクセント句モデルのリスト
        speaker_id : int
            話者ID
        Returns
        -------
        accent_phrases : List[AccentPhrase]
            母音・子音の長さが設定されたアクセント句モデルのリスト
        """
        # 母音・子音の長さを設定するのは不可能なのでそのまま返す
        return accent_phrases

    def replace_mora_pitch(
        self, accent_phrases: List[AccentPhrase], speaker_id: int
    ) -> List[AccentPhrase]:
        """
        accent_phrasesの音高(ピッチ)を設定する
        Parameters
        ----------
        accent_phrases : List[AccentPhrase]
            アクセント句モデルのリスト
        speaker_id : int
            話者ID
        Returns
        -------
        accent_phrases : List[AccentPhrase]
            音高(ピッチ)が設定されたアクセント句モデルのリスト
        """
        # 音高を設定するのは不可能なのでそのまま返す
        return accent_phrases

    def _synthesis_impl(self, query: AudioQuery, speaker_id: int):
        """
        音声合成クエリから音声合成に必要な情報を構成し、実際に音声合成を行う
        Parameters
        ----------
        query : AudioQuery
            音声合成クエリ
        speaker_id : int
            話者ID
        Returns
        -------
        wave : numpy.ndarray
            音声合成結果
        """
        self.initialize_speaker_synthesis(speaker_id, skip_reinit=True)
        _speaker = self._get_style(speaker_id)

        assert _speaker.text2speech is not None
        assert _speaker.token_id_converter is not None

        if len(query.accent_phrases) == 0:
            return np.array([], dtype=np.float64)

        with torch.no_grad():
            tokens = query2tokens(query, _speaker.g2p)
            ids = np.array(_speaker.token_id_converter.tokens2ids(tokens))
            _speaker.text2speech.decode_conf.update({"alpha": 1 / query.speedScale})
            wave = _speaker.text2speech(ids, **_speaker.tts_inference_call_args.dict())
            wave = wave["wav"].view(-1).cpu().numpy()

        # 閾値30dbで前後の無音をトリミング
        wave, _ = librosa.effects.trim(wave, top_db=30)
        wave = wave.astype(np.float64)

        # 開始無音
        if query.prePhonemeLength != 0:
            wave = np.concatenate(
                [
                    np.zeros(int(self.default_sampling_rate * query.prePhonemeLength)),
                    wave,
                ],
                0,
            )

        # 終了無音
        if query.postPhonemeLength != 0:
            wave = np.concatenate(
                [
                    wave,
                    np.zeros(int(self.default_sampling_rate * query.postPhonemeLength)),
                ],
                0,
            )

        # WORLDで加工する
        fs = query.outputSamplingRate

        # 音高
        onkou = (query.pitchScale * 3) + 1

        # 基本周波数の抽出
        _f0, t = pyworld.dio(wave, fs)
        f0 = pyworld.stonemask(wave, _f0, t, fs)
        sp = pyworld.cheaptrick(wave, f0, t, fs)
        ap = pyworld.d4c(
            wave,
            f0,
            t,
            fs,
            # threshold=0.50   # voiced/unvoiced threshold
        )

        # f0 の平均値を求め、中央からどれだけ離れているかで、抑揚を表現する
        total = 0
        index = 0
        for f in f0:
            if f != 0:
                total += f
                index += 1

        ave = total / index

        pos = 0
        for f in f0:
            if f != 0:
                f0[pos] = ave * onkou + (f - ave) * query.intonationScale
            pos += 1

        # 合成する

        # 音高と抑揚のスライダーがデフォルト時は加工しない
        if query.intonationScale != 1 or onkou != 1:
            synthesized = pyworld.synthesize(
                f0,
                sp,
                ap,
                fs,
            )
            wave = synthesized.astype(np.float)

        # 音量
        if query.volumeScale != 1:
            wave *= query.volumeScale

        # サンプリングレート変更
        wave = resample(
            wave,
            query.outputSamplingRate * len(wave) // self.default_sampling_rate,
        )
        # ステレオ化
        if query.outputStereo:
            wave = np.array([wave, wave]).T

        return wave
