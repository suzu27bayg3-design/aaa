# 第 17 回 整圧器（ガバナ）

**分野：ガス技術（供給）**

## ねらい
- 整圧器が出口圧力を一定に保つ仕組みを、ダイヤフラムにかかる力のつり合いから説明できる。
- 流量が増えると出口圧力が少し下がる「オフセット（ドループ）」が生じる理由を、ばねの性質から導ける。
- 大きく減圧するとガスが冷える理由（ジュール・トムソン効果）と、凍結や加温の必要性を説明できる。

## 1. 原理編

### 1.1 整圧器の役割
- 都市ガスは高い圧力で送り出され、導管の途中のガバナ（整圧器）で減圧して需要家に供給される。ガバナは、二次側（出口）の圧力が設定圧力になるように、ガス流路の開き具合を調整する（[特許 JPH07217800A：エネルギー回収装置付き都市ガス整圧装置](https://patents.google.com/patent/JPH07217800A/ja)）。
- 例えば大津市では、中圧 A の整圧器で中圧 B に下げ、さらに中圧 B の整圧器で低圧に下げて家庭に配っている（[大津市企業局 事業概要](https://www.city.otsu.lg.jp/material/files/group/1/151-160jigyougaiyou.pdf)）。
- 流量は季節や時間で変わるが、出口圧力は一定に保ちたい。これは第 15 回のフィードバック制御そのものである。

### 1.2 力のつり合い（直動式）
直動式の整圧器では、ダイヤフラム（膜）の片側を出口圧力 P₂ が押し、反対側をばねが押します。弁はダイヤフラムにつながっています。

  **F_s = P₂ × A_d + F_f**

| 記号 | 意味 | 単位 |
|------|------|------|
| F_s | ばねの力（設定圧力を決める） | N |
| P₂ | 出口（二次側）圧力 | Pa |
| A_d | ダイヤフラムの有効面積 | m² |
| F_f | 弁や軸の摩擦・流れの力 | N |

（[FOCAPO-CPC 2017 論文：圧力調整器のモデル](https://skoge.folk.ntnu.no/prost/proceedings/focapo-cpc-2017/FOCAPO-CPC%202017%20Contributed%20Papers/106_FOCAPO_Contributed.pdf)）

**動き方**：
- 需要が増える → 出口の圧力 P₂ が下がる → ダイヤフラムを押す力が弱まる → ばねが勝って弁が開く → ガスが多く流れて P₂ が戻る。
- 需要が減ると逆に弁が閉じる。
- 測る（ダイヤフラム）・比べる（ばねとのつり合い）・操作する（弁）を、電気を使わずに 1 つの機械で行っている。

### 1.3 オフセット（ドループ）が生じる理由
弁を大きく開けるには、ダイヤフラムが大きく動く必要があります。するとばねが伸び、ばねの力はフックの法則 F = k × x のとおり小さくなります。つり合いの式から、

  **P₂ = (F₀ − k·x) / A_d**

（F₀：弁が閉じているときのばねの力、x：弁の開き（ストローク）、k：ばね定数）

流量が多いほど x が大きくなり、出口圧力 P₂ は設定値より下がります。これがオフセット（ドループ）で、第 15 回の「P 制御のオフセット」と同じ性質です。出口圧力のずれがあって初めて弁が開いたままになる、という仕組みだからです。
- ドループの原因は、①ストロークでばねの力が変わる「ばね効果」と、②ダイヤフラムの有効面積が変わる「ダイヤフラム効果」の 2 つである（[US4842013A：ドループを補償した直動式調整器](https://patents.google.com/patent/US4842013)、[Project Materials：What is pressure regulator](https://blog.projectmaterials.com/quick-answers/valves/what-is-pressure-regulator/)）。
- **小さくする方法**：ばね定数 k を小さくする（柔らかいばね）、ダイヤフラムを大きくする（A_d を大きくする）、パイロット式にする。

### 1.4 パイロット式
- 小さくて感度のよい「パイロット」整圧器が出口圧力を感じとり、その出力で大きな主弁を動かす。直動式を 2 つ直列につないだものと考えられる。直動式よりドループをかなり小さくできる（[Project Materials](https://blog.projectmaterials.com/quick-answers/valves/what-is-pressure-regulator/)、[EPC Land：Pressure regulators](https://epcland.com/pressure-regulators-types-working-principles/)）。
- 大型の整圧器には、主整圧器とパイロットを持ち、主整圧器内のガス圧力を抜くことで作動させるアンローディング型がある（[特許 JPS6254309A：アンローディングタイプガバナ](https://patents.google.com/patent/JPS6254309A/esLanguage)）。
- **原理**：パイロットが「増幅器」の役をするので、出口圧力の小さなずれで主弁を大きく動かせる。P 制御でゲインを大きくするとオフセットが小さくなる（第 15 回）のと同じ理屈である。

### 1.5 減圧でガスが冷える：ジュール・トムソン効果
- 弁で絞って圧力を下げる過程は、外と熱や仕事のやりとりがなければ、エンタルピーが変わらない（等エンタルピー変化。第 05 回）。
- 理想気体ならエンタルピーは温度だけで決まるので温度は変わらないが、実在のガスでは分子間力の影響で温度が下がる。これがジュール・トムソン効果である。
- 天然ガスでは、30〜80 bar の範囲で、おおよそ **2 bar の減圧につき約 1 ℃** 下がる。冷えると、ガス中や周りの水分が凝縮・凍結することがある。対策は、減圧ごとの再加温、上流での除湿、ハイドレート防止剤（メタノールなど）である（[Industrial Monitor Direct：Natural gas temperature drop](https://industrialmonitordirect.com/blogs/knowledgebase/natural-gas-temperature-drop-joule-thomson-pressure-reduction-calculation)）。
- この係数は温度・圧力・組成で大きく変わるので、設計では実在気体の状態式で計算する（[Marić 2005 論文（Scribd）](https://www.scribd.com/document/642287607/maric2005-pdf)）。

## 2. 実務とのつながり
- **整圧器の多段構成**：高圧 → 中圧 A → 中圧 B → 低圧と、何段かに分けて下げる。1 段で大きく下げると、オフセットや温度低下が大きくなるからである。
- **加温設備**：高圧から大きく減圧する整圧所では、ガスを予熱して凍結を防ぐ（計算例 2）。
- **点検**：整圧器の出口圧力・閉塞圧力（流量 0 のときの出口圧力）を点検し、異常があれば分解整備する。
- **安全装置**：整圧器が故障して出口圧力が上がりすぎたときに備え、緊急遮断弁や安全弁を設ける。

## 3. 計算例
（python で検算済み）

**例 1：直動式のドループ**
設定圧力 2 kPa、ダイヤフラムの有効面積 0.05 m²（直径約 25 cm）、ばね定数 2,000 N/m、全開のストローク 10 mm とする。
- 閉じているときのばねの力：F₀ = 2,000 Pa × 0.05 m² = **100 N**
- 全開のとき：ばねの力は 100 − 2,000 × 0.010 = 80 N なので、P₂ = 80 / 0.05 = **1,600 Pa**
- 出口圧力は設定より 400 Pa 下がり、ドループは **20 %**。
- パイロットで 10 倍に増幅すれば、ずれは約 **40 Pa（2 %）** に小さくなる。

**例 2：減圧による温度低下と加温量**
「2 bar あたり 1 ℃」の目安を使う。
| 減圧 | 温度低下 |
|------|---------|
| 中圧 0.4 MPa → 低圧（約 4 bar） | 約 2 ℃ |
| 高圧 7 MPa → 1 MPa（60 bar） | 約 30 ℃ |
- 高圧の例で、10,000 m³N/h（約 2.0 kg/s、密度 0.717 kg/m³N と仮定）を 30 ℃ 温め直すには、比熱を 2.2 kJ/(kg·K) と仮定して、2.0 × 2.2 × 30 = **約 130 kW** の加温が必要になる。

## 4. 理解確認

### 理解確認 1
直動式の整圧器で、流量が増えると出口圧力が少し下がるのはなぜか。

<details><summary>解答</summary>

流量を増やすには弁を大きく開ける必要があり、そのときダイヤフラムが動いてばねが伸びる。ばねの力はフックの法則で小さくなるので、つり合う出口圧力 P₂ = ばねの力 / 面積 も下がる。出口圧力が設定より低い状態でなければ、弁を開いたままにできない。
</details>

### 理解確認 2
パイロット式にすると、ドループが小さくなるのはなぜか。

<details><summary>解答</summary>

感度の高い小さなパイロットが出口圧力のずれを感じ、その出力を増幅して大きな主弁を動かすから。小さな圧力のずれで主弁を大きく動かせるので、P 制御のゲインを大きくしたのと同じように、オフセットが小さくなる。
</details>

### 理解確認 3（誤っているものはどれか）
(a) 整圧器のばね定数を小さくすると、ドループは小さくなる。
(b) 弁で減圧したガスの温度が下がるのは、エンタルピーが減るからである。
(c) 高圧から大きく減圧する整圧所では、凍結を防ぐためにガスを加温することがある。

<details><summary>解答</summary>

誤りは **(b)**。弁での減圧（絞り）では、エンタルピーはほぼ変わらない（等エンタルピー変化）。温度が下がるのは、実在のガスで分子間力が働くためのジュール・トムソン効果である。
</details>

## 参考文献
- [特許 JPH07217800A：エネルギー回収装置付き都市ガス整圧装置](https://patents.google.com/patent/JPH07217800A/ja)
- [大津市企業局 事業概要（整圧器と導管）](https://www.city.otsu.lg.jp/material/files/group/1/151-160jigyougaiyou.pdf)
- [FOCAPO-CPC 2017 論文：圧力調整器のモデル](https://skoge.folk.ntnu.no/prost/proceedings/focapo-cpc-2017/FOCAPO-CPC%202017%20Contributed%20Papers/106_FOCAPO_Contributed.pdf)
- [US4842013A：Droop compensated direct acting pressure regulator](https://patents.google.com/patent/US4842013)
- [Project Materials：What is pressure regulator](https://blog.projectmaterials.com/quick-answers/valves/what-is-pressure-regulator/)
- [EPC Land：Pressure regulators – types and working principles](https://epcland.com/pressure-regulators-types-working-principles/)
- [特許 JPS6254309A：アンローディングタイプガバナ](https://patents.google.com/patent/JPS6254309A/esLanguage)
- [Industrial Monitor Direct：Natural gas temperature drop（Joule-Thomson）](https://industrialmonitordirect.com/blogs/knowledgebase/natural-gas-temperature-drop-joule-thomson-pressure-reduction-calculation)
- [Marić 2005 論文（天然ガスのジュール・トムソン係数）](https://www.scribd.com/document/642287607/maric2005-pdf)
