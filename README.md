# blender-lineart-node
this repository is scripts for blender.

blender の、主に漫画背景制作用途に作ったスクリプトです

# comicLineartNode.py
addon になっています
実行すると レンダリング設定用のノードを生成します
出力先はデスクトップの rendering/1 フォルダに設定されます

|file name| 用途|
|:-----|:----------|
| base | Material Pass Index に準じた基本配色|
| AO | Ambient Occrusion のみ|
|lineart| 線画のみ|
|shadow| 陰影のみ|
|tex| texture image を割り振ったオブジェクトのみ|

## 作成の経緯
単純に一枚の画像にレンダリング出力されると、clip studio paint で作業する際に不便を感じることが多かったため、後処理の利便の向上のために作成しました
ex.
- この線だけ太くしたい
- 基本配色部分だけ薄くしたいor濃くしたい
- 陰影を、（物理法則通りではないけど、見た目上よくするために）調整したい

## pass index の関係
material pass index は properties -> material -> options -> pass index で設定します
マンガ原稿側で、10% トーンを割り振るマテリアルに pass index を 1に、 20% を割り振るマテリアルに pass indx を 2に、という具合に割り振ります。（現状、1:10%, 2:20%, 3:30%, 4:40% のみになっています）

object pass index は properties -> object -> rerations -> pass index で設定します
object pass index に10000 を割り振ってあるオブジェクトのみ、rendering_tex001.png に出力されます

# proxify.py
link して取り込んだデータを proxy に変換し、group にまとめます

TODO 
- [ ] 取り込む際の file 名を group 名に自動で割り振る

# softenMirrorMergeLimit.py / softenArrayMergeLimit.py
ミラー/アレイ モディファイアのマージリミットを一括して設定します。

# その他のファイル
だいたいゴミなのでそのうち整理します(^^;;
