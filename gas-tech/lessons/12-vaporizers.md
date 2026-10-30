# 第 12 回 気化器（ORV・SCV・IFV）

**分野：ガス技術（製造）**

## ねらい
- LNG を常温のガスにするのに必要な熱量を、エネルギー収支（潜熱 + 顕熱）から見積もれる。
- 3 種類の気化器（ORV・SCV・IFV）が、それぞれどこから熱をもらい、どんな問題を避けているのかを説明できる。
- 必要な海水量や燃料の割合を、熱収支から計算できる。

> 注：テーマ表では「SMV」と書いたが、燃焼式の気化器は一般に SCV（Submerged Combustion Vaporizer：水中燃焼式）と呼ばれるので、本文では SCV と書く。

## 1. 原理編

### 1.1 必要な熱量：エネルギー収支
LNG（−162 ℃の液体）を、常温（約 25 ℃）のガスにするまでに必要な熱は、次の和です。
1. 液のまま沸点まで温める顕熱（大気圧で貯めた LNG はほぼ沸点にあるので、ほぼ 0）
2. 蒸発潜熱（約 510〜550 kJ/kg。第 11 回）
3. できたガスを常温まで温める顕熱（ガスの比熱 × 約 190 K）

**q = h(ガス, 常温) − h(LNG)** と、比エンタルピーの差で表せます（第 05 回の第一法則。定常流れでは、加えた熱 = エンタルピーの増加）。
- LNG を −162 ℃から 25 ℃の気体にするまでのエンタルピー差は、「冷熱」として約 **830 kJ/kg** と見積もられている（[Chemical Engineering Transactions Vol.61（AIDIC）](https://www.aidic.it/cet/17/61/185.pdf)）。気化器に与える熱は、この冷熱と同じ大きさになる。
- 必要な熱は、LNG が持つエネルギー（発熱量）の約 1.5〜1.7 % にあたる（[IntechOpen：LNG regasification の章](https://www.intechopen.com/chapters/54526)）。

**基本の式**：
  **Q = ṁ_LNG × q = ṁ_熱媒 × c_p × ΔT_熱媒**

| 記号 | 意味 | 単位 |
|------|------|------|
| ṁ_LNG | LNG の処理量 | kg/s |
| q | 1 kg あたりの必要熱量 | kJ/kg |
| ṁ_熱媒 | 海水などの流量 | kg/s |
| ΔT_熱媒 | 熱媒の温度低下 | K |

右辺が意味するのは、**熱源の温度を下げた分だけ LNG が温まる**ということです。熱の出どころを何にするかで、気化器の種類が決まります。

### 1.2 ORV（オープンラック式）：海水を流し下ろす
- フィン付きの伝熱管を並べたパネルの外面に海水を流し下ろし、管の中を上る LNG を気化させる（[神戸製鋼所：ORV](https://www.kobelco.co.jp/english/products/ecmachinery/lng/orv.html)、[住友精密工業：LNG 気化器](https://www.spp.co.jp/en/netsu/products/lng/)）。
- 熱源が海水なので燃料が要らず、CO₂ をほとんど出さない。
- パネルはアルミニウム合金で、海水による腐食を防ぐため外面に亜鉛合金を被覆している（第 10 回の犠牲陽極と同じ考え方）。
- **弱点**：海水の温度が低い冬は、能力が下がる。管の外面で海水が凍る（着氷）と、熱抵抗が増える（第 09 回）。

### 1.3 SCV（水中燃焼式）：燃料を燃やして温水で温める
- バーナの燃焼ガスを水槽の水の中に吹き込み、その温水で、水中に沈めた管の中の LNG を気化させる（[Chart Industries：SCV 資料](https://azure-na-assets.contentstack.com/v3/assets/blt8c6446abc03f2c8b/blt30b4b4352a073f94/67b34daf0493e8d8a101269b/3001-scv-web.pdf)、[Digital Refining：Submerged combustion vaporisers](https://digitalrefining.com/article/1000326/submerged-combustion-vaporisers-for-lng-distribution-facilities)）。
- 燃焼ガスを直接水に吹き込むので、排ガスの熱（水蒸気の潜熱まで）を水が受け取り、熱効率が高い。
- 気化したガスの 1〜2 % を燃料として使う（[Justia：気化方法の特許出願](https://patents.justia.com/patent/20080155996)）。
- 起動が速いので、冬のピーク時や、ORV の補助（バックアップ）に使われる。

### 1.4 IFV（中間媒体式）：プロパンを仲立ちにする
- 海水で中間媒体（プロパンなど）を蒸発させ、その蒸気が LNG の管の外で凝縮するときの熱で LNG を気化させる。最後に、海水で天然ガスを常温まで温める（[神戸製鋼所：IFV](https://www.kobelco.co.jp/english/products/ecmachinery/lng/ifv.html)）。
- 大阪ガスが 1970 年代に開発した方式（TRI-EX）である（[神戸製鋼所 技術資料](https://www.kobelco.co.jp/english/ktr/pdf/ktr_39/006-012.pdf)）。
- 海水が LNG の管に直接触れないので、**海水が凍らない**。そのため、冷たい海水でも使える（[Frontiers in Energy：IFV のレビュー](https://journal.hep.com.cn/fie/EN/1159575542364168919)）。
- 中間媒体には、伝熱性能がよいプロパンやジメチルエーテルが向く（[IAEA INIS：中間媒体の比較研究](https://inis.iaea.org/records/7s3ph-nst80)）。
- **原理のポイント**：中間媒体は、蒸発と凝縮をくり返して熱を運ぶ（相変化）。潜熱を使うので、温度差が小さくても、多くの熱を運べる。

### 1.5 3 方式の比較
| 方式 | 熱源 | 長所 | 主な課題 |
|------|------|------|---------|
| ORV | 海水（直接） | 燃料不要、構造が簡単 | 冬の能力低下、着氷、海水設備 |
| SCV | 燃料の燃焼 | 起動が速い、海水不要 | 燃料を 1〜2 % 消費、CO₂ が出る |
| IFV | 海水（中間媒体経由） | 海水が凍らない、船上（FSRU）でも使える | 構造が複雑、可燃性の中間媒体を扱う |

## 2. 実務とのつながり
- **LNG 基地の運用**：ふだんは ORV でベースの量をまかない、需要の多い冬や ORV の点検中は SCV で補う、という組み合わせが多い。
- **冷熱利用**：LNG が持つ 830 kJ/kg の冷熱は、冷熱発電、空気の液化分離、冷凍倉庫などに使える（[Chemical Engineering Transactions Vol.61](https://www.aidic.it/cet/17/61/185.pdf)）。気化器で海に捨てる熱を減らす工夫である。
- **熱量調整（第 13 回）**：気化した直後のガスに LPG を混ぜて、送り出すガスの熱量をそろえる。

## 3. 計算例
（python で検算済み）

**例 1：必要な熱量**
LNG を 100 t/h 気化させる場合、必要な熱量は q = 830 kJ/kg として、
- Q = (100,000 / 3,600) kg/s × 830 kJ/kg = **約 23.1 MW**

**例 2：ORV に必要な海水量**
海水の比熱を 4.0 kJ/(kg·K)、密度を 1,025 kg/m³ とし、海水の温度低下 ΔT を仮定する。
| 海水の温度低下 | 海水の流量 |
|-------------|-----------|
| 5 K | 1,153 kg/s（約 4,050 m³/h） |
| 7 K | 823 kg/s（約 2,890 m³/h） |

LNG 100 t/h を気化させるのに、その約 30〜40 倍の質量の海水が必要になる。ΔT を大きくとると海水は減るが、出口の海水温度が下がって、凍りやすくなる。

**例 3：SCV の燃料の割合**
燃料にするガスの低位発熱量を 50 MJ/kg（メタン相当）と仮定すると、
- 必要な熱 / 発熱量 = 830 / 50,000 = **1.66 %**（上の「1.5〜1.7 %」と一致）
- 水槽の熱効率を 95 % とすると、燃料は **1.75 %** になる（上の「1〜2 %」と一致）。

## 4. 理解確認

### 理解確認 1
IFV で、海水が凍りにくいのはなぜか。

<details><summary>解答</summary>

海水は、−162 ℃の LNG の管には直接触れず、中間媒体（プロパンなど）を蒸発させるだけだから。プロパンの凝縮温度は海水の凝固点よりずっと高いので、海水側の管の表面温度は低くなりすぎない。冷たい LNG の熱を受け持つのは、凝縮する中間媒体である。
</details>

### 理解確認 2
SCV の燃料が、気化したガスの 1〜2 % 程度で済むのはなぜか。

<details><summary>解答</summary>

LNG を常温のガスにするのに必要な熱（約 830 kJ/kg）は、ガスの発熱量（約 50,000 kJ/kg）の 1.7 % 程度しかないから。さらに SCV は、燃焼ガスを水の中に吹き込んで水蒸気の潜熱まで回収するので効率が高く、燃料のロスが小さい。
</details>

### 理解確認 3（誤っているものはどれか）
(a) ORV は、海水の温度が低い季節には気化能力が下がる。
(b) SCV は燃料を燃やすので、海水がなくても使える。
(c) IFV では、LNG と海水が同じ管の内側と外側で直接熱交換する。

<details><summary>解答</summary>

誤りは **(c)**。IFV では、海水は中間媒体を蒸発させ、中間媒体の凝縮熱で LNG を気化させる。LNG と海水は直接は熱交換しない（最後に天然ガスを温める段だけ、ガスと海水が熱交換する）。
</details>

## 参考文献
- [Chemical Engineering Transactions Vol.61（AIDIC）：LNG の冷熱](https://www.aidic.it/cet/17/61/185.pdf)
- [IntechOpen：LNG regasification の章](https://www.intechopen.com/chapters/54526)
- [神戸製鋼所：Open Rack Vaporizer](https://www.kobelco.co.jp/english/products/ecmachinery/lng/orv.html)
- [住友精密工業：LNG 気化器](https://www.spp.co.jp/en/netsu/products/lng/)
- [Chart Industries：Submerged Combustion Vaporizer 資料](https://azure-na-assets.contentstack.com/v3/assets/blt8c6446abc03f2c8b/blt30b4b4352a073f94/67b34daf0493e8d8a101269b/3001-scv-web.pdf)
- [Digital Refining：Submerged combustion vaporisers for LNG distribution facilities](https://digitalrefining.com/article/1000326/submerged-combustion-vaporisers-for-lng-distribution-facilities)
- [Justia：液化ガスの気化方法（特許出願 20080155996）](https://patents.justia.com/patent/20080155996)
- [神戸製鋼所：Intermediate Fluid Vaporizer](https://www.kobelco.co.jp/english/products/ecmachinery/lng/ifv.html)
- [神戸製鋼所 技術資料（IFV）](https://www.kobelco.co.jp/english/ktr/pdf/ktr_39/006-012.pdf)
- [Frontiers in Energy：IFV とその伝熱特性のレビュー](https://journal.hep.com.cn/fie/EN/1159575542364168919)
- [IAEA INIS：中間媒体の伝熱性能の研究](https://inis.iaea.org/records/7s3ph-nst80)
