# 生成AIと肖像権

![](https://raw.githubusercontent.com/yKesamaru/mongodb/master/assets/eye_catch_5.png)

- [生成AIと肖像権](#生成aiと肖像権)
  - [はじめに](#はじめに)
  - [削除要請はだれがやるのか？](#削除要請はだれがやるのか)
  - [生成AIの肖像権](#生成aiの肖像権)
  - [どうすればいいのか？](#どうすればいいのか)
  - [一般女性も被害にあう](#一般女性も被害にあう)
  - [まとめ](#まとめ)


## はじめに
まずこちらの画像をご覧ください。公開されている生成AI画像です。
![](https://raw.githubusercontent.com/yKesamaru/mongodb/master/assets/woman4.png)

この画像は`find_similarity_from_mongodb.py`をもとに、名前を割り出しました。
（というか、皆さんがご存知の女優さんを選びました。）

https://zenn.dev/ykesamaru/articles/daf1ea9def85f4

```bash
Similar document ID: 651a3a85836ecd32e441a33f
Similarity Score (Cosine Similarity): 0.6967436075210571
Similar file name: 鈴木京香_O9q4.jpg.png.png_0.png_0_align_resize.png
Similar document ID: 651a3a85836ecd32e441a39e
Similarity Score (Cosine Similarity): 0.6858800649642944
Similar file name: 鈴木京香_16..png.png.png.png_0.png_0_align_resize.png
Similar document ID: 651a3a85836ecd32e441a345
Similarity Score (Cosine Similarity): 0.6529852151870728
Similar file name: 鈴木京香_16..png.png.png_0.png_0_align_resize.png
Similar document ID: 651a3a85836ecd32e441a36f
Similarity Score (Cosine Similarity): 0.6392073631286621
Similar file name: 鈴木京香_16.png.png.png_0_align_resize.png
Similar document ID: 651a3a85836ecd32e441a376
Similarity Score (Cosine Similarity): 0.6222307085990906
Similar file name: 鈴木京香_TvdV.jpg.png.png_0.png_0_align_resize.png
処理時間: 0分 20.73秒
```
高い確率で、「鈴木京香」さんに類似していることが分かります。

次にこちらの画像をご覧ください。
![](https://raw.githubusercontent.com/yKesamaru/mongodb/master/assets/2023-10-02-22-28-25.png)
> [鈴木京香、三谷大河に“皆勤賞” 『鎌倉殿の13人』丹後局役で出演決定](https://www.oricon.co.jp/news/2191840/full/)

背景などをみても明らかに、この写真をモデルの学習に使ったことは明白です。

生成AI画像では、胸の谷間が強調されていますが、プロンプト次第では、際どい写真にすることも可能です。
というより、技術ブログに載せられる程度の参考写真を持ってきました。ほとんどはここに載せることをためらわれる生成写真です。

これらの写真がredditで投稿・公開されています。

![](https://raw.githubusercontent.com/yKesamaru/mongodb/master/assets/image918.png)

## 削除要請はだれがやるのか？
顔認証・顔類似検索システムを持っているので、私が削除要請を出すことは可能です。
可能ではありますが、義理はありません。なにしろ大量にありますから、顔類似検索システムを休みなく稼働させる必要があります。

今は過渡期なので、手に追える範囲ですが、あっという間に手に負えなくなるでしょう。

その前に、芸能プロダクションや芸能事務所は動かないのでしょうか？
だれかが傷ついてから、大問題になってから、動くのでしょうか？
おそすぎる気がします。

## 生成AIの肖像権
もちろん、女優さん・アイドルの方々・芸能プロダクション、芸能事務所に権利があるはずです。
少し前のディープフェイクとは次元が違い、もはや普通の写真と区別がつきません。
redditなどに投稿するのは、知的欲求のためでしょうか？承認欲でしょうか？
自分の顔で、知らない部屋で、知らない下着姿の写真を撮られているようなものです。
ご本人は深く傷つきますし、芸能プロダクション・芸能事務所も大きな損失です。

## どうすればいいのか？
とりあえず、規制されるまで傍観していては、取り返しのつかないことになるでしょう。
redditに投稿されている写真を、顔認証・顔類似検索システムで検索し、削除要請を出すことが必要です。規模が今くらいのうちに。

## 一般女性も被害にあう
LoRAであれば、顔画像が20枚ほどあれば、モデルが作れてしまいます。
リベンジなんとかの被害の可能性も、十分考えられます。

## まとめ
少し前から気になっていたことを、書きました。
わたしなんかより、芸能プロダクション・芸能事務所の方が、もっと気になっているでしょう。
自発的に何らかの手段を考えてらっしゃると思いますから、わたしの杞憂かもしれません。


いじょうです。ありがとうございました。

