# 第 07 回 流体力学 I：ベルヌーイの式と流量計測

**分野：基礎理論**

## ねらい
- ベルヌーイの式を、流線に沿ったエネルギーの保存として導き、使える条件（前提）を説明できる。
- 連続の式とベルヌーイの式から、オリフィス流量計の式を導き、流出係数 C が何を補正しているかを説明できる。
- ガスメーター（膜式・超音波式）の計測原理を、物理の言葉で説明できる。

## 1. 原理編

### 1.1 ベルヌーイの式
流線（流れに沿った線）の上で、流体の小さなかたまりにニュートンの第二法則（オイラーの運動方程式）を当てはめます。密度一定として積分すると、

  **p + ½ρV² + ρgz = 一定**　（ヘッドの形では p/ρg + V²/2g + z = 一定）

（[Iowa 大学 講義ノート Chapter 3](https://user.engineering.uiowa.edu/~fluids/archive/lecture_notes/Chapter_3_Sec1/Chapter_3.pdf)、[Purdue 大学 講義ノート](https://engineering.purdue.edu/~wassgren/teaching/ME30800/NotesAndReading/BernoullisEquation_LectureNotes.pdf)）

| 記号 | 意味 | 単位 |
|------|------|------|
| p | 静圧 | Pa |
| ½ρV² | 動圧（流れの運動エネルギー） | Pa |
| ρgz | 高さによる位置エネルギー | Pa |

**前提**（どれかが崩れると、式はそのままでは使えない）
- 定常流れ（時間で変わらない）
- 粘性による損失がない（非粘性）
- 非圧縮（流速が音速よりずっと小さい）
- 同じ流線の上で比べる（渦のない流れなら、流線をまたいでも同じ一定値）
- 熱の出入りがない

（[NASA Glenn: Bernoulli's Equation](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/bernoullis-equation/)）

**意味**：流れが速くなるところでは、静圧が下がります。エネルギーの総量は保存されたまま、圧力の形から運動の形へ移るからです。

### 1.2 連続の式
管の中では、断面積 A と流速 V の積（体積流量）が、どの断面でも同じです（非圧縮の場合）。

  **A₁V₁ = A₂V₂**

細いところでは流れが速くなります。

### 1.3 オリフィス流量計の式
管（内径 D）の中に、穴（直径 d）のあいた板を入れます。上流 1 と穴の位置 2 で、ベルヌーイの式と連続の式を組み合わせます。

1. p₁ − p₂ = ½ρ(V₂² − V₁²)
2. 連続の式から V₁ = V₂·(d/D)² = V₂·β²（β = d/D：絞り直径比）
3. 1 に代入して V₂ について解くと、V₂ = √(2Δp / (ρ(1 − β⁴)))
4. 質量流量は q_m = ρ·(π/4)d²·V₂

実際の流れでは、穴を通った流れが穴より細く縮み（縮流）、摩擦の損失もあります。これを**流出係数 C** で補正します。気体では、圧力が下がると膨張する分を**膨張補正係数 ε**（ε < 1。液体なら ε = 1）で補正します。

  **q_m = C·ε·(π/4)d²·√(2ρΔp / (1 − β⁴))**

（[Wikipedia: Orifice plate](https://en.wikipedia.org/wiki/Orifice_plate)）

- C は 0.6〜0.85 程度で、形状や圧力の取り出し位置によって変わる（[Deltares Wanda: Orifice](https://deltares-wanda-core.readthedocs-hosted.com/en/latest/liquid/component_orifice.html)）。
- ISO 5167-2 では、C を Reader-Harris/Gallagher の式で求める。この式の定数項は約 0.596 で、0.2 ≦ β ≦ 0.75 の範囲で使える（[Wikipedia: Orifice plate](https://en.wikipedia.org/wiki/Orifice_plate)）。
- ε の式には議論があり、見直しを提案する論文もある（[Lviv 工科大学 論文](https://science.lpnu.ua/node/5449)）。
- ISO 5167 は、満水の管の中の、音速以下で単相の流れに使える規格である（[ISO 5167-1 Amd 1](https://iteh.es/catalog/standards/iso/316250a5-b651-4757-82c5-af37eff1fd24/iso-5167-1-1991-amd-1-1998)）。

**大事な性質**：流量は **√Δp に比例**します。差圧が 4 倍になっても、流量は 2 倍にしかなりません。そのため、流量が小さいと差圧がとても小さくなり、測りにくくなります。

### 1.4 ガスメーターの計測原理
- **膜式**：2 つの計量室を膜で仕切り、ガスの圧力差で膜を往復させる。1 往復で決まった体積が送られるので、往復の回数を数えれば体積が分かる（容積式。[特許 JP2898619B1 温度補正機能付膜式ガスメータ](https://patents.google.com/patent/JP2898619B1/ja)）。
- **超音波式**：流れの上流側と下流側に向かい合わせた 2 つのセンサーで、超音波が届く時間を測る。流れに乗った向き（下流向き）は速く、逆らう向き（上流向き）は遅く届く。その差から流速を求める（[TI: ガスメーター](https://www.ti.com/solution/ja-jp/gas-meter)、[Impress 家電 Watch](https://kaden.watch.impress.co.jp/docs/news/1400853.html)）。可動部品がない。

  音速を c、センサー間の距離を L、流れとのなす角を θ とすると、
  - t_下流向き = L / (c + V cosθ)
  - t_上流向き = L / (c − V cosθ)
  - **V = L / (2cosθ) × (1/t_下流向き − 1/t_上流向き)**

  この式では c が消えます。そのため、ガスの種類や温度で音速が変わっても、流速を求められます。

- 都市ガスのメーター約 3,500 万台のうち、約 350 万台が超音波式である（[経済産業省 計量行政審議会資料](https://www.meti.go.jp/shingikai/keiryogyoseishin/kihon/pdf/2025_002_04_00.pdf)）。

## 2. 実務とのつながり
- **バーナのノズル（第 01 回）**：ウォッベ指数の導出は、1.3 と同じく「ノズルを通る流量 ∝ √(Δp/ρ)」から出てきた。
- **一次空気の吸い込み（第 21 回）**：ガスがノズルから速く噴き出すと、まわりの圧力が下がって空気を吸い込む。これもベルヌーイの式で説明できる。
- **大口の流量計測**：工場や整圧所では、オリフィス流量計や超音波流量計が使われる。計量した体積は、温度・圧力を補正して標準状態に換算する（第 02 回）。
- **圧力損失（第 08 回）**：実際の管の中では摩擦でエネルギーが失われるので、ベルヌーイの式に損失の項を加える。

## 3. 計算例
（python で検算済み）

**例 1：オリフィス流量計**
管の内径 D = 100 mm、穴の直径 d = 50 mm（β = 0.5）、ガスの密度 ρ = 4.0 kg/m³、差圧 Δp = 10 kPa。C = 0.605、ε = 0.98 と仮定する。
- q_m = 0.605 × 0.98 × (π/4) × 0.05² × √(2 × 4.0 × 10,000 / (1 − 0.5⁴)) = **0.340 kg/s**
- 体積流量（その場の状態）：0.340 / 4.0 = 0.085 m³/s = **306 m³/h**
- 標準状態に換算すると（13A の密度を 0.64 × 1.292 = 0.827 kg/Nm³ とする。第 02 回）、**約 1,480 Nm³/h**

**例 2：超音波式の時間差**
L = 0.1 m、θ = 45°、音速 c = 440 m/s（メタン程度と仮定）、流速 V = 5 m/s のとき、
- 下流向きと上流向きの到達時間の差は **約 3.65 μs**
- 1.4 の式に戻すと、V = 5.00 m/s が求まる（音速の値によらない）。

## 4. 理解確認

### 理解確認 1
オリフィスの式に流出係数 C が必要なのはなぜか。

<details><summary>解答</summary>

ベルヌーイの式は、損失のない理想的な流れで、穴の直径いっぱいに流れると仮定しているから。実際には、流れが穴より細く縮み（縮流）、摩擦の損失もあるので、理想の流量より少なくなる。その差を補正するのが C である。
</details>

### 理解確認 2
オリフィス流量計で、流量を 2 倍にすると差圧は何倍になるか。それはなぜか。

<details><summary>解答</summary>

4 倍。流量は √Δp に比例するからである。ベルヌーイの式で、差圧が流速の 2 乗（動圧 ½ρV²）に対応しているためである。
</details>

### 理解確認 3（誤っているものはどれか）
(a) ベルヌーイの式は、粘性による損失がない流れを前提にしている。
(b) 超音波式ガスメーターは、往復時間の差から流速を求めるので、音速が変わっても流速を求められる。
(c) 膜式ガスメーターは、ガスの流速を測って体積を計算する。

<details><summary>解答</summary>

誤りは **(c)**。膜式は、膜の往復 1 回ごとに決まった体積が送られる「容積式」で、往復の回数から体積を求める。流速は測らない。
</details>

## 参考文献
- [Iowa 大学 講義ノート Chapter 3 Bernoulli Equation](https://user.engineering.uiowa.edu/~fluids/archive/lecture_notes/Chapter_3_Sec1/Chapter_3.pdf)
- [Purdue 大学 ME308 Bernoulli's Equation 講義ノート](https://engineering.purdue.edu/~wassgren/teaching/ME30800/NotesAndReading/BernoullisEquation_LectureNotes.pdf)
- [NASA Glenn: Bernoulli's Equation](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/bernoullis-equation/)
- [Wikipedia: Orifice plate](https://en.wikipedia.org/wiki/Orifice_plate)
- [Deltares Wanda: Orifice](https://deltares-wanda-core.readthedocs-hosted.com/en/latest/liquid/component_orifice.html)
- [ISO 5167-1:1991/Amd 1:1998](https://iteh.es/catalog/standards/iso/316250a5-b651-4757-82c5-af37eff1fd24/iso-5167-1-1991-amd-1-1998)
- [Lviv 工科大学 論文（膨張補正係数）](https://science.lpnu.ua/node/5449)
- [特許 JP2898619B1 温度補正機能付膜式ガスメータ](https://patents.google.com/patent/JP2898619B1/ja)
- [Texas Instruments: ガスメーター](https://www.ti.com/solution/ja-jp/gas-meter)
- [Impress 家電 Watch（超音波式ガスメーター）](https://kaden.watch.impress.co.jp/docs/news/1400853.html)
- [経済産業省 計量行政審議会資料（ガスメーターの台数）](https://www.meti.go.jp/shingikai/keiryogyoseishin/kihon/pdf/2025_002_04_00.pdf)
