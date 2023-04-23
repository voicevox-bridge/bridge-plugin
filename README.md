# Bridge Plugin

[![build](https://github.com/voicevox-bridge/bridge-plugin/actions/workflows/build.yml/badge.svg)](https://github.com/voicevox-bridge/bridge-plugin/actions/workflows/build.yml)
[![releases](https://img.shields.io/github/v/release/voicevox-bridge/bridge-plugin)](https://github.com/voicevox-bridge/bridge-plugin/releases)

[![test](https://github.com/voicevox-bridge/bridge-plugin/actions/workflows/test.yml/badge.svg)](https://github.com/voicevox-bridge/bridge-plugin/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/voicevox-bridge/bridge-plugin/badge.svg)](https://coveralls.io/github/voicevox-bridge/bridge-plugin)

[ESPnet](https://github.com/espnet/espnet)を使用して作られたモデルを読み込み、[VOICEVOX](https://voicevox.hiroshiba.jp/) の互換のエンジンとして動作させる事ができるソフトウェアです。  
このリポジトリは、[VOICEVOX Engine](https://github.com/VOICEVOX/voicevox_engine)のフォークです。  


## ライセンス

VOICEVOXの開発者である、[ヒホ氏](https://twitter.com/hiho_karuta)より、別ライセンスを取得して開発しています。  
本ソフトウェアのライセンスは、[こちら](https://github.com/voicevox-bridge/bridge-plugin/blob/master/LICENSE)をご覧ください。  
このソフトウェアで使用できる音声合成モデルに、「音声合成化を許諾している提供者の音声を元に作られていること」という制限を設けています。  
音声提供者が望まない形での音声合成化が行われることを助長しないために、このような制限を設けさせていただきました。ご理解いただけますと幸いです。  

## 採用ソフトウェア

- [LMROID](https://lmroidsoftware.wixsite.com/nhoshio) (by [@ssohsn](https://twitter.com/ssohsn))
- [ITVOICE](http://itvoice.starfree.jp/index.html) (by [@iTahobi](https://twitter.com/iTahobi))

## ダウンロード

[こちら](https://github.com/voicevox-bridge/bridge-plugin/releases/latest)から対応するエンジンをダウンロードしてください。

## 使用方法

ダウンロードして解凍した先に、以下のファイル・フォルダを配置してください。

- bridge_config.yaml
- modelフォルダ（モデルの置き場所）
- speaker_infoフォルダ（初期配置のものはダミーなので置き換えが必要）

`bridge_config.yaml`は、Bridge Pluginの設定ファイルです。  
現時点では、VOICEVOX Bridgeの`engine_config.yaml`と互換性があります。  
（ただし、`name`、`port`、`engine_uuid`、`engine_version`、`min_vvb_version`、`speakers/styles`内の`sampling_rate`は無視されます）  
初期状態のBridge Pluginのフォルダには、ダミーのspeaker_infoが配置されています。  
これを使用するモデルに合ったものに置き換えてください。（VOICEVOX Engineと同じ構造です）  
speaker_infoフォルダ内のUUIDは、`bridge_config.yaml`で設定した`speaker_uuid`と揃えてください。  
次に、`engine_manifest_assets`フォルダ内の以下のファイルを書き換えてください。  

- icon.png (エンジンのアイコン)
- terms_of_service.md
- update_infos.json

最後に、`engine_manifest.json`を書き換えてください。  
書き換えが必要な項目は以下の通りです。  

- name
- brand_name
- uuid
- version
- url
- port
- default_sampling_rate

Bridge Pluginの入ったフォルダをzipで圧縮し、拡張子を.vvppに変更すると、プラグインエンジンのファイルとして扱うことができます。  

<details>
<summary>bridge_config.yamlの例</summary>

[BridgeConfig.py](https://github.com/voicevox-bridge/bridge-plugin/blob/master/voicevox_engine/bridge_config/BridgeConfig.py)も参照してください。  

```yaml
gloal_style_setting: &gloal_style_setting
  sampling_rate: 44100
  g2p: pyopenjtalk_accent_with_pause

global_tts_inference_init_args: &global_tts_inference_init_args
  speed_control_alpha: 1.0
  noise_scale: 0.333
  noise_scale_dur: 0.333

global_token_id_converter_init_args: &global_token_id_converter_init_args
  token_list:
    - <blank>
    - <unk>
    - '1'
    - '2'
    - '0'
    - '3'
    - '4'
    - '-1'
    - '5'
    - a
    - o
    - '-2'
    - i
    - '-3'
    - u
    - e
    - k
    - n
    - t
    - '6'
    - r
    - '-4'
    - s
    - N
    - m
    - pau
    - '7'
    - sh
    - d
    - g
    - w
    - '8'
    - U
    - '-5'
    - I
    - cl
    - h
    - y
    - b
    - '9'
    - j
    - ts
    - ch
    - '-6'
    - z
    - p
    - '-7'
    - f
    - ky
    - ry
    - '-8'
    - gy
    - '-9'
    - hy
    - ny
    - '-10'
    - by
    - my
    - '-11'
    - '-12'
    - '-13'
    - py
    - '-14'
    - '-15'
    - v
    - '10'
    - '-16'
    - '-17'
    - '11'
    - '-21'
    - '-20'
    - '12'
    - '-19'
    - '13'
    - '-18'
    - '14'
    - dy
    - '15'
    - ty
    - '-22'
    - '16'
    - '18'
    - '19'
    - '17'
    - <sos/eos>


host: '127.0.0.1'
speakers:
  - name: DUMMY
    speaker_uuid: aa33c99b-a43b-49b0-a2c8-6a81922f8213
    version: 0.0.1
    styles:
      - name: ノーマル
        id: 0
        <<: *gloal_style_setting
        tts_inference_init_args:
          train_config: model/DUMMY_config.yaml
          model_file: model/DUMMY_model.pth
          <<: *global_tts_inference_init_args
        token_id_converter_init_args:
          <<: *global_token_id_converter_init_args
```

</details>

## API ドキュメント

[VOICEVOX公式 API ドキュメント](https://voicevox.github.io/voicevox_engine/api/)をご参照ください。  
（いくつか非互換の機能がありますのでご注意ください）  

VOICEVOX エンジンもしくはエディタを起動した状態で http://127.0.0.1:50021/docs にアクセスすると、起動中のエンジンのドキュメントも確認できます。  

リクエスト・レスポンスの文字コードはすべて UTF-8 です。

### HTTP リクエストで音声合成するサンプルコード

```bash
echo -n "こんにちは、音声合成の世界へようこそ" >text.txt

curl -s \
    -X POST \
    "127.0.0.1:50021/audio_query?speaker=1"\
    --get --data-urlencode text@text.txt \
    > query.json

curl -s \
    -H "Content-Type: application/json" \
    -X POST \
    -d @query.json \
    "127.0.0.1:50021/synthesis?speaker=1" \
    > audio.wav
```

生成される音声はサンプリングレートが 24000Hz と少し特殊なため、音声プレーヤーによっては再生できない場合があります。

`speaker` に指定する値は `/speakers` エンドポイントで得られる `style_id` です。互換性のために `speaker` という名前になっています。

### 読み方を AquesTalk 記法で取得・修正するサンプルコード

`/audio_query`のレスポンスにはエンジンが判断した読み方が AquesTalk ライクな記法([本家の記法](https://www.a-quest.com/archive/manual/siyo_onseikigou.pdf)とは一部異なります)で記録されています。
記法は次のルールに従います。

- 全てのカナはカタカナで記述される
- アクセント句は`/`または`、`で区切る。`、`で区切った場合に限り無音区間が挿入される。
- カナの手前に`_`を入れるとそのカナは無声化される
- アクセント位置を`'`で指定する。全てのアクセント句にはアクセント位置を 1 つ指定する必要がある。
- アクセント句末に`？`(全角)を入れることにより疑問文の発音ができる

```bash
# 読ませたい文章をutf-8でtext.txtに書き出す
echo -n "ディープラーニングは万能薬ではありません" >text.txt

curl -s \
    -X POST \
    "127.0.0.1:50021/audio_query?speaker=1" \
    --get --data-urlencode text@text.txt \
    > query.json

cat query.json | grep -o -E "\"kana\":\".*\""
# 結果... "kana":"ディ'イプ/ラ'アニングワ/バンノオヤクデワアリマセ'ン"

# "ディイプラ'アニングワ/バンノ'オヤクデワ/アリマセ'ン"と読ませたいので、
# is_kana=trueをつけてイントネーションを取得しnewphrases.jsonに保存
echo -n "ディイプラ'アニングワ/バンノ'オヤクデワ/アリマセ'ン" > kana.txt
curl -s \
    -X POST \
    "127.0.0.1:50021/accent_phrases?speaker=1&is_kana=true" \
    --get --data-urlencode text@kana.txt \
    > newphrases.json

# query.jsonの"accent_phrases"の内容をnewphrases.jsonの内容に置き換える
cat query.json | sed -e "s/\[{.*}\]/$(cat newphrases.json)/g" > newquery.json

curl -s \
    -H "Content-Type: application/json" \
    -X POST \
    -d @newquery.json \
    "127.0.0.1:50021/synthesis?speaker=1" \
    > audio.wav
```

### ユーザー辞書機能について

APIからユーザー辞書の参照、単語の追加、編集、削除を行うことができます。

#### 参照

`/user_dict`にGETリクエストを投げることでユーザー辞書の一覧を取得することができます。

```bash
curl -s -X GET "127.0.0.1:50021/user_dict"
```

#### 単語追加

`/user_dict_word`にPOSTリクエストを投げる事でユーザー辞書に単語を追加することができます。  
URLパラメータとして、以下が必要です。
- surface （辞書に登録する単語）
- pronunciation （カタカナでの読み方）
- accent_type （アクセント核位置、整数）

アクセント核位置については、こちらの文章が参考になるかと思います。  
〇型となっている数字の部分がアクセント核位置になります。  
https://tdmelodic.readthedocs.io/ja/latest/pages/introduction.html  

成功した場合の返り値は単語に割り当てられるUUIDの文字列になります。

```bash
surface="test"
pronunciation="テスト"
accent_type="1"

curl -s -X POST "127.0.0.1:50021/user_dict_word" \
    --get \
    --data-urlencode "surface=$surface" \
    --data-urlencode "pronunciation=$pronunciation" \
    --data-urlencode "accent_type=$accent_type"
```

#### 単語修正

`/user_dict_word/{word_uuid}`にPUTリクエストを投げる事でユーザー辞書の単語を修正することができます。  
URLパラメータとして、以下が必要です。
- surface （辞書に登録するワード）
- pronunciation （カタカナでの読み方）
- accent_type （アクセント核位置、整数）

word_uuidは単語追加時に確認できるほか、ユーザー辞書を参照することでも確認できます。  
成功した場合の返り値は`204 No Content`になります。

```bash
surface="test2"
pronunciation="テストツー"
accent_type="2"
# 環境によってword_uuidは適宜書き換えてください
word_uuid="cce59b5f-86ab-42b9-bb75-9fd3407f1e2d"

curl -s -X PUT "127.0.0.1:50021/user_dict_word/$word_uuid" \
    --get \
    --data-urlencode "surface=$surface" \
    --data-urlencode "pronunciation=$pronunciation" \
    --data-urlencode "accent_type=$accent_type"
```

#### 単語削除

`/user_dict_word/{word_uuid}`にDELETEリクエストを投げる事でユーザー辞書の単語を削除することができます。  

word_uuidは単語追加時に確認できるほか、ユーザー辞書を参照することでも確認できます。  
成功した場合の返り値は`204 No Content`になります。

```bash
# 環境によってword_uuidは適宜書き換えてください
word_uuid="cce59b5f-86ab-42b9-bb75-9fd3407f1e2d"

curl -s -X DELETE "127.0.0.1:50021/user_dict_word/$word_uuid"
```

### プリセット機能について

`presets.yaml`を編集することで話者や話速などのプリセットを使うことができます。

```bash
echo -n "プリセットをうまく活用すれば、サードパーティ間で同じ設定を使うことができます" >text.txt

# プリセット情報を取得
curl -s -X GET "127.0.0.1:50021/presets" > presets.json

preset_id=$(cat presets.json | sed -r 's/^.+"id"\:\s?([0-9]+?).+$/\1/g')
style_id=$(cat presets.json | sed -r 's/^.+"style_id"\:\s?([0-9]+?).+$/\1/g')

# AudioQueryの取得
curl -s \
    -X POST \
    "127.0.0.1:50021/audio_query_from_preset?preset_id=$preset_id"\
    --get --data-urlencode text@text.txt \
    > query.json

# 音声合成
curl -s \
    -H "Content-Type: application/json" \
    -X POST \
    -d @query.json \
    "127.0.0.1:50021/synthesis?speaker=$style_id" \
    > audio.wav
```

- `speaker_uuid`は、`/speakers`で確認できます
- `id`は重複してはいけません
- エンジン起動後にファイルを書き換えるとエンジンに反映されます


### 話者の追加情報を取得するサンプルコード

追加情報の中の portrait.png を取得するコードです。  
（[jq](https://stedolan.github.io/jq/)を使用して json をパースしています。）

```bash
curl -s -X GET "127.0.0.1:50021/speaker_info?speaker_uuid=7ffcb7ce-00ec-4bdc-82cd-45a8889e43ff" \
    | jq  -r ".portrait" \
    | base64 -d \
    > portrait.png
```


### CORS設定

VOICEVOXではセキュリティ保護のため`localhost`・`127.0.0.1`・`app://`・Originなし以外のOriginからリクエストを受け入れないようになっています。
そのため、一部のサードパーティアプリからのレスポンスを受け取れない可能性があります。  
これを回避する方法として、エンジンから設定できるUIを用意しています。

#### 設定方法

1. <http://127.0.0.1:50021/setting> にアクセスします。
2. 利用するアプリに合わせて設定を変更、追加してください。
3. 保存ボタンを押して、変更を確定してください。
4. 設定の適用にはエンジンの再起動が必要です。必要に応じて再起動をしてください。

### その他の引数

エンジン起動時に引数を指定できます。詳しいことは`-h`引数でヘルプを確認してください。

```bash
$ python run.py -h

usage: run.py [-h] [--host HOST] [--port PORT] [--use_gpu] [--voicevox_dir VOICEVOX_DIR] [--voicelib_dir VOICELIB_DIR] [--runtime_dir RUNTIME_DIR] [--enable_mock] [--enable_cancellable_synthesis] [--init_processes INIT_PROCESSES] [--load_all_models]
              [--cpu_num_threads CPU_NUM_THREADS] [--output_log_utf8] [--cors_policy_mode {CorsPolicyMode.all,CorsPolicyMode.localapps}] [--allow_origin [ALLOW_ORIGIN ...]] [--setting_file SETTING_FILE]

VOICEVOX のエンジンです。

options:
  -h, --help            show this help message and exit
  --host HOST           接続を受け付けるホストアドレスです。
  --port PORT           接続を受け付けるポート番号です。
  --use_gpu             指定するとGPUを使って音声合成するようになります。
  --voicevox_dir VOICEVOX_DIR
                        VOICEVOXのディレクトリパスです。
  --voicelib_dir VOICELIB_DIR
                        VOICEVOX COREのディレクトリパスです。
  --runtime_dir RUNTIME_DIR
                        VOICEVOX COREで使用するライブラリのディレクトリパスです。
  --enable_mock         指定するとVOICEVOX COREを使わずモックで音声合成を行います。
  --enable_cancellable_synthesis
                        指定すると音声合成を途中でキャンセルできるようになります。
  --init_processes INIT_PROCESSES
                        cancellable_synthesis機能の初期化時に生成するプロセス数です。
  --load_all_models     指定すると起動時に全ての音声合成モデルを読み込みます。
  --cpu_num_threads CPU_NUM_THREADS
                        音声合成を行うスレッド数です。指定しないと、代わりに環境変数VV_CPU_NUM_THREADSの値が使われます。VV_CPU_NUM_THREADSが空文字列でなく数値でもない場合はエラー終了します。
  --output_log_utf8     指定するとログ出力をUTF-8でおこないます。指定しないと、代わりに環境変数 VV_OUTPUT_LOG_UTF8 の値が使われます。VV_OUTPUT_LOG_UTF8 の値が1の場合はUTF-8で、0または空文字、値がない場合は環境によって自動的に決定されます。
  --cors_policy_mode {CorsPolicyMode.all,CorsPolicyMode.localapps}
                        CORSの許可モード。allまたはlocalappsが指定できます。allはすべてを許可します。localappsはオリジン間リソース共有ポリシーを、app://.とlocalhost関連に限定します。その他のオリジンはallow_originオプションで追加できます。デフォルトはlocalapps。
  --allow_origin [ALLOW_ORIGIN ...]
                        許可するオリジンを指定します。スペースで区切ることで複数指定できます。
  --setting_file SETTING_FILE
                        設定ファイルを指定できます。
```

## アップデート

エンジンディレクトリ内にあるファイルを全て消去し、新しいものに置き換えてください。

## 貢献者の方へ

Issue を解決するプルリクエストを作成される際は、別の方と同じ Issue に取り組むことを避けるため、
Issue 側で取り組み始めたことを伝えるか、最初に Draft プルリクエストを作成してください。

## 環境構築

`Python 3.11.3` を用いて開発されています。
インストールするには、各 OS ごとの C/C++ コンパイラ、CMake が必要になります。

```bash
# 開発に必要なライブラリのインストール
python -m pip install -r requirements-dev.txt -r requirements-test.txt

# とりあえず実行したいだけなら代わりにこちら
python -m pip install -r requirements.txt
```

## 実行

コマンドライン引数の詳細は以下のコマンドで確認してください。

```bash
python run.py --help
```

<!--```bash
# 製品版 VOICEVOX でサーバーを起動
VOICEVOX_DIR="C:/path/to/voicevox" # 製品版 VOICEVOX ディレクトリのパス
python run.py --voicevox_dir=$VOICEVOX_DIR
```-->

<!-- 差し替え可能な音声ライブラリまたはその仕様が公開されたらコメントを外す
```bash
# 音声ライブラリを差し替える
VOICELIB_DIR="C:/path/to/your/tts-model"
python run.py --voicevox_dir=$VOICEVOX_DIR --voicelib_dir=$VOICELIB_DIR
```
-->

```bash
# モックでサーバー起動
python run.py --enable_mock
```

```bash
# ログをUTF8に変更
python run.py --output_log_utf8
# もしくは VV_OUTPUT_LOG_UTF8=1 python run.py
```

## コードフォーマット

このソフトウェアでは、リモートにプッシュする前にコードフォーマットを確認する仕組み(静的解析ツール)を利用できます。
利用するには、開発に必要なライブラリのインストールに加えて、以下のコマンドを実行してください。
プルリクエストを作成する際は、利用することを推奨します。

```bash
pre-commit install -t pre-push
```

エラーが出た際は、以下のコマンドで修正することが可能です。なお、完全に修正できるわけではないので注意してください。

```bash
pysen run format lint
```

## タイポチェック

[typos](https://github.com/crate-ci/typos) を使ってタイポのチェックを行っています。
[typos をインストール](https://github.com/crate-ci/typos#install) した後

```bash
typos
```

でタイポチェックを行えます。
もし誤判定やチェックから除外すべきファイルがあれば
[設定ファイルの説明](https://github.com/crate-ci/typos#false-positives) に従って`_typos.toml`を編集してください。

## API ドキュメントの確認

[API ドキュメント](https://voicevox.github.io/voicevox_engine/api/)（実体は`docs/api/index.html`）は自動で更新されます。  
次のコマンドで API ドキュメントを手動で作成することができます。

```bash
python make_docs.py
```

## 依存関係

### 更新

[Poetry](https://python-poetry.org/) を用いて依存ライブラリのバージョンを固定しています。
以下のコマンドで操作できます:

```bash
# パッケージを追加する場合
poetry add `パッケージ名`
poetry add --group dev `パッケージ名` # 開発依存の追加
poetry add --group test `パッケージ名` # テスト依存の追加

# パッケージをアップデートする場合
poetry update `パッケージ名`
poetry update # 全部更新

# requirements.txtの更新
poetry export --without-hashes -o requirements.txt # こちらを更新する場合は下３つも更新する必要があります。
poetry export --without-hashes --with dev -o requirements-dev.txt
poetry export --without-hashes --with test -o requirements-test.txt
poetry export --without-hashes --with license -o requirements-license.txt
```

## ユーザー辞書の更新について

以下のコマンドで openjtalk のユーザー辞書をコンパイルできます。

```bash
python -c "import pyopenjtalk; pyopenjtalk.create_user_dict('default.csv','user.dic')"
```

## マルチエンジン機能に関して

VOICEVOX エディターでは、複数のエンジンを同時に起動することができます。
この機能を利用することで、自作の音声合成エンジンや既存の音声合成エンジンを VOICEVOX エディター上で動かすことが可能です。

<img src="./docs/res/マルチエンジン概念図.svg" width="320">

<details>

### マルチエンジン機能の仕組み

VOICEVOX API に準拠した複数のエンジンの Web API をポートを分けて起動し、統一的に扱うことでマルチエンジン機能を実現しています。
エディターがそれぞれのエンジンを実行バイナリ経由で起動し、EngineID と結びつけて設定や状態を個別管理します。

### マルチエンジン機能への対応方法

VOICEVOX API 準拠エンジンを起動する実行バイナリを作ることで対応が可能です。
VOICEVOX ENGINE リポジトリを fork し、一部の機能を改造するのが簡単です。

改造すべき点はエンジン情報・キャラクター情報・音声合成の３点です。

エンジンの情報はエンジンマニフェスト（`engine_manifest.json`）で管理されています。
マニフェストファイル内の情報を見て適宜変更してください。
音声合成手法によっては、例えばモーフィング機能など、VOICEVOX と同じ機能を持つことができない場合があります。
その場合はマニフェストファイル内の`supported_features`内の情報を適宜変更してください。

キャラクター情報は`speaker_info`ディレクトリ内のファイルで管理されています。
ダミーのアイコンなどが用意されているので適宜変更してください。

音声合成は`voicevox_engine/synthesis_engine/synthesis_engine.py`で行われています。
VOICEVOX API での音声合成は、エンジン側で音声合成クエリ`AudioQuery`の初期値を作成してユーザーに返し、ユーザーが必要に応じてクエリを編集したあと、エンジンがクエリに従って音声合成することで実現しています。
クエリ作成は`/audio_query`エンドポイントで、音声合成は`/synthesis`エンドポイントで行っており、最低この２つに対応すれば VOICEVOX API に準拠したことになります。

### マルチエンジン機能対応エンジンの配布方法

VVPP ファイルとして配布するのがおすすめです。
VVPP は「VOICEVOX プラグインパッケージ」の略で、中身はビルドしたエンジンなどを含んだディレクトリの Zip ファイルです。
拡張子を`.vvpp`にすると、ダブルクリックで VOICEVOX エディターにインストールできます。

エディター側は受け取った VVPP ファイルをローカルディスク上に Zip 展開したあと、ルートの直下にある`engine_manifest.json`に従ってファイルを探査します。
VOICEVOX エディターにうまく読み込ませられないときは、エディターのエラーログを参照してください。

また、`xxx.vvpp`は分割して連番を付けた`xxx.0.vvppp`ファイルとして配布することも可能です。
これはファイル容量が大きくて配布が困難な場合に有用です。

</details>
