# 第 04 回 燃焼範囲・燃焼速度・着火

**分野：基礎理論**

## ねらい
- 燃えるガスの濃度に上限と下限（燃焼範囲）がある理由を、燃焼で出る熱と失われる熱のつり合いから説明できる。
- 混合ガスの燃焼下限界を、ル・シャトリエの式で見積もれる。
- 燃焼速度と最小着火エネルギーが、バーナの炎の安定や着火事故の防止にどう関わるかを理解する。

## 1. 原理編

### 1.1 燃焼範囲はなぜあるか
可燃性ガスと空気の混合気に火をつけたとき、炎が自分で広がっていくには、次の条件が要ります。

  **燃焼で出る熱 ≧ まわりに逃げる熱 ＋ 次の層を着火温度まで温める熱**

- **ガスが薄すぎる**：燃料が少なく、出る熱が足りない。余分な空気を温めるのに熱を取られ、炎が消える → **燃焼下限界（LFL、爆発下限界）**
- **ガスが濃すぎる**：今度は O₂ が足りず、燃え残った燃料が熱を吸う → **燃焼上限界（UFL、爆発上限界）**

燃焼下限界は、着火したときに炎が広がる最低の濃度、上限界は最高の濃度として定義され、ふつうは 1 気圧・常温での値を指します（[Weblio「explosion limit」](https://www.weblio.jp/content/explosion+limit)）。

**理論混合比との関係**：第 03 回の理論空気量から、ちょうど過不足なく燃える濃度（理論混合比）が求まります。

  燃料の濃度 [%] = 100 / (1 + A₀)

- メタン：100/(1+9.52) = **9.5 %**。燃焼範囲 5.0〜15.0 % のほぼ中ほどにある。
- プロパン：4.0 %
- 水素：29.6 %

| ガス | 燃焼範囲（空気中, vol%） | 出典 |
|------|------|------|
| メタン | 5.0〜15.0 | [消防庁 検討会資料](https://www.fdma.go.jp/singi_kento/kento/items/kento223_19_shiryo2-1-2.pdf) |
| 水素 | 4.0〜75.0 | 同上 |
| プロパン | 下限 1.8〜2.3、上限 8.5〜9.5（資料により異なる） | [大津市 LPG SDS](https://www.city.otsu.lg.jp/material/files/group/327/SDS_LPG_20260327.pdf)（1.8〜9.5）、[AIChE Beacon](https://aiche.org/sites/default/files/beacon-article/2002-01-Beacon-Japanese_0.pdf)（2.3〜9.5）、[GS Caltex SDS](https://www.gscaltex.com/downloadMsds/808)（1.9〜8.5, NIOSH） |

プロパンのように資料によって値が違うのは、測定の方法（容器の大きさ・着火源・炎が広がったと判定する基準）が違うためです。**安全側に使うときは、低いほうの下限界を採用する**のが基本です。

### 1.2 混合ガスの燃焼下限界：ル・シャトリエの式
可燃性ガスだけを取り出したときの、成分 i の体積分率を yᵢ（Σyᵢ = 1）とすると、

  **LFL_mix = 1 / Σ(yᵢ / LFLᵢ)**

（[Wikipedia: Lower flammability limit](https://en.wikipedia.org/wiki/Lower_flammability_limit)、[Industrial Monitor Direct](https://industrialmonitordirect.com/blogs/knowledgebase/gas-flammability-limits-using-nitrogen-equivalent-method)）

**この式の考え方**：各成分を「その成分の下限界の何割まで入っているか」で数えます。その割合の合計が 1（＝100 %）に達したとき、混合気全体がちょうど下限界になる、と考えます。
背景には、「下限界の混合気は、どれも燃えたときに同じくらいの熱（同じ炎の温度）を出す」という仮定があります。調和平均の形になるのはこのためです。

**使うときの注意**
- yᵢ は**可燃性成分だけで正規化**した割合。N₂ などの不活性ガスは除いて計算する（[Open Exam Prep](https://open-exam-prep.com/study-guides/fe-chemical/safety-health-environment/hazards-hygiene-limits)）。
- 不活性ガスを加えると、下限界は上がる。この単純な式では、その効果は表せない（[Flammability limit（Wikipedia 転載）](https://kolibri.teacherinabox.org.au/modules/en-olpc/wikislice-physics-en/files/articles/Flammability_limit.htm)）。
- H₂/CH₄ の混合などでは、この式でおおむね良い見積もりが得られると報告されている（[東北大学（中国）学報の論文](https://cjournal.hep.com.cn/1005-3026/CN/PDF/1160014247137828967)）。

### 1.3 燃焼速度
**層流燃焼速度** S_L は、静止した混合気の中を炎の面が進む速さです。炎の面では、熱と活性な分子が、まだ燃えていない側へ拡散していきます。そのため、拡散しやすく反応の速いガスほど S_L が大きくなります。

| 混合気 | 最大の層流燃焼速度 | そのときの当量比 |
|------|------|------|
| 天然ガス／空気 | 0.374 m/s | 1.1 |
| 水素／空気 | 2.933 m/s | 1.7 |

（[Frontiers of Chemical Science and Engineering 2010](https://journal.hep.com.cn/fcse/EN/Y2010/V4/I4/417)）

- 当量比は、空気比 m の逆数（燃料が濃い側で 1 を超える）。燃焼速度が最大になるのは、理論混合比より少し燃料が濃い側である。
- 炭化水素どうしでは、同じ当量比で C₃H₈ > C₂H₆ > CH₄ の順に速いとされる（[ICHS 2009 論文](https://conference.ing.unipi.it/ichs2009/images/stories/papers/189.pdf)）。
- 窒素で薄めると燃焼速度は下がる（[CIESC Journal 2019](https://hgxb.cip.com.cn/EN/Y2019/V70/I8/3011)）。

**バーナの炎がその場にとどまる条件**：バーナの出口では、混合気が流れ出る速さ u と燃焼速度 S_L がつり合っています。
- **u < S_L**：炎がバーナの中に入り込む → **逆火**
- **u ≫ S_L**：炎が押し流されて浮き上がる → **リフティング（吹き消え）**

水素は S_L が天然ガスの約 8 倍あります。そのため、都市ガスに水素を混ぜると逆火が起こりやすくなります（[名古屋大学 学位論文審査要旨](https://nagoya.repo.nii.ac.jp/record/2002605/files/k14060_review.pdf)）。第 01 回で、ウォッベ指数だけでは互換性を判断できず、燃焼速度（MCP）も必要だとした理由がこれです。

### 1.4 着火：最小着火エネルギー
燃焼範囲の中にある混合気でも、火がつくには、ある量以上のエネルギーを小さな空間に与える必要があります。その最小値が**最小着火エネルギー（MIE）**です。
- 水素／空気：**0.017 mJ**。一般的な可燃性ガスは 0.1 mJ より大きい（[Ulster 大学 研究](https://pure.ulster.ac.uk/en/publications/minimum-ignition-energy-of-hydrogen-air-mixtures-at-ambient-and-c/)）。
- 引火性の蒸気は 0.2〜0.3 mJ の火花で着火しうる。人体からの静電気放電は、その 100 倍ほどのエネルギーになることがある（[AIChE Beacon 2021](https://www.aiche.org/sites/default/files/202102beaconjapanese.pdf)）。

人の静電気だけでも、ほとんどの可燃性ガスに火をつけるのに十分です。そのため、漏えいしたガスが燃焼範囲に入っている場所では、**着火源を「なくす」ことより、燃焼範囲に「入れない」こと（換気・漏えい防止）が保安の基本**になります。

## 2. 実務とのつながり
- **ガス検知器の警報**：検知器は、濃度を下限界に対する割合（%LEL）で表示することが多い。下限界の何分の 1 で警報を出すかを決めておけば、燃焼範囲に入る前に気づける（第 19 回）。
- **重いガスと軽いガス**：プロパンは空気より重く低い所にたまる（[Worthington SDS（Purdue 大学掲載）](https://www.physics.purdue.edu/primelab/safety/MSDS/SDS/propane%20(compressed%20gas)%20-%20Worthington.pdf)）。都市ガス（13A）は空気より軽い（第 02 回の比重 0.64）。検知器を付ける高さは、この違いで決まる。
- **パージ（置換）**：配管や設備を開けるとき、可燃性ガスを窒素で置き換えてから空気を入れる。こうすれば、途中で燃焼範囲を通らずに済む。
- **水素混合**：燃焼範囲が広く、燃焼速度が速く、着火エネルギーが小さい。この 3 点で、メタンより取り扱いの余裕が小さい（[消防庁 資料](https://www.fdma.go.jp/singi_kento/kento/items/kento223_19_shiryo2-1-2.pdf)）。

## 3. 計算例
（python で検算済み）

**例 1：可燃分と窒素を含むガス**
メタン 65 %、エタン 25 %、窒素 10 % のガスの燃焼下限界は？（メタン 5.0 %、エタン 3.0 %）
- 可燃分だけで正規化：メタン 0.65/0.90 = 0.722、エタン 0.25/0.90 = 0.278
- LFL = 1 / (0.722/5.0 + 0.278/3.0) = **4.22 %**（[Open Exam Prep の例題](https://open-exam-prep.com/study-guides/fe-chemical/safety-health-environment/hazards-hygiene-limits)と一致）

**例 2：水素 20 % 混合の都市ガス（メタンで近似）**
- LFL = 1 / (0.8/5.0 + 0.2/4.0) = **4.76 %**。メタン単独の 5.0 % より少し下がる。
- 同じ式で上限界を見積もると、1 / (0.8/15 + 0.2/75) = 17.9 %。上限界にル・シャトリエの式を使うと誤差が大きくなりやすいので、あくまで目安とする。

## 4. 理解確認

### 理解確認 1
燃焼下限界より薄い混合気で、炎が広がらないのはなぜか。

<details><summary>解答</summary>

燃料が少ないので、燃焼で出る熱が、まわりの余分な空気を着火温度まで温めるのに足りないため。炎の先の層に着火できず、炎が消える。
</details>

### 理解確認 2
ル・シャトリエの式で yᵢ を求めるとき、窒素を除いて正規化するのはなぜか。

<details><summary>解答</summary>

この式は「可燃性成分どうしが、下限界に対してどれだけの割合を受け持つか」を足し合わせるものだから。不活性ガスは燃焼の熱を出さないので、可燃性成分の割合には入れない。不活性ガスの影響（下限界を上げる）は、別に考える必要がある。
</details>

### 理解確認 3（誤っているものはどれか）
(a) 混合気が流れ出る速さが燃焼速度より小さいと、逆火が起こりやすい。
(b) 水素はメタンより燃焼範囲が広く、最小着火エネルギーも小さい。
(c) 燃焼速度が最大になるのは、必ず理論混合比（当量比 1.0）のときである。

<details><summary>解答</summary>

誤りは **(c)**。天然ガスでは当量比 1.1、水素では 1.7 で最大になる。どちらも燃料が少し濃い側である。
(a) は炎の面の速度のつり合いから導ける。(b) は消防庁の資料と MIE の値のとおり。
</details>

## 参考文献
- [消防庁 検討会資料（水素とメタンの物性比較）](https://www.fdma.go.jp/singi_kento/kento/items/kento223_19_shiryo2-1-2.pdf)
- [Weblio「explosion limit」](https://www.weblio.jp/content/explosion+limit)
- [大津市 LPG 安全データシート](https://www.city.otsu.lg.jp/material/files/group/327/SDS_LPG_20260327.pdf)
- [AIChE Process Safety Beacon 2002-01（日本語）](https://aiche.org/sites/default/files/beacon-article/2002-01-Beacon-Japanese_0.pdf) ／ [2021-02（日本語）](https://www.aiche.org/sites/default/files/202102beaconjapanese.pdf)
- [GS Caltex プロパン SDS](https://www.gscaltex.com/downloadMsds/808)
- [Wikipedia: Lower flammability limit](https://en.wikipedia.org/wiki/Lower_flammability_limit)
- [Industrial Monitor Direct: Gas Flammability Limits](https://industrialmonitordirect.com/blogs/knowledgebase/gas-flammability-limits-using-nitrogen-equivalent-method)
- [Open Exam Prep: Flammability, Toxicity, and Industrial Hygiene](https://open-exam-prep.com/study-guides/fe-chemical/safety-health-environment/hazards-hygiene-limits)
- [Flammability limit（Wikipedia 転載）](https://kolibri.teacherinabox.org.au/modules/en-olpc/wikislice-physics-en/files/articles/Flammability_limit.htm)
- [東北大学（中国）学報の論文（H₂/CH₄ 混合の爆発限界）](https://cjournal.hep.com.cn/1005-3026/CN/PDF/1160014247137828967)
- [Experimental study on the laminar flame speed of hydrogen/natural gas/air mixtures（2010）](https://journal.hep.com.cn/fcse/EN/Y2010/V4/I4/417)
- [ICHS 2009 論文（水素・炭化水素混合の燃焼速度）](https://conference.ing.unipi.it/ichs2009/images/stories/papers/189.pdf)
- [CIESC Journal 2019（メタン火炎の燃焼速度と希釈）](https://hgxb.cip.com.cn/EN/Y2019/V70/I8/3011)
- [名古屋大学 学位論文審査要旨（水素混合と逆火）](https://nagoya.repo.nii.ac.jp/record/2002605/files/k14060_review.pdf)
- [Ulster 大学：水素／空気の最小着火エネルギー](https://pure.ulster.ac.uk/en/publications/minimum-ignition-energy-of-hydrogen-air-mixtures-at-ambient-and-c/)
- [Worthington プロパン SDS（Purdue 大学掲載）](https://www.physics.purdue.edu/primelab/safety/MSDS/SDS/propane%20(compressed%20gas)%20-%20Worthington.pdf)
