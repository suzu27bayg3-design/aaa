# 第 2 周 第 02 回 実在気体の深掘り：圧縮係数 Z を状態方程式から導く

**分野：基礎理論（第 02 回の応用）**

## ねらい
- 理想気体の 2 つの前提（分子の大きさがゼロ、分子間に力が働かない）を 1 つずつ外すと、ファンデルワールス式になることを説明できる。
- 臨界点の条件から定数 a、b を導き、「対応状態原理」で Z をおおまかに推定できる理由を説明できる。
- 高圧のメタン（CNG 容器）で、理想気体の式を使うとどのくらいずれるかを Z で見積もれる。

## 1. 原理編

### 1.1 記号と前提
| 記号 | 意味 | 単位 |
|------|------|------|
| p | 圧力 | Pa |
| V_m | モル体積 | m³/mol |
| T | 絶対温度 | K |
| R | 気体定数 8.314 | J/(mol·K) |
| Z | 圧縮係数 pV_m/(RT) | 無次元 |
| T_c, p_c | 臨界温度、臨界圧力 | K, Pa |
| T_r = T/T_c, p_r = p/p_c | 換算温度、換算圧力 | 無次元 |
| ω | 偏心因子 | 無次元 |

第 02 回で見たように、理想気体の式 pV_m = RT は、分子運動論の 2 つの前提から出てきます。
1. 分子そのものの体積はゼロとみなす。
2. 分子どうしは衝突のとき以外は力を及ぼし合わない。

Z = 1 からのずれは、この 2 つが崩れた分を表します。

### 1.2 前提を 1 つずつ外す → ファンデルワールス式
- **分子の体積（斥力の効果）**：分子が自由に動ける空間は、容器の体積から分子自身が占める分 b を引いた V_m − b になります。
- **分子間の引力**：壁に当たる直前の分子は、内側の分子に引き戻されます。その分だけ壁を押す力が弱まります。引き戻す相手の数も、当たる分子の数も密度（1/V_m）に比例するので、圧力の減り方は a/V_m² になります。

この 2 つを入れると、次の式になります。

  **(p + a/V_m²)(V_m − b) = RT**

Z で書き直すと、2 つの効果の向きがはっきりします。

  Z = V_m/(V_m − b) − a/(RT·V_m)

- 第 1 項：分子の体積の効果で、**Z > 1** の側に押します。高圧（V_m が小さい）ほど強く効きます。
- 第 2 項：引力の効果で、**Z < 1** の側に押します。低温ほど強く効きます。

