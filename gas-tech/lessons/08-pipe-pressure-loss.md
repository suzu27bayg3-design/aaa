# 第 08 回 流体力学 II：管内の圧力損失

**分野：基礎理論**

## ねらい
- 管の中の圧力損失の式（ダルシー・ワイスバッハの式）を、流体の円柱に働く力のつり合いから導ける。
- 層流で f = 64/Re になる理由を、速度分布（放物線）から説明できる。乱流では、f がレイノルズ数と管壁の粗さで決まることを説明できる。
- ガスの圧力が大きく下がる長い導管では、なぜ p₁² − p₂² の形の式を使うのかを説明できる。

## 1. 原理編

### 1.1 力のつり合いから圧力損失の式を導く
第 07 回のベルヌーイの式は「損失がない」流れの式でした。実際の管では、壁との摩擦で圧力が下がります。

内径 D、長さ L のまっすぐな管の中にある流体の円柱を考えます。流れが定常で、どこでも速度分布が同じ（十分に発達した流れ）なら、流体は加速しません。そのため、円柱に働く力はつり合っています。

- 押す力：両端の圧力差 × 断面積 = Δp · πD²/4
- 引き戻す力：壁のせん断応力 τ_w × 壁の面積 = τ_w · πDL

  Δp · πD²/4 = τ_w · πDL　→　**Δp = 4 τ_w L / D**

τ_w を動圧 ½ρV² と比べた無次元の数を、ダルシーの摩擦係数 f と定義します（f = 8τ_w / ρV²）。これを代入すると、

  **Δp = f · (L/D) · ρV²/2**　（ダルシー・ワイスバッハの式）

