import os
import sys
import traceback
from pathlib import Path

# コンパイル済環境でchdirをした場合、root_dirが書き換わるので、初期値を保存しておく
_root_dir = Path(sys.argv[0]).parent.resolve(strict=True)


def engine_root() -> Path:
    if is_development():
        root_dir = Path(__file__).parents[2]

    # Nuitka/Pyinstallerでビルドされている場合
    else:
        root_dir = Path(str(_root_dir))

    return root_dir.resolve(strict=True)


def is_development() -> bool:
    """
    開発版かどうか判定する関数
    Nuitka/Pyinstallerでコンパイルされていない場合は開発環境とする。
    """
    # nuitkaビルドをした際はグローバルに__compiled__が含まれる
    if "__compiled__" in globals():
        return False

    # pyinstallerでビルドをした際はsys.frozenが設定される
    elif getattr(sys, "frozen", False):
        return False

    return True


def delete_file(file_path: str) -> None:
    try:
        os.remove(file_path)
    except OSError:
        traceback.print_exc()
