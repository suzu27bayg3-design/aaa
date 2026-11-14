# 第 26 回 燃料電池（PEFC／SOFC）

**分野：ガス技術（消費）**

## ねらい
- 燃料電池の理論起電力 1.229 V を、ギブズエネルギー ΔG = −nFE から導ける。
- 燃料電池の理論効率の上限 ΔG/ΔH が、熱機関のカルノー効率とは別の原理で決まることを説明できる。
- 都市ガスから水素を作る改質の反応と、PEFC と SOFC の違い（作動温度・改質・触媒）を説明できる。

## 1. 原理編

### 1.1 起電力の導出
燃料電池は、水素と酸素の反応を「燃やす」のではなく、電子の受け渡しを外の回路に通して、化学エネルギーを直接電気に変えます。

  H₂ + ½O₂ → H₂O（液体）　ΔG° = −237 kJ/mol、ΔH° = −286 kJ/mol

第 10 回のネルンストの式と同じ考え方で、反応が外にする電気の仕事の最大値はギブズエネルギーの減少量に等しいので、

  **ΔG = −n · F · E　→　E = −ΔG / (nF)**

| 記号 | 意味 | 値 |
|------|------|-----|
| n | 水素 1 mol で移る電子の数 | 2 |
| F | ファラデー定数 | 96,485 C/mol |
| ΔG | ギブズエネルギー変化 | −237 kJ/mol（25 ℃、液体の水ができる） |

  E = 237,000 / (2 × 96,485) = **1.229 V**

