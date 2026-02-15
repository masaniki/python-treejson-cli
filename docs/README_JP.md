# 概要

ディレクトリの入れ子構造をJSONやYAMLで出力します。

英語のドキュメントは[ここ](../README.md)です。

# インストール方法

`pip install treejson-cli`

# 使用例

`treejson [-h|--help]`

helpを表示する。

`treejson [-v|--version]`

versionを表示する。

`treejson <directory> [-y|--yaml] [-a|--all]`

ディレクトリの構造をJSONに纏めて、標準出力する。

`-y`が指定された時は、YAML形式で出力する。

`-a`が指定された時は、隠しファイル('.'から始まるファイル)を表示する。

`treejson <directory> [-d|--depth] <depth>`

探索の深さを指定する。

深さ0の時はカレントディレクトリのみを表示する。

`treejson <directory> [-f|--file] <file>`

directory構造を\<file\>へを出力する。


## 例
- `treejson tests/sample`
  ```
  {'sample': [{'parent01': [{'child01_01': ['grandchild01.txt']}, {'child01_02': ['grandchild02.txt']}, 'child01_03.txt']}, {'parent02': [{'child02_01': ['grandchild02_01.txt']}]}]}
  ```
- `treejson tests/sample -f tests/output.json`

  [tests/output.json](../tests/output.json)

- `treejson tests/sample -yf tests/output.yaml`

  [tests/output.yaml](../tests/output.yaml)

# ToDo

directoryをmap型の入れ子で表現する。

fileはscalar型を格納することで表現する。
