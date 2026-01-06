---
layout: post
title: "DuckDB on LoongArch"
author: "Hannes Mühleisen"
thumb: "/images/blog/thumbs/morefine-m700s.svg"
image: "/images/blog/thumbs/morefine-m700s.jpg"
excerpt: "In today's “What's on your desk?” episode, we test a Loongson CPU with the LoongArch architecture."
tags: ["benchmark"]
---

It’s not every day that a new CPU architecture arrives on your desk. I grew up on the [Intel 486](https://en.wikipedia.org/wiki/I486) back in the early 90s. I also still remember AMD releasing its [64-bit x86 extension](https://en.wikipedia.org/wiki/X86-64#History) in 2000. Then not a lot happened until Apple released the ARM-based M1 architecture in 2020. But today is the day again (for me), with the long-awaited arrival of the “MOREFINE M700S” in our office.

<img src="{% link images/blog/loongarch/morefine-computer.jpg %}" width="800" />

The M700S contains a Loongson CPU. Also called “LoongArch” or “Godson” processors, this CPU was developed in China [based](https://www.tomshardware.com/pc-components/cpus/chinese-chipmaker-loongson-wins-case-over-rights-to-mips-architecture-companys-new-cpu-architecture-heavily-resembles-existing-mips) on the (somewhat esoteric) [MIPS architecture](https://en.wikipedia.org/wiki/MIPS_architecture). This is part of a plan to become technologically self-sufficient as part of the government-funded [Made in China 2025](https://en.wikipedia.org/wiki/Made_in_China_2025) plan.

It is probably safe to assume that – given the ongoing trade shenanigans – the Loongson will become much more popular in China as time goes on. DuckDB already sees quite a lot of usage from China, so naturally we want to make sure that DuckDB runs well on the Loongson. Thankfully, one of our community members has already opened a [pull request](https://github.com/duckdb/duckdb/pull/19962) with two minimal changes to allow DuckDB to compile. We became curious.

We purchased the M700S on (where else?) [AliExpress](https://nl.aliexpress.com/item/1005008047862187.html?spm=a2g0o.order_list.order_list_main.5.685479d21SDmQG&gatewayAdapt=glo2nld) for around 500 EUR. Besides the Loongson 8-core 3A6000 CPU it contains 16 GB of main memory and a 256 GB solid-state disk. 

<img src="{% link images/blog/loongarch/morefine-aliexpress-listing.png %}" width="800" />

Once plugged in and booted up, things feel pretty normal besides the loud fan that seems to be always on. On the screen, a variant of Debian called [Loongnix](https://www.loongson.cn/EN/system/loongnix) boots up. The GUI seems to be KDE-based and comes with a custom browser “LBrowser” which is a fork of Chromium. Just because it was not obvious we document it here: the default `root` password is `M700S`. There is also a user account `m700s` with the same password. 

<img src="{% link images/blog/loongarch/loongnix.jpg %}" width="800" />

Overall, the software seems a little dated, even after running `apt upgrade`: The Linux kernel seems to be version 4.19, which was released back in 2018, and which has been EOL for a year now. The GCC version is 8.3, which similarly came out in 2019.

With the [aforementioned patch](https://github.com/duckdb/duckdb/pull/19962), we managed to compile DuckDB 1.4.3 on Loongnix. There was one small issue where the CMake file `append_metadata.cmake` was not compatible with the older CMake version (3.13.4) available on Loongnix. But simply replacing that file with an empty one allowed us to complete the build. Of course we could also have updated CMake, but life is short. Once completed, we ran DuckDB’s extensive unit test suite (`make allunit`) to confirm that our build runs correctly on the Loongson CPU. Results looked good.

For performance comparison, we re-used the methodology from our [previous blog post](https://duckdb.org/2025/01/17/raspberryi-pi-tpch) that ran DuckDB on a Raspberry Pi. In short, we run the 22 TPC-H benchmark queries on “Scale Factor” 100 and 300, which in DuckDB format is a 25 GB and 78 GB database file, respectively. We compare those numbers with the nearest computer, which is my day-to-day MacBook Pro with an M3 Max CPU. For fairness, we limit DuckDB to 14 GB of RAM on both platforms. The reported timings are “hot” runs, meaning we re-ran the query set and took the timings from the second run.

Here are the results, and they are not great. We start with aggregated timings:

| SF    | System   | Geometric mean |   Sum |
| ----- | -------- | -------------: | ----: |
| SF100 | MacBook  |            0.6 |  16.9 |
| SF100 | MOREFINE |            6.1 | 192.8 |
| SF300 | MacBook  |            2.8 |  78.8 |
| SF300 | MOREFINE |           27.3 | 791.6 |

We can see that the MacBook is around *ten times faster* than the MOREFINE on this benchmark, both in the geometric mean of runtimes as well as in the sum.
If you are interested in the individual query runtimes, you can find them below.
<details markdown='1'>
<summary markdown='span'>
Click here to see the individual query runtimes.
</summary>
<div>
<table>
<thead>
<tr>
<th style="text-align: right;">Q</th>
<th style="text-align: right;">SF100/MacBook</th>
<th style="text-align: right;">SF100/MOREFINE</th>
<th style="text-align: right;">SF300/MacBook</th>
<th style="text-align: right;">SF300/MOREFINE</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align: right;">1</td>
<td style="text-align: right;">1.247</td>
<td style="text-align: right;">7.363</td>
<td style="text-align: right;">4.528</td>
<td style="text-align: right;">26.475</td>
</tr>
<tr>
<td style="text-align: right;">2</td>
<td style="text-align: right;">0.117</td>
<td style="text-align: right;">1.058</td>
<td style="text-align: right;">0.474</td>
<td style="text-align: right;">4.101</td>
</tr>
<tr>
<td style="text-align: right;">3</td>
<td style="text-align: right;">0.697</td>
<td style="text-align: right;">8.563</td>
<td style="text-align: right;">2.759</td>
<td style="text-align: right;">32.432</td>
</tr>
<tr>
<td style="text-align: right;">4</td>
<td style="text-align: right;">0.570</td>
<td style="text-align: right;">7.348</td>
<td style="text-align: right;">2.331</td>
<td style="text-align: right;">27.185</td>
</tr>
<tr>
<td style="text-align: right;">5</td>
<td style="text-align: right;">0.631</td>
<td style="text-align: right;">8.498</td>
<td style="text-align: right;">3.217</td>
<td style="text-align: right;">34.462</td>
</tr>
<tr>
<td style="text-align: right;">6</td>
<td style="text-align: right;">0.180</td>
<td style="text-align: right;">1.236</td>
<td style="text-align: right;">1.395</td>
<td style="text-align: right;">13.225</td>
</tr>
<tr>
<td style="text-align: right;">7</td>
<td style="text-align: right;">0.620</td>
<td style="text-align: right;">7.702</td>
<td style="text-align: right;">3.119</td>
<td style="text-align: right;">37.411</td>
</tr>
<tr>
<td style="text-align: right;">8</td>
<td style="text-align: right;">0.640</td>
<td style="text-align: right;">5.593</td>
<td style="text-align: right;">3.611</td>
<td style="text-align: right;">29.914</td>
</tr>
<tr>
<td style="text-align: right;">9</td>
<td style="text-align: right;">1.906</td>
<td style="text-align: right;">30.560</td>
<td style="text-align: right;">6.670</td>
<td style="text-align: right;">99.884</td>
</tr>
<tr>
<td style="text-align: right;">10</td>
<td style="text-align: right;">0.923</td>
<td style="text-align: right;">11.755</td>
<td style="text-align: right;">4.036</td>
<td style="text-align: right;">40.412</td>
</tr>
<tr>
<td style="text-align: right;">11</td>
<td style="text-align: right;">0.102</td>
<td style="text-align: right;">1.037</td>
<td style="text-align: right;">0.709</td>
<td style="text-align: right;">4.444</td>
</tr>
<tr>
<td style="text-align: right;">12</td>
<td style="text-align: right;">0.535</td>
<td style="text-align: right;">6.422</td>
<td style="text-align: right;">2.918</td>
<td style="text-align: right;">31.501</td>
</tr>
<tr>
<td style="text-align: right;">13</td>
<td style="text-align: right;">1.847</td>
<td style="text-align: right;">21.185</td>
<td style="text-align: right;">6.394</td>
<td style="text-align: right;">74.081</td>
</tr>
<tr>
<td style="text-align: right;">14</td>
<td style="text-align: right;">0.408</td>
<td style="text-align: right;">5.616</td>
<td style="text-align: right;">3.240</td>
<td style="text-align: right;">26.613</td>
</tr>
<tr>
<td style="text-align: right;">15</td>
<td style="text-align: right;">0.252</td>
<td style="text-align: right;">2.652</td>
<td style="text-align: right;">1.906</td>
<td style="text-align: right;">17.454</td>
</tr>
<tr>
<td style="text-align: right;">16</td>
<td style="text-align: right;">0.273</td>
<td style="text-align: right;">3.108</td>
<td style="text-align: right;">0.879</td>
<td style="text-align: right;">11.480</td>
</tr>
<tr>
<td style="text-align: right;">17</td>
<td style="text-align: right;">0.805</td>
<td style="text-align: right;">5.184</td>
<td style="text-align: right;">4.655</td>
<td style="text-align: right;">28.469</td>
</tr>
<tr>
<td style="text-align: right;">18</td>
<td style="text-align: right;">1.538</td>
<td style="text-align: right;">15.492</td>
<td style="text-align: right;">7.619</td>
<td style="text-align: right;">71.845</td>
</tr>
<tr>
<td style="text-align: right;">19</td>
<td style="text-align: right;">0.779</td>
<td style="text-align: right;">9.143</td>
<td style="text-align: right;">4.379</td>
<td style="text-align: right;">39.111</td>
</tr>
<tr>
<td style="text-align: right;">20</td>
<td style="text-align: right;">0.441</td>
<td style="text-align: right;">4.993</td>
<td style="text-align: right;">3.234</td>
<td style="text-align: right;">25.967</td>
</tr>
<tr>
<td style="text-align: right;">21</td>
<td style="text-align: right;">1.996</td>
<td style="text-align: right;">23.231</td>
<td style="text-align: right;">9.503</td>
<td style="text-align: right;">96.452</td>
</tr>
<tr>
<td style="text-align: right;">22</td>
<td style="text-align: right;">0.441</td>
<td style="text-align: right;">5.036</td>
<td style="text-align: right;">1.237</td>
<td style="text-align: right;">18.709</td>
</tr>
</tbody>
</table>

</div>
</details>

It is always exciting to get DuckDB running on a new platform. Of course, we have built DuckDB to be ulta-portable and agnostic to hardware environments while still delivering excellent performance. So it was not that surprising that it was not that difficult to get DuckDB running on the MOREFINE with its new-ish CPU. However, performance on the standard TPC-H benchmark was not that impressive, with the MacBook being around ten times faster than the MOREFINE.

Of course, there are many opportunities for improvement. For starters, the `gcc` toolchain on LoongArch is likely not as advanced by far compared with its x86/ARM counterpart, so advances there could make a big difference. The same applies of course to IO performance, which we have not measured separately. But hey, the “glass half full” department could also rightfully claim that the Loongson CPU can complete TPC-H SF300!

One could also argue that a MacBook Pro is much more expensive than 500 EUR MOREFINE. However, a recent M4 Mac Mini with the same memory and storage specs will cost around 700 EUR, not that much more all things considered. It will run circles around the MOREFINE. And it will not constantly annoy you with its fan. 
