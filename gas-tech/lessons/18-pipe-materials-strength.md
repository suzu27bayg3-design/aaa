# 第 18 回 導管材料と強度

**分野：ガス技術（供給）**

## ねらい
- 内圧を受ける管の周方向の応力 σ = pD/2t（フープ応力）を、半分に切った管の力のつり合いから導ける。
- 軸方向の応力がその半分になる理由を説明でき、管が縦に割れやすい理由が分かる。
- ポリエチレン（PE）管の使用圧力が、長期強度（MRS）と SDR から決まる仕組みと、地震に強い理由を説明できる。

## 1. 原理編

### 1.1 フープ応力の導出
内径 D・肉厚 t・長さ L の管に内圧 p がかかっているとします。管を軸を含む面で縦に半分に切って、片側だけを考えます。
- **押し広げる力**：内圧が、切り口に投影した面積 D × L に働く → p·D·L
- **こらえる力**：切り口は上下 2 か所あり、それぞれ断面積 t × L で周方向の応力 σ_h が引っ張る → 2·σ_h·t·L

つり合いから p·D·L = 2·σ_h·t·L なので、

  **σ_h = p·D / (2t)**（フープ応力、周方向応力）

（[Industrial Monitor Direct：Thin-wall pressure vessel hoop stress](https://industrialmonitordirect.com/blogs/knowledgebase/thin-wall-pressure-vessel-hoop-stress-cylinder-vs-barlow-formula)、[Engineers Edge：Hoop stress](https://engineersedge.com/material_science/hoop-stress.htm)）

| 記号 | 意味 | 単位 |
|------|------|------|
| σ_h | 周方向の応力 | Pa（N/m²） |
| p | 内圧（ゲージ圧） | Pa |
| D | 管の直径 | m |
| t | 肉厚 | m |

- **前提**：肉厚が半径に比べて薄い（目安は半径の 1/10〜1/20 以下）。厚肉の管ではラメの式を使う（[Industrial Monitor Direct](https://industrialmonitordirect.com/blogs/knowledgebase/thin-wall-pressure-vessel-hoop-stress-cylinder-vs-barlow-formula)）。
- 外径を使った同じ形の式を、配管の分野では**バーロウの式**と呼ぶ。外径を使うと内径より大きい値になり、安全側の計算になる。

### 1.2 軸方向の応力は半分
今度は管を輪切りにして考えます。管の端（閉じた端）を押す力は、内圧 × 円の面積 p·πD²/4 です。これを管の断面（周の長さ πD × 肉厚 t）がこらえるので、

  **σ_L = p·D / (4t)**（軸方向応力 = フープ応力の 1/2）

**意味**：同じ管では周方向の応力が 2 倍大きいので、内圧で破裂するときは、管が**縦（軸方向）に裂ける**ことが多くなります。

### 1.3 肉厚の決め方（鋼管）
σ_h を材料が安全に耐えられる応力（規格最小降伏強さ SMYS × 設計係数 F）以下にすると、

  **t = p·D / (2·F·SMYS)**

設計係数 F は、人家が多い所ほど小さく（肉厚を厚く）とるのが一般的です。

### 1.4 ポリエチレン管の圧力の決め方
PE 管は、長い時間かけてゆっくり変形する（クリープ）性質があるので、短時間の強度ではなく、**長期の強度**で考えます。
- **MRS（最小要求強度）**：20 ℃で 50 年間の使用に耐えると統計的に見込まれる応力。PE100 は MRS = 10 MPa の材料である（[Pipeline & Gas Journal：PE 100 Material](https://pgjonline.com/2011/12/30/pe-100-material-makes-manitoba-gas-main-project-economically-viable/)）。
- **SDR（標準寸法比）**：外径 ÷ 肉厚。SDR が同じなら、太さによらず同じ圧力に耐える。
- 1.1 の式を外径 D と SDR で書き直すと、肉厚の中心の直径は D − t なので σ = p(D − t)/2t = p(SDR − 1)/2 になる。これを MRS ÷ 設計係数 C と等しくおくと、

  **使用圧力 MOP = 2·MRS / (C·(SDR − 1))**（bar で表すと 20·MRS / (C·(SDR − 1))）

- 水道では C = 1.25、ガスでは C = 2.0 以上（カナダ規格 CSA Z662 の例）が使われる（[Pipeline & Gas Journal](https://pgjonline.com/2011/12/30/pe-100-material-makes-manitoba-gas-main-project-economically-viable/)）。ガスのほうが漏れたときの危険が大きいので、余裕を大きくとる。

### 1.5 PE 管が地震に強い理由
- PE は柔らかく伸びが大きいので、地盤が動いても管が曲がって追従し、割れにくい。
- 管と継手を電熱線で溶かしてつなぐ**電気融着（EF）接合**では、管と継手が一体になり、継手から抜けにくい（[日本水道協会など Q&A：ポリエチレン管の耐震性](https://www.jwrc-net.or.jp/docs/publication-outreach/qa/09-95.pdf)）。
- 阪神・淡路大震災でも PE 管は全く破損しなかったとされ、以後ガス管・水道管は鋼管から PE 管への交換が進んだ（[中部大学 研究報告](https://www.chubu.ac.jp/research/wp-content/uploads/sites/16/2022/04/institute-production-engineering-research-report-report-2011-02.pdf)）。東日本大震災でも柔軟性による地震への強さが確かめられた（[大津市企業局：ガス管の耐震化](https://www.city.otsu.lg.jp/material/files/group/327/gas_taishinka_pr.pdf)）。
- 一方、ねじ接合の亜鉛めっき鋼管では、地震で継手部の亀裂・折損が報告されている（[経済産業省 ガス安全小委員会 資料](https://www.meti.go.jp/shingikai/sankoshin/hoan_shohi/gas_anzen/pdf/014_02_02.pdf)）。
- PE 管は腐食しないことも長所である（第 10 回の電気防食が要らない）。

## 2. 実務とのつながり
- **使い分け**：高圧・中圧の太い管は鋼管（強度が高く、溶接でつなぐ）。低圧の細い管は PE 管、太い低圧管はダクタイル鋳鉄管（[大津市企業局 資料](https://www.city.otsu.lg.jp/material/files/group/14/gasu_1.pdf)）。
- **耐圧試験**：完成検査の耐圧試験（常用圧力の 1.5 倍など）は、フープ応力に余裕があることを実際に確かめる試験である（法令の一般則と同じ考え方）。
- **PE 管の弱点**：紫外線や熱に弱く、強度が鋼より低いので、高い圧力には使えない。外からの掘削による損傷にも注意が要る。

## 3. 計算例
（python で検算済み）

**例 1：鋼管のフープ応力**
外径 508 mm、肉厚 7.9 mm の鋼管に内圧 7 MPa（ゲージ圧）がかかるとき、
- σ_h = 7 × 508 / (2 × 7.9) = **約 225 MPa**
- σ_L = 225 / 2 = **約 113 MPa**

**例 2：必要な肉厚**
同じ管で、規格最小降伏強さを 359 MPa（仮定）とすると、
| 設計係数 F | 必要な肉厚 |
|-----------|-----------|
| 0.72 | 6.9 mm |
| 0.4 | 12.4 mm |
設計係数を小さくすると、肉厚は反比例して厚くなる。

**例 3：PE100・SDR 11 の使用圧力**
- 水道（C = 1.25）：20 × 10 / (1.25 × 10) = **16 bar**
- ガス（C = 2.0）：20 × 10 / (2.0 × 10) = **10 bar**（約 1.0 MPa）
- このとき管壁の応力は MRS / C = 5 MPa で、1.4 の式 σ = p(SDR − 1)/2 = 1.0 × 10 / 2 = 5 MPa と一致する。

## 4. 理解確認

### 理解確認 1
内圧で破裂した管が、縦に裂けることが多いのはなぜか。

<details><summary>解答</summary>

周方向の応力 pD/2t は、軸方向の応力 pD/4t の 2 倍だから。縦に切った面では、内圧が押す面積（D × L）に対して、こらえる断面が 2 か所（2t × L）しかない。輪切りの面では、押す面積（πD²/4）に対してこらえる断面が周全体（πD × t）あるので、応力が半分で済む。
</details>

### 理解確認 2
PE 管の使用圧力を、短時間の強度ではなく MRS（50 年の長期強度）で決めるのはなぜか。

<details><summary>解答</summary>

PE は荷重がかかり続けると少しずつ変形が進む（クリープ）ので、長く使うほど、壊れずに耐えられる応力が下がるから。導管は何十年も使うので、使用期間の終わりまで耐えられる応力を基準にする必要がある。
</details>

### 理解確認 3（誤っているものはどれか）
(a) 同じ SDR の PE 管なら、太さによらず同じ圧力に耐える。
(b) 肉厚を 2 倍にすると、フープ応力は 1/2 になる。
(c) 管の直径を 2 倍にしても、同じ内圧ならフープ応力は変わらない。

<details><summary>解答</summary>

誤りは **(c)**。σ_h = pD/2t なので、肉厚が同じなら直径が 2 倍でフープ応力も 2 倍になる。太い管ほど、同じ圧力に耐えるには厚い肉厚が要る。(a) は、SDR = D/t が同じなら pD/2t が同じになるので正しい。
</details>

## 参考文献
- [Industrial Monitor Direct：Thin-wall pressure vessel hoop stress（cylinder vs Barlow）](https://industrialmonitordirect.com/blogs/knowledgebase/thin-wall-pressure-vessel-hoop-stress-cylinder-vs-barlow-formula)
- [Engineers Edge：Hoop stress](https://engineersedge.com/material_science/hoop-stress.htm)
- [Pipeline & Gas Journal：PE 100 Material Makes Manitoba Gas Main Project Economically Viable](https://pgjonline.com/2011/12/30/pe-100-material-makes-manitoba-gas-main-project-economically-viable/)
- [日本水道協会など Q&A：ポリエチレン管の耐震性](https://www.jwrc-net.or.jp/docs/publication-outreach/qa/09-95.pdf)
- [中部大学 研究報告（ポリエチレン管）](https://www.chubu.ac.jp/research/wp-content/uploads/sites/16/2022/04/institute-production-engineering-research-report-report-2011-02.pdf)
- [大津市企業局：ガス管の耐震化](https://www.city.otsu.lg.jp/material/files/group/327/gas_taishinka_pr.pdf)
- [大津市企業局：ガス導管の資料](https://www.city.otsu.lg.jp/material/files/group/14/gasu_1.pdf)
- [経済産業省 ガス安全小委員会 資料（地震被害）](https://www.meti.go.jp/shingikai/sankoshin/hoan_shohi/gas_anzen/pdf/014_02_02.pdf)
