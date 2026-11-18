# 第 2 周 第 04 回 燃焼範囲の深掘り：下限界を「火炎温度」から導く

**分野：基礎理論（第 04 回の応用）**

## ねらい
- 炭化水素の燃焼下限界（LFL）では、断熱火炎温度がおよそ一定（約 1500 K）になることを、第 2 周第 03 回のエネルギー収支で確かめられる。
- この「限界火炎温度が一定」という考え方から、次の 3 つを導ける。
  - ル・シャトリエの式がなぜ成り立つか
  - 予熱すると下限界が下がること（Burgess-Wheeler 則）
  - 不活性化の目安になる限界酸素濃度（LOC）
- 水素だけがこの考え方から大きく外れる理由を、拡散（ルイス数）の観点から説明できる。

## 1. 原理編

### 1.1 記号と前提
| 記号 | 意味 | 単位 |
|------|------|------|
| x | 混合気中の燃料のモル分率 | 無次元 |
| LFL | 燃焼下限界 | vol% |
| T_ad | 断熱火炎温度 | K |
| T_lim | 限界火炎温度（下限界での T_ad） | K |
| z | 燃料 1 mol を燃やすのに必要な O₂ の mol 数 | 無次元 |
| LOC | 限界酸素濃度 | vol% |

前提：エネルギー収支は第 2 周第 03 回と同じです（定圧・断熱・完全燃焼、エンタルピーは NIST Shomate 式）。
燃料が薄い側（希薄側）では生成物の温度が低いので、解離は無視できます。

### 1.2 第 04 回の復習と、今回の問い
第 04 回では、炎が自分で広がる条件を「燃焼で出る熱 ≧ 逃げる熱 ＋ 次の層を温める熱」と説明しました。
これを数値で表すには、「どのくらい熱ければ炎は自分で広がれるか」を決める必要があります。

