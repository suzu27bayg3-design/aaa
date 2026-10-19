# 第 01 回 都市ガスの組成・発熱量・ウォッベ指数

## ねらい
- 都市ガス「13A」が何を意味するかを、組成と燃焼性から説明できる。
- ウォッベ指数 WI = H / √d を、ノズルを流れるガスの式から導ける。
- ガスの種類を変えたとき（水素混合など）、機器の入熱がどう変わるか見積もれる。

## 1. 基礎原理

### 1.1 都市ガスの組成
日本の都市ガスはほとんどが規格「13A」で、主な原料はメタンを主成分とする LNG です
（[三井住友トラスト基礎研究所 用語集](https://smtrc.jp/useful/glossary/detail/n/3446)）。
組成の目安はメタン約 90 %、エタン約 6 %、プロパン約 3 % です
（[幻冬舎ゴールドオンライン](https://gentosha-go.com/articles/-/12199)。事業者ごとの実際の値は SDS で確認すること。例：[仙台市ガス局 都市ガス13A SDS](https://divcom02.gas.city.sendai.jp/top/natural-gas/uploads/2026/05/01_toshigas13a_sds.pdf)、[大津市 13A SDS](https://www.city.otsu.lg.jp/material/files/group/327/SDS_13A_20260327.pdf)）。
13A の標準熱量は 45 MJ/m³ です（標準熱量制度の議論は [経産省 ガス事業制度検討WG資料](https://www.meti.go.jp/shingikai/enecho/denryoku_gas/denryoku_gas/gas_jigyo_wg/pdf/018_s01_00.pdf)）。

### 1.2 発熱量：高位 (HHV) と低位 (LHV)
燃焼すると水 H₂O ができます。
- **高位発熱量 HHV（総発熱量）**：生じた水蒸気が液体の水に戻るときの凝縮潜熱も含む値。
- **低位発熱量 LHV（真発熱量）**：凝縮潜熱を含まない値。

メタンでは CH₄ + 2O₂ → CO₂ + 2H₂O となり、1 mol から水が 2 mol できます。
そのため HHV と LHV の差は約 10 % になります。日本のガス料金や 13A の「45 MJ/m³」は HHV の値です。
潜熱回収型の給湯器（第 21 回）は、この差の分を回収する技術です。

### 1.3 ウォッベ指数の導出（ここが本題）
バーナのノズル（オリフィス）を考えます。ノズルの前後の圧力差を Δp、ガスの密度を ρ とします。
ベルヌーイの式から、噴き出す速さは

  v = √(2Δp / ρ)

体積流量 Q は、ノズル面積 A と流量係数 C を使って

  Q = C·A·√(2Δp / ρ)

機器に入る熱量（**入熱** Φ）は、体積流量に体積あたりの発熱量 H を掛けたものです。

  Φ = H·Q = C·A·√(2Δp/ρ_air) · **H / √d**   （d = ρ/ρ_air：空気に対する比重）

同じ機器（C, A は一定）を同じ供給圧（Δp は一定）で使うとき、入熱は **H/√d** だけで決まります。これがウォッベ指数です。

  **WI = H / √d**

- 発熱量 H が高くても、比重 d が大きい（重い）ガスはノズルを通りにくいので、入熱はその分しか増えません。
- WI が同じガスどうしは、ノズルを交換しなくても同じ入熱になります。これがガスの**互換性**の第一条件です。

定義の出典：[Wobbe index - Wikipedia](https://en.wikipedia.org/wiki/Wobbe_index)、[Neutrium: Wobbe Index](https://neutrium.net/articles/properties/wobbe-index/)。
WI は 1926 年に提案された「単一指標」による互換性の判定法です（[Pomerantz & Smyth, EPA 掲載資料](https://19january2021snapshot.epa.gov/sites/static/files/2016-06/documents/pomerantz.pdf)）。

### 1.4 WI だけでは足りない：燃焼速度
WI が同じでも、**燃焼速度**が違うと炎の形が変わります。
- 燃焼速度が速すぎる → **逆火**（炎がバーナの中に戻る）
- 遅すぎる → **リフティング**（炎がバーナから浮き上がる）
- 空気が足りない → **イエローチップ**（炎の先が黄色くなる）→ 不完全燃焼や CO が出るおそれ

このため、WI だけでは互換性を判断できません（[Wikipedia](https://en.wikipedia.org/wiki/Wobbe_index)）。
AGA Bulletin #36（1946）や Weaver（1951）などの多指標法が作られました（[EPA 掲載資料](https://19january2021snapshot.epa.gov/sites/static/files/2016-06/documents/pomerantz.pdf)）。
日本では **WI と最大燃焼速度 (MCP)** の 2 つを軸にして、「13A」などの**ガスグループ**を決めています。
ガス事業者は、この 2 つを測定・記録して、供給約款で定めた範囲に収まるよう管理します（[Weblio「WI」解説](https://www.weblio.jp/content/WI)）。
「13A」の **13** は WI の区分、**A** は燃焼速度の区分（A＝遅い／B＝中間／C＝速い）を表します。

## 2. 応用・実務
- **熱量変更（転換）**：昔は 6B・5C などのガスグループがありました。13A に統一したときは、家庭ごとに機器のノズルを交換する作業が必要でした。これは WI が変わるためです。
- **成分の変動管理**：LNG の産地が違うと組成も変わります。そのため製造工程で LPG を混ぜて熱量を調整し、WI と MCP を範囲内に保ちます（第 11 回）。
- **水素混合・e-メタン**：水素を混ぜると WI が下がり、燃焼速度が大きく上がります（下の計算例）。これがガス互換性の主な課題です（第 26・27 回）。
- **海外の規格**：欧州では天然ガスを WI で分類しています。たとえば Family 2H は 45.5–55.0 MJ/Nm³、Family 2L は 39.0–45.0 MJ/Nm³ です（[Wikipedia](https://en.wikipedia.org/wiki/Wobbe_index)）。

## 3. 計算例
発熱量 H は HHV [MJ/m³N]、比重 d は空気＝1 とします。

| ガス | H | d | WI = H/√d |
|------|---|---|-----------|
| メタン | 39.8 | 0.555 | 53.5 |
| 13A（代表値） | 45.0 | 0.64 | 56.2 |
| 水素 | 12.75 | 0.0695 | 48.4 |
| プロパン | 99.0 | 1.52 | 80.2 |

**13A に水素を 20 vol% 混ぜた場合**（単純な体積加重で概算）：
- H = 0.8×45 + 0.2×12.75 = 38.6 MJ/m³
- d = 0.8×0.64 + 0.2×0.0695 = 0.526
- WI = 38.6 / √0.526 = **53.2**

13A の 56.2 から約 5 % 下がります。同じ機器では入熱も約 5 % 下がります。
体積あたりの発熱量は約 14 % 下がりますが、ガスが軽くなって流量が増えるため、入熱の低下は約 5 % にとどまります。これが WI という考え方の要点です。
（実際には燃焼速度が大きく上がる影響のほうが重要で、MCP 側の検討が必要です。）

## 4. 確認問題

1. ウォッベ指数が H/√d の形になる理由を、ノズルを流れるガスの式から説明せよ。
<details><summary>解答</summary>
流量 Q ∝ A√(Δp/ρ) なので、入熱 Φ = HQ ∝ H/√ρ ∝ H/√d になる。機器と圧力が同じなら、入熱は WI だけで決まる。
</details>

2. 「13A」の「13」と「A」はそれぞれ何を表すか。
<details><summary>解答</summary>
13 はウォッベ指数の区分、A は燃焼速度の区分（遅い側）を表す。
</details>

3. WI が同じ 2 種類のガスでも、互換性がないことがある。なぜか。
<details><summary>解答</summary>
燃焼速度が違うと、逆火・リフティング・イエローチップなど炎の安定性が変わるため。そのため、WI に加えて MCP などの指標も必要になる。
</details>

## 参考文献
- [Wobbe index - Wikipedia](https://en.wikipedia.org/wiki/Wobbe_index)
- [Neutrium: Wobbe Index](https://neutrium.net/articles/properties/wobbe-index/)
- [Pomerantz & Smyth, Gas interchangeability（EPA 掲載資料, PDF）](https://19january2021snapshot.epa.gov/sites/static/files/2016-06/documents/pomerantz.pdf)
- [Weblio「WI」（ウォッベ指数の解説）](https://www.weblio.jp/content/WI)
- [三井住友トラスト基礎研究所 用語集（都市ガス）](https://smtrc.jp/useful/glossary/detail/n/3446)
- [幻冬舎ゴールドオンライン（都市ガスの成分）](https://gentosha-go.com/articles/-/12199)
- [仙台市ガス局 都市ガス13A 安全データシート（PDF）](https://divcom02.gas.city.sendai.jp/top/natural-gas/uploads/2026/05/01_toshigas13a_sds.pdf)
- [大津市 都市ガス13A SDS（PDF）](https://www.city.otsu.lg.jp/material/files/group/327/SDS_13A_20260327.pdf)
- [経済産業省 ガス事業制度検討WG 資料（標準熱量）](https://www.meti.go.jp/shingikai/enecho/denryoku_gas/denryoku_gas/gas_jigyo_wg/pdf/018_s01_00.pdf)
- [ガス主任技術者試験 - Wikibooks](https://ja.wikibooks.org/wiki/%E3%82%AC%E3%82%B9%E4%B8%BB%E4%BB%BB%E6%8A%80%E8%A1%93%E8%80%85%E8%A9%A6%E9%A8%93)
