# 第 05 回 熱力学の第一法則・第二法則

**分野：基礎理論**

## ねらい
- 第一法則（エネルギーの保存）を、流れのある装置（圧縮機・整圧器・熱交換器）に使える形 **q − w = Δh** に直せる。
- 第二法則から、熱を仕事に変える効率に上限（カルノー効率）があることを説明できる。
- 整圧器（ガバナ）でガスが冷える理由（ジュール・トムソン効果）を、エンタルピー一定の考え方で説明できる。

## 1. 原理編

### 1.1 第一法則：閉じた系
物質の出入りがない系（閉じた系）では、

  **ΔU = Q − W**

系に入った熱 Q は、内部エネルギー U の増加と、系が外にする仕事 W に分かれます。エネルギーは作られも消えもしない、という保存則です。

### 1.2 開いた系とエンタルピー
ガス設備の多くは、ガスが流れ込んで流れ出ていく**開いた系**です。流れ込むガスは、後ろのガスに押し込まれて入ってきます。このとき、単位質量あたり **pv**（圧力 × 比体積）の仕事（**流れ仕事**）を受け取ります（[LearnChemE: First Law for Open Systems](https://learncheme.com/quiz-yourself/interactive-modules/first-law-open-systems/first-law-open-systems-summary)）。

内部エネルギーと流れ仕事をまとめた量が**エンタルピー**です。

  **h = u + pv**　（全体量では H = U + PV、[長崎大学 講義資料](https://www.cms.nagasaki-u.ac.jp/lab/bukka/A/_src/762/kagakuhenka_doc1.pdf)）

定常流れ（どの位置でも状態が時間で変わらない）で、運動エネルギーと位置エネルギーの変化が小さいときは、単位質量あたり

  **q − w_s = h₂ − h₁**

となります（q：入る熱、w_s：外に取り出す軸仕事。[LearnChemE](https://learncheme.com/quiz-yourself/interactive-modules/first-law-open-systems/first-law-open-systems-summary)、[Lesics: First Law for an open system](https://lesics.com/first-law-of-thermodynamics-for-an-open-system.html)）。

| 装置 | 仮定 | 第一法則から |
|------|------|------------|
| 熱交換器・気化器 | 仕事なし | q = Δh（入った熱がそのままエンタルピーを上げる） |
| 圧縮機 | 断熱 | −w_s = Δh（加えた仕事がエンタルピーを上げる） |
| 弁・整圧器（絞り） | 断熱・仕事なし | **Δh = 0**（エンタルピー一定） |

### 1.3 第二法則：熱はすべては仕事にならない
**クラウジウスの不等式**：どんなサイクルについても

  **∮ dQ/T ≦ 0**（等号は可逆なサイクルのとき）

可逆な変化について dS = dQ_rev/T と定義した**エントロピー** S は、状態だけで決まる量（状態量）になります（[UNM 講義ノート「Carnot to entropy」](https://darkuniverse.unm.edu/course_webpages/PHYS301_Spr26/Lectures/Carnot_to_entropy.pdf)、[MIT OCW 5.60 第 9 回](https://www.ocw.mit.edu/courses/5-60-thermodynamics-kinetics-spring-2008/c7aa46fceba856268744fed584fc1d80_lec_9.pdf)）。

**カルノー効率の導出**：高温 T_H の熱源から熱 Q_H を受け取り、低温 T_C の熱源に Q_C を捨て、仕事 W = Q_H − Q_C を取り出す熱機関を考えます。
- クラウジウスの不等式から Q_H/T_H − Q_C/T_C ≦ 0。つまり Q_C ≧ Q_H·T_C/T_H。
- 効率は η = W/Q_H = 1 − Q_C/Q_H ≦ **1 − T_C/T_H**

可逆でない機関の効率は、これより必ず低くなります（[UNM 講義ノート「2nd law irreversibility」](https://darkuniverse.unm.edu/course_webpages/PHYS301_Spr26/Lectures/2nd_law_irreversibility.pdf)、[arXiv cs/0602023](https://arxiv.org/pdf/cs/0602023)）。

**意味**：熱を仕事に変えるときは、必ず一部を低温側に捨てなければなりません。捨てる割合は、温度差が小さいほど大きくなります。

| 記号 | 意味 | 単位 |
|------|------|------|
| T_H, T_C | 高温・低温の熱源の温度 | K（絶対温度） |
| Q_H, Q_C | 受け取る熱・捨てる熱 | J |
| S | エントロピー | J/K |

### 1.4 ジュール・トムソン効果：整圧器でガスが冷える理由
弁で圧力を下げる**絞り**は、1.2 の表のとおり**エンタルピー一定**の変化です。理想気体ならエンタルピーは温度だけで決まるので、温度は変わりません。
実在気体では、膨張すると分子どうしの引力に逆らって分子間の距離が広がり、そのぶんエネルギーが使われます。そのため、多くの気体は温度が下がります（[コトバンク「ジュール・トムソン効果」](https://kotobank.jp/word/%E3%82%B8%E3%83%A5%E3%83%BC%E3%83%AB-%E3%83%88%E3%83%A0%E3%82%BD%E3%83%B3%E5%8A%B9%E6%9E%9C-3155699)、[COMSOL: The Joule-Thomson Effect](https://www.comsol.jp/multiphysics/joule-thomson-effect)）。

温度の下がり方は**ジュール・トムソン係数** μ_JT = (∂T/∂p)_h で表します。
- 天然ガス：約 0.48 K/bar（1 bar・300 K）、約 0.44 K/bar（40 bar）（[DGC: JT effect of hydrogen/natural gas mixtures](https://dgc.dk/media/55ufksdg/jt_hydrogen_ng_mix.pdf)）。約 5 K/MPa とする資料もある（[Drilling journal 論文](https://yadda.icm.edu.pl/baztech/element/bwmeta1.element.baztech-4c9b1ba9-da68-42e7-ba2a-44fcc3026cbf/c/drill.2016.33.2.433.pdf)）。
- 水素：常温付近では 0 に近い負の値で、絞っても冷えない（[DGC](https://dgc.dk/media/55ufksdg/jt_hydrogen_ng_mix.pdf)）。

## 2. 実務とのつながり
- **整圧器の凍結**：大きく減圧する整圧器では、ガスの温度が 0 ℃を下回ることがある。その結果、弁の凍結やハイドレート（水和物）の生成が起きる（[Drilling journal 論文](https://yadda.icm.edu.pl/baztech/element/bwmeta1.element.baztech-4c9b1ba9-da68-42e7-ba2a-44fcc3026cbf/c/drill.2016.33.2.433.pdf)、[Catco: Gas Regulator Freeze Prevention](https://catcousa.com/?p=6405)）。そのため、ガバナの手前でガスを温める設備（ヒーター）を置くことがある（第 17 回）。
- **気化器（第 12 回）**：LNG を気化させるのに必要な熱は q = Δh で決まる。
- **圧縮機（第 14 回）**：断熱圧縮では、加えた仕事がガスのエンタルピー（温度）を上げる。そのため、圧縮機の出口ではガスが熱くなる。
- **コージェネ（第 06 回）**：発電で捨てる熱（Q_C）を給湯や暖房に使うと、燃料のエネルギーを使い切る割合が上がる。これは、第二法則で必ず出る捨て熱を有効に使う工夫である。

## 3. 計算例
（python で検算済み）

**例 1：カルノー効率**
| 高温側 | 低温側 | 1 − T_C/T_H |
|-------|-------|------------|
| 1,500 ℃（1,773 K。燃焼ガス程度） | 25 ℃ | 0.832 |
| 600 ℃（873 K） | 25 ℃ | 0.659 |
| 80 ℃（353 K。温水程度） | 25 ℃ | 0.156 |

80 ℃の温水からは、理想的な機関でも熱の 16 % しか仕事にできません。低い温度の熱は「量はあっても仕事にしにくい」ことが、数字で分かります。

**例 2：整圧器での温度低下**
天然ガスを 7 MPa から 0.7 MPa まで減圧する（Δp = 63 bar）。μ_JT を 0.45 K/bar とすると、
- ΔT ≒ 63 × 0.45 ≒ **28 K の低下**
- 入口が 15 ℃なら、出口は約 −13 ℃。凍結対策が必要な温度になる。

**例 3：理想気体の圧縮仕事（1 mol、300 K、0.1 → 1 MPa）**
- 等温圧縮：w = RT ln(p₂/p₁) = 8.314 × 300 × ln 10 = **5.74 kJ/mol**
- 断熱圧縮（比熱比 k = 1.31 と仮定。メタン程度の値）
  - 出口温度：T₂ = 300 × 10^((k−1)/k) = **517 K（244 ℃）**
  - 仕事：w = k/(k−1)·RT₁[(p₂/p₁)^((k−1)/k) − 1] = **7.64 kJ/mol**
- 断熱のほうが仕事が大きい。圧縮でガスが熱くなって体積が大きくなり、そのぶん押し込む仕事が増えるからである。多段圧縮の途中でガスを冷やす（中間冷却）のは、この仕事を減らすためである。

## 4. 理解確認

### 理解確認 1
開いた系のエネルギー収支に、内部エネルギー u ではなくエンタルピー h を使うのはなぜか。

<details><summary>解答</summary>

流れ込むガスは、内部エネルギーのほかに、後ろのガスに押し込まれるときの流れ仕事 pv も持ち込むから。この 2 つをまとめた量が h = u + pv なので、h で収支を取ると、流れ仕事を別に数えなくて済む。
</details>

### 理解確認 2
高温の熱源さえあれば、熱をすべて仕事に変えられる機関を作れないのはなぜか。

<details><summary>解答</summary>

クラウジウスの不等式から、サイクルを回すには必ず Q_C ≧ Q_H·T_C/T_H の熱を低温側に捨てなければならないから。T_C が 0 K でない限り、Q_C は 0 にならない。そのため、効率は 1 − T_C/T_H を超えられない。
</details>

### 理解確認 3（誤っているものはどれか）
(a) 弁による断熱の絞りでは、ガスのエンタルピーはほぼ一定に保たれる。
(b) 理想気体を絞ると、温度は下がる。
(c) 天然ガスを整圧器で大きく減圧すると、温度が 0 ℃を下回ることがある。

<details><summary>解答</summary>

誤りは **(b)**。理想気体のエンタルピーは温度だけで決まるので、エンタルピーが一定なら温度も変わらない。温度が下がるのは、分子間の引力がはたらく実在気体だからである。
</details>

## 参考文献
- [LearnChemE: First Law for Open Systems（まとめ）](https://learncheme.com/quiz-yourself/interactive-modules/first-law-open-systems/first-law-open-systems-summary)
- [Lesics: First Law of Thermodynamics for an open system](https://lesics.com/first-law-of-thermodynamics-for-an-open-system.html)
- [長崎大学 講義資料（エンタルピーの定義）](https://www.cms.nagasaki-u.ac.jp/lab/bukka/A/_src/762/kagakuhenka_doc1.pdf)
- [UNM PHYS301 講義ノート「Carnot to entropy」](https://darkuniverse.unm.edu/course_webpages/PHYS301_Spr26/Lectures/Carnot_to_entropy.pdf) ／ [「2nd law irreversibility」](https://darkuniverse.unm.edu/course_webpages/PHYS301_Spr26/Lectures/2nd_law_irreversibility.pdf)
- [MIT OCW 5.60 Lecture 9](https://www.ocw.mit.edu/courses/5-60-thermodynamics-kinetics-spring-2008/c7aa46fceba856268744fed584fc1d80_lec_9.pdf)
- [arXiv cs/0602023: Information theory and Thermodynamics](https://arxiv.org/pdf/cs/0602023)
- [コトバンク「ジュール・トムソン効果」](https://kotobank.jp/word/%E3%82%B8%E3%83%A5%E3%83%BC%E3%83%AB-%E3%83%88%E3%83%A0%E3%82%BD%E3%83%B3%E5%8A%B9%E6%9E%9C-3155699)
- [COMSOL: The Joule-Thomson Effect](https://www.comsol.jp/multiphysics/joule-thomson-effect)
- [DGC: JT effect of hydrogen / natural gas mixtures](https://dgc.dk/media/55ufksdg/jt_hydrogen_ng_mix.pdf)
- [Drilling journal 論文（整圧所での温度低下）](https://yadda.icm.edu.pl/baztech/element/bwmeta1.element.baztech-4c9b1ba9-da68-42e7-ba2a-44fcc3026cbf/c/drill.2016.33.2.433.pdf)
- [Catco: Joule-Thomson Effect と Gas Regulator Freeze Prevention](https://catcousa.com/?p=6405)