その答えが**限界火炎温度**です。下限界の混合気で断熱火炎温度を計算すると、燃料の種類によらず、およそ一定の値になることが知られています。
- この「断熱火炎温度一定」の仮定は、**下限界には使えるが、上限界には使えない**とされています（[arXiv:1701.00909](https://arxiv.org/pdf/1701.00909v1)）。
- 下限界でのしきい値として 1440 K を使った研究もあります（[Razus ほか（Scribd 掲載）](https://www.scribd.com/document/440454385/Razus-pdf)）。
- 1 bar・定圧での限界火炎温度を、熱力学計算プログラムで求めた研究もあります（[CDC Stacks 収録論文](https://stacks.cdc.gov/view/cdc/37084)）。

### 1.3 下限界でのエネルギー収支
燃料のモル分率を x とすると、燃料 1 mol あたりの空気は (1−x)/x mol になります。そのため、生成物は次のようになります。

  CO₂、H₂O、余った O₂ = 0.21·(1−x)/x − z、N₂ = 0.79·(1−x)/x

断熱火炎温度は、第 2 周第 03 回と同じ式で求めます。

  Σ n_i [H_i(T_ad) − H_i(298)] = LHV

x を下限界の値にして T_ad を計算すれば、それが T_lim です。

### 1.4 T_lim 一定から導けること

**(a) ル・シャトリエの式**
希薄な混合気では、生成物の大部分は N₂ と O₂ です。そのため、混合気の熱容量は燃料の種類にほとんどよりません。
T_lim が一定なら、下限界の混合気は「1 mol あたりの発熱量がほぼ一定」の混合気だということになります。つまり、次のように書けます。

  LFL_i × ΔH_c,i ≒ 一定

混合燃料では、成分 i を濃度 c_i で含むとき、各成分の発熱の寄与を足し合わせます。すると、炎が広がる条件は次のようになります。

  Σ (c_i / LFL_i) ≥ 1

これがル・シャトリエの式です（第 04 回 1.2）。

**(b) 予熱すると下限界が下がる（Burgess-Wheeler 則）**
混合気をあらかじめ温めておくと、燃焼熱が少なくても T_lim に届きます。そのため、下限界は温度とともに下がります。
「下限界での発熱量と、反応物が持つ顕熱の和は一定」という形で、Burgess と Wheeler（1911）、のちに Zabetakis が定式化しました（[UNESP 論文リポジトリ](https://repositorio.unesp.br/bitstreams/7e5ba846-4d9c-4c77-9bac-ef2fa8a6e7cb/download)）。

**(c) 限界酸素濃度（LOC）の目安**
不活性ガス（N₂ など）を加えていくと、あるところで O₂ が足りなくなり、どんな燃料濃度でも炎が広がらなくなります。そのときの O₂ 濃度が LOC です。
燃焼範囲図（flammability diagram）では、LFL の高さに引いた水平線と量論線の交点から、LOC を次のように見積もります（[Wikipedia: Flammability diagram](https://en.wikipedia.org/wiki/Flammability_diagram)、[Crowl の解説（Scribd）](https://www.scribd.com/document/461380787/Flammability-Diagram)）。

  **LOC ≒ z × LFL**

これは「下限界の燃料をちょうど燃やしきるだけの O₂」という意味です。

### 1.5 水素はなぜ外れるか
水素は分子が軽く、拡散がとても速い気体です。熱の拡散に対する物質の拡散の比を表すルイス数でいうと、Le < 1 です。
そのため、希薄な水素の炎では、水素が炎の先端に選択的に集まる**優先拡散**が起こります。局所的には、平均の濃度より濃い状態で燃えることになります。
その結果、平均濃度から計算した T_ad が低くても、炎は（部分的に）上向きに広がれます。
- 伸長した炎では、ルイス数の効果で局所の燃焼の強さが大きく変わります（[MDPI Energies 13(23) 6263](https://www.mdpi.com/1996-1073/13/23/6263)）。
- 希薄な水素の炎では、優先拡散によって予熱帯の構造が変わります（[arXiv:2607.18993](https://arxiv.org/pdf/2607.18993)）。
- 水素 4〜6 % の混合気では、着火源に直接触れた分子しか燃えず、「4 % で爆発する」という説明は誤りだという主張もあります（[Kiwa IGRC 2024 発表資料](https://careers.kiwa.com/globalassets/netherlands/kiwa-technology/downloads/igrc2024-the-lower-flammability-limit-of-hydrogen-oral-presentation-bart-vogelzang.pdf)）。
  これは業界の 1 つの見解として扱います。

## 2. 実務とのつながり
- **パージと不活性化（第 2 周で法令とも関連）**：設備を修理するときは、可燃性ガスを窒素などで置換して O₂ を LOC より下げる、または燃料を LFL より下げます。メタンの LOC は、N₂ で希釈したとき O₂ 12 vol% とされています（[Wikipedia: Limiting oxygen concentration](https://wikipedia.com/wiki/Limiting_oxygen_concentration)）。
  ただし、LOC の値は試験容器の大きさや判定基準によって違います。たとえば Zlochower と Green（NIOSH）は、120 L・20 L の球形容器で、圧力上昇 7 % を基準に、従来の燃焼管より**低い** LOC を報告しています（[NIOSH PDF](https://cdc.gov/NIOSH/mining/UserFiles/works/pdfs/tloca.pdf)、[EPA HERO 書誌](https://hero.epa.gov/hero/index.cfm/reference/details/reference_id/4018290)）。安全側の値を使うのが基本です。
- **高温の設備**：予熱された混合気では、下限界が下がります。常温の値を使うと危険側になります。
- **水素混合ガスのガス検知器の設定**：ル・シャトリエの式で混合ガスの LFL を出しますが、水素は「平均の熱」の考え方から外れます（1.5）。そのため、検知器の LEL 設定は水素の値を基準に考えます。

## 3. 計算例（python で検算済み）

前提：LHV はメタン 802.3、プロパン 2043.1、水素 241.8 kJ/mol とします。LFL はメタン 5.0、プロパン 2.1、水素 4.0 vol% です（第 04 回の表を参照）。

### 計算例 1：下限界での断熱火炎温度
| 燃料 | LFL [%] | T_ad [K] | z | LOC の目安 z×LFL [%] |
|------|---------|----------|---|-------------------|
| メタン | 5.0 | **1483** | 2 | 10.0 |
| プロパン | 2.1 | **1531** | 5 | 10.5 |
| 水素 | 4.0 | **627** | 0.5 | 2.0 |

- メタンとプロパンは、LFL の値が 2 倍以上違うのに、T_ad はどちらも約 1500 K にそろいます。T_lim 一定の考え方が成り立っています。
- 水素は 627 K で、大きく外れます。1.5 の優先拡散の効果です。
- メタンの LOC の目安 10 % は、表の値 12 % より低く出ます。目安として使う分には安全側です。

### 計算例 2：T_lim = 1507 K（メタンとプロパンの平均）から LFL を逆算する
| 燃料 | 予測した LFL [%] | 表の値 [%] |
|------|-------------|---------|
| メタン | 5.12 | 5.0 |
| プロパン | 2.05 | 2.1 |
| 水素 | 15.5 | 4.0 |

炭化水素では、予測が 3 % 以内で合います。水素では、熱だけを考える方法は使えません。

### 計算例 3：予熱による下限界の低下（メタン、T_lim = 1483 K で固定）
| 初期温度 | 予測した LFL [%] |
|---------|-------------|
| 25 °C | 5.00 |
| 100 °C | 4.73 |
| 200 °C | 4.36 |

200 °C に予熱すると、下限界は約 13 % 下がります。

### 計算例 4：メタン 80 % ＋ 水素 20 % の混合燃料
- ル・シャトリエの式：1 / (0.8/5.0 + 0.2/4.0) = **4.76 %**
- T_lim 一定の方法（1483 K）：5.77 %

両者がずれるのは、水素を「熱」だけで扱っているためです。実測値に近いのはル・シャトリエの式（各成分の実測 LFL を使う）のほうです。
※ この組成での実測値は、今回は確認していません（要確認）。

## 4. 理解確認

### 理解確認 1（なぜ）
メタンとプロパンは LFL の値が 2 倍以上違うのに、下限界での断熱火炎温度はどちらも約 1500 K になる。この事実から、ル・シャトリエの式が成り立つ理由を説明せよ。
<details><summary>解答</summary>

希薄な混合気の熱容量は、ほぼ空気（N₂、O₂）で決まり、燃料の種類にほとんどよらない。T_lim が同じということは、下限界では「混合気 1 mol あたりの発熱量」が燃料によらずほぼ一定ということである。混合燃料では各成分の発熱が足し合わされるので、条件は Σ(c_i/LFL_i) = 1 になる。これがル・シャトリエの式である。
</details>

### 理解確認 2（計算）
エタン（C₂H₆ + 3.5O₂ → 2CO₂ + 3H₂O）の LFL を 3.0 % とする。LOC の目安を求めよ。
<details><summary>解答</summary>

手順：z = 3.5 なので、LOC ≒ z × LFL = 3.5 × 3.0 = **10.5 vol%**。

これはあくまで目安で、実測値とは数 % ずれることがある。
</details>

### 理解確認 3（誤っているものはどれか）
1. (イ) 混合気を予熱すると、燃焼熱が少なくても限界火炎温度に届くので、燃焼下限界は下がる。
2. (ロ) 水素の下限界 4 % で断熱火炎温度を計算すると約 1500 K になる。そのため、水素も T_lim 一定の考え方でよく説明できる。
3. (ハ) LOC ≒ z × LFL は、下限界の燃料をちょうど燃やしきるだけの O₂ 濃度を意味する。

<details><summary>解答</summary>

誤りは **(ロ)**。水素 4 % での T_ad は約 630 K で、1500 K に遠く及ばない。水素は拡散が速く（Le < 1）、優先拡散によって局所的に濃い状態で燃えるので、平均濃度の熱収支では説明できない。
</details>

## 5. よくある誤解・ひっかけ
- **「T_lim 一定」を上限界に使う**：上限界では、O₂ 不足による反応のしくみの変化が支配的なので、この仮定は成り立ちません（[arXiv:1701.00909](https://arxiv.org/pdf/1701.00909v1)）。
- **LOC の値をそのまま使う**：LOC は試験容器や判定基準によって違います。設計では余裕をとります（NFPA 69 などの規格値を確認すること）。
- **水素を炭化水素と同じに扱う**：水素は熱収支だけでは説明できません。優先拡散があるので、平均濃度だけで判断しないようにします。

## 参考文献
- [arXiv:1701.00909（下限界での断熱火炎温度一定の仮定）](https://arxiv.org/pdf/1701.00909v1)
- [Razus ほか（下限界のしきい火炎温度 1440 K, Scribd）](https://www.scribd.com/document/440454385/Razus-pdf)
- [CDC Stacks 収録論文（限界火炎温度の計算）](https://stacks.cdc.gov/view/cdc/37084)
- [UNESP リポジトリ（修正 Burgess-Wheeler 則）](https://repositorio.unesp.br/bitstreams/7e5ba846-4d9c-4c77-9bac-ef2fa8a6e7cb/download)
- [Wikipedia: Flammability diagram](https://en.wikipedia.org/wiki/Flammability_diagram)
- [Crowl の Flammability Diagram 解説（Scribd）](https://www.scribd.com/document/461380787/Flammability-Diagram)
- [Wikipedia: Limiting oxygen concentration](https://wikipedia.com/wiki/Limiting_oxygen_concentration)
- [Zlochower & Green, NIOSH（LOC と燃焼限界, PDF）](https://cdc.gov/NIOSH/mining/UserFiles/works/pdfs/tloca.pdf)
- [EPA HERO 書誌（Zlochower & Green 2009）](https://hero.epa.gov/hero/index.cfm/reference/details/reference_id/4018290)
- [MDPI Energies 13(23) 6263（ルイス数と下限界）](https://www.mdpi.com/1996-1073/13/23/6263)
- [arXiv:2607.18993（希薄水素火炎の優先拡散）](https://arxiv.org/pdf/2607.18993)
- [Kiwa IGRC 2024「The lower flammability limit of hydrogen」（PDF）](https://careers.kiwa.com/globalassets/netherlands/kiwa-technology/downloads/igrc2024-the-lower-flammability-limit-of-hydrogen-oral-presentation-bart-vogelzang.pdf)
