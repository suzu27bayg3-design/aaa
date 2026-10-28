# 第 10 回 腐食と防食

**分野：基礎理論**

## ねらい
- 鉄の腐食を「電池」として説明し、アノード（溶ける側）とカソード（電子を受け取る側）の役割を言える。
- ネルンストの式から電位が濃度で変わることを、ファラデーの法則から腐食量が電流で決まることを導ける。
- 電気防食（流電陽極方式・外部電源方式）が、なぜ腐食を止められるのかを、電位の言葉で説明できる。

## 1. 原理編

### 1.1 腐食は小さな電池
水と酸素がある所で、鉄の表面には 2 つの反応が同時に起こります。
- **アノード反応（酸化）**：Fe → Fe²⁺ + 2e⁻（鉄が溶ける）
- **カソード反応（還元）**：O₂ + 2H₂O + 4e⁻ → 4OH⁻（中性〜アルカリ性）、または 2H⁺ + 2e⁻ → H₂（酸性）

アノードで出た電子は金属の中を通ってカソードへ流れ、イオンは水（電解質）の中を動きます。つまり腐食は、**金属・電解質・2 つの反応がそろった電池（腐食電池）** です。どれか 1 つを断てば、腐食は止まります。

### 1.2 電位とネルンストの式
金属が溶けやすいかどうかは、電極電位で表します。標準水素電極を 0 V とした標準電極電位（25 ℃、濃度 1 mol/L）の例は、次のとおりです（[Wikipedia: Standard electrode potential (data page)](https://en.wikipedia.org/wiki/Standard_electrode_potential_(data_page))）。

| 反応 | E°（V） |
|------|---------|
| Mg²⁺ + 2e⁻ ⇌ Mg | −2.37 |
| Zn²⁺ + 2e⁻ ⇌ Zn | −0.76 |
| Fe²⁺ + 2e⁻ ⇌ Fe | −0.44 |

電位が低い（マイナスが大きい）金属ほど溶けやすく、電池ではアノードになります。

実際の電位はイオンの濃度で変わります。これを表すのが**ネルンストの式**です（[IUPAC Gold Book: Nernst equation](https://goldbook.iupac.org/terms/view/09068)、[DoITPOMS（ケンブリッジ大学）: The Nernst equation](https://doitpoms.ac.uk/tlplib/pourbaix/nernst.php)）。

  **E = E° − (RT/zF)·ln(a_red/a_ox)**　（25 ℃では E = E° − (0.0592/z)·log₁₀(a_red/a_ox)）

| 記号 | 意味 | 単位 |
|------|------|------|
| E | 平衡電極電位 | V |
| R | 気体定数 8.314 | J/(mol·K) |
| T | 温度 | K |
| z | 反応で移る電子の数 | — |
| F | ファラデー定数 96,485 | C/mol |
| a | 活量（薄い溶液ではほぼ濃度） | — |

**導出の考え方**：電池がする電気的な仕事（zFE）は、反応のギブズエネルギー変化（ΔG = ΔG° + RT ln Q）と等しくなります（ΔG = −zFE）。両辺を −zF で割ると、ネルンストの式になります。第 05 回の熱力学が、電気化学にもつながっています。

### 1.3 ファラデーの法則：腐食量は電流で決まる
アノードで溶けた鉄 1 mol につき、2 mol の電子（2F クーロン）が流れます。したがって、腐食電流 I [A] が t 秒流れたときに溶ける鉄の質量は、

  **m = I·t·M / (z·F)**

M は原子量です（鉄 55.85 g/mol、z = 2）。これを面積と密度で割ると、腐食の速さ（深さ/年）になります。鉄では電流密度 1 μA/cm² が約 0.46 mpy（約 0.0117 mm/年）に相当します（[KFUPM 講義：Faraday's Laws and Rate of Corrosion](https://faculty.kfupm.edu.sa/me/hussaini/corrosion%20engineering/03.02.01.htm)）。
ただし、この計算は表面全体が均一に腐食する場合のものです。一部分に集中する局部腐食では、深さを過小に見積もります（[Gamry: Calculation of Corrosion Rate](https://help.gamry.com/?p=468658)）。

### 1.4 埋設管で特に怖い「マクロセル腐食」
- 腐食電池のアノードとカソードが、離れた場所に大きく分かれてできるものを**マクロセル腐食**という。
- 代表例は**コンクリート／土壌マクロセル腐食**。建物のコンクリート中の鉄筋（電位が高く、カソードになる）と、土壌中の配管（アノードになる）が電気的につながって起こる（[日本水道鋼管協会などの Q&A](https://www.jwrc-net.or.jp/docs/publication-outreach/qa/13-26.pdf)、[ナカボーテック 技術資料](https://www.nakabohtec.co.jp/presentation/pdf/presentation03.pdf)）。
- 塗覆装（被覆）に小さな傷があると、電流がその傷に集中する。そのため、小さい傷ほど電流密度が大きくなり、速く深く穴があく（計算例 2）。

### 1.5 電気防食：電位を下げて、溶けない側にする
電気防食は、守りたい金属に外から電流を流し込み、**全体をカソードにして**電位を下げる方法です。電位が十分に下がると、鉄が溶ける反応が起こらなくなります。
- **流電陽極方式（犠牲陽極）**：鉄より電位の低い金属（マグネシウム、亜鉛、アルミニウムなど）を導線でつなぐ。電池作用で防食電流が流れ、陽極の金属が代わりに溶けて消耗する（[ナカボーテック 技術資料](https://www.nakabohtec.co.jp/presentation/pdf/presentation03.pdf)）。
- **外部電源方式**：直流電源で電流を流し込む。長い導管の本線などに使われる（[Fabrico: Cathodic protection](https://www.fabrico.io/blog/cathodic-protection/)）。
- **防食の目安**：鋼の場合、飽和硫酸銅電極を基準に **−0.85 V** より卑な（低い）電位に保つことが広く使われる基準である（[Southwestern Petroleum Short Course 資料](https://www.swpshortcourse.org/ppdl/1976)）。
- 被覆（プラスチック被覆鋼管など）と電気防食を組み合わせると、被覆の傷の部分にだけ防食電流を流せばよいので、必要な電流が小さく済む（[日本水道鋼管協会などの Q&A](https://www.jwrc-net.or.jp/docs/publication-outreach/qa/13-26.pdf)）。

## 2. 実務とのつながり
- **ガス導管**：鋼管は塗覆装と電気防食で守る。低圧の細い管では、腐食しない PE 管への置き換えが進んでいる（第 18 回）。
- **建物の貫通部**：配管がコンクリートを貫通する部分は、マクロセル腐食を防ぐため、さや管などで鉄筋と絶縁する。
- **陽極の寿命**：流電陽極は溶けて減るので、ファラデーの法則で寿命を見積もり、点検で電位を測って交換時期を判断する（計算例 3）。
- **迷走電流**：電鉄などから土に漏れた電流が配管に出入りすると、電流が出ていく所で腐食が進む。これも同じ電池の原理で説明できる。

## 3. 計算例
（python で検算済み）

**例 1：ネルンストの式**
Fe²⁺ の濃度が 10⁻⁶ mol/L のとき（腐食の判定でよく使う濃度）、
- E = −0.447 + (0.0592/2) × log₁₀(10⁻⁶) = **−0.625 V**（標準水素電極基準。E° には −0.447 V を使った）
- 0.0592 は (RT/F)·ln 10 を 25 ℃で計算した値（= 0.05916）。
- 濃度が 1/10 になるごとに、電位は 0.0296 V 下がる。

**例 2：電流密度と腐食速度**
鉄に電流密度 1 A/m²（= 100 μA/cm²）の腐食電流が流れ続けると、
- 1 m² あたり 1 年で溶ける量：1 × 3.156×10⁷ s × 55.85 / (2 × 96,485) = **約 9.1 kg**
- 密度 7.87 g/cm³ で割ると、深さは **約 1.16 mm/年**。
- 被覆の 1 cm² の傷に電流が集中して 1 A/m² 相当になれば、肉厚 4 mm の管でも 3〜4 年で貫通しうる。小さな傷ほど危ないのは、このためである。

**例 3：マグネシウム陽極の寿命**
- マグネシウムの理論発生電気量：2 × 96,485 / 24.305 / 3.6 = **約 2,205 A·h/kg**
- 実際の効率は約 50 % とされる（[KFUPM 講義：Characteristics of Galvanic Anodes](https://faculty.kfupm.edu.sa/ME/hussaini/Corrosion%20Engineering/05.03.02.htm)）。
- 10 kg の陽極で 20 mA の防食電流を流し続けると、10 × 2,205 × 0.5 / (0.02 × 8,766) = **約 63 年**。

## 4. 理解確認

### 理解確認 1
腐食が「電池」であると考えると、どんな方法で腐食を止められるか。3 つ挙げよ。

<details><summary>解答</summary>

電池が成り立つには、アノード反応・カソード反応・電子の通り道（金属）・イオンの通り道（電解質）がそろう必要がある。止め方の例は次の 3 つ。
- 被覆で電解質と酸素を遮る。
- 絶縁して、異なる金属どうし（鉄筋と配管など）の電気的なつながりを断つ。
- 電気防食で、守りたい金属全体をカソードにする。
</details>

### 理解確認 2
被覆の傷が小さいほど、その部分が速く深く腐食しやすいのはなぜか。

<details><summary>解答</summary>

カソード（広い鉄筋や広い面積）から流れ込む腐食電流の総量は変わらないのに、アノードの面積が小さいので、電流密度が大きくなる。ファラデーの法則から、腐食の深さの速さは電流密度に比例するので、小さな傷に集中して穴があく。
</details>

### 理解確認 3（誤っているものはどれか）
(a) 流電陽極方式では、鉄より電位の低い金属が溶けて、鉄を守る。
(b) 電気防食は、守りたい金属をアノードにして腐食を止める方法である。
(c) ネルンストの式は、ΔG = −zFE と ΔG = ΔG° + RT ln Q から導かれる。

<details><summary>解答</summary>

誤りは **(b)**。電気防食は、守りたい金属に電流を流し込んで**カソード**にし、電位を下げて溶けないようにする方法である。
</details>

## 参考文献
- [Wikipedia: Standard electrode potential (data page)](https://en.wikipedia.org/wiki/Standard_electrode_potential_(data_page))
- [IUPAC Gold Book: Nernst equation](https://goldbook.iupac.org/terms/view/09068)
- [DoITPOMS（ケンブリッジ大学）: The Nernst equation](https://doitpoms.ac.uk/tlplib/pourbaix/nernst.php)
- [KFUPM 講義：Faraday's Laws and Rate of Corrosion](https://faculty.kfupm.edu.sa/me/hussaini/corrosion%20engineering/03.02.01.htm)
- [KFUPM 講義：Cathodic Protection（流電陽極の特性）](https://faculty.kfupm.edu.sa/ME/hussaini/Corrosion%20Engineering/05.03.02.htm)
- [Gamry: Calculation of Corrosion Rate](https://help.gamry.com/?p=468658)
- [日本水道鋼管協会などの Q&A（マクロセル腐食・電気防食）](https://www.jwrc-net.or.jp/docs/publication-outreach/qa/13-26.pdf)
- [ナカボーテック 技術資料（電気防食）](https://www.nakabohtec.co.jp/presentation/pdf/presentation03.pdf)
- [Southwestern Petroleum Short Course 資料（防食電位の基準）](https://www.swpshortcourse.org/ppdl/1976)
- [Fabrico: Cathodic protection](https://www.fabrico.io/blog/cathodic-protection/)
