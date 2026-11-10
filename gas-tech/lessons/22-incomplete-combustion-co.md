# 第 22 回 不完全燃焼と CO 中毒

**分野：ガス技術（消費）**

## ねらい
- 不完全燃焼で CO（一酸化炭素）が出る理由を、「酸素不足」と「途中で冷やされて反応が止まる（クエンチ）」の 2 つから説明できる。
- CO が少しの濃度でも危険な理由を、ヘモグロビンとの結合の強さ（ホールデンの式）から計算できる。
- 室内の CO 濃度を、換気の物質収支（第 19 回と同じ式）から見積もれる。

## 1. 原理編

### 1.1 完全燃焼と不完全燃焼
メタンが完全に燃えると、CO₂ と水だけができます（第 03 回）。

  CH₄ + 2O₂ → CO₂ + 2H₂O

燃焼は一度に進むのではなく、途中で CO を経由します。最後の段階 **CO → CO₂** は比較的ゆっくり進む反応で、これが途中で止まると CO が残ります。止まる原因は主に 2 つです。

1. **酸素が足りない**：空気比が 1 より小さいと、炭素を CO₂ まで酸化するだけの酸素がない。開放型のストーブなどは室内の酸素を使って燃えるので、換気しないと室内の酸素濃度が下がり、不完全燃焼が進んで CO が急に増える（[東京都保健医療局：一酸化炭素](https://www.hokeniryo.metro.tokyo.lg.jp/tthc/kankyou/soudan/sitsunai/carbonmonoxide.html)）。
2. **途中で冷やされる（クエンチ）**：炎が冷たい固体の表面などに触れると、熱を奪われて反応が途中で止まる。これも不完全燃焼の原因である（[Wikipedia: Combustion](https://Www.wikipedia.org/wiki/burning)）。メタンの炎に冷たい板を近づけた実験では、板が約 4 mm の距離のとき CO の放出が最大になり、供給したメタンの約 10 % に達した。さらに近づけると炎は消えた（[UC Irvine：衝突する拡散炎からの CO 放出](https://escholarship.org/uc/item/5r1243km)）。

**意味**：空気が十分にあっても、炎が鍋底や熱交換器に強く当たって冷やされると CO が出ます。ガス器具が「空気」と「炎の当たり方」の両方を設計しているのはこのためです。給湯器の熱交換器にほこりやすすがたまると、空気の通りが悪くなり CO が出やすくなる（[NITE 事故事例資料](https://www.nite.go.jp/data/000004864.pdf)）。

### 1.2 CO が危ない理由：ヘモグロビンとの結合
血液中のヘモグロビン（Hb）は酸素を運びますが、CO は酸素の**約 200〜250 倍**強くヘモグロビンと結合します（[米国学術会議（NAP）：Carbon monoxide](https://www.nap.edu/read/10242/chapter/5)）。CO が結合したヘモグロビン（COHb）は酸素を運べないので、体が酸欠になります。

平衡では、酸素と CO がヘモグロビンを取り合うので、次の関係（ホールデンの式）が成り立ちます。

  **COHb / O₂Hb = M × (p_CO / p_O₂)**

| 記号 | 意味 |
|------|------|
| M | 結合の強さの比（約 220） |
| p_CO, p_O₂ | 肺の中の CO と O₂ の分圧 |

COHb の割合は COHb/(COHb + O₂Hb) = M·p_CO / (p_O₂ + M·p_CO) です。

**意味**：M が大きいので、空気中の酸素（約 21 %）に比べてごくわずかな CO（100 ppm = 0.01 %）でも、ヘモグロビンのかなりの部分を奪います（計算例 1）。
- 空気中の CO が 100 ppm の環境では、平衡時の COHb が約 16 % になり、はっきりした症状が出る程度である（[StatPearls（NCBI）：Carbon monoxide toxicity](https://www.ncbi.nlm.nih.gov/books/NBK430740/)）。
- 空気中の濃度が 200 ppm 前後になると頭痛などが起こり、濃度が上がると吐き気・めまいへと進み、最悪の場合は死に至る（[東京都保健医療局](https://www.hokeniryo.metro.tokyo.lg.jp/tthc/kankyou/soudan/sitsunai/carbonmonoxide.html)）。
- 1,000 ppm（0.1 %）は生命に危険で、1,500 ppm では短時間で死に至る（[StatPearls（NCBI）](https://www.ncbi.nlm.nih.gov/books/NBK430740/)）。
- CO は無色・無臭なので、気付きにくい。

### 1.3 室内の濃度：換気の物質収支
部屋（容積 V）で CO が発生量 G で出続け、換気回数 n で換気されているとき、第 19 回と同じ式で、

  **V · dC/dt = G − nV·C、　C_∞ = G / (nV)**

- 換気が少ないと C_∞ が大きくなる。さらに、換気が少ないと室内の酸素が減り、不完全燃焼が進んで G 自体が増える。この**悪循環**が、CO 中毒事故が急に起こる理由である。
- 東京消防庁の検証では、密閉した 6 畳ほどの部屋で七輪や発電機を使うと、35〜50 分で CO 濃度が 700 ppm に達した（[東京消防庁：一酸化炭素中毒に注意](https://www.tfd.metro.tokyo.lg.jp/lfe/topics/nichijou/co.html)）。

## 2. 実務とのつながり
- **給排気（第 23 回）**：燃焼に使う空気を外から取り、排ガスを外に出す方式（FF 式など）にすれば、室内の酸素も減らず、CO も室内に出ない。
- **安全装置**：不完全燃焼防止装置は、炎の状態などから不完全燃焼を感知して、ガスを止める。
- **点検と換気**：換気扇を使い、定期的に窓を開ける。火気器具は定期的に点検・清掃する。CO 警報器の設置も有効である（[東京消防庁](https://www.tfd.metro.tokyo.lg.jp/lfe/topics/nichijou/co.html)）。
- **気分の悪い人が出たら**：まず換気し、ためらわずに病院を受診する（[愛知労働局 リーフレット](https://jsite.mhlw.go.jp/aichi-roudoukyoku/content/contents/CO_leaf2021.pdf)）。

## 3. 計算例
（python で検算済み）

**例 1：CO 濃度と COHb（M = 220）**
| 空気中の CO | p_O₂ = 0.21 で計算 | 肺胞の p_O₂ ≈ 0.132 で計算 |
|------------|------------------|------------------------|
| 50 ppm | 5.0 % | 7.7 % |
| 100 ppm | 9.5 % | 14.3 % |
| 200 ppm | 17.3 % | 25.0 % |
- 肺の奥（肺胞）の酸素分圧は、吸う空気より低い（約 100 mmHg ÷ 760 ≈ 0.132 と仮定）。こちらで計算すると、100 ppm で約 14 % となり、上の資料の「約 16 %」に近い。
- 実際の COHb は、濃度だけでなく吸っていた時間にもよる。この計算は十分長く吸ったとき（平衡）の値である。

**例 2：部屋の CO 濃度**
容積 30 m³ の部屋で、CO が 0.005 m³/h 出続ける場合。
- 換気回数 0.5 回/h：C_∞ = 0.005 / 15 = **約 330 ppm**（落ち着くまでの時定数 約 2 時間）
- 換気回数 2 回/h：**約 83 ppm**

## 4. 理解確認

### 理解確認 1
空気が十分にあるのに CO が出ることがあるのはなぜか。

<details><summary>解答</summary>

炎が冷たい表面（鍋底や熱交換器）に触れて熱を奪われると、CO が CO₂ に酸化される最後の段階が途中で止まる（クエンチ）から。酸素の量だけでなく、反応が進むのに十分な温度と時間が必要である。
</details>

### 理解確認 2
空気中の CO が 0.01 %（100 ppm）しかなくても、体に大きな影響が出るのはなぜか。

<details><summary>解答</summary>

CO は酸素の約 220 倍強くヘモグロビンと結合するから。ホールデンの式 COHb/O₂Hb = M·p_CO/p_O₂ で、M が大きいので、酸素の約 2,000 分の 1 の CO でもヘモグロビンの 1 割以上を奪う。CO と結合したヘモグロビンは酸素を運べない。
</details>

### 理解確認 3（誤っているものはどれか）
(a) 換気が少ないと、室内の酸素が減って不完全燃焼が進み、CO の発生量も増える。
(b) CO はにおいがあるので、漏れればすぐに気付ける。
(c) 部屋の CO 濃度は、換気回数を増やすほど低い値で落ち着く。

<details><summary>解答</summary>

誤りは **(b)**。CO は無色・無臭なので気付きにくい。そのため、CO 警報器や不完全燃焼防止装置が必要になる。（都市ガスの付臭剤は、燃える前のガスの漏れに気付くためのもので、CO のにおいではない。）
</details>

## 参考文献
- [東京都保健医療局：一酸化炭素](https://www.hokeniryo.metro.tokyo.lg.jp/tthc/kankyou/soudan/sitsunai/carbonmonoxide.html)
- [Wikipedia: Combustion（不完全燃焼）](https://Www.wikipedia.org/wiki/burning)
- [UC Irvine：衝突する拡散炎からの CO 放出（eScholarship）](https://escholarship.org/uc/item/5r1243km)
- [NITE 事故事例資料](https://www.nite.go.jp/data/000004864.pdf)
- [米国学術会議（NAP）：Carbon monoxide](https://www.nap.edu/read/10242/chapter/5)
- [StatPearls（NCBI）：Carbon monoxide toxicity](https://www.ncbi.nlm.nih.gov/books/NBK430740/)
- [東京消防庁：一酸化炭素中毒に注意](https://www.tfd.metro.tokyo.lg.jp/lfe/topics/nichijou/co.html)
- [愛知労働局 リーフレット（一酸化炭素中毒）](https://jsite.mhlw.go.jp/aichi-roudoukyoku/content/contents/CO_leaf2021.pdf)
