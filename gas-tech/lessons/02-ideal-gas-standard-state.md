# 第 02 回 理想気体と標準状態（Nm³）

**分野：基礎理論**

## ねらい
- 理想気体の状態方程式 pV = nRT を、分子の衝突から導き、何を仮定しているかを説明できる。
- 「Nm³（ノルマル立方メートル）」が何を基準にした量かを理解し、ガスメーターの読みや容器の中身を Nm³ に換算できる。
- 混合ガスの分圧の考え方（ドルトンの法則）と、理想気体の式が使えなくなる条件を知る。

## 1. 原理編

### 1.1 圧力はどこから来るか（気体分子運動論）
一辺 L の立方体の箱に、質量 m の分子が N 個入っているとします。

1. x 方向の速さ vₓ の分子が壁に**弾性衝突**すると、運動量の変化は 2mvₓ。
2. 同じ壁に戻ってくるまでの時間は 2L/vₓ。したがって、1 個の分子が壁に及ぼす平均の力は 2mvₓ ÷ (2L/vₓ) = mvₓ²/L。
3. N 個の分子について平均をとり、⟨vₓ²⟩ = ⟨v²⟩/3（向きに偏りがないので）を使い、壁の面積 L² で割ると

  **p = (1/3)·(N/V)·m⟨v²⟩**　（V = L³）