（[Wikipedia: Darcy–Weisbach equation](https://en.wikipedia.org/wiki/Darcy%E2%80%93Weisbach_equation)）

| 記号 | 意味 | 単位 |
|------|------|------|
| Δp | 長さ L での圧力損失 | Pa |
| f | ダルシーの摩擦係数（無次元） | — |
| L, D | 管の長さ、内径 | m |
| ρ | 流体の密度 | kg/m³ |
| V | 平均流速 | m/s |

- **意味**：圧力損失は、長さに比例し、内径に反比例し、動圧（流速の 2 乗）に比例します。
- **注意**：ダルシーの f は、ファニングの摩擦係数の 4 倍です。文献を読むときは、どちらの定義かを確かめる必要があります（[Wikipedia: Darcy–Weisbach equation](https://en.wikipedia.org/wiki/Darcy%E2%80%93Weisbach_equation)）。

### 1.2 f は何で決まるか：レイノルズ数と相対粗さ
τ_w に影響するのは、ρ・V・D・粘度 μ・壁の凹凸の高さ ε です。次元をそろえて整理すると、f は 2 つの無次元数だけの関数になります。

  **f = φ(Re, ε/D)**、　**Re = ρVD/μ**

- **レイノルズ数 Re**：慣性力と粘性力の比です。Re が小さいと、粘性が乱れを抑えて、流れが層になります（層流）。Re が大きいと、乱れが育ちます（乱流）（[CFD Online: Reynolds number](https://www.cfd-online.com/Wiki/Reynolds_Number)）。
- **境目の Re**：円管では Re ≈ 2300 より小さいと層流です。2300〜4000 は遷移域で、流れが定まりません（[Pipe Flow Software: Friction factor calculations](https://www.pipeflow.com/pipe-friction-factors)）。
- **相対粗さ ε/D**：ε は管壁の凹凸の高さです。目安は、市販の鋼管で 0.045〜0.09 mm、PE などの平滑なプラスチック管で 0.0015〜0.007 mm です（[Engineering ToolBox: Surface roughness](https://www.engineeringtoolbox.com/surface-roughness-ventilation-ducts-d_209.html)）。

### 1.3 層流：f = 64/Re を導く
半径 r の流体円柱にも、1.1 と同じ力のつり合いを当てはめます。

1. τ(r) = (Δp/L) · r/2。せん断応力は中心で 0、壁で最大になり、半径に比例します。
2. ニュートンの粘性法則 τ = −μ du/dr を使って積分し、壁で u = 0 とします。すると **u(r) = (Δp / 4μL)(R² − r²)** となり、速度分布は放物線になります。
3. 断面で平均すると、V = Δp R² / (8μL)。D = 2R で書き直すと、**Δp = 32μLV / D²**（ハーゲン・ポアズイユの式）。
4. これを Δp = f (L/D) ρV²/2 と比べると、**f = 64μ / (ρVD) = 64/Re**。

（[Wikipedia: Hagen–Poiseuille equation](https://en.wikipedia.org/wiki/Hagen%E2%80%93Poiseuille_equation)）

**意味**：層流の損失は、粘性だけで決まります。そのため、壁の粗さは関係しません。また Δp は V に比例し、V² には比例しません。式の上で f が 1/Re に比例するのは、このためです。

### 1.4 乱流：コールブルックの式とムーディ線図
乱流では、管壁のごく近くの薄い層（粘性底層）と、壁の凹凸の大きさの関係で f が決まります。理論だけでは導けないので、実験を整理した**コールブルック・ホワイトの式**を使います。

  **1/√f = −2.0 log₁₀[ (ε/D)/3.7 + 2.51/(Re√f) ]**

- f が両辺にあるので、くり返し計算で解きます。
- 陽に解ける近似式もあります。ハーランドの式 1/√f = −1.8 log₁₀[ ((ε/D)/3.7)^1.11 + 6.9/Re ] などです（[Wikipedia: Darcy friction factor formulae](https://en.wikipedia.org/wiki/Darcy_friction_factor_formulae)）。
- この関係を、Re と ε/D をパラメータにしてグラフにしたものが**ムーディ線図**です（1944 年）（[Wikipedia: Moody chart](https://en.wikipedia.org/wiki/Moody_chart)）。

式の 2 つの項の意味は次のとおりです。

| 状態 | 大きい項 | f の決まり方 |
|------|---------|-------------|
| 凹凸が粘性底層に隠れている（なめらかな管） | 2.51/(Re√f) | Re だけで決まる |
| 凹凸が底層より大きい（完全に粗い管） | (ε/D)/3.7 | ε/D だけで決まり、Re によらない |

完全に粗い管では、凹凸の後ろにできる渦（形状抵抗）が損失の主役になります。そのため、Δp はほぼ V² に比例します（[Pipe Flow Software](https://www.pipeflow.com/pipe-friction-factors)）。

### 1.5 内径の効き方：Δp ∝ Q²/D⁵
流量 Q が一定なら、V = 4Q/(πD²) です。f をおおよそ一定とみると、

  Δp = f (L/D) ρ/2 · (4Q/πD²)² ∝ **f · L · ρ · Q² / D⁵**

内径を 2 倍にすると、圧力損失は約 1/32 になります。導管の口径を選ぶとき、内径がとても強く効くのは、このためです。
層流なら Δp = 32μLV/D² = 128μLQ/(πD⁴) なので、Δp ∝ Q/D⁴ になります。

### 1.6 ガス（圧縮性流体）の場合
ガスは、圧力が下がると密度が下がります。そのため、下流ほど流速が上がります。質量流束 G = ρV（= 質量流量 / 断面積）は管の途中で一定なので、微小な長さ dx の運動量のつり合いは次のようになります。

  dp + G dV + f/(2D) · G²/ρ · dx = 0

等温の理想気体（ρ = pM/RT）として L まで積分すると、

  **p₁² − p₂² = G² (RT/M) · [ f L/D + 2 ln(p₁/p₂) ]**

（[Engineers Edge: Isothermal flow of compressible fluid](https://host.engineersedge.com/calculators/isothermal_flow_compressible_fluid_16362.htm)、[University of Technology（Iraq）講義資料 Compressible fluid](https://che.apps.uotechnology.edu.iq/wp-content/uploads/2024/12/Lect-4-Compressible-fluid.pdf)）

| 記号 | 意味 | 単位 |
|------|------|------|
| p₁, p₂ | 入口・出口の絶対圧力 | Pa |
| G | 質量流束 | kg/(m²·s) |
| R | 気体定数 8.314 | J/(mol·K) |
| T | 温度（一定とする） | K |
| M | ガスのモル質量 | kg/mol |

- ln の項は、ガスが膨張して加速する分です。長い導管では f L/D に比べて小さいので、省略できます。
- 省略すると **p₁² − p₂² ∝ f L G²** となります。中圧・高圧の導管の流量公式が p₁² − p₂² の形をしているのは、この式から来ています（第 16 回で扱う）。
- 圧力降下が入口圧力の 10 % 程度より小さければ、平均の密度を使ったダルシーの式でもほぼ合います。40 % を超えるようなら、圧縮性を考えた式を使います（[Pipe Flow Calculations: Compressible gas flow](https://www.pipeflowcalculations.com/pipe-valve-fitting-flow/compressible-gas-flow.xhtml)）。
- 低圧供給（家庭に届く数 kPa 程度）では圧力降下がとても小さいので、ガスもほぼ非圧縮として扱えます。

## 2. 実務とのつながり
- **低圧導管の口径選定**：低圧導管は、地区ガバナ（整圧器）の下流から需要家まで、少ない圧力差でガスを届けます。使える圧力差が小さいので、Δp ∝ Q²/D⁵ の関係から口径を決めます。
  - 太い管にはダクタイル鋳鉄管、細い管にはポリエチレン管が使われます（[大津市企業局 資料](https://www.city.otsu.lg.jp/material/files/group/14/gasu_1.pdf)）。
  - PE 管は壁がなめらか（ε が小さい）なので、同じ内径なら損失が少し小さくなります（計算例 1）。
- **導管の圧力区分**：導管は、中のガスの圧力で高圧・中圧・低圧に分けられます（[コトバンク：ガス導管](https://kotobank.jp/word/%E3%81%8C%E3%81%99%E5%B0%8E%E7%AE%A1-44612)）。圧力が高いほど、1.6 の圧縮性を考えた式が必要になります。
- **整圧器・メーター・継手**：まっすぐな管の損失（摩擦損失）のほかに、曲がりや弁などでの局所損失（ζ · ρV²/2 の形）もあります。第 17 回（整圧器）・第 25 回（メーター）で、機器の差圧として出てきます。

## 3. 計算例
（python で検算済み）

**共通の条件**
- 13A（標準状態の密度 0.827 kg/Nm³。第 02 回）を、15 ℃・ゲージ圧 2 kPa で流す。このときの密度は ρ = 0.799 kg/m³。
- 粘度は、メタンの値 μ = 1.107 × 10⁻⁵ Pa·s（25 ℃・1 atm）で代用する（[Engineering ToolBox: Methane viscosity](https://www.engineeringtoolbox.com/methane-dynamic-kinematic-viscosity-temperature-pressure-d_2068.html)）。

**例 1：低圧の鋼管で 20 m³/h を流す**
内径 D = 52.9 mm、L = 100 m、ε = 0.045 mm とする。
1. V = Q/A = (20/3600) / (π × 0.0529²/4) = **2.53 m/s**
2. Re = ρVD/μ = 0.799 × 2.53 × 0.0529 / 1.107×10⁻⁵ = **約 9,660**（乱流）
3. コールブルックの式で f = **0.0324**（ハーランドの式では 0.0323）
4. Δp = 0.0324 × (100/0.0529) × 0.799 × 2.53²/2 = **約 157 Pa**

同じ内径の PE 管（ε = 0.007 mm）にすると、f = 0.0314、Δp = **約 152 Pa** になります。この Re では、まだ「なめらかな管」に近いので、粗さの差は小さく効きます。

**例 2：内径を 2 倍にする**
同じ 20 m³/h を内径 105.3 mm の鋼管で流すと、Δp = **約 5.9 Pa** になり、約 1/26.5 に下がります。
1/32 にならないのは、V が 1/4、Re が 1/2（約 4,800）になって、f が約 1.2 倍に増えるからです。

**例 3：層流の場合**
0.5 m³/h を内径 25 mm の管で流すと、V = 0.283 m/s、Re = **約 511**（層流）です。f = 64/511 = 0.125 で、10 m あたりの Δp = **約 1.6 Pa** になります。

**例 4：高圧導管（圧縮性）**
- 条件：p₁ = 1.0 MPa（絶対圧）、D = 0.15 m、L = 5 km、T = 288 K、M = 0.0185 kg/mol（0.827 × 22.414 から）、ε = 0.045 mm、質量流量 1.5 kg/s（約 6,500 Nm³/h）。
- Re ≈ 1.15 × 10⁶、f = 0.0156。
- 1.6 の式をくり返し計算で解くと、p₂ = **約 718 kPa**、Δp = **約 282 kPa** になります。ln の項を省いても p₂ は 718.7 kPa で、ほぼ同じです。
- 入口の密度のまま非圧縮のダルシーの式を使うと、Δp = 242 kPa となり、**約 14 % 小さく見積もって**しまいます。下流で密度が下がり、流速が上がる分を見落とすからです。

## 4. 理解確認

### 理解確認 1
十分に発達した管内の流れで、Δp = 4τ_w L/D が成り立つのはなぜか。

<details><summary>解答</summary>

速度分布が流れの方向に変わらないので、流体の円柱は加速しない。そのため、円柱を押す力（Δp × 断面積）と、壁の摩擦力（τ_w × 壁の面積）がつり合うからである。断面積は D² に、壁の面積は D·L に比例するので、L/D が残る。
</details>

### 理解確認 2
層流では壁の粗さが f に効かないが、完全に粗い乱流では f が粗さだけで決まる。なぜか。

<details><summary>解答</summary>

- 層流：損失は粘性によるせん断だけで決まり、速度分布は放物線に決まる。壁の小さな凹凸は、この分布をほとんど変えない。
- 完全に粗い乱流：凹凸が粘性底層より高く突き出し、凹凸の後ろにできる渦（形状抵抗）が損失の主役になる。この抵抗は粘度によらず ρV² に比例するので、f は Re によらず ε/D だけで決まる。
</details>

### 理解確認 3（誤っているものはどれか）
(a) 流量が同じなら、内径を 2 倍にすると、乱流の圧力損失はおよそ 1/30 程度になる。
(b) 長い高圧ガス導管で、入口の密度のままダルシーの式を使うと、圧力損失を大きく見積もりすぎる。
(c) 層流の圧力損失は、平均流速に比例する。

<details><summary>解答</summary>

誤りは **(b)**。下流ほど圧力が下がって密度が小さくなり、流速が上がる。そのため、実際の損失は入口の密度で計算した値より**大きく**なる（例 4 では約 14 % 大きい）。
</details>

## 参考文献
- [Wikipedia: Darcy–Weisbach equation](https://en.wikipedia.org/wiki/Darcy%E2%80%93Weisbach_equation)
- [Wikipedia: Darcy friction factor formulae](https://en.wikipedia.org/wiki/Darcy_friction_factor_formulae)
- [Wikipedia: Moody chart](https://en.wikipedia.org/wiki/Moody_chart)
- [Wikipedia: Hagen–Poiseuille equation](https://en.wikipedia.org/wiki/Hagen%E2%80%93Poiseuille_equation)
- [CFD Online: Reynolds number](https://www.cfd-online.com/Wiki/Reynolds_Number)
- [Pipe Flow Software: Friction factor calculations](https://www.pipeflow.com/pipe-friction-factors)
- [Engineering ToolBox: Surface roughness](https://www.engineeringtoolbox.com/surface-roughness-ventilation-ducts-d_209.html)
- [Engineering ToolBox: Methane – dynamic and kinematic viscosity](https://www.engineeringtoolbox.com/methane-dynamic-kinematic-viscosity-temperature-pressure-d_2068.html)
- [Engineers Edge: Isothermal flow of compressible fluid](https://host.engineersedge.com/calculators/isothermal_flow_compressible_fluid_16362.htm)
- [University of Technology（Iraq）講義資料 Lect 4 Compressible fluid](https://che.apps.uotechnology.edu.iq/wp-content/uploads/2024/12/Lect-4-Compressible-fluid.pdf)
- [Pipe Flow Calculations: Compressible gas flow](https://www.pipeflowcalculations.com/pipe-valve-fitting-flow/compressible-gas-flow.xhtml)
- [大津市企業局 ガス導管の資料](https://www.city.otsu.lg.jp/material/files/group/14/gasu_1.pdf)
- [コトバンク：ガス導管](https://kotobank.jp/word/%E3%81%8C%E3%81%99%E5%B0%8E%E7%AE%A1-44612)
