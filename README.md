# makefun-news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Qiuwineth/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Qiuwineth/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

**The World on Friday — 20 November 2026 in one picture.** A 1024×1024
front-page poster that sums up the world news of Friday 20 November 2026:
the AI sell-off going global (Nikkei −4.8%, KOSPI −4.7%, Taiex −6.4%,
SoftBank −16%, gold −4.2%), Russian missiles hitting Kyiv's three Dnipro
bridges, COP31's final day in Antalya with no deal in sight, the UK–EU
reset deal in Brussels (100,000 youth visas a year), and Europe's youth
day of action across 25+ countries — plus an IN BRIEF strip (the Pete
Rose pardon, Fiji and Tonga disaster declarations, record Florida
flooding, and Peres Jepchirchir's three-year doping ban).

Every story was verified as news of 20 November 2026 against at least
two reputable sources before it was drawn: Reuters, AP, BBC News, CNN,
CNBC, Al Jazeera, The Hindu, France 24, The Times, NPR, AFP, The Japan
Times, RFI, RNZ Pacific, ABC News (Australia) and UPI.

`entry.png` is the poster. It is drawn by `draw.py` (Pillow), which is
fully deterministic — fixed geometry and text, no clocks, no randomness —
so re-running it reproduces the same bytes. `main.py` is the entrypoint
the grader runs: standard library only, it copies `entry.png` to the
output directory.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

That writes `out/entry.png`. To redraw the poster from source (needs
Pillow and the Liberation/DejaVu fonts):

```sh
python3 draw.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=whndskex&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
