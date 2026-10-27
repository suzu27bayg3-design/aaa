# 第 09 回 伝熱と熱交換器

**分野：基礎理論**

## ねらい
- 伝導・対流による熱の流れを「熱抵抗の直列」として表し、熱通過率 U を組み立てられる。
- 熱交換器の対数平均温度差（LMTD）を、微小区間のエネルギー収支から導ける。
- 向流が並流より有利な理由と、「どこを改善すれば熱がよく通るか」を、抵抗の大きさから判断できる。

## 1. 原理編

### 1.1 フーリエの法則と熱抵抗
固体の中を熱が伝わる量は、温度の勾配に比例します（フーリエの法則。実験から得られた線形の法則）。

  **q = −k · dT/dx**　（平板では Q = k·A·(T₁ − T₂)/L）

（[University of Waterloo ECE309 講義資料 Chapter 5](https://www.mhtlab.uwaterloo.ca/courses/ece309_mechatronics/lectures/pdffiles/chapter5.pdf)）

| 記号 | 意味 | 単位 |
|------|------|------|
| q | 熱流束（単位面積あたりの熱流） | W/m² |
| k | 熱伝導率 | W/(m·K) |
| L | 壁の厚さ | m |
| A | 伝熱面積 | m² |

式を **Q = ΔT / R** と書き直すと、電気回路のオームの法則（I = V/R）と同じ形になります。
- 温度差が「電圧」、熱流が「電流」にあたる。
- 壁の熱抵抗は R = L/(kA)。
- 流体と壁の間の対流（熱伝達）の抵抗は R = 1/(hA)。h は熱伝達率 [W/(m²·K)]。

### 1.2 熱通過率 U：抵抗を直列につなぐ
高温の流体 → 壁 → 低温の流体と熱が通るとき、3 つの抵抗が直列に並びます。直列の抵抗は足し算なので、

  **1/U = 1/h₁ + L/k + 1/h₂**、　**Q = U·A·ΔT**

（[open-exam-prep：Steady-State Conduction & Multilayer Thermal Resistance](https://open-exam-prep.com/study-guides/pe-mechanical-hvac/heat-transfer-principles/conduction-thermal-resistance)）

**大事な性質**：U は、**いちばん大きい抵抗**でほぼ決まります。
- 気体側の h は数十 W/(m²·K)、水側は数千 W/(m²·K) と、桁が違うことが多い。
- そのため気体側にフィン（ひれ）を付けて面積を増やすのが効果的です。計算例 1 で確かめます。

### 1.3 熱交換器と対数平均温度差（LMTD）の導出
熱交換器の中では、場所によって高温側と低温側の温度差 ΔT が変わります。そこで、全体を代表する温度差が必要になります。

微小な伝熱面積 dA で考えます（向流・並流のどちらでも同じ手順）。
1. 熱の移動：dQ = U·ΔT·dA
2. 高温側の流体は温度が下がる：dQ = −C_h·dT_h（C = 質量流量 × 比熱。熱容量流量 [W/K]）
3. 低温側の流体は温度が上がる（並流なら dQ = C_c·dT_c）
4. 2 と 3 から、d(ΔT) = d(T_h − T_c) = −(1/C_h ± 1/C_c)·dQ。つまり ΔT は Q に対して**直線的**に変わる。
5. 1 を代入すると d(ΔT)/ΔT = −(定数)·U·dA。これを積分すると ln が出てくる。
6. 全体の熱量 Q でまとめ直すと、

  **Q = U·A·ΔT_lm、　ΔT_lm = (ΔT₁ − ΔT₂) / ln(ΔT₁/ΔT₂)**

ΔT₁、ΔT₂ は熱交換器の両端での温度差です（[Wikipedia: Logarithmic mean temperature difference](https://en.wikipedia.org/wiki/Logarithmic_mean_temperature_difference)、[R. Paul Singh：Introduction to Food Engineering 講義](https://rpaulsingh.com/course/lectures/heatexch.html)）。

- **前提**：定常で、U と比熱が一定、外への熱損失がない。
- **ln が出てくる理由**：温度差が大きい入口では熱がたくさん移り、そのぶん温度差が急に縮む。温度差は指数関数的に変わるので、単純な平均（算術平均）ではなく対数平均になる。
- 直交流や、バッフル付きの多管式などの複雑な形では、LMTD に補正係数をかけて使います（[Wikipedia: LMTD](https://en.wikipedia.org/wiki/Logarithmic_mean_temperature_difference)）。

### 1.4 向流と並流
- **並流**：2 つの流体が同じ向きに流れる。入口の温度差は大きいが、出口に向かって急に縮む。低温側の出口温度は、高温側の出口温度を超えられない。
- **向流**：2 つの流体が逆向きに流れる。温度差が全体でそろいやすく、同じ温度条件なら LMTD が大きい。低温側の出口温度は、高温側の出口温度より高くできる。

### 1.5 出口温度が分からないとき：ε-NTU 法
出口温度が分からないと、LMTD は計算できません。そのときは ε-NTU 法を使います（[Wikipedia: NTU method](https://en.wikipedia.org/wiki/NTU_method)）。
- **NTU = U·A / C_min**：熱交換器の「大きさ」を表す無次元数。
- **有効度 ε = Q / Q_max**：Q_max は、無限に長い向流熱交換器で移せる最大の熱量（= C_min × 入口温度差）。ε は 0〜1 の値をとる。
- 向流の場合、ε = [1 − exp(−NTU(1 − C_r))] / [1 − C_r·exp(−NTU(1 − C_r))]（C_r = C_min/C_max）。

## 2. 実務とのつながり
- **LNG 気化器（第 12 回）**：オープンラック式気化器（ORV）では、フィン付き伝熱管を並べたパネルの外面に海水を流し下ろし、管の中の LNG を気化させる。パネルはアルミニウム合金製で、海水による腐食を防ぐため外面に亜鉛合金を被覆する（[神戸製鋼所：ORV](https://www.kobelco.co.jp/english/products/ecmachinery/lng/orv.html)、[住友精密工業：LNG 気化器](https://www.spp.co.jp/en/netsu/products/lng/)）。
- **給湯器・ボイラー（第 24 回）**：燃焼ガス側（気体）の h が小さいので、フィン付きの熱交換器を使う。潜熱回収型では、排ガスを露点以下まで冷やすために伝熱面積を大きくする。
- **熱交換器の汚れ**：スケールや汚れも熱抵抗として 1/U に足し算される。U が下がったら、汚れの抵抗が増えたと考えて清掃の時期を判断する。

## 3. 計算例
（python で検算済み）

**例 1：熱通過率と「効く抵抗」**
厚さ 5 mm の鋼板（k = 50 W/(m·K)）で、片側が水（h = 1000）、反対側が燃焼ガス（h = 50）の場合。
- 抵抗の内訳：1/1000 = 0.001、0.005/50 = 0.0001、1/50 = 0.02 [m²·K/W]
- U = 1 / 0.0211 = **47.4 W/(m²·K)**
- 抵抗の割合：ガス側 94.8 %、水側 4.7 %、鋼板 0.5 %
- ガス側の h を 100 に倍増すると U = **90.1**（約 1.9 倍）。鋼板を薄くしても、ほとんど変わらない。

**例 2：向流と並流の LMTD**
高温側 90 → 60 ℃、低温側（水 0.5 kg/s、比熱 4.18 kJ/(kg·K)）20 → 45 ℃。
- 熱量：Q = 0.5 × 4180 × 25 = **52.25 kW**
- 向流：両端の温度差は 90 − 45 = 45、60 − 20 = 40 → LMTD = **42.45 K**
- 並流：両端の温度差は 90 − 20 = 70、60 − 45 = 15 → LMTD = **35.70 K**
- U = 1000 W/(m²·K) とすると、必要な面積は向流 **1.23 m²**、並流 **1.46 m²**。並流は約 19 % 大きな面積が必要。

**例 3：ε-NTU 法で検算**
例 2 の向流で、C_h = 1742 W/K、C_c = 2090 W/K → C_min = 1742、C_r = 0.833。
- NTU = 1000 × 1.231 / 1742 = 0.707
- 向流の式から ε = **0.429**
- 直接計算 Q / (C_min × (90 − 20)) = 0.429 と一致する。

## 4. 理解確認

### 理解確認 1
熱交換器の平均温度差に、算術平均ではなく対数平均を使うのはなぜか。

<details><summary>解答</summary>

温度差が大きいところほど熱がたくさん移り、そのぶん温度差が速く縮む。微小区間で d(ΔT)/ΔT が一定の割合になるので、温度差は面積に対して指数関数的に変わる。これを全体で積分すると ln が現れる。
</details>

### 理解確認 2
水と燃焼ガスの間の熱交換器で、熱の通りをよくするには、どちらの側を改善するのがよいか。それはなぜか。

<details><summary>解答</summary>

燃焼ガス側。熱抵抗は直列で足し算になり、U はいちばん大きい抵抗でほぼ決まる。気体側の h は液体側より 1〜2 桁小さく、抵抗の大部分を占めるので、フィンで面積を増やすなどの対策が効く（例 1 では 95 % がガス側）。
</details>

### 理解確認 3（誤っているものはどれか）
(a) 同じ入口・出口温度なら、向流の LMTD は並流より大きい。
(b) 並流では、低温側の出口温度を高温側の出口温度より高くできる。
(c) 熱交換器の汚れは、熱抵抗が増えるのと同じ効果を持つ。

<details><summary>解答</summary>

誤りは **(b)**。並流では 2 つの流体の温度が出口で近づくだけで、低温側が高温側を追い越すことはできない。追い越せるのは向流の場合である。
</details>

## 参考文献
- [University of Waterloo ECE309 講義資料 Chapter 5（伝導）](https://www.mhtlab.uwaterloo.ca/courses/ece309_mechatronics/lectures/pdffiles/chapter5.pdf)
- [open-exam-prep：Steady-State Conduction & Multilayer Thermal Resistance](https://open-exam-prep.com/study-guides/pe-mechanical-hvac/heat-transfer-principles/conduction-thermal-resistance)
- [Wikipedia: Logarithmic mean temperature difference](https://en.wikipedia.org/wiki/Logarithmic_mean_temperature_difference)
- [R. Paul Singh：Introduction to Food Engineering（熱交換器）](https://rpaulsingh.com/course/lectures/heatexch.html)
- [Wikipedia: NTU method](https://en.wikipedia.org/wiki/NTU_method)
- [神戸製鋼所：Open Rack Vaporizer](https://www.kobelco.co.jp/english/products/ecmachinery/lng/orv.html)
- [住友精密工業：LNG 気化器](https://www.spp.co.jp/en/netsu/products/lng/)