（[DoITPOMS（ケンブリッジ大学）：PEM fuel cell efficiency](https://doitpoms.ac.uk/tlplib/fuel-cells/pem_efficiency.php)、[ヴロツワフ工科大学：Thermodynamics of fuel cell](https://wme-z1.pwr.edu.pl/wp-content/uploads/2017/05/thermodynamics-of-fuel-cell-1.pdf)）

### 1.2 理論効率の上限：ΔG / ΔH
燃やしたときに出る熱は ΔH、電気として取り出せる最大は ΔG です。差の TΔS は、どうしても熱として出ていく分です（第 05 回の第二法則）。

  **η_最大 = ΔG / ΔH = 237 / 286 = 約 83 %**

（[ヴロツワフ工科大学](https://wme-z1.pwr.edu.pl/wp-content/uploads/2017/05/thermodynamics-of-fuel-cell-1.pdf)、[Scribd：Fuel cell performance 講義資料](https://www.scribd.com/document/602282552/Fuelcell-performance)）

**カルノー効率との違い**：熱機関（第 05・06 回）は、熱をいったん作ってから仕事に変えるので、高温と低温の温度差で効率の上限が決まります。燃料電池は熱を経由しないので、カルノー効率の制約を受けません。上限は反応の ΔG と ΔH の比で決まります。

**実際の電圧**：電流を流すと、電極での反応の遅れ（活性化過電圧）、膜の電気抵抗などで電圧が下がる。活性化過電圧だけで約 0.1〜0.2 V 下がる（[Scribd：Fuel cell performance](https://www.scribd.com/document/602282552/Fuelcell-performance)）。実際の効率は、セル電圧を 1.229 V で割り、理論効率を掛けて見積もれる。例えば 0.75 V のセルでは (0.75/1.229) × 0.8296 = 約 51 %（[Scribd：Fuel cell performance](https://www.scribd.com/document/602282552/Fuelcell-performance)）。

### 1.3 温度による違い
ΔG = ΔH − TΔS で、水ができる反応は ΔS < 0 なので、**温度が高いほど ΔG の絶対値が小さくなり、理論起電力は下がります**（計算例 2）。一方で、高温では電極の反応が速く、過電圧が小さくなります。PEFC と SOFC の設計は、この 2 つの効果のバランスで考えます。

### 1.4 都市ガスから水素を作る：改質
家庭用燃料電池（エネファーム）は、都市ガスのメタンを改質して水素を作ります。
- **水蒸気改質**：CH₄ + H₂O → CO + 3H₂　ΔH = +206 kJ/mol（強い吸熱。高温ほど進む）
- **シフト反応**：CO + H₂O → CO₂ + H₂　ΔH = −41 kJ/mol（弱い発熱。低温ほど進む）
- 合わせると CH₄ + 2H₂O → CO₂ + **4H₂**。メタン 1 mol から水素 4 mol ができる。
- 工業的には水蒸気と炭素の比を約 3 にする。

（[Reaction Chemistry & Engineering 2025 レビュー](https://pubs.rsc.org/en/content/articlepdf/2025/re/d5re00001g)、[Wikipedia: Steam reforming（ミラー）](https://ipfs.ssi.eecc.de/ipns/en.wikipedia-on-ipfs.org/wiki/Steam_reforming)、[TNO 報告](https://publications.tno.nl/publication/34629708/L41g8p/i04003.pdf)）

### 1.5 PEFC と SOFC
| 項目 | PEFC（固体高分子形） | SOFC（固体酸化物形） |
|------|------------------|------------------|
| 電解質 | 高分子膜 | セラミック |
| 作動温度 | 70〜80 ℃ | 約 700〜750 ℃ |
| 触媒 | 白金（低温で反応を進めるため） | 貴金属が不要 |
| CO の扱い | 毒になるので 10 ppm 以下に除く（シフト・CO 除去器が必要） | CO も燃料として使える |
| 改質の熱 | バーナで改質器を加熱 | スタックの排熱で賄える |
| 発電効率（当時の家庭用の例） | 約 39 % | 約 45〜46.5 % |
| 総合効率（発電＋熱回収） | 約 87 % | 約 87 % |

（[ENEOS 技術レビュー](https://www.ENEOS.co.jp/company/rd/technical_review/pdf/vol55_no02_05.pdf)、[MONOist：家庭の電力の 7 割をまかなう燃料電池](https://monoist.itmedia.co.jp/mn/articles/1109/20/news012.html)、[大和総研 レポート](https://www.dir.co.jp/report/research/introduction/economics/esg-hydrogen/20140625_008686.pdf)）

**原理で見ると**：
- PEFC は低温なので、反応を進めるのに白金が必要で、白金は CO で働かなくなる（被毒）。そのため、改質ガスの CO を徹底的に取り除く。
- SOFC は高温なので、触媒なしでも反応が速く、CO も酸化物イオンと反応して電気を生む。改質の吸熱（+206 kJ/mol）も、スタックの排熱で賄えるので、発電効率が上がる。
- 発電効率の数値は 2011〜2014 年ごろの資料のもので、最新の製品とは違う。

## 2. 実務とのつながり
- **コージェネ（第 06 回）**：エネファームは、発電の排熱で給湯する。総合効率 87 % 程度は、熱の使い道があってこそ実現する（第 06 回の「熱の需要があるときだけ得になる」と同じ）。
- **潜熱回収（第 24 回）**：排熱回収の効率を上げるには、戻り水の温度を低くする。
- **水素社会**：都市ガスに水素を混ぜる、あるいは水素を直接使う方向でも、燃料電池は中心になる技術である。

## 3. 計算例
（python で検算済み）

**例 1：理論起電力と効率**
- E = 237,100 / (2 × 96,485) = **1.229 V**
- 理論効率：237.1 / 285.8 = **83.0 %**
- ΔH を全部電気にした場合の電圧（熱中性電圧）：285,800 / (2 × 96,485) = **1.481 V**
- セル電圧 0.75 V のときの発電効率（高位発熱量基準）：0.75 / 1.481 = **約 50.6 %**（1.2 の式の 51 % と一致）

**例 2：温度と理論起電力（生成物は水蒸気、ΔH = −241.8 kJ/mol、ΔS = −44.4 J/(mol·K) を一定と仮定）**
| 温度 | 理論起電力 |
|------|-----------|
| 80 ℃（PEFC） | 約 1.17 V |
| 750 ℃（SOFC） | 約 1.02 V |
高温ほど理論起電力は下がるが、SOFC は過電圧が小さく排熱で改質できるので、全体の発電効率は高くなる。

**例 3：改質で得られる水素**
メタン 1 m³N から、改質とシフト反応で水素が最大 **4 m³N** できる。

## 4. 理解確認

### 理解確認 1
燃料電池の理論効率の上限が、カルノー効率ではなく ΔG/ΔH で決まるのはなぜか。

<details><summary>解答</summary>

燃料電池は、燃料をいったん燃やして熱にしてから仕事に変えるのではなく、化学反応の電子の受け渡しから直接電気を取り出すから。熱を経由しないので、高温と低温の温度差による制約（カルノー効率）は受けない。取り出せる電気の最大はギブズエネルギー ΔG で、反応の全エネルギー ΔH との比が上限になる。
</details>

### 理解確認 2
PEFC では改質ガスから CO をほとんど取り除く必要があるのに、SOFC では必要ないのはなぜか。

<details><summary>解答</summary>

PEFC は 70〜80 ℃と低温なので、反応を進めるのに白金触媒が必要で、その白金が CO に強く吸着されて働かなくなる（被毒）から。SOFC は 700 ℃以上の高温で、貴金属触媒がなくても反応が速く、CO も燃料として酸化物イオンと反応できる。
</details>

### 理解確認 3（誤っているものはどれか）
(a) 水素の燃料電池の理論起電力は、25 ℃でおよそ 1.23 V である。
(b) 水ができる反応では、温度が高いほど理論起電力は大きくなる。
(c) 水蒸気改質は吸熱反応なので、高温のほうが進みやすい。

<details><summary>解答</summary>

誤りは **(b)**。水ができる反応は ΔS < 0 なので、ΔG = ΔH − TΔS の絶対値は温度が高いほど小さくなり、理論起電力は**小さく**なる（例 2）。
</details>

## 参考文献
- [DoITPOMS（ケンブリッジ大学）：PEM fuel cell efficiency](https://doitpoms.ac.uk/tlplib/fuel-cells/pem_efficiency.php)
- [ヴロツワフ工科大学：Thermodynamics of fuel cell](https://wme-z1.pwr.edu.pl/wp-content/uploads/2017/05/thermodynamics-of-fuel-cell-1.pdf)
- [Scribd：Fuel cell performance 講義資料](https://www.scribd.com/document/602282552/Fuelcell-performance)
- [Reaction Chemistry & Engineering 2025 レビュー（水蒸気改質）](https://pubs.rsc.org/en/content/articlepdf/2025/re/d5re00001g)
- [Wikipedia: Steam reforming（ミラー）](https://ipfs.ssi.eecc.de/ipns/en.wikipedia-on-ipfs.org/wiki/Steam_reforming)
- [TNO 報告（水蒸気改質）](https://publications.tno.nl/publication/34629708/L41g8p/i04003.pdf)
- [ENEOS 技術レビュー（SOFC 型エネファーム）](https://www.ENEOS.co.jp/company/rd/technical_review/pdf/vol55_no02_05.pdf)
- [MONOist：家庭の電力の 7 割をまかなう燃料電池](https://monoist.itmedia.co.jp/mn/articles/1109/20/news012.html)
- [大和総研 レポート（水素・燃料電池）](https://www.dir.co.jp/report/research/introduction/economics/esg-hydrogen/20140625_008686.pdf)
