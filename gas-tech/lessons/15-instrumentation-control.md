# 第 15 回 計装・制御（フィードバック制御と PID）

**分野：ガス技術（製造）**

## ねらい
- フィードバック制御の仕組み（測る → 比べる → 操作する）を、ブロックのつながりとして説明できる。
- 比例（P）制御だけでは「オフセット（残留偏差）」が残る理由を式で導き、積分（I）動作で消える理由を説明できる。
- プロセスの時定数とむだ時間の意味と、制御が難しくなる理由を説明できる。

## 1. 原理編

### 1.1 フィードバック制御の要素
ガス設備の圧力・流量・温度・熱量は、次のループで一定に保たれています。
1. **検出**：センサー（圧力計、流量計、熱量計）で制御量 y を測る。
2. **比較**：目標値（設定値）r との差、偏差 e = r − y を求める。
3. **調節**：調節計が e から操作量 u を計算する。
4. **操作**：調節弁などを動かし、プロセスに働きかける。

ずれを見て、ずれを減らす方向に操作するので「フィードバック」と呼びます。

### 1.2 PID 制御の式
  **u(t) = K_p·e(t) + K_i·∫e dt + K_d·de/dt**

（[Wikipedia: Proportional–integral–derivative controller](https://en.wikipedia.org/wiki/Proportional%E2%80%93integral%E2%80%93derivative_controller)）

| 動作 | 何に反応するか | 役割 |
|------|---------------|------|
| P（比例） | 今の偏差 | 偏差に比例して素早く操作する |
| I（積分） | 偏差の積み重ね（過去） | 偏差が残る限り操作を変え続け、オフセットを消す |
| D（微分） | 偏差の変化の速さ（未来の傾向） | 行き過ぎ（オーバーシュート）を抑え、安定させる |

（各動作の役割：[Michigan Tech CM416 講義資料](https://pages.mtu.edu/~tbco/cm416/lecture_06_2020.pdf)、[Automation Forum](https://automationforum.co/proportional-integral-derivative-control/)）

### 1.3 プロセスのモデル：一次遅れ
多くのプロセス（タンクの圧力、熱交換器の温度など）は、次の「一次遅れ」で近似できます。

  **τ·dy/dt + y = K·u**

| 記号 | 意味 |
|------|------|
| K | プロセスゲイン（u を 1 変えたとき、最終的に y がいくつ変わるか） |
| τ | 時定数（反応の遅さ） |

u を階段状に変えると、y は y(t) = K·Δu·(1 − e^(−t/τ)) と変わります。t = τ のとき 1 − e⁻¹ = 0.632 なので、**時定数は最終変化の 63.2 % に達するまでの時間**です。実際のプロセスには、操作してから反応が始まるまでの**むだ時間 L** もあります（一次遅れ + むだ時間、FOPDT モデル）（[APMonitor: First Order Plus Dead Time](https://apmonitor.com/pdc/index.php/Main/FirstOrderSystems)）。

### 1.4 P 制御のオフセットを導く
一次遅れのプロセスを P 制御（u = K_p·e）で動かし、落ち着いた状態（dy/dt = 0）を考えます。
1. プロセス：y = K·u
2. 調節計：u = K_p·(r − y)
3. 代入すると y = K·K_p·(r − y) → **y = r × K·K_p / (1 + K·K_p)**
4. オフセット：r − y = **r / (1 + K·K_p)**

**意味**：P 制御は「偏差があるから操作する」ので、操作量を出し続けるには偏差が必要です。K_p を大きくするとオフセットは小さくなりますが、0 にはなりません。大きくしすぎると、ノイズを増幅したり振動したりします（[Michigan Tech 講義資料](https://pages.mtu.edu/~tbco/cm416/lecture_06_2020.pdf)、[Wikipedia: PID controller](https://en.wikipedia.org/wiki/PID_controller)）。

**I 動作で消える理由**：落ち着いた状態では、積分項 ∫e dt も一定のはずです。積分が一定になるには e = 0 でなければなりません。つまり、I 動作があれば、落ち着いた状態では必ず偏差がなくなります。偏差がなくなれば、積分項はそれ以上増えなくなります。

### 1.5 むだ時間が制御を難しくする理由と調整
- 操作の効果が遅れて現れるので、その間に調節計が操作をし過ぎて、行き過ぎや振動が起きやすい。
- ジーグラー・ニコルスの方法（ステップ応答法）では、FOPDT の K・τ・L から、PI 制御の比例ゲインを K_p = 0.9·τ/(K·L) などと決める。この初期値は行き過ぎやすいので、20〜30 % 弱めることも多い。むだ時間が大きいプロセスには、Cohen-Coon 法やラムダ法などが勧められる（[gitconnected：Ziegler-Nichols PID Tuning](https://levelup.gitconnected.com/ziegler-nichols-pid-tuning-from-first-principles-the-method-that-brought-control-theory-out-of-the-0062c96dbaf3)、[open-exam-prep：Loop Tuning Methodologies](https://open-exam-prep.com/study-guides/isa-cap/development-simulation-tuning-fat/loop-tuning-methodologies)）。

### 1.6 積分ワインドアップ
- 調節弁は全開より開けないのに、積分項は偏差がある限り増え続ける。すると、計算上は「110 %、120 % 開け」となり、状況が戻ったときに大きく行き過ぎ、回復が遅れる。これを積分ワインドアップという。
- 対策は、弁が限界にある間は積分を止める（クランプ）、実際の弁の位置を積分に戻す（バックカリキュレーション）などである。最近の DCS や PLC には、この対策が組み込まれている（[luisllamas：Anti-windup and actuator saturation](https://www.luisllamas.es/en/anti-windup-and-actuator-saturation/)、[Industrial Monitor Direct：Integral Windup](https://industrialmonitordirect.com/blogs/knowledgebase/integral-windup-in-pid-controllers-prevention-solutions)）。

## 2. 実務とのつながり
- **熱量調整（第 13 回）**：熱量計で送り出すガスの熱量を測り、LPG の流量調節弁を PI 制御して 45 MJ/m³ に保つ。熱量計の分析には時間がかかるので、むだ時間が大きいループになる。
- **整圧器（第 17 回）**：ばねとダイヤフラムで動く整圧器は、それ自体が P 制御に近い。そのため流量が変わると出口圧力が少しずれる（オフセット）。これを第 17 回で「オフセット」として扱う。
- **LNG タンクの圧力（第 11 回）**：BOG 圧縮機の運転台数や回転数を調節して、タンクの圧力を一定に保つ。
- **安全計装**：通常の制御とは別に、異常時に自動で緊急遮断弁を閉める仕組みを設ける（法令ドリルのインターロックや緊急遮断装置の問題）。

## 3. 計算例
（python で検算済み。オイラー法で時間を追って計算した値と、式の値を比べた）

一次遅れのプロセス：K = 2、τ = 10 s、目標値 r = 1。

**例 1：P 制御のオフセット**
| 比例ゲイン K_p | 落ち着いた値 y | オフセット |
|---------------|---------------|-----------|
| 2 | 0.800（式：4/5） | 0.200 |
| 10 | 0.952（式：20/21） | 0.048 |
シミュレーションの値は、1.4 の式と一致した。

**例 2：PI 制御**
K_p = 2 に積分ゲイン K_i = 0.2 を加えると、落ち着いた値は **y = 1.000** になり、オフセットは消える。

**例 3：時定数とジーグラー・ニコルスの調整**
- t = τ での応答：1 − e⁻¹ = **0.632**（63.2 %）
- むだ時間 L = 2 s がある場合、PI 制御の比例ゲインは K_p = 0.9 × 10 / (2 × 2) = **2.25**。積分時間は L / 0.3 = **6.7 s**（ジーグラー・ニコルスのステップ応答法の値）。

## 4. 理解確認

### 理解確認 1
P 制御だけでは、偏差が 0 にならないのはなぜか。

<details><summary>解答</summary>

P 制御の操作量は u = K_p·e なので、操作量を 0 でない値に保つには、偏差 e が 0 でない必要がある。プロセスを目標値に保つには何らかの操作量が要るので、偏差が残る。式では、オフセット = r/(1 + K·K_p) で、K_p が有限なら 0 にならない。
</details>

### 理解確認 2
I 動作があると、落ち着いた状態で偏差が 0 になるのはなぜか。

<details><summary>解答</summary>

落ち着いた状態では操作量が一定なので、積分項 ∫e dt も一定でなければならない。積分が増えも減りもしないのは e = 0 のときだけである。つまり、偏差が残っている限り積分項が操作量を変え続け、偏差が 0 になったところで止まる。
</details>

### 理解確認 3（誤っているものはどれか）
(a) むだ時間が大きいプロセスほど、ゲインを大きくすると振動しやすい。
(b) 時定数は、ステップ入力に対して最終変化の 63.2 % に達するまでの時間である。
(c) 調節弁が全開のまま偏差が残っても、積分項は増えなくなるので、ワインドアップは起こらない。

<details><summary>解答</summary>

誤りは **(c)**。弁が全開で操作の効果がそれ以上出なくても、偏差が残っていれば積分項は増え続ける。これが積分ワインドアップで、状況が戻ったときに大きな行き過ぎや回復の遅れを起こす。
</details>

## 参考文献
- [Wikipedia: Proportional–integral–derivative controller](https://en.wikipedia.org/wiki/Proportional%E2%80%93integral%E2%80%93derivative_controller)
- [Wikipedia: PID controller](https://en.wikipedia.org/wiki/PID_controller)
- [Michigan Tech CM416 講義資料（PI 制御とオフセット）](https://pages.mtu.edu/~tbco/cm416/lecture_06_2020.pdf)
- [Automation Forum: Proportional, Integral and Derivative Control](https://automationforum.co/proportional-integral-derivative-control/)
- [APMonitor: First Order Plus Dead Time (FOPDT)](https://apmonitor.com/pdc/index.php/Main/FirstOrderSystems)
- [gitconnected：Ziegler-Nichols PID Tuning from First Principles](https://levelup.gitconnected.com/ziegler-nichols-pid-tuning-from-first-principles-the-method-that-brought-control-theory-out-of-the-0062c96dbaf3)
- [open-exam-prep：Loop Tuning Methodologies](https://open-exam-prep.com/study-guides/isa-cap/development-simulation-tuning-fat/loop-tuning-methodologies)
- [luisllamas：Anti-windup and actuator saturation](https://www.luisllamas.es/en/anti-windup-and-actuator-saturation/)
- [Industrial Monitor Direct：Integral Windup in PID Controllers](https://industrialmonitordirect.com/blogs/knowledgebase/integral-windup-in-pid-controllers-prevention-solutions)
