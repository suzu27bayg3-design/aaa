# 第 06 回 ガスサイクル（ブレイトン／ランキン／コージェネ）

**分野：基礎理論**

## ねらい
- ガスタービン（ブレイトンサイクル）の理論効率が圧力比だけで決まることを、断熱変化の式から導ける。
- コンバインドサイクルの効率を、エネルギー収支から η_cc = η_GT + (1 − η_GT)·η_ST と表せる。
- コージェネの「総合効率」と「省エネ効果」の違いを、熱の使い道に注意して計算できる。

## 1. 原理編

### 1.1 ブレイトンサイクル（ガスタービン）
ガスタービンは、次の 4 つの過程を繰り返します（空気標準サイクル。作動流体を理想気体の空気とし、比熱は一定、損失はないと仮定）。

| 過程 | 装置 | 変化 |
|------|------|------|
| 1 → 2 | 圧縮機 | 断熱（等エントロピー）圧縮 |
| 2 → 3 | 燃焼器 | 等圧で加熱（q_in = c_p(T₃ − T₂)） |
| 3 → 4 | タービン | 断熱膨張 |
| 4 → 1 | （大気へ放出） | 等圧で放熱（q_out = c_p(T₄ − T₁)） |

**効率の導出**
1. 第 05 回の第一法則から、η = 1 − q_out/q_in = 1 − (T₄ − T₁)/(T₃ − T₂)。
2. 断熱変化では T₂/T₁ = (p₂/p₁)^((k−1)/k) = r_p^((k−1)/k)。膨張側も同じ圧力比なので、T₃/T₄ も同じ値になる（[IIT Kanpur: Air standard Brayton cycle](https://home.iitk.ac.in/~suller/lectures/lec29a.htm)、[NPTEL Module 6](https://archive.nptel.ac.in/content/storage2/courses/112104113/lecture30/30_4.htm)）。
3. T₄ − T₁ と T₃ − T₂ の比も同じ値になるので、

  **η_Brayton = 1 − 1 / r_p^((k−1)/k)**

（[MIT 16.unified 講義ノート](https://web.mit.edu/16.unified/www/FALL/thermodynamics/notes/node47.html)、[GATE 2014 問題](https://me.gateoverflow.in/144/gate-mechanical-2014-set-2-question-13)）

| 記号 | 意味 |
|------|------|
| r_p = p₂/p₁ | 圧力比 |
| k = c_p/c_v | 比熱比（空気で 1.4） |

**意味**：理論効率は圧力比だけで決まり、最高温度 T₃ には関係しません。ただし、T₃ を上げると 1 サイクルで取り出せる仕事が増えます。そのため、タービン翼の材料が耐えられる限り高温化が進められてきました（[IIT Kanpur](https://home.iitk.ac.in/~suller/lectures/lec29a.htm)）。

### 1.2 ランキンサイクル（蒸気タービン）
水をポンプで加圧し、ボイラーで蒸発させ、蒸気タービンで膨張させ、復水器で水に戻すサイクルです。
液体の水を加圧するのに必要な仕事はとても小さい（水は体積がほとんど変わらないため）。そのため、取り出す仕事に比べて、ポンプが使う仕事はわずかで済みます。
復水器で 30 ℃程度まで冷やせるので、低温側の温度 T_C を低くでき、そのぶん効率が上がります（第 05 回のカルノー効率）。

### 1.3 コンバインドサイクル
ガスタービンの排気（数百 ℃）は、まだ仕事にできる熱を持っています。これでボイラーを回して蒸気タービンも動かすのが、コンバインドサイクルです。

燃料の熱を 1 とすると、
- ガスタービンの仕事：η_GT
- 排気に残る熱：1 − η_GT
- そのうち蒸気タービンで仕事になる分：(1 − η_GT)·η_ST

  **η_cc = η_GT + (1 − η_GT)·η_ST**

高温の熱をガスタービンで、中くらいの温度の熱を蒸気タービンで使うので、温度の高いところから順に熱を使い切ることになります。実際の発電所では、効率 63.08 % がギネス世界記録に認定された例（中部電力 西名古屋火力 7-1 号）があります（[GE プレスリリース](https://www.ge.com/news/press-releases/ge-sets-guinness-world-records™-title-most-efficient-power-plant/jp)）。
ただし、効率には HHV（高位発熱量）基準と LHV（低位発熱量）基準、発電端と送電端の違いがあります。LHV 基準のほうが高い値になるので、比べるときは基準をそろえる必要があります（[環境省 資料](https://www.env.go.jp/content/900521305.pdf)、[三菱重工 プレスリリース](https://www.mhi.com/jp/news/1206015214.html)）。

### 1.4 コージェネレーション
燃料で発電し、同時に出る排熱も回収して、給湯・暖房・蒸気に使います。
- 燃料のエネルギーのうち、電気が約 20〜45 %、熱が約 30〜60 %、利用しにくい廃熱が 20〜25 %。**総合効率は 75〜80 %**（[資源エネルギー庁 発電コスト検証 WG 資料](https://www.enecho.meti.go.jp/committee/council/basic_policy_subcommittee/mitoshi/cost_wg/2021/data/02_06.pdf)）。
- 一般的な発電効率は 30〜50 % 程度、総合効率は最大で 90 % 程度（[環境省 算定ガイドライン資料](https://www.env.go.jp/earth/ondanka/gel/ghg-guideline/search/pdf/01_100.pdf)）。
- 実際の事例では、排熱の使い道が少ないと総合効率は 57.6 % にとどまった、という報告もある（[東京都 資料](https://www.sangyo-rodo.metro.tokyo.lg.jp/documents/d/sangyo-rodo/fc466281fe9472f30211f30127bdaf73_12)）。

**原理**：第二法則（第 05 回）から、発電すると必ず捨て熱 Q_C が出ます。コージェネは、この捨て熱を「どうせ必要な熱」として使うことで、燃料の利用率を上げます。**熱の需要があるときだけ得になる**のがポイントです。

## 2. 実務とのつながり
- **都市ガスの需要**：ガスタービン・ガスエンジンのコージェネや、GTCC 発電所は、天然ガスの大口需要先である。
- **燃料電池（第 26 回）**：熱機関を通さずに化学エネルギーを直接電気にするので、カルノー効率の制約を受けない。エネファームは、これをコージェネとして使っている。
- **設置の判断**：コージェネは、病院・ホテル・工場など、熱の需要が一年を通して大きい建物で効果が大きい。

## 3. 計算例
（python で検算済み）

**例 1：ブレイトンサイクルの理論効率（k = 1.4）**
| 圧力比 r_p | 10 | 20 | 30 |
|-----------|----|----|----|
| η | 0.482 | 0.575 | 0.622 |

**例 2：コンバインドサイクル**
η_GT = 0.40、η_ST = 0.35 とすると、η_cc = 0.40 + 0.60 × 0.35 = **0.61**

**例 3：コージェネの省エネ効果**
燃料 100 で、電気 35 と熱 45 が得られるとする。同じ電気と熱を別々に作る場合（系統の電気の発電効率 40 %、ボイラー効率 90 % と仮定）と比べる。
- 別々に作る場合の燃料：35/0.40 + 45/0.90 = 87.5 + 50 = **137.5**
- 省エネ率：1 − 100/137.5 = **27 %**
- 熱を 15 しか使えない場合：35/0.40 + 15/0.90 = 104.2 となり、省エネ率は **4 %** にまで下がる。

熱の使い道があるかどうかで効果が大きく変わることが、数字で確かめられます。

## 4. 理解確認

### 理解確認 1
ブレイトンサイクルの理論効率が、最高温度 T₃ に関係しないのはなぜか。

<details><summary>解答</summary>

断熱圧縮と断熱膨張の圧力比が同じなので、T₂/T₁ と T₃/T₄ が同じ値 r_p^((k−1)/k) になるから。効率の式 1 − (T₄ − T₁)/(T₃ − T₂) で、この比だけが残り、T₃ は消える。T₃ が効くのは、効率ではなく、1 サイクルあたりの仕事の大きさである。
</details>

### 理解確認 2
コンバインドサイクルの効率がガスタービン単独より高くなるのはなぜか。

<details><summary>解答</summary>

ガスタービンの排気に残る熱 1 − η_GT を、蒸気タービンでもう一度仕事にするから。温度の高い熱から順に使い、捨てる熱を減らしている。
</details>

### 理解確認 3（誤っているものはどれか）
(a) コージェネの総合効率は、発電効率と排熱利用率の和である。
(b) コージェネは、熱の需要が少ない建物でも、発電所の電気を買うより必ず大きな省エネになる。
(c) 発電効率は、HHV 基準か LHV 基準かで値が変わる。

<details><summary>解答</summary>

誤りは **(b)**。例 3 のとおり、熱を使えないと、別々に作る場合との差はほとんどなくなる。
</details>

## 参考文献
- [IIT Kanpur: Air standard Brayton cycle](https://home.iitk.ac.in/~suller/lectures/lec29a.htm)
- [NPTEL Module 6 Lecture 30](https://archive.nptel.ac.in/content/storage2/courses/112104113/lecture30/30_4.htm)
- [MIT 16.unified Thermodynamics notes](https://web.mit.edu/16.unified/www/FALL/thermodynamics/notes/node47.html)
- [GATE Mechanical 2014 Set 2 Q13](https://me.gateoverflow.in/144/gate-mechanical-2014-set-2-question-13)
- [GE プレスリリース（西名古屋火力 7-1 号 ギネス世界記録）](https://www.ge.com/news/press-releases/ge-sets-guinness-world-records™-title-most-efficient-power-plant/jp)
- [三菱重工 プレスリリース（LHV 基準の表記）](https://www.mhi.com/jp/news/1206015214.html)
- [環境省 資料（HHV と LHV の併記）](https://www.env.go.jp/content/900521305.pdf)
- [資源エネルギー庁 発電コスト検証 WG 資料（コージェネ）](https://www.enecho.meti.go.jp/committee/council/basic_policy_subcommittee/mitoshi/cost_wg/2021/data/02_06.pdf)
- [環境省 算定ガイドライン資料（コージェネ）](https://www.env.go.jp/earth/ondanka/gel/ghg-guideline/search/pdf/01_100.pdf)
- [東京都 資料（コージェネの実績例）](https://www.sangyo-rodo.metro.tokyo.lg.jp/documents/d/sangyo-rodo/fc466281fe9472f30211f30127bdaf73_12)
