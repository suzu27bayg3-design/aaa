# 第 11 回 LNG の物性と BOG（ボイルオフガス）

**分野：ガス技術（製造）**

## ねらい
- LNG が −162 ℃の液体であることと、体積がガスの約 1/600 になる理由を、密度から説明できる。
- タンクに入る熱と、蒸発する量（BOG）の関係を、エネルギー収支（侵入熱 = 蒸発量 × 蒸発潜熱）から導ける。
- 成分の違いで起こる現象（ウェザリング、層状化、ロールオーバー）の原理を説明できる。

## 1. 原理編

### 1.1 LNG とは：沸点にある液体
- LNG は、天然ガス（主成分メタン）を約 −162 ℃まで冷やして液体にしたもの。沸点はおよそ −161.5 ℃、密度は約 410〜500 kg/m³（組成による）（[Engineering ToolBox: LNG](https://engineeringtoolbox.com/liquefied-natural-gas-lng-d_1092.html)、[World Ports Sustainability Program: What is LNG?](https://sustainableworldports.org/clean-marine-fuels/lng-bunkering/what-is-lng/)）。
- 液体にすると、体積はガスの約 **1/600** になる。そのため、遠くまで船で運べる（[World Ports Sustainability Program](https://sustainableworldports.org/clean-marine-fuels/lng-bunkering/what-is-lng/)）。
- 大気圧のタンクの中の LNG は、**沸点にある液体**（飽和液）です。熱が入っても温度はほとんど上がらず、その熱は液を蒸発させるのに使われます。これが BOG の発生源です。

**1/600 の理由（密度の比）**：
  体積比 = 液体の密度 / ガスの密度

メタンの場合、液体の密度は約 450 kg/m³、標準状態（0 ℃、1 atm）のガスの密度は約 0.717 kg/m³ です。比は約 630 になります（計算例 1）。分子の間の距離が縮まり、同じ質量が小さな体積に収まるからです（第 02 回の理想気体の式で、気体の密度は ρ = pM/RT）。

### 1.2 蒸発潜熱
- メタンの沸点は 111.5 K、蒸発潜熱は 8.19 kJ/mol。分子量 16.04 で割ると、約 **511 kJ/kg** になる（[Engineering ToolBox: Methane](https://www.engineeringtoolbox.com/methane-d_1420.html)）。
- 蒸発潜熱は、液体の分子どうしを引き離すのに必要なエネルギーです。温度を上げずに状態だけを変える熱なので「潜熱」と呼びます。

### 1.3 BOG の量：侵入熱 = 蒸発量 × 潜熱
タンクを 1 つの系と考え、第一法則（第 05 回）を当てはめます。定常状態で液の温度が一定なら、入った熱はすべて蒸発に使われるので、

  **ṁ_BOG = Q_in / L**

| 記号 | 意味 | 単位 |
|------|------|------|
| ṁ_BOG | 蒸発するガスの質量流量 | kg/s |
| Q_in | 断熱材を通って入る熱（侵入熱） | W |
| L | 蒸発潜熱 | J/kg |

**ボイルオフ率（BOR）**：1 日に蒸発する量を、タンク内の LNG の量で割った割合（%/日）です。
- 陸上タンクや LNG 船では、1 日あたり 0.05〜0.15 % 程度。断熱は、気化を全容量の 0.05 %/日未満に抑えるように選ばれる（[米国特許 10808887](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10808887)、[LAPSE 2023.27212（BOG に関するレビュー）](https://psecommunity.org/LAPSE:2023.27212)）。
- **大事な性質**：侵入熱 Q_in は液の量にあまりよらない（断熱材とタンクの表面積で決まる）。そのため、液が少ないほど BOR（%/日）は大きくなる。260,000 m³ のタンクのシミュレーションでは、80 % 充填で 0.012 wt%/日、10 % 充填で 0.12 wt%/日だった（[Energies 2020（DOAJ）](https://doaj.org/article/24d1ff8757e74f818fc12dbffb40f509)）。

### 1.4 成分の違いで起こる現象
LNG はメタンだけでなく、窒素・エタン・プロパンなどの混合物です。沸点が低い成分ほど先に蒸発します。
- **ウェザリング（エージング）**：沸点の低いメタンが先に蒸発するので、残った液は重い成分の割合が増え、密度と発熱量が上がる（[IChemE Symposium Series 139](https://www.icheme.org/media/25371/major-hazards-onshore-and-offshore-ii-icheme-symposium-series-139-1995-46-baker.pdf)）。
- **窒素が多い場合**：窒素（沸点 −196 ℃）が 1 % を超えるほど含まれると、窒素が先に抜けて、表面の液のほうが下の液より軽くなることがある。すると表面に蓋をする層ができ、下の層に熱がたまる（オートストラティフィケーション）（[IChemE Symposium Series 139](https://www.icheme.org/media/25371/major-hazards-onshore-and-offshore-ii-icheme-symposium-series-139-1995-46-baker.pdf)）。
- **層状化**：密度の違う LNG を受け入れると、上下に層ができる。密度差 1 kg/m³ でも、ゆっくり受け入れると層ができうる（[SIGTTO: Guidance for the Prevention of Rollover on LNG Ships](https://www.sigtto.org/media/1398/guidance-for-the-prevention-of-rollover-on-lng_ships.pdf)）。
- **ロールオーバー**：下の層は上の層に押さえられて蒸発できず、熱をためて温度が上がる。やがて両層の密度が近づくと、下の層が一気に上がってきて、ためていた熱で大量の BOG が急に発生する。タンクの過圧の危険がある。直前には、BOG がかえって**減る**のが特徴（[Skuld: LNG Stratification & Rollover](https://www.skuld.com/topics/cargo/liquid-bulk/lng-stratification--rollover/)、[SIGTTO](https://www.sigtto.org/media/1398/guidance-for-the-prevention-of-rollover-on-lng_ships.pdf)）。

## 2. 実務とのつながり
- **BOG の処理**：LNG 基地では、BOG を圧縮機で送り出したり、再液化（リコンデンサ）したりする。LNG 船では推進用の燃料にすることが多い（[米国特許 10808887](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10808887)）。
- **ロールオーバーの防止**：密度の違う LNG は、上部から入れるか下部から入れるかを選んで混ぜる。タンクの温度と密度を高さ方向に監視し、層ができたら循環で混ぜる。
- **気化器（第 12 回）**：LNG を気化させて送り出すには、潜熱 + 顕熱のぶんの熱を、海水などから与える。
- **熱量調整（第 13 回）**：ウェザリングで LNG の発熱量が変わるので、送り出すガスの熱量を調整する必要がある。

## 3. 計算例
（python で検算済み）

**例 1：体積が 1/600 になる理由**
- 液体の密度 450 kg/m³、標準状態のメタンガスの密度 0.717 kg/m³ とすると、450 / 0.717 = **約 630**。
- 蒸発潜熱の換算：8.19 kJ/mol ÷ 0.01604 kg/mol = **510.6 kJ/kg**

**例 2：BOR から侵入熱を逆算する**
容量 180,000 m³ の地上式タンクが満液（密度 450 kg/m³ → 81,000 t）で、BOR が 0.05 %/日の場合。
- 1 日の BOG：81,000 t × 0.0005 = **40.5 t/日**（標準状態で約 2,350 Nm³/h）
- 侵入熱：40,500 kg × 511 kJ/kg ÷ 86,400 s = **約 240 kW**
- タンクの表面積（直径 80 m、高さ 36 m の円筒と仮定）約 19,100 m² で割ると、熱流束は **約 12.5 W/m²**。断熱材がとても小さな熱しか通していないことが分かる。

**例 3：液が減ると BOR が上がる**
侵入熱 240 kW（BOG 40.5 t/日）が一定のまま、液の量が減った場合。
| 充填率 | BOR |
|--------|-----|
| 100 % | 0.05 %/日 |
| 50 % | 0.10 %/日 |
| 10 % | 0.50 %/日 |

**例 4：BOG を抜かなかったら**
タンクを閉じて BOG を抜かず、熱がすべて液の温度上昇（顕熱）に使われたとする。LNG の比熱を約 3.5 kJ/(kg·K) と仮定すると、240 kW × 86,400 s ÷ (81,000,000 kg × 3,500) = **約 0.073 K/日**。温度が上がると飽和圧力も上がるので、タンクの圧力が上昇する。BOG を抜くことは、圧力を保つためでもある。

## 4. 理解確認

### 理解確認 1
LNG タンクに熱が入っても、液の温度がほとんど上がらないのはなぜか。

<details><summary>解答</summary>

大気圧のタンク内の LNG は沸点にある液体（飽和液）だから。入った熱は、温度を上げる（顕熱）のではなく、液を蒸発させる（潜熱）のに使われる。蒸発したガス（BOG）を抜き続けていれば、圧力と温度はほぼ一定に保たれる。
</details>

### 理解確認 2
同じタンクで、液が少ないときほどボイルオフ率（%/日）が大きくなるのはなぜか。

<details><summary>解答</summary>

侵入熱は断熱材とタンクの表面積で決まり、液の量にはあまりよらない。そのため、1 日に蒸発する量（kg/日）はほぼ一定になる。それを割る分母（液の量）が小さくなるので、割合（%/日）は大きくなる。
</details>

### 理解確認 3（誤っているものはどれか）
(a) ウェザリングが進むと、残った LNG の発熱量は上がる傾向がある。
(b) ロールオーバーの直前には、BOG の発生量が増え続けるのが特徴である。
(c) LNG の体積がガスの約 1/600 になるのは、液体と気体の密度の比による。

<details><summary>解答</summary>

誤りは **(b)**。層状化していると、下の層は上の層に押さえられて蒸発できず、熱をためこむ。そのため、ロールオーバーの直前には BOG がむしろ減り、その後に一気に急増する。
</details>

## 参考文献
- [Engineering ToolBox: Liquefied Natural Gas (LNG)](https://engineeringtoolbox.com/liquefied-natural-gas-lng-d_1092.html)
- [World Ports Sustainability Program: What is LNG?](https://sustainableworldports.org/clean-marine-fuels/lng-bunkering/what-is-lng/)
- [Engineering ToolBox: Methane – Thermophysical Properties](https://www.engineeringtoolbox.com/methane-d_1420.html)
- [米国特許 10808887（ボイルオフ率の判定と管理）](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10808887)
- [LAPSE 2023.27212（BOG に関するレビュー）](https://psecommunity.org/LAPSE:2023.27212)
- [Energies 2020（DOAJ）：充填率と BOR のシミュレーション](https://doaj.org/article/24d1ff8757e74f818fc12dbffb40f509)
- [IChemE Symposium Series 139（1995）：LNG のロールオーバー](https://www.icheme.org/media/25371/major-hazards-onshore-and-offshore-ii-icheme-symposium-series-139-1995-46-baker.pdf)
- [SIGTTO: Guidance for the Prevention of Rollover on LNG Ships](https://www.sigtto.org/media/1398/guidance-for-the-prevention-of-rollover-on-lng_ships.pdf)
- [Skuld: LNG Stratification & Rollover](https://www.skuld.com/topics/cargo/liquid-bulk/lng-stratification--rollover/)
