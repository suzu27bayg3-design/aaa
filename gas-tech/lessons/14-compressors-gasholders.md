# 第 14 回 圧縮機とガスホルダー

**分野：ガス技術（製造）**

## ねらい
- 圧縮の仕事を、等温・断熱（ポリトロープ）の場合について、第一法則と状態方程式から導ける。
- 多段圧縮と中間冷却で仕事が減る理由と、各段の圧力比をそろえるとよい理由を説明できる。
- ガスホルダーが「時間による需要の変動」を吸収する原理と、送り出せるガスの量を計算できる。

## 1. 原理編

### 1.1 ポリトロープ変化
圧縮や膨張の途中では、圧力と体積の関係を次の式で表せることが多いです（ポリトロープ変化）。

  **p·Vⁿ = 一定**

n の値で、さまざまな変化を 1 つの式で表せます（[Wikipedia: Polytropic process](https://en.wikipedia.org/wiki/Polytropic_process)）。

| n | 変化 |
|---|------|
| 0 | 等圧 |
| 1 | 等温（理想気体） |
| k（比熱比） | 断熱（熱の出入りなし） |
| ∞ | 等積 |

実際の圧縮機は、多少冷やされるが等温ほどではないので、1 < n < k になります。

### 1.2 圧縮の仕事：導出
連続してガスを送る圧縮機（定常流れ）では、1 kg のガスを圧縮するのに必要な仕事（工業仕事）は、運動・位置エネルギーの変化を無視すると、

  **w = ∫ v dp**（v は比体積）

となります（第 05 回の開いた系の第一法則から）。
- **等温（n = 1）**：pv = RT が一定なので、v = RT/p を積分すると **w = R·T₁·ln(p₂/p₁)**
- **ポリトロープ（n）**：pvⁿ = 一定を使って積分すると **w = (n/(n−1))·R·T₁·[(p₂/p₁)^((n−1)/n) − 1]**（断熱なら n = k）
- **出口温度**：T₂ = T₁·(p₂/p₁)^((n−1)/n)（第 06 回のブレイトンサイクルと同じ関係）

| 記号 | 意味 | 単位 |
|------|------|------|
| R | ガス定数（= 8.314 / 分子量） | J/(kg·K) |
| T₁ | 吸込み温度 | K |
| p₁, p₂ | 吸込み・吐出しの絶対圧力 | Pa |
| k | 比熱比（メタンで約 1.3） | — |

**大事な性質**：同じ圧力比なら、必要な仕事は等温がいちばん小さく、断熱がいちばん大きく、ポリトロープはその間です（[Turbomachinery Magazine: Isothermal and intercooled compression](https://www.turbomachinerymag.com/view/isothermal-and-intercooled-compression)）。圧縮すると温度が上がり、体積が膨らむぶん、さらに押し込む仕事が増えるからです。p-V 線図では、断熱の曲線のほうが等温より急で、囲む面積（仕事）が大きくなります。

### 1.3 多段圧縮と中間冷却
1 段で高い圧力比まで圧縮すると、出口温度が高くなりすぎ、仕事も大きくなります。そこで、
1. 途中まで圧縮する
2. 中間冷却器（インタークーラ）で吸込み温度まで冷やす
3. 続きを圧縮する

と分けると、全体として等温圧縮に近づき、仕事が減ります。

**最適な中間圧力**：2 段で、どちらも吸込み温度から圧縮する場合、全体の仕事 w = c·[(pₘ/p₁)^m − 1] + c·[(p₂/pₘ)^m − 1] を pₘ で微分して 0 とおくと、

  **pₘ = √(p₁·p₂)**（各段の圧力比が等しい）

N 段なら、各段の圧力比を全体の圧力比の N 乗根にそろえると、仕事が最小になります（[open-exam-prep：Air & Gas Compressors](https://open-exam-prep.com/study-guides/in-cil-mt/paper-2-thermodynamics/air-gas-compressors)）。
ただし実際には、中間冷却器での圧力損失などがあるので、段数を増やしすぎると逆に不利になります（[Turbomachinery Magazine](https://www.turbomachinerymag.com/view/isothermal-and-intercooled-compression)）。

### 1.4 ガスホルダー：時間の変動を吸収する
- 都市ガスの使用量は、季節や時間帯で大きく変わる。ガスホルダーは、LNG 基地で作ったガスを使用量の少ない時間に貯めて、多い時間帯に送り出す。球形のホルダーは多数の鋼板を接合して造り、大地震にも耐えるよう設計されている（[世田谷区：東京ガスネットワーク 世田谷整圧所の資料](https://www.city.setagaya.lg.jp/documents/16037/124omote.pdf)）。
- **球形（高圧）ホルダー**：容積は一定で、**圧力を変えて**ガスを出し入れする。
- **容量可変型（低圧）ホルダー**：圧力は一定で、**容積を変えて**出し入れする。三菱重工の COS 型では、内屋根がガス量に応じて上下し、シール油でガスの漏れを防ぐ（[三菱重工：ガスホルダー](https://www.mhi.com/jp/business/products-services/industrial-machinery/storage-tanks-gas-holder/gas-holder)、[三菱重工：技術情報](https://www.mhi.com/jp/business/products-services/industrial-machinery/storage-tanks-gas-holder/gas-holder/technical-information)）。

**球形ホルダーから送り出せる量**（ボイルの法則、第 02 回）：
  **Q = V × (p_max − p_min) / p₀ × (T₀ / T)**

V はホルダーの容積、p₀・T₀ は標準状態の圧力と温度です。圧力の上限と下限の差だけが送り出せる量になり、下限の圧力までのガスは、下流に送るための圧力として残しておきます。

## 2. 実務とのつながり
- **圧縮機の種類**：往復動式は高い圧力比が得やすく、遠心式（ターボ）は大流量に向く。どちらも、吐出し温度の上限と、所要動力を考えて段数を決める。
- **BOG 圧縮機（第 11 回）**：LNG タンクの BOG を圧縮して送り出す。吸込みがとても低温なので、材料と潤滑に注意が要る。
- **ガスホルダーと整圧器**：ホルダーから出したガスは、整圧器（第 17 回）で一定の圧力に下げて導管へ送る。
- **高圧ガスの保安**：圧縮機やホルダーは高圧ガス設備として、耐圧・気密の検査や安全装置の規制を受ける（法令ドリルの一般則の問題で頻出）。

## 3. 計算例
（python で検算済み）

**例 1：天然ガスを 1.0 MPa から 4.0 MPa（絶対圧）に圧縮する**
メタン（R = 518.3 J/(kg·K)、k = 1.3）、吸込み温度 300 K。
| 方式 | 1 kg あたりの仕事 | 出口温度 |
|------|------------------|---------|
| 等温（理想） | 215.6 kJ/kg | 300 K |
| 断熱 1 段 | 254.0 kJ/kg | 413 K（140 ℃） |
| 断熱 2 段（中間圧力 2.0 MPa、中間冷却で 300 K に戻す） | 233.8 kJ/kg | 352 K（79 ℃） |
- 2 段にすると、仕事は 1 段より **8 %** 減り、出口温度も 60 K 下がる。
- 10 kg/s を圧縮するのに必要な動力は、1 段で約 2,540 kW、2 段で約 2,340 kW（どちらも効率 100 % とした理論値）。

**例 2：球形ホルダーから送り出せる量**
容積 30,000 m³、運転圧力 0.85 MPa（ゲージ圧）→ 0.35 MPa（ゲージ圧）、ガスの温度 15 ℃。
- Q = 30,000 × 0.5 / 0.101325 × 273.15 / 288.15 = **約 140,000 m³N**
- 容積の約 4.7 倍のガスを、需要の多い時間帯に送り出せる。

## 4. 理解確認

### 理解確認 1
同じ圧力比でも、断熱圧縮は等温圧縮より大きな仕事が必要になるのはなぜか。

<details><summary>解答</summary>

断熱圧縮では、加えた仕事でガスの温度が上がり、同じ圧力での体積（比体積 v）が等温の場合より大きくなる。仕事は w = ∫ v dp なので、v が大きいぶん積分（p-V 線図の面積）が大きくなる。
</details>

### 理解確認 2
2 段圧縮で、各段の圧力比をそろえる（中間圧力を幾何平均にする）と仕事が最小になるのはなぜか。

<details><summary>解答</summary>

各段の仕事は (圧力比)^m − 1 の形で、圧力比について下に凸に増える。片方の段の圧力比を大きくすると、もう片方で減らせる量より増える量のほうが大きい。全体の仕事を中間圧力で微分すると、両段の圧力比が等しいときに最小になる。
</details>

### 理解確認 3（誤っているものはどれか）
(a) 中間冷却をすると、全体の圧縮は等温圧縮に近づく。
(b) 球形ガスホルダーは、圧力を一定にして容積を変えながらガスを出し入れする。
(c) ポリトロープ指数 n が 1 のときは等温変化、比熱比 k のときは断熱変化を表す。

<details><summary>解答</summary>

誤りは **(b)**。球形ホルダーは容積が一定で、**圧力**を変えて出し入れする。圧力を一定にして容積を変えるのは、内屋根などが上下する容量可変型（低圧）ホルダーである。
</details>

## 参考文献
- [Wikipedia: Polytropic process](https://en.wikipedia.org/wiki/Polytropic_process)
- [Turbomachinery Magazine: Isothermal and intercooled compression](https://www.turbomachinerymag.com/view/isothermal-and-intercooled-compression)
- [open-exam-prep：Air & Gas Compressors（多段圧縮）](https://open-exam-prep.com/study-guides/in-cil-mt/paper-2-thermodynamics/air-gas-compressors)
- [世田谷区：東京ガスネットワーク 世田谷整圧所の資料](https://www.city.setagaya.lg.jp/documents/16037/124omote.pdf)
- [三菱重工：ガスホルダー](https://www.mhi.com/jp/business/products-services/industrial-machinery/storage-tanks-gas-holder/gas-holder)
- [三菱重工：ガスホルダー 技術情報](https://www.mhi.com/jp/business/products-services/industrial-machinery/storage-tanks-gas-holder/gas-holder/technical-information)
