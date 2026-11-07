# 第 19 回 漏えい検知と保安

**分野：ガス技術（供給）**

## ねらい
- 漏れたガスの広がり方を、拡散（フィックの法則）と浮力・換気の物質収支から説明できる。
- 警報器の取り付け位置（天井付近か床付近か）が、ガスの比重から決まる理由を説明できる。
- 接触燃焼式・半導体式・赤外線式の検知器が、それぞれ何の物理・化学現象を使っているかを説明できる。

## 1. 原理編

### 1.1 拡散：フィックの法則
濃度に差があると、分子は濃い方から薄い方へ移動します（拡散）。

  **J = −D · dc/dx**（フィックの第一法則）

| 記号 | 意味 | 単位 |
|------|------|------|
| J | 単位面積・単位時間あたりに通る量（流束） | mol/(m²·s) |
| D | 拡散係数 | m²/s |
| c | 濃度 | mol/m³ |
| x | 距離 | m |

（[Wikipedia: Mass diffusivity](https://www.wikipedia.org/wiki/Mass_diffusivity)）

- 空気中のメタンの拡散係数は、大気圧で約 0.21 cm²/s（= 2.1 × 10⁻⁵ m²/s）程度である（[Engineering ToolBox：Air diffusion coefficients](https://engineeringtoolbox.com/air-diffusion-coefficient-gas-mixture-temperature-d_2010.html)。表の温度欄は元の表で確認すること）。
- 拡散だけで広がる距離は、時間の平方根に比例する（目安 x ≈ √(2Dt)）。距離が 2 倍になると、かかる時間は 4 倍になる。

**意味**：計算例 1 のとおり、拡散だけでは 1 m 広がるのに何時間もかかります。実際の部屋では、**浮力**（軽いガスは上へ、重いガスは下へ）と**空気の流れ**（換気・対流）のほうが、ずっと速くガスを運びます。

### 1.2 浮力：警報器の位置が決まる理由
- メタンの密度は空気の約 0.55 倍なので、漏れた都市ガス（13A）は上に昇って天井付近にたまる。LP ガス（プロパン・ブタン）は空気より重いので床付近にたまる（第 13 回の比重 d）。
- そのため、空気より軽いガスの検知器は、燃焼器から水平距離 8 m 以内で、検知器の下端が天井面の下 0.3 m 以内になるように付ける（[名古屋市消防局 資料](https://www.city.nagoya.jp/shobo/cmsfiles/contents/0000118/118362/11.pdf)、[京都市消防局 標準仕様](https://www.city.kyoto.lg.jp/shobo/cmsfiles/contents/0000229/229395/06_gasumorekasaikeihousetubi.pdf)）。
- 空気より重いガスでは、検知器の上端を床面の上 30 cm 以内に付ける（[岡山市 資料](https://www.city.okayama.jp/kurashi/cmsfiles/contents/0000021/21204/03-11.pdf)）。
- ガス器具の真上は、燃焼ガスの熱気流などの影響を受けるので避ける（[パナソニック 技術資料](https://www2.panasonic.biz/ls/densetsu/ha/bousai_net/gijyutu1/ninshou/1gkanti/pdfs/SBCT1B73_214.pdf)）。

### 1.3 部屋の濃度：換気がある場合の物質収支
部屋（容積 V）に漏えい量 q のガスが出続け、換気回数 n（1 時間に部屋の空気が何回入れ替わるか）で換気されているとします。よく混ざっている（どこも同じ濃度 C）と仮定すると、

  **V · dC/dt = q − (q + nV) · C**

- 入ってくる量は q、出ていく量は「出ていく空気の量 × 濃度」。
- 十分時間がたつと dC/dt = 0 なので、**C_∞ = q / (q + nV) ≈ q / (nV)**。
- 濃度が C_∞ に近づく速さの目安（時定数）は τ ≈ 1/n（換気回数の逆数）。

**意味**：
- 換気がなければ（n = 0）、濃度は増え続け、いつか燃焼範囲（メタンは約 5〜15 %。第 04 回）に入る。
- 換気があれば、濃度はある値で頭打ちになる。換気回数を増やすほど、その値は下がる。

### 1.4 検知器の原理
| 方式 | 使う現象 | 特徴 |
|------|---------|------|
| 接触燃焼式 | 触媒の上でガスを燃やし、その熱で白金線の抵抗が変わる | 出力が濃度にほぼ比例し、爆発下限界までの測定に向く |
| 半導体式 | 酸化スズの表面にガスが吸着・反応し、電気抵抗が変わる | 感度が高く安価。家庭用警報器に広く使われる |
| 赤外線式 | メタンが特定の波長の赤外線を吸収する | 触媒を使わないので劣化しにくい。離れた所からの検知もできる |

- **接触燃焼式**：触媒を塗ったセラミックの玉の中に白金コイルを入れ、500 ℃以下に加熱する。可燃性ガスが触媒の上で燃えると、その熱でコイルの抵抗が変わり、ホイートストンブリッジで読み取る。ブリッジには、触媒のない「補償素子」を組み合わせ、周りの温度の影響を打ち消す。爆発下限界までの濃度の測定に使う（[arXiv：A Survey on Gas Sensing Technology](https://arxiv.org/pdf/1305.7427)、[フィガロ技研：接触燃焼式の原理](https://figarosensor.com/technicalinfo/principle/catalytic-type.html)）。
- **半導体式**：1970 年代はじめに、田口尚義氏が酸化スズ（SnO₂）を使った実用的なガスセンサーを作り、特許を取った（[arXiv：A Survey on Gas Sensing Technology](https://arxiv.org/pdf/1305.7427)）。
- **赤外線式**：メタンは波長 3.3 μm 付近に強い吸収を持つ。透過した光の強さは、ランベルト・ベールの法則 **I = I₀ · exp(−α · c · L)** に従って弱くなる（α：吸収係数、c：濃度、L：光が通る距離）。吸収のない波長の光も測って比べることで、光源の変化を補正する（[ISHN：How infrared sensors measure LEL](https://www.ishn.com/articles/99428-how-infrared-sensors-measure-lel-combustible-gas)）。安価な近赤外レーザーを使う遠隔検知もあり、1.65 μm 付近の吸収線を使う（感度は中赤外より低い）（[米国特許 7075653：レーザー式の遠隔メタン漏えい検知](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7075653)）。

## 2. 実務とのつながり
- **家庭の警報器**：13A なら天井付近、LP ガスなら床付近。燃焼器から 8 m 以内に付ける。
- **導管の漏えい調査**：道路に沿って検知器を持って歩く、または車で走りながら、地表に出てくるガスを検知する。レーザー式は、離れた場所の漏えいを遠くから見つけられる。
- **付臭（第 13 回）**：人の鼻も「検知器」の 1 つ。付臭剤のにおいで、警報器が鳴る前に気付けるようにする。
- **高圧ガス設備**：一般則では、可燃性ガスと毒性ガスの製造施設に漏えい検知警報設備を設ける（法令ドリル）。

## 3. 計算例
（python で検算済み）

**例 1：拡散だけで広がる時間**（D = 2.1 × 10⁻⁵ m²/s、t = x²/(2D)）
| 距離 | 時間 |
|------|------|
| 10 cm | 約 4 分 |
| 1 m | 約 6.6 時間 |
| 3 m | 約 60 時間 |
距離が 10 倍になると、時間は 100 倍になる。

**例 2：換気と部屋の濃度**
容積 30 m³ の部屋に、0.1 m³/h のガスが漏れ続ける場合。
- 換気がないとき：メタンの爆発下限界 5 %（1.5 m³）に達するまで **約 15 時間**
- 換気回数 0.5 回/h：落ち着く濃度は 0.1 / (0.1 + 15) = **約 0.66 %**（時定数 約 2 時間）
- 換気回数 2 回/h：落ち着く濃度は **約 0.17 %**

**例 3：浮力**
メタンの密度 0.717 kg/m³N ÷ 空気 1.293 kg/m³N = **0.555**。空気より軽いので、天井付近にたまる。

## 4. 理解確認

### 理解確認 1
都市ガス（13A）とLP ガスで、警報器の取り付け位置が天井付近と床付近に分かれるのはなぜか。

<details><summary>解答</summary>

ガスの比重（空気に対する密度の比）が違うから。13A の主成分メタンは空気より軽い（約 0.55 倍）ので、浮力で上に昇って天井付近にたまる。LP ガスは空気より重いので床付近にたまる。拡散だけでは広がるのがとても遅いので、浮力でガスがたまる場所に検知器を置く必要がある。
</details>

### 理解確認 2
換気のある部屋では、漏れが続いても濃度が一定の値で止まるのはなぜか。

<details><summary>解答</summary>

濃度が上がるほど、換気で出ていくガスの量（換気量 × 濃度）も増えるから。出ていく量が漏れてくる量と等しくなったところで、濃度は増えなくなる。その値は q/(nV) で、換気回数を増やすほど低くなる。
</details>

### 理解確認 3（誤っているものはどれか）
(a) 接触燃焼式の検知器は、ガスが触媒の上で燃えるときの熱による抵抗の変化を測る。
(b) 赤外線式の検知器は、メタンが特定の波長の赤外線を吸収することを利用する。
(c) 室内で漏れたメタンは、主に拡散によって数分で部屋全体に均一に広がる。

<details><summary>解答</summary>

誤りは **(c)**。拡散だけでは 1 m 広がるのに何時間もかかる。実際には、浮力（軽いガスは上昇）と空気の流れがガスを運ぶので、濃度は均一にならず、天井付近にたまりやすい。
</details>

## 参考文献
- [Wikipedia: Mass diffusivity](https://www.wikipedia.org/wiki/Mass_diffusivity)
- [Engineering ToolBox：Air diffusion coefficients](https://engineeringtoolbox.com/air-diffusion-coefficient-gas-mixture-temperature-d_2010.html)
- [名古屋市消防局 資料（ガス漏れ検知器の設置）](https://www.city.nagoya.jp/shobo/cmsfiles/contents/0000118/118362/11.pdf)
- [京都市消防局 標準仕様（ガス漏れ火災警報設備）](https://www.city.kyoto.lg.jp/shobo/cmsfiles/contents/0000229/229395/06_gasumorekasaikeihousetubi.pdf)
- [岡山市 資料（空気より重いガスの検知器）](https://www.city.okayama.jp/kurashi/cmsfiles/contents/0000021/21204/03-11.pdf)
- [パナソニック 技術資料（ガス漏れ検知器の取り付け）](https://www2.panasonic.biz/ls/densetsu/ha/bousai_net/gijyutu1/ninshou/1gkanti/pdfs/SBCT1B73_214.pdf)
- [arXiv：A Survey on Gas Sensing Technology](https://arxiv.org/pdf/1305.7427)
- [フィガロ技研：接触燃焼式の原理](https://figarosensor.com/technicalinfo/principle/catalytic-type.html)
- [ISHN：How infrared sensors measure LEL combustible gas](https://www.ishn.com/articles/99428-how-infrared-sensors-measure-lel-combustible-gas)
- [米国特許 7075653：レーザー式の遠隔メタン漏えい検知](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7075653)
