<p align="center">
  <a href="https://github.com/tsukinokun">
    <img src="https://img.shields.io/badge/Author-Tsukino-blue?style=flat-square&logo=github" alt="Author">
  </a>
  <a href="https://github.com/tsukinokun/ImportFromZip/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-GPL%20v3.0-blue.svg?style=flat-square" alt="License: GPL v3.0">
  </a>
  <img src="https://img.shields.io/badge/Blender-4.2%2B-orange?style=flat-square&logo=blender" alt="Blender 4.2+">
  <a href="https://qiita.com/tsukino_">
    <img src="https://img.shields.io/badge/Qiita-tsukino__-brightgreen?style=flat-square&logo=qiita" alt="Qiita">
  </a>
</p>

<p align="center">
  <img src="image/Logo.png" alt="ImportFromZip Logo">
</p>

<h1 align="center">ImportFromZip</h1>

[English README is here](README.md)

Blenderに、`.zip` アーカイブの中身を直接インポートできる機能を追加する
シンプルなアドオンです。手動でZIPを解凍する手間が不要になります。

## 対応フォーマット

- FBX (`.fbx`)
- OBJ (`.obj`)
- glTF / GLB (`.gltf`, `.glb`)

対応フォーマットは簡単に追加できます。詳しくは下記の
[対応フォーマットの追加方法](#対応フォーマットの追加方法)を参照してください。

## 特徴

- **File > Import > Import From Zip (.zip)** メニューを追加
- 選択したZIPを一時フォルダに展開
- 展開先を再帰的に探索し、対応する全ファイルを検出(サブフォルダ内も含む)
- 見つかったファイルをすべて現在のシーンにインポート
- 処理後、一時フォルダは自動的に削除される
- インポートしたファイル数を通知(1つも見つからなければ警告を表示)

## 動作要件

- Blender **4.2** 以降(Extensionsシステムを使用)

## インストール方法

1. [Releases](../../releases) ページから最新の配布用ZIPをダウンロード
   (またはこのリポジトリをクローンし、プロジェクトルート直下のファイルをZIP化)
2. Blenderで `Edit > Preferences > Get Extensions > Install from Disk` を開く
3. ダウンロードした `.zip` ファイルを選択
4. アドオン一覧で **Import From Zip** が有効になっていることを確認

## 使い方

1. `File > Import > Import From Zip (.zip)` を選択
2. 対応フォーマットのファイルが入った `.zip` ファイルを選ぶ
3. **Import** ボタンをクリック

アーカイブ内で見つかった対応ファイルは(サブフォルダ内のものも含めて)すべて
現在のシーンにインポートされます。複数フォーマットが混在している場合
(例:FBXのキャラクター + GLBの小道具)も、1回の操作でまとめてインポートされます。

## 対応フォーマットの追加方法

インポート処理は `__init__.py` 内の `IMPORTERS` という1つの辞書にまとまっており、
拡張子ごとにインポート用の関数を対応付けています。

```python
def _import_fbx(filepath):
    bpy.ops.import_scene.fbx(filepath=filepath)

def _import_obj(filepath):
    bpy.ops.wm.obj_import(filepath=filepath)

def _import_glb(filepath):
    bpy.ops.import_scene.gltf(filepath=filepath)

IMPORTERS = {
    ".fbx": _import_fbx,
    ".obj": _import_obj,
    ".glb": _import_glb,
    ".gltf": _import_glb,
}
```

新しいフォーマットを追加したい場合は、該当する `bpy.ops.import_scene.*` /
`wm.*_import` オペレーターを呼び出す小さな `_import_xxx(filepath)` 関数を書き、
この辞書に追加するだけです。

## 配布用ZIPの作り方

Blenderにインストールするzipは、`blender_manifest.toml` と `__init__.py` が
**zipのルート直下**に入っている必要があります(サブフォルダの中に入れないこと)。

```bash
zip -j import_from_zip.zip __init__.py blender_manifest.toml
```

## ライセンス

[GPL-3.0-or-later](LICENSE)

## コントリビュート

Issue・Pull Requestを歓迎します。特に新しいフォーマット対応の追加は大歓迎です。
詳しくは [CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。

## 詳細
- [解説記事(Qiita)](https://qiita.com/tsukino_/items/b3dda3704b48267863f87)

## 作者

山﨑愛/Tsukino

- [Qiita: tsukino_](https://qiita.com/tsukino_) 
- [GitHub: tsukino](https://github.com/tsukinokun)