常温・中圧のメタンでは引力の効果が勝って Z < 1 になります。さらに圧力を上げると体積の効果が追いつき、Z はいったん最小値をとってから上がり始めます。
（式と導出：[Kiel 大学 講義ノート「Critical constants and vdW equation」](https://www.tf.uni-kiel.de/matwis/amat/td_kin_i/kap_1/backbone/r_su1.html)）

### 1.3 臨界点から a、b を決める → 対応状態原理
臨界点では、等温線が水平になり、しかも変曲点になります。式で書くと次の 2 条件です。

  (∂p/∂V_m)_T = 0、 (∂²p/∂V_m²)_T = 0

この 2 条件をファンデルワールス式に当てはめて解くと、次の関係が出ます。
- V_c = 3b
- T_c = 8a/(27Rb)
- p_c = a/(27b²)

これを逆に解くと、測定できる臨界定数から a、b が決まります。

  **a = 27R²T_c²/(64p_c)、 b = RT_c/(8p_c)**

さらに、臨界点での圧縮係数は Z_c = 3/8 = 0.375 になります。この値は物質によらず同じです
（[Udai Pratap College 講義資料（PDF）](https://www.upcollege.ac.in/Upload/econtent/2359.pdf)、[Kiel 大学 講義ノート](https://web.tf.uni-kiel.de/matwis/amat/td_kin_i/kap_1/backbone/r_su1.html)）。

p、V、T を臨界値で割った換算量で書き直すと、a と b は式から消えます。つまり「**T_r と p_r が同じなら、どの気体も Z はほぼ同じ**」ということになります。これが**対応状態原理**で、一般化 Z 線図の根拠になっています。

ただし、実在の気体の Z_c はおおむね 0.21〜0.31 で、0.375 より小さくなります（[Kiel 大学 講義ノート](https://www.tf.uni-kiel.de/matwis/amat/td_kin_i/kap_1/backbone/r_su1.html)）。
ファンデルワールス式は定性的には正しいものの、定量的には粗い近似だということです。

### 1.4 補正の第 3 のパラメータ：偏心因子 ω と Peng-Robinson 式
Pitzer は、分子の形の違いを表す 3 つ目のパラメータとして**偏心因子** ω を導入しました。

  ω = −1 − log₁₀(p_sat/p_c)　（T_r = 0.7 のとき）

希ガスのような単純な球形分子では、T_r = 0.7 での換算蒸気圧 p_sat/p_c が約 0.1 になります。このとき ω = 0 です。メタンは **ω ≒ 0.011** で、ほぼ球形の分子です
（[Acentric factor - Wikipedia](https://en.wikipedia.org/wiki/Acentric_factor)、[Penn State PNG 520](https://courses.ems.psu.edu/png520/m8_p3.html)）。

実務でよく使われる **Peng-Robinson 式（1976）** は、次の形をしています。

  p = RT/(V_m − b) − a·α(T)/[V_m(V_m + b) + b(V_m − b)]

係数は次のとおりです。
- a = 0.45724·R²T_c²/p_c
- b = 0.07780·RT_c/p_c
- α = [1 + κ(1 − √T_r)]²
- κ = 0.37464 + 1.54226ω − 0.26992ω²

この式では Z_c ≒ 0.307 になり、実在の気体に近い値です
（[Penn State PNG 520「Peng-Robinson EOS (1976)」](https://courses.ems.psu.edu/png520/node/1933)、[NTNU 講義資料（PDF）](https://www.ipt.ntnu.no/~curtis/courses/PhD-PVT/PVT-HOT-Vienna-May-2016x/e-course/Day2_Part2/LectureNotes/Peng-Robinson.pdf)）。

### 1.5 低圧の近似：ビリアル式
低圧では、Z を密度または圧力のべき級数に展開できます。最初の補正項だけをとったのが Pitzer-Abbott の第 2 ビリアル係数の相関式です。

  Z = 1 + (B⁰ + ωB¹)·p_r/T_r
  B⁰ = 0.083 − 0.422/T_r^1.6、 B¹ = 0.139 − 0.172/T_r^4.2

この式は Z を圧力の 1 次式で近似しています。そのため、Z の最小値やその後の上昇は表せず、**中圧までしか使えません**（下の計算例 1 で確認します）。

## 2. 実務とのつながり
- **CNG 容器・高圧ガス設備**：20 MPa 級の容器に何 m³N 入るかは、Z を使わないと大きくずれます（計算例 2）。容器の内容積からガス量を見積もるときは、Z による補正が必須です（第 02 回 1.5）。
- **高圧導管のラインパック**：導管の中にためておけるガス量も pV/(ZRT) で計算します。数 MPa 程度でも数 % の差になります（計算例 3）。
- **天然ガスの取引計量**：ガスの体積を基準状態に換算するときは Z で補正します。たとえば PTB（ドイツ物理工学研究所）は、天然ガスの p-V-T 性質を 270〜300 K、6 MPa までの範囲で精密に測定しています（[Weiss, PTB（NFOGM 掲載, PDF）](https://nfogm.no/wp-content/uploads/2019/02/1986-07-p-V-T-Properties-of-Natural-Gas-at-Temperatures-between-270-K-and-300-K-and-Pressures-of-up-to-6-MPa-Weiss-PTB.pdf)）。
- **メタンの Z の傾向**：常温付近では Z < 1 で、最小値は約 0.8 です。Z が最小になる圧力は約 138〜172 bar（温度によって変わる）とされています（[米国特許 US6632266（PDF）](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6632266)、[米国特許 US6217626（PDF）](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6217626)）。

## 3. 計算例（python で 3 次方程式を解いて検算済み）

前提：メタンの臨界定数は T_c = 190.56 K、p_c = 4.599 MPa です（[NIST WebBook（methane）](https://webbook.nist.gov/cgi/cbook.cgi?ID=C74828&Mask=9) では T_c = 190.6 K）。偏心因子は ω = 0.011、温度は T = 15 °C = 288.15 K（T_r = 1.51）とします。
各状態方程式を Z の 3 次方程式に書き直し、気相の根（最大の実根）を Z とします。

### 計算例 1：3 つの式の比較
| p [MPa] | ファンデルワールス | Peng-Robinson | ビリアル（第 2 係数まで） |
|--------|------|------|------|
| 0.1 | 0.998 | 0.998 | 0.998 |
| 1 | 0.978 | 0.976 | 0.981 |
| 5 | 0.887 | 0.886 | 0.904 |
| 10 | 0.786 | 0.806 | 0.808 |
| 20 | 0.808 | **0.783** | 0.616 |
| 25 | 0.891 | 0.817 | 0.520 |

- 低圧（1 MPa 以下）では、3 つの式はほぼ一致します。
- 20 MPa を超えると、ビリアル式は Z の上昇を表せず、大きく外れます（1.5 で述べた限界）。
- Peng-Robinson 式では、Z が最小になるのは約 16 MPa で、その値は Z ≒ 0.77 です。
  上の特許文献の「最小値はやや 0.8 超、138〜172 bar」と比べると、圧力の位置はおおむね合っていますが、Z の値は数 % 低く出ています。
  ※ 15 °C・20 MPa でのメタンの Z の**一次資料による基準値は、今回は確認できませんでした（要確認）**。正確な値は、NIST の流体物性ページなど、メタン専用の高精度な状態方程式で確認してください。

### 計算例 2：CNG 容器（内容積 50 L、20 MPa、15 °C）に入るメタンの量
物質量は n = pV/(ZRT) で求めます。0 °C・101.325 kPa の標準状態に換算するため、22.414 L/mol を掛けます。

| 計算法 | n [mol] | 標準状態の体積 [m³N] |
|--------|---------|-------------|
| 理想気体（Z = 1） | 417 | 9.36 |
| Peng-Robinson（Z = 0.783） | 533 | **11.95** |

理想気体の式で計算すると、入っている量を約 **22 % 少なく**見積もることになります。
（Z = 0.783 なので 1/Z = 1.28 です。PR の値を基準にすると、理想気体の値は約 22 % 小さくなります。）
Z < 1 になるのは、分子間の引力によって、同じ圧力でも分子がより多く詰め込まれるためです。

### 計算例 3：1 MPa の導管
Peng-Robinson 式では Z = 0.976 です。理想気体の式で計算すると、ためられるガス量を約 **2.5 %** 小さく見積もります。
取引の計量では無視できない大きさです。

## 4. 理解確認

### 理解確認 1（なぜ）
常温のメタンを圧縮していくと、Z はいったん 1 より小さくなり、さらに高圧になると上がり始める。ファンデルワールス式の 2 つの項を使って理由を説明せよ。
<details><summary>解答</summary>

Z = V_m/(V_m−b) − a/(RT·V_m) を使う。
- 中圧までは、分子間の引力の項 a/(RT·V_m) が勝つので、Z < 1 になる。
- さらに圧縮して V_m が b に近づくと、第 1 項 V_m/(V_m−b) が急に大きくなる。そのため Z は最小値を過ぎて上がり始める。
</details>

### 理解確認 2（計算）
ファンデルワールス式の臨界条件から求めた関係 V_c = 3b、T_c = 8a/(27Rb)、p_c = a/(27b²) を使い、Z_c = p_cV_c/(RT_c) を計算せよ。また、実在の気体の Z_c がこの値より小さいことは何を意味するか。
<details><summary>解答</summary>

手順：
Z_c = [a/(27b²)]·3b / [R·8a/(27Rb)] = (3a/(27b)) · (27b/(8a)) = **3/8 = 0.375**。

実在の気体の Z_c は約 0.21〜0.31 で、これより小さい。ファンデルワールス式では、臨界点付近の分子の詰まり方や引力の表し方が粗いことを意味する。そのため、実務では ω を加えた Peng-Robinson 式などを使う。
</details>

### 理解確認 3（誤っているものはどれか）
1. (イ) 換算温度と換算圧力が同じなら、異なる気体でも Z はほぼ等しい（対応状態原理）。
2. (ロ) 第 2 ビリアル係数までの式は、20 MPa 級の CNG 容器でも十分な精度で使える。
3. (ハ) 15 °C・20 MPa のメタンを理想気体として計算すると、容器内のガス量を少なく見積もることになる。

<details><summary>解答</summary>

誤りは **(ロ)**。第 2 ビリアル係数までの式は Z を圧力の 1 次式で近似するので、Z の最小値やその後の上昇を表せない。計算例 1 では、20 MPa で Z = 0.62 となり、Peng-Robinson 式の 0.78 から大きく外れる。

(ハ) は正しい。Z < 1 なので n = pV/(ZRT) は理想気体より大きくなる。
</details>

## 5. よくある誤解・ひっかけ
- **「高圧ほど Z は小さい」とは限らない**：Z には最小値があり、それより高圧では上がります。十分に高圧なら Z > 1 にもなります。
- **3 次方程式の根の選び方**：気相の Z は最大の実根、液相の Z は最小の実根です。間違った根を選ぶと、値が桁違いにずれます。
- **標準状態の取り違え**：「Nm³」が 0 °C 基準か 15 °C 基準かで、モル体積は 22.414 L と約 23.6 L のように違います（第 02 回）。

## 参考文献
- [Kiel 大学 講義ノート「Critical constants and vdW equation」](https://www.tf.uni-kiel.de/matwis/amat/td_kin_i/kap_1/backbone/r_su1.html)
- [Udai Pratap College 講義資料（ファンデルワールス式の臨界定数, PDF）](https://www.upcollege.ac.in/Upload/econtent/2359.pdf)
- [Acentric factor - Wikipedia](https://en.wikipedia.org/wiki/Acentric_factor)
- [Penn State PNG 520「Acentric Factor and Corresponding States」](https://courses.ems.psu.edu/png520/m8_p3.html)
- [Penn State PNG 520「Peng-Robinson EOS (1976)」](https://courses.ems.psu.edu/png520/node/1933)
- [NTNU Curtis Whitson 講義資料「Peng-Robinson」（PDF）](https://www.ipt.ntnu.no/~curtis/courses/PhD-PVT/PVT-HOT-Vienna-May-2016x/e-course/Day2_Part2/LectureNotes/Peng-Robinson.pdf)
- [NIST Chemistry WebBook: Methane（相変化データ・臨界定数）](https://webbook.nist.gov/cgi/cbook.cgi?ID=C74828&Mask=9)
- [米国特許 US6632266（メタンの Z の最小値, PDF）](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6632266)
- [米国特許 US6217626（メタンの Z < 1, PDF）](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6217626)
- [Weiss, PTB: 天然ガスの p-V-T 性質（NFOGM 掲載, PDF）](https://nfogm.no/wp-content/uploads/2019/02/1986-07-p-V-T-Properties-of-Natural-Gas-at-Temperatures-between-270-K-and-300-K-and-Pressures-of-up-to-6-MPa-Weiss-PTB.pdf)