導出の流れは [Save My Exams: Derivation of the Kinetic Theory of Gases Equation](https://www.savemyexams.com/a-level/physics/cie/25/revision-notes/15-ideal-gases/15-3-kinetic-theory-of-gases/derivation-of-the-kinetic-theory-of-gases-equation/) と [schoolphysics: Kinetic theory equation](https://www.schoolphysics.co.uk/age16-19/Thermal%20physics/Kinetic%20theory%20of%20matter/text/Kinetic_theory_equation/index.html) を参照。

### 1.2 温度との結び付け → 状態方程式
温度は、分子の平均の運動エネルギーの大きさを表します。

  (1/2)m⟨v²⟩ = (3/2)·k·T　（k：ボルツマン定数）

これを 1.1 の式に代入すると、pV = NkT。
分子の数 N を物質量 n [mol] で書くと N = n·N_A なので、

  **pV = nRT**　（R = N_A·k）

| 記号 | 意味 | 単位・値 |
|------|------|---------|
| p | 圧力（**絶対圧**） | Pa |
| V | 体積 | m³ |
| n | 物質量 | mol |
| T | 絶対温度 | K（= ℃ + 273.15） |
| k | ボルツマン定数 | 1.380649×10⁻²³ J/K（定義値） |
| N_A | アボガドロ定数 | 6.02214076×10²³ mol⁻¹（定義値） |
| R | 気体定数 | 8.314462618… J/(mol·K)（定義値の積なので厳密な値） |

k と N_A は 2019 年の SI 改定で定義値になり、R も厳密な値になりました
（[Weblio「気体定数」（Wikipedia 転載）](https://www.weblio.jp/content/%E6%B0%97%E4%BD%93%E5%AE%9A%E6%95%B0)、[Cantera: Physical Constants](https://www.cantera.org/3.2/cxx/db/d22/group__physConstants.html)）。
古い資料の 8.314472 などは改定前の値です（[気象学会 定数表（CODATA 2002 値）](https://metsoc.jp/member_pages/yogo_temp/constants.files/sheet002.htm)）。

**前提（理想気体の仮定）**
- 分子そのものの体積は無視できる。
- 分子どうしの間に力（引力・斥力）がはたらかない。
- 衝突は弾性的である。

（[Save My Exams](https://www.savemyexams.com/a-level/physics/cie/25/revision-notes/15-ideal-gases/15-3-kinetic-theory-of-gases/derivation-of-the-kinetic-theory-of-gases-equation/)）

ボイルの法則（T 一定で pV 一定）とシャルルの法則（p 一定で V/T 一定）は、どちらもこの式の特別な場合です。

### 1.3 標準状態とモル体積
0 ℃（273.15 K）、101.325 kPa（1 atm）で 1 mol が占める体積は

  V_m = RT/p = 8.31446 × 273.15 / 101325 = 0.022414 m³ = **22.414 L/mol**

**Nm³** は、「この標準状態に換算したときの体積」です。1 Nm³ はおよそ 44.62 mol に当たります。
Nm³ の基準を 0 ℃・1 atm とする定義が一般的ですが、業界や地域によって 15 ℃や 60 °F を基準にする例もあり、単一の決まりはありません
（[petroleumacronyms: Nm3](https://www.petroleumacronyms.com/glossary/nm3)、[Industrial Monitor Direct: Nm3 standard conditions](https://industrialmonitordirect.com/blogs/knowledgebase/nm3-gas-volume-standard-conditions-explained)）。
基準の圧力を 1 bar（100 kPa）にすると、モル体積は 22.711 L/mol に変わります。**どの基準の値なのかを必ず確認する**ことが重要です。

### 1.4 混合ガスと分圧（ドルトンの法則）
互いに反応しない気体を混ぜたとき、全圧は各成分の分圧の和になります。

  p = Σpᵢ、　pᵢ = xᵢ·p　（xᵢ：モル分率 = 体積分率）

各成分がそれぞれ pᵢV = nᵢRT に従うとして足し合わせれば、pV = nRT がそのまま出てきます
（[コトバンク「分圧」](https://kotobank.jp/word/%E5%88%86%E5%9C%A7)、[metricgate: ドルトンの分圧の法則](https://metricgate.com/docs/ja/daltons-law-partial-pressure/)）。
理想気体では「体積分率 = モル分率」が成り立ちます。そのため、都市ガスの組成を vol% で表せば、そのまま mol% として計算に使えます。

### 1.5 理想気体の式が使えなくなるとき
高い圧力や低い温度では、分子の体積や分子間の力が無視できなくなり、理想気体の式からずれます（[metricgate](https://metricgate.com/docs/ja/daltons-law-partial-pressure/)）。
このずれは圧縮係数 Z = pV/(nRT) で表します（理想気体なら Z = 1）。
高圧ガスの容器や高圧導管を扱うときは、Z を使った補正が必要になります。

## 2. 実務とのつながり
- **ガスメーターの換算**：メーターは、その場の温度・圧力での体積を測ります。料金や熱量の計算では、標準状態への補正を考える必要があります（下の計算例 1）。
- **ウォッベ指数の比重（第 01 回）**：比重 d は、同じ温度・圧力での密度の比で、モル質量の比に等しい。メタン 16.04 ÷ 空気 28.97 ≒ 0.554 となり、第 01 回で使った値 0.555 と一致します。
- **高圧ガスの量の基準**：高圧ガス保安法の「処理容積 100 m³/日」「貯蔵 300 m³」などの容積も、温度・圧力を決めて換算した値です（法令トラック セット 01）。
- **ゲージ圧と絶対圧**：pV = nRT に入れる p は絶対圧です。圧力計の読み（ゲージ圧）には大気圧を足して使います。

## 3. 計算例

**例 1：ガスメーターの読みを Nm³ に換算する**
メーターの読みが 100 m³、ガスの温度が 20 ℃、メーター内の圧力が大気圧 + 2.0 kPa のとき、標準状態（0 ℃・101.325 kPa）での体積は？

- 手順：n が一定なので、p₁V₁/T₁ = p₀V₀/T₀ を V₀ について解く。
- V₀ = 100 × (103.325/101.325) × (273.15/293.15) = **95.0 Nm³**
- 温度が高いとガスは膨張しているので、標準状態に直すと体積は小さくなる。圧力の補正は逆向きに少しはたらく。

**例 2：容器の中身を見積もる**
内容積 47 L の容器に、圧縮ガスが 15 MPa（絶対圧）・35 ℃で入っている。理想気体と仮定すると何 Nm³ か？

- n = pV/(RT) = 15×10⁶ × 0.047 / (8.314 × 308.15) = 275 mol
- 体積 = 275 × 0.022414 = **6.17 Nm³**
- 注意：15 MPa では Z ≠ 1 なので、実際の値はガスの種類によってずれる。

（数値は python で検算済み）

## 4. 理解確認

### 理解確認 1
気体分子運動論の導出で、圧力が m⟨v²⟩ に比例するのはなぜか。

<details><summary>解答</summary>

壁に及ぼす力は「1 回の衝突での運動量変化 2mvₓ」と「単位時間あたりの衝突回数 vₓ/2L」の積になる。そのため、v の 2 乗が現れる。速い分子ほど強く、しかも頻繁に壁に当たるからである。
</details>

### 理解確認 2
同じ「1 Nm³」でも、資料によってモル数が違うことがある。なぜか。

<details><summary>解答</summary>

「標準状態」の定義が統一されていないため。0 ℃・101.325 kPa なら 22.414 L/mol、0 ℃・100 kPa なら 22.711 L/mol、15 ℃基準ならさらに違う値になる。基準を確認せずに比べると、数 % の誤差が出る。
</details>

### 理解確認 3（誤っているものはどれか）
(a) pV = nRT の p には、圧力計の読み（ゲージ圧）をそのまま入れる。
(b) 理想気体の混合物では、体積分率とモル分率は等しい。
(c) 高圧・低温では、実在の気体は理想気体の式からずれる。

<details><summary>解答</summary>

誤りは **(a)**。状態方程式の p は絶対圧で、ゲージ圧に大気圧を足した値を使う。
(b) はドルトンの法則と状態方程式から導ける。(c) は分子の体積と分子間の力の影響による。
</details>

## 参考文献
- [Save My Exams: Derivation of the Kinetic Theory of Gases Equation](https://www.savemyexams.com/a-level/physics/cie/25/revision-notes/15-ideal-gases/15-3-kinetic-theory-of-gases/derivation-of-the-kinetic-theory-of-gases-equation/)
- [schoolphysics: Kinetic theory equation](https://www.schoolphysics.co.uk/age16-19/Thermal%20physics/Kinetic%20theory%20of%20matter/text/Kinetic_theory_equation/index.html)
- [Weblio「気体定数」](https://www.weblio.jp/content/%E6%B0%97%E4%BD%93%E5%AE%9A%E6%95%B0)
- [Cantera 3.2: Physical Constants](https://www.cantera.org/3.2/cxx/db/d22/group__physConstants.html)
- [日本気象学会 定数表（旧 CODATA 値の例）](https://metsoc.jp/member_pages/yogo_temp/constants.files/sheet002.htm)
- [petroleumacronyms: Nm3](https://www.petroleumacronyms.com/glossary/nm3)
- [Industrial Monitor Direct: Nm3 Gas Volume Standard Conditions Explained](https://industrialmonitordirect.com/blogs/knowledgebase/nm3-gas-volume-standard-conditions-explained)
- [コトバンク「分圧」](https://kotobank.jp/word/%E5%88%86%E5%9C%A7)
- [metricgate: ドルトンの分圧の法則](https://metricgate.com/docs/ja/daltons-law-partial-pressure/)
