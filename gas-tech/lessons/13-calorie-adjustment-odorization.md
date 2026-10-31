# 第 13 回 熱量調整（LPG 増熱）と付臭

**分野：ガス技術（製造）**

## ねらい
- 混合ガスの発熱量と比重が体積分率の加重平均で決まることを、理想気体の性質から導ける。
- 熱量の低い LNG を 45 MJ/m³ に合わせるのに必要な LPG の量を、混合の式から計算できる。
- 付臭剤の濃度がとても小さくて済む理由を、「どの濃度で気付かせたいか」と嗅覚の閾値から説明できる。

## 1. 原理編

### 1.1 なぜ熱量をそろえるのか
- 都市ガスは、需要先での利用に適した発熱量（13A では 45 MJ/m³）が厳密に定められている（[経済産業省 ガス事業制度検討 WG 資料](https://www.meti.go.jp/shingikai/enecho/denryoku_gas/denryoku_gas/gas_jigyo_wg/pdf/011_06_00.pdf)）。
- 家庭の機器はノズルの大きさが決まっていて、入熱はウォッベ指数 WI = H/√d で決まる（第 01 回）。熱量や比重が変わると、機器の入熱や炎の状態が変わってしまう。
- 輸入 LNG には、熱量の低い「リーン」なものもある。標準熱量を維持して低熱量 LNG を受け入れるには、LPG を加える量が増え、そのコストと設備の増強が課題になる（[経済産業省 ガス事業制度検討 WG 資料](https://www.meti.go.jp/shingikai/enecho/denryoku_gas/denryoku_gas/gas_jigyo_wg/pdf/011_06_00.pdf)）。
- 東邦ガスは、増熱用 LPG を減らす目的もあって、2015 年 9 月に標準熱量を 46.04655 MJ/m³ から 45 MJ/m³ に引き下げた（[経済産業省 ガス事業制度検討 WG 資料](https://www.meti.go.jp/shingikai/enecho/denryoku_gas/denryoku_gas/gas_jigyo_wg/pdf/008_03_00.pdf)）。

### 1.2 混合ガスの発熱量と比重：加重平均になる理由
理想気体では、同じ温度・圧力の 1 m³ には、どのガスでも同じ数の分子（同じ mol 数）が入っています（アボガドロの法則。第 02 回）。そのため、体積分率はモル分率と同じになります。

- **発熱量（体積あたり）**：1 m³ の混合ガスを燃やした熱は、各成分の熱の和です。

  **H_mix = Σ xᵢ·Hᵢ**

- **比重（空気 = 1）**：体積あたりの質量も、各成分の和です。比重は分子量の比（d = M/28.96）なので、

  **d_mix = Σ xᵢ·dᵢ**

| 記号 | 意味 | 単位 |
|------|------|------|
| xᵢ | 成分 i の体積分率（= モル分率） | — |
| Hᵢ | 成分 i の高位発熱量（体積あたり、0 ℃・1 atm 基準） | MJ/m³N |
| dᵢ | 成分 i の比重（空気 = 1） | — |

前提は、理想気体として扱えることと、混ぜても反応しないことです。

**成分ごとの値**（1 mol あたりの燃焼熱を 22.414 L/mol で割って求める。燃焼熱は [Engineering ToolBox: Gross and Net Heating Values](https://www.engineeringtoolbox.com/gross-net-heating-values-d_420.html) を参照）：
- メタン：890.6 kJ/mol → H = **39.7 MJ/m³N**、d = 16.04/28.96 = **0.554**
- プロパン：2,219 kJ/mol → H = **99.0 MJ/m³N**、d = 44.10/28.96 = **1.52**

プロパンは、体積あたりの熱量がメタンの約 2.5 倍あります。少し混ぜるだけで熱量が大きく上がるのは、このためです。

### 1.3 必要な LPG の割合
目標の発熱量 H_t にするためのプロパンの体積分率 x は、1.2 の式を x について解くと、

  **x = (H_t − H_0) / (H_P − H_0)**

（H_0：元のガスの発熱量、H_P：プロパンの発熱量）

**大事な性質**：プロパンは比重も大きいので、熱量を上げると比重も上がります。WI = H/√d なので、H の上がり方より WI の上がり方は少しゆるやかになります（計算例 1）。

### 1.4 付臭：気付かせたい濃度から逆算する
- 天然ガスにはにおいがないので、少しの漏れでも早く気付けるよう、付臭剤を加えている（[上越市ガス水道局 資料](https://gwhp.city.joetsu.niigata.jp/fm/wp-content/uploads/sites/8/2016/06/gas201412.pdf)）。
- 付臭剤には、THT（テトラヒドロチオフェン）や TBM（ターシャリーブチルメルカプタン）などが使われる。上越市では、硫黄分を減らすため、THT から TBM とシクロヘキセンの混合物に変えた（[上越市ガス水道局 資料](https://gwhp.city.joetsu.niigata.jp/fm/wp-content/uploads/sites/8/2016/06/gas201412.pdf)）。
- TBM の嗅覚の閾値（においを感じる最小の濃度）は約 0.81 ppb ととても低い（[Haz-Map: tert-Butyl mercaptan](https://haz-map.com/Agents/5954)）。
- 米国の規則では、ガスが空気中で爆発下限界の 1/5 の濃度になれば容易に気付けるように付臭する（[Indiana Utility Regulatory Commission 資料](https://www.in.gov/iurc/files/Proper_Testing_of_Odorant_Levels_7-12_2.pdf)）。日本の付臭の基準は、ガス工作物の技術上の基準を定める省令と、その解釈例で定められている（[経済産業省：ガス工作物技術基準の解釈例など](https://www.meti.go.jp/policy/safety_security/industrial_safety/sangyo/citygas/hourei/20230210-01-02.pdf)。具体的な数値は条文で確認すること）。

**原理**：ガスが空気中で濃度 c_g（体積分率）まで薄まったときに、付臭剤が閾値 c_th に届けばよいので、ガスの中の付臭剤の濃度は

  **c_od ≥ c_th / c_g**

あれば足ります。爆発下限界よりずっと薄い段階で気付かせるので、c_g は小さい値です。それでも閾値がとても低いので、ガス中の濃度は ppm の桁で済みます（計算例 2）。

**注意**：配管のさびや土壌に付臭剤が吸着されて、においが弱くなる「臭気フェード」が起こることがある。付臭は、漏れを必ず知らせてくれるとは限らない（[Chevron Phillips Chemical：付臭剤の SDS](https://www.cpchem.com/sites/default/files/2022-08/01770641.pdf)）。

## 2. 実務とのつながり
- **熱量調整設備**：LNG 基地では、気化した天然ガスに LPG を混ぜ、熱量計で連続して測りながら、混合の割合を制御している（第 15 回の制御につながる）。
- **標準熱量の見直し**：将来の 44 MJ/m³ への引き下げや、熱量の幅で管理する「熱量バンド制」が議論されてきた（[経済産業省 ガス事業制度検討 WG 資料](https://www.meti.go.jp/shingikai/enecho/denryoku_gas/denryoku_gas/gas_jigyo_wg/pdf/018_s01_00.pdf)）。
- **水素の混入（第 01 回）**：水素は体積あたりの熱量が小さいので、混ぜると H も WI も下がる。同じ加重平均の式で見積もれる。
- **付臭濃度の管理**：ガス事業者は、送り出すガスの付臭剤の濃度を定期的に測定する。

## 3. 計算例
（python で検算済み）

**例 1：リーン LNG を 45 MJ/m³ に増熱する**
元のガス：H_0 = 41.0 MJ/m³N、d_0 = 0.60（仮定）。プロパンで増熱する。
- x = (45 − 41.0) / (99.0 − 41.0) = **0.069**（約 6.9 vol%）
- 混ぜた後の比重：d = 0.931 × 0.60 + 0.069 × 1.523 = **0.664**
- WI：混ぜる前 41.0/√0.60 = **52.9** → 混ぜた後 45/√0.664 = **55.2**
- 発熱量は 9.8 % 上がるが、WI は 4.4 % しか上がらない（比重も上がるため）。
- 100,000 m³N/h を送り出すなら、プロパンは約 **6,900 m³N/h（約 13.6 t/h）** 必要になる。

**例 2：付臭剤の最小濃度**
空気中にガスが 0.1 vol%（1/1000）まで薄まった段階で、TBM（閾値 0.81 ppb）のにおいに気付かせたい場合。
- c_od ≥ 0.81 ppb / 0.001 = **0.81 ppm**（ガスの中の TBM の濃度）
- メタンの爆発下限界は約 5 vol%（第 04 回）。0.1 vol% はその 1/50 なので、十分な余裕を持って気付ける。
- 実際には、人による感じ方の差や臭気フェードを考えて、これより多めに加える。

## 4. 理解確認

### 理解確認 1
混合ガスの発熱量（体積あたり）が、体積分率の加重平均で求められるのはなぜか。

<details><summary>解答</summary>

理想気体では、同じ温度・圧力の同じ体積に、ガスの種類によらず同じ数の分子が入っている（アボガドロの法則）。そのため体積分率はモル分率と等しく、1 m³ の混合ガスの燃焼熱は、各成分の「1 m³ あたりの燃焼熱 × 体積分率」の和になる。
</details>

### 理解確認 2
プロパンで増熱すると、発熱量の上がり方ほどにはウォッベ指数が上がらないのはなぜか。

<details><summary>解答</summary>

プロパンは分子量が大きく、比重（1.52）が天然ガス（約 0.6）より大きいから。混ぜると比重 d も上がり、WI = H/√d の分母が大きくなる。そのぶん、H の増加の一部が打ち消される。
</details>

### 理解確認 3（誤っているものはどれか）
(a) 付臭剤は嗅覚の閾値がとても低いので、ガス中の濃度は ppm の桁で足りる。
(b) 付臭していれば、ガス漏れは必ずにおいで分かる。
(c) 熱量の低い LNG を受け入れるほど、増熱に必要な LPG の量は増える。

<details><summary>解答</summary>

誤りは **(b)**。配管のさびや土壌への吸着などで付臭剤が減る「臭気フェード」があり、においが弱くなることがある。人によって感じ方にも差がある。
</details>

## 参考文献
- [経済産業省 ガス事業制度検討 WG 資料（標準熱量・LPG 増熱）](https://www.meti.go.jp/shingikai/enecho/denryoku_gas/denryoku_gas/gas_jigyo_wg/pdf/011_06_00.pdf)
- [経済産業省 ガス事業制度検討 WG 資料（標準熱量の引き下げ）](https://www.meti.go.jp/shingikai/enecho/denryoku_gas/denryoku_gas/gas_jigyo_wg/pdf/008_03_00.pdf)
- [経済産業省 ガス事業制度検討 WG 資料（熱量制度の議論）](https://www.meti.go.jp/shingikai/enecho/denryoku_gas/denryoku_gas/gas_jigyo_wg/pdf/018_s01_00.pdf)
- [Engineering ToolBox: Gases – Gross and Net Heating Values](https://www.engineeringtoolbox.com/gross-net-heating-values-d_420.html)
- [上越市ガス水道局 資料（付臭剤）](https://gwhp.city.joetsu.niigata.jp/fm/wp-content/uploads/sites/8/2016/06/gas201412.pdf)
- [Haz-Map: tert-Butyl mercaptan](https://haz-map.com/Agents/5954)
- [Indiana Utility Regulatory Commission: Proper Testing of Odorant Levels](https://www.in.gov/iurc/files/Proper_Testing_of_Odorant_Levels_7-12_2.pdf)
- [経済産業省：ガス工作物技術基準の解釈例など](https://www.meti.go.jp/policy/safety_security/industrial_safety/sangyo/citygas/hourei/20230210-01-02.pdf)
- [Chevron Phillips Chemical：付臭剤の SDS](https://www.cpchem.com/sites/default/files/2022-08/01770641.pdf)
