#!/usr/bin/env python3
"""
Benchmark charts — professional redesign with visual polish.

9 charts matching benchmark_comparison.md references:
  00_infographic, 01_executive_summary, 02_accuracy, 03_latency,
  04_cost, 05_complexity, 06_architecture, 07_scorecard, 08_detail_grid

Design: small figures (7-10in), big fonts, drop shadows, colored accents,
subtle backgrounds, path effects on titles.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np
import os

OUT = os.path.join(os.path.dirname(__file__), 'charts')
os.makedirs(OUT, exist_ok=True)

# ── Palette ──
# Presentation-oriented Snowflake vs Databricks palette
CORTEX   = '#2563EB';  CORTEX_D = '#1D4ED8';  CORTEX_L = '#93C5FD';  CORTEX_BG = '#EFF6FF'
DBX      = '#FF3621';  DBX_D    = '#C52A1B';   DBX_L    = '#FFB3AA';  DBX_BG    = '#FFF0EE'
GREEN    = '#0F9D75';  GREEN_BG = '#EAF8F3'
AMBER    = '#D97706'
SF_DARK  = '#0B2239'
TEXT     = '#1E293B';  SUB      = '#64748B';   LGRAY    = '#E2E8F0'
WHITE    = '#FFFFFF';  BG       = '#F6F9FB'
DPI = 220

# ── Global style ──
plt.rcParams.update({
    'figure.facecolor': BG,
    'savefig.facecolor': BG,
    'axes.facecolor': WHITE,
    'axes.edgecolor': LGRAY,
    'axes.labelcolor': TEXT,
    'text.color': TEXT,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Aptos', 'Helvetica Neue', 'Arial', 'DejaVu Sans'],
    'font.size': 12,
    'axes.grid': False,
    'xtick.color': SUB,
    'ytick.color': SUB,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'axes.titleweight': 'bold',
})

TITLE_FX = []

# ── Helpers ──
def shadow_card(ax, x, y, w, h, radius='round,pad=0.15', face=WHITE, edge=LGRAY, lw=1.2):
    """Draw a card with a drop shadow."""
    sh = mpatches.FancyBboxPatch((x+0.04, y-0.04), w, h, boxstyle=radius,
                                   facecolor='#B8C7D3', edgecolor='none', alpha=0.14, zorder=1)
    card = mpatches.FancyBboxPatch((x, y), w, h, boxstyle=radius,
                                     facecolor=face, edgecolor=edge, linewidth=lw, zorder=2)
    ax.add_patch(sh)
    ax.add_patch(card)
    return card

def accent_strip(ax, x, y, h, color, width=0.12):
    """Colored left-border accent on a card."""
    strip = mpatches.FancyBboxPatch((x, y), width, h, boxstyle='round,pad=0.02',
                                      facecolor=color, edgecolor='none', zorder=3)
    ax.add_patch(strip)


def polish_axis(ax, grid_axis='y'):
    """Consistent executive-chart treatment: subtle grid, no box, restrained ticks."""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(LGRAY)
    ax.spines['bottom'].set_color(LGRAY)
    ax.tick_params(axis='both', length=0, pad=6)
    if grid_axis:
        ax.grid(axis=grid_axis, color=LGRAY, linewidth=0.8, alpha=0.65)
    ax.set_axisbelow(True)


def brand_header(ax, title, subtitle=None, color=CORTEX):
    ax.text(0.0, 1.08, title, transform=ax.transAxes, ha='left', va='bottom',
            fontsize=25, fontweight='bold', color=SF_DARK)
    ax.add_patch(mpatches.Rectangle((0.0, 1.045), 0.075, 0.012,
                                    transform=ax.transAxes, facecolor=color,
                                    edgecolor='none', clip_on=False))
    if subtitle:
        ax.text(0.0, 1.015, subtitle, transform=ax.transAxes, ha='left', va='bottom',
                fontsize=11, color=SUB)

# ── Data ──
questions = [f'P{i:02d}' for i in range(1, 13)]
cortex_lat = [41,40,28,41,40,22,23,32,41,63,39,39]
dbx_lat    = [39,48,34,110,184,34,100,237,82,113,110,112]
cortex_tok = [217375,289954,93558,738939,496478,127938,123488,491698,183892,230527,361087,95939]
dbx_tok    = [12529,16550,13280,105512,279160,149944,314122,578042,317074,348287,453940,411194]
cortex_correct = [True]*12
dbx_correct    = [True,True,True,False,True,True,True,True,True,True,True,True]
dbx_fail       = [not c for c in dbx_correct]

categories = ['Coded\nColumns','Complex\nJoins','Noise\nFiltering','Model\nQuality','Hybrid\nFiltered']
cortex_acc = [3,2,3,2,2]
dbx_acc    = [3,1,3,2,2]
cat_totals = [3,2,3,2,2]

cat_map = {0:'Coded Cols',1:'Coded Cols',2:'Coded Cols',3:'Complex Joins',4:'Complex Joins',
           5:'Noise Filter',6:'Noise Filter',7:'Noise Filter',8:'Model Qual.',9:'Model Qual.',
           10:'Hybrid Filt.',11:'Hybrid Filt.'}


# ======================================================================
# 0  HERO INFOGRAPHIC
# ======================================================================
fig = plt.figure(figsize=(10, 13))
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 10); ax.set_ylim(0, 13)
ax.axis('off'); ax.set_facecolor(BG)

# Gradient-ish header (two overlapping rects)
ax.add_patch(mpatches.FancyBboxPatch((0, 11.0), 10, 2.0, boxstyle='square,pad=0',
             facecolor='#0F172A', edgecolor='none'))
ax.add_patch(mpatches.FancyBboxPatch((0, 11.0), 10, 0.4, boxstyle='square,pad=0',
             facecolor=SF_DARK, edgecolor='none', alpha=0.6))
ax.text(5, 12.25, 'Snowflake Cortex  vs  Databricks Genie', ha='center', va='center',
        fontsize=32, fontweight='bold', color=WHITE,
        path_effects=[pe.withStroke(linewidth=2, foreground='#0F172A')])
ax.text(5, 11.4, 'SEC v. Meridian Capital  |  Legal Benchmark  |  Aug 2026',
        ha='center', va='center', fontsize=14, color='#94A3B8')

# Dataset strip with card
shadow_card(ax, 0.3, 9.8, 9.4, 1.0, face=WHITE)
items = [('12','Tables'),('1.39M','Rows'),('22','Docs'),('~9K','Pages'),('12','Questions'),('5','Categories')]
sw = 9.4/len(items)
for i,(v,l) in enumerate(items):
    cx = 0.3 + sw*(i+0.5)
    ax.text(cx, 10.5, v, ha='center', fontsize=22, fontweight='bold', color=SF_DARK)
    ax.text(cx, 10.05, l, ha='center', fontsize=12, color=SUB)

# 4 KPI cards (2x2)
kpis = [('ACCURACY','100%','92%','+8 pp',CORTEX),
        ('AVG LATENCY','37s','100s','2.7× faster',CORTEX),
        ('TOTAL COST','$3.28','$14.40','77% lower cost',GREEN),
        ('COST / CORRECT','$0.27','$1.31','79% lower / correct',GREEN)]
cw, ch = 4.3, 2.9
positions = [(0.35,6.5),(5.35,6.5),(0.35,3.2),(5.35,3.2)]

for (px,py),(title,cv,dv,delta,acol) in zip(positions,kpis):
    shadow_card(ax, px, py, cw, ch)
    accent_strip(ax, px, py, ch, acol)
    mid = px + cw/2
    ax.text(mid, py+ch-0.35, title, ha='center', fontsize=13, fontweight='bold', color=SUB, zorder=4)
    ax.text(px+cw*0.30, py+ch-1.15, cv, ha='center', fontsize=38, fontweight='bold', color=CORTEX, zorder=4)
    ax.text(px+cw*0.30, py+ch-1.7,  'Snowflake', ha='center', fontsize=14, fontweight='bold', color=CORTEX, zorder=4)
    ax.text(px+cw*0.72, py+ch-1.15, dv, ha='center', fontsize=38, fontweight='bold', color=DBX, zorder=4)
    ax.text(px+cw*0.72, py+ch-1.7,  'Databricks', ha='center', fontsize=14, fontweight='bold', color=DBX, zorder=4)
    badge = mpatches.FancyBboxPatch((px+0.5, py+0.2), cw-1.0, 0.55,
            boxstyle='round,pad=0.12', facecolor=GREEN, edgecolor='none', zorder=4)
    ax.add_patch(badge)
    ax.text(mid, py+0.47, delta, ha='center', va='center', fontsize=15, fontweight='bold', color=WHITE, zorder=5)

# Platform config
shadow_card(ax, 0.3, 0.8, 9.4, 2.1, face=WHITE)
configs = [('Snowflake:','Single agent, parallel tools, semantic model, Cortex Search, user-selected model'),
           ('Databricks:','Supervisor >> sub-agents sequentially, raw schema, no user model choice')]
for j,(k,v) in enumerate(configs):
    yy = 2.4 - j*0.6
    ax.text(0.6, yy, k, fontsize=12, fontweight='bold', color=SUB, zorder=4)
    ax.text(1.8, yy, v, fontsize=11, color=TEXT, zorder=4)
ax.text(5, 1.0, 'Pricing: Claude Sonnet 4.6 rates  |  Bharath Suresh, SE',
        ha='center', fontsize=10, color=SUB, fontstyle='italic', zorder=4)

plt.savefig(f'{OUT}/00_infographic.png', dpi=DPI, bbox_inches='tight', facecolor=BG)
plt.close()
print('[1/8] Infographic')


# ======================================================================
# 1  EXECUTIVE SUMMARY
# ======================================================================
fig = plt.figure(figsize=(10, 5))
fig.patch.set_facecolor(BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 10); ax.set_ylim(0, 5)
ax.axis('off'); ax.set_facecolor(BG)

ax.text(5, 4.6, 'EXECUTIVE SUMMARY', ha='center', fontsize=28, fontweight='bold',
        color=SF_DARK, path_effects=TITLE_FX)

kpi_ex = [('Accuracy','12/12','100%','11/12','92%','Snowflake +8 pp'),
          ('Avg Latency','37s','max 63s','100s','max 237s','2.7× faster'),
          ('Token Cost','$3.28','12 Qs','$14.40','12 Qs','77% lower cost'),
          ('Cost/Correct','$0.27','','$1.31','','79% lower / correct')]
for i,(title,cv,csub,dv,dsub,verdict) in enumerate(kpi_ex):
    cx = 0.15 + i*2.45
    shadow_card(ax, cx, 0.3, 2.25, 3.8)
    accent_strip(ax, cx, 0.3, 3.8, CORTEX)
    mid = cx + 1.125
    ax.text(mid, 3.75, title, ha='center', fontsize=14, fontweight='bold', color=SUB, zorder=4)
    ax.text(cx+0.58, 2.7, cv, ha='center', fontsize=20, fontweight='bold', color=CORTEX, zorder=4)
    ax.text(cx+0.58, 2.15, 'Snowflake', ha='center', fontsize=11, color=CORTEX_L, zorder=4)
    if csub:
        ax.text(cx+0.56, 1.8, csub, ha='center', fontsize=10, color=SUB, zorder=4)
    ax.text(cx+1.67, 2.7, dv, ha='center', fontsize=20, fontweight='bold', color=DBX, zorder=4)
    ax.text(cx+1.67, 2.15, 'Databricks', ha='center', fontsize=11, color=DBX_L, zorder=4)
    if dsub:
        ax.text(cx+1.69, 1.8, dsub, ha='center', fontsize=10, color=SUB, zorder=4)
    vb = mpatches.FancyBboxPatch((cx+0.2, 0.5), 1.85, 0.5, boxstyle='round,pad=0.1',
                                   facecolor=GREEN, edgecolor='none', zorder=4)
    ax.add_patch(vb)
    ax.text(mid, 0.75, verdict, ha='center', va='center', fontsize=13, fontweight='bold', color=WHITE, zorder=5)

plt.savefig(f'{OUT}/01_executive_summary.png', dpi=DPI, bbox_inches='tight', facecolor=BG)
plt.close()
print('[2/8] Executive Summary')


# ======================================================================
# 2  ACCURACY
# ======================================================================
fig, ax = plt.subplots(figsize=(9, 5.5))
fig.patch.set_facecolor(BG)
y = np.arange(len(categories))
h = 0.35
ax.barh(y+h/2, cortex_acc, h, label='Snowflake (12/12)', color=CORTEX, edgecolor=CORTEX_D, lw=0.8, zorder=3)
ax.barh(y-h/2, dbx_acc,    h, label='Databricks (11/12)', color=DBX,    edgecolor=DBX_D,    lw=0.8, zorder=3)

for i in range(len(categories)):
    ax.text(cortex_acc[i]+0.08, y[i]+h/2, f'{cortex_acc[i]}/{cat_totals[i]}',
            va='center', fontsize=18, fontweight='bold', color=CORTEX_D)
    fail = (dbx_acc[i] < cat_totals[i])
    suf = '  FAIL' if fail else ''
    ax.text(dbx_acc[i]+0.08, y[i]-h/2, f'{dbx_acc[i]}/{cat_totals[i]}{suf}',
            va='center', fontsize=18, fontweight='bold', color=DBX_D)

ax.set_yticks(y)
ax.set_yticklabels([c.replace('\n',' ') for c in categories], fontsize=15)
ax.set_xlim(0, 4.2); ax.set_xticks([0,1,2,3])
ax.set_xlabel('Correct Answers', fontsize=15, fontweight='bold')
brand_header(ax, 'Accuracy by Category', 'Correct answers by benchmark category')

polish_axis(ax)

fig.text(0.5, -0.02, 'Genie fails on complex join query (P04) -- truncated results led to hallucinated win counts.',
         ha='center', fontsize=12, color=SUB, fontstyle='italic')
plt.tight_layout()
plt.savefig(f'{OUT}/02_accuracy.png', dpi=DPI, bbox_inches='tight', facecolor=BG)
plt.close()
print('[3/8] Accuracy')


# ======================================================================
# 3  LATENCY
# ======================================================================
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor(BG)
x = np.arange(12); w = 0.38

ax.bar(x-w/2, cortex_lat, w, label='Snowflake', color=CORTEX, edgecolor=CORTEX_D, lw=0.6, zorder=3)
dc = [DBX_D if f else DBX for f in dbx_fail]
ax.bar(x+w/2, dbx_lat, w, label='Databricks', color=dc, edgecolor=DBX_D, lw=0.6, zorder=3)

for i in range(12):
    ax.text(x[i]-w/2, cortex_lat[i]+8, f'{cortex_lat[i]}s', ha='center',
            fontsize=10, color=CORTEX_D, fontweight='bold')
    suf = ' FAIL' if dbx_fail[i] else ''
    col = '#7F1D1D' if dbx_fail[i] else DBX_D
    ax.text(x[i]+w/2, dbx_lat[i]+8, f'{dbx_lat[i]}s{suf}', ha='center',
            fontsize=10, color=col, fontweight='bold')

ax.annotate('7.4x slower', xy=(7+w/2, 237), xytext=(5, 280),
            fontsize=16, fontweight='bold', color=DBX_D,
            arrowprops=dict(arrowstyle='->', color=DBX_D, lw=2.5))
ax.annotate('4.6x', xy=(4+w/2, 184), xytext=(2.5, 220),
            fontsize=16, fontweight='bold', color=DBX_D,
            arrowprops=dict(arrowstyle='->', color=DBX_D, lw=2.5))

avg_c = np.mean(cortex_lat); avg_d = np.mean(dbx_lat)
ax.axhline(avg_c, color=CORTEX, ls='--', lw=1.5, alpha=0.5)
ax.axhline(avg_d, color=DBX, ls=':', lw=1.5, alpha=0.4)

ax.set_xticks(x); ax.set_xticklabels(questions, fontsize=12)
ax.set_ylabel('Seconds', fontsize=15, fontweight='bold')
brand_header(ax, 'Per-Question Latency', '12 benchmark questions — lower is better')

ax.set_ylim(0, 320)

polish_axis(ax)

ax.text(0.98, 0.97, f'Snowflake avg {avg_c:.0f}s  vs  Databricks avg {avg_d:.0f}s\n2.7x faster overall',
        transform=ax.transAxes, ha='right', va='top', fontsize=14, fontweight='bold', color=SF_DARK,
        bbox=dict(boxstyle='round,pad=0.5', facecolor=CORTEX_BG, edgecolor=CORTEX, lw=1.5))

plt.tight_layout()
plt.savefig(f'{OUT}/03_latency.png', dpi=DPI, bbox_inches='tight', facecolor=BG)
plt.close()
print('[4/8] Latency')


# ======================================================================
# 4  COST
# ======================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6), gridspec_kw={'width_ratios': [1, 1.2]})
fig.patch.set_facecolor(BG)

platforms = ['Snowflake','Databricks']
c_cr,c_cw,c_out = 0.84, 1.84, 0.60
d_in,d_out = 7.65, 6.75

ax1.bar(platforms,[c_cr,0],0.5,label='cache_read', color='#3B82F6', edgecolor=CORTEX_D, lw=0.6, zorder=3)
ax1.bar(platforms,[c_cw,0],0.5,bottom=[c_cr,0],label='cache_write', color='#60A5FA', edgecolor=CORTEX_D, lw=0.6, zorder=3)
ax1.bar(platforms,[c_out,0],0.5,bottom=[c_cr+c_cw,0],label='output', color=CORTEX_L, edgecolor=CORTEX_D, lw=0.6, zorder=3)
ax1.bar(platforms,[0,d_in],0.5,label='input', color=DBX, edgecolor=DBX_D, lw=0.6, zorder=3)
ax1.bar(platforms,[0,d_out],0.5,bottom=[0,d_in],label='DBX output', color=DBX_L, edgecolor=DBX_D, lw=0.6, zorder=3)

ax1.text(0, 3.65, '$3.28', ha='center', fontsize=26, fontweight='bold', color=CORTEX_D)
ax1.text(1, 14.75, '$14.40', ha='center', fontsize=26, fontweight='bold', color=DBX_D)

ax1.set_ylabel('USD', fontsize=14, fontweight='bold')
ax1.set_title('Total Cost (12 Qs)', fontsize=22, fontweight='bold', color=SF_DARK, pad=12,
              path_effects=TITLE_FX)
ax1.set_ylim(0, 18)
ax1.spines['top'].set_visible(False); ax1.spines['right'].set_visible(False)


fig.text(0.22, -0.02, 'Snowflake 77% lower cost', ha='center', fontsize=14,
         fontweight='bold', color=GREEN,
         bbox=dict(boxstyle='round,pad=0.3', facecolor=GREEN_BG, edgecolor=GREEN))

# Table
ax2.axis('off'); ax2.set_xlim(0,10); ax2.set_ylim(0,10)
ax2.set_title('Cost Breakdown', fontsize=22, fontweight='bold', color=SF_DARK, pad=12,
              path_effects=TITLE_FX)

rows = [('Total cost','$3.28','$14.40'),('Cost / question','$0.27','$1.20'),
        ('Cost / correct','$0.27','$1.31'),('Total tokens','3.45M','3.0M'),
        ('Eff. rate / MTok','$0.95','$4.80'),('Cache efficiency','85.1%','N/A'),
        ('Wasted tokens','0','384K'),('Wasted cost','$0.00','$1.84')]

ax2.text(0.2,9.3,'Metric',fontsize=14,fontweight='bold',color=SUB)
ax2.text(6.2,9.3,'Snowflake',fontsize=14,fontweight='bold',color=CORTEX,ha='center')
ax2.text(8.8,9.3,'Databricks',fontsize=14,fontweight='bold',color=DBX,ha='center')
ax2.plot([0,10],[8.8,8.8],color=LGRAY,lw=1.5)

for i,(m,cv,dv) in enumerate(rows):
    yy = 8.2 - i*1.05
    if i%2==0:
        ax2.add_patch(mpatches.FancyBboxPatch((0,yy-0.35),10,0.75,
                      boxstyle='round,pad=0.05',facecolor=WHITE,edgecolor='none'))
    ax2.text(0.2,yy,m,fontsize=13,color=TEXT)
    ax2.text(6.2,yy,cv,fontsize=14,fontweight='bold',color=CORTEX_D,ha='center')
    ax2.text(8.8,yy,dv,fontsize=14,fontweight='bold',color=DBX_D,ha='center')

plt.tight_layout()
plt.savefig(f'{OUT}/04_cost.png', dpi=DPI, bbox_inches='tight', facecolor=BG)
plt.close()
print('[5/8] Cost')


# ======================================================================
# 5  COMPLEXITY SCALING
# ======================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5.5))
fig.patch.set_facecolor(BG)

complexity = ['Simple','Medium','Complex']
c_avg = [round(np.mean([41,41,39])), round(np.mean([22,23,32,41])), round(np.mean([40,28,40]))]
d_avg = [round(np.mean([39,110,112])), round(np.mean([34,100,237,82])), round(np.mean([48,34,184]))]
ratios = [d/c for c,d in zip(c_avg, d_avg)]

xc = np.arange(3); wc = 0.35
ax1.bar(xc-wc/2, c_avg, wc, label='Snowflake', color=CORTEX, edgecolor=CORTEX_D, lw=0.6, zorder=3)
ax1.bar(xc+wc/2, d_avg, wc, label='Databricks',  color=DBX,    edgecolor=DBX_D,    lw=0.6, zorder=3)

for i in range(3):
    ax1.text(i-wc/2, c_avg[i]+5, f'{c_avg[i]}s', ha='center', fontsize=15, fontweight='bold', color=CORTEX_D)
    ax1.text(i+wc/2, d_avg[i]+5, f'{d_avg[i]}s', ha='center', fontsize=15, fontweight='bold', color=DBX_D)

ax1.set_ylabel('Avg Latency (s)', fontsize=14, fontweight='bold')
ax1.set_title('Latency vs Complexity', fontsize=22, fontweight='bold', color=SF_DARK, pad=12,
              path_effects=TITLE_FX)
ax1.set_xticks(xc); ax1.set_xticklabels(complexity, fontsize=13)
ax1.set_ylim(0, 180)
ax1.legend(fontsize=12, facecolor=WHITE, edgecolor=LGRAY)
ax1.spines['top'].set_visible(False); ax1.spines['right'].set_visible(False)

# Speed advantage bars (replaces growth multiplier)
y2 = np.arange(3)
colors = [AMBER if r >= 3 else SUB for r in ratios]
bars = ax2.barh(y2, ratios, 0.5, color=colors, edgecolor=[DBX_D if r >= 3 else '#6B7280' for r in ratios],
                lw=1.2, zorder=3, alpha=0.85)
ax2.axvline(1.0, color=LGRAY, ls='--', lw=1.5, zorder=1)
for i, r in enumerate(ratios):
    ax2.text(r + 0.12, i, f'{r:.1f}x slower', fontsize=16, fontweight='bold',
             color=DBX_D if r >= 3 else '#374151', va='center')

ax2.set_title('Speed Advantage (Snowflake)', fontsize=22, fontweight='bold', color=SF_DARK, pad=12,
              path_effects=TITLE_FX)
ax2.set_yticks(y2); ax2.set_yticklabels(complexity, fontsize=13)
ax2.set_xlabel('DBX / Snowflake Ratio', fontsize=13, fontweight='bold')
ax2.set_xlim(0, 5.5)
ax2.invert_yaxis()
ax2.spines['top'].set_visible(False); ax2.spines['right'].set_visible(False)

fig.text(0.5, -0.04, 'Snowflake stays flat (30-40s). DBX is 2-4x slower across all complexity levels.',
         ha='center', fontsize=12, color=SF_DARK, fontstyle='italic',
         bbox=dict(boxstyle='round,pad=0.4', facecolor=DBX_BG, edgecolor=DBX, lw=1))

plt.tight_layout()
plt.savefig(f'{OUT}/05_complexity.png', dpi=DPI, bbox_inches='tight', facecolor=BG)
plt.close()
print('[6/8] Complexity')


# ======================================================================
# 6  ARCHITECTURE  (aggregate across all 12 queries)
# ======================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 9.5))
fig.patch.set_facecolor(BG)
for a in [ax1, ax2]:
    a.set_xlim(0,10); a.set_ylim(-1.5,12.5); a.axis('off'); a.set_facecolor(BG)

def abox(ax, cx, cy, txt, col, w=5, h=1.0, fs=13, bg_alpha=0.12):
    sh = mpatches.FancyBboxPatch((cx-w/2+0.06, cy-h/2-0.06), w, h, boxstyle='round,pad=0.2',
                                   facecolor='#94A3B8', edgecolor='none', alpha=0.2, zorder=1)
    r  = mpatches.FancyBboxPatch((cx-w/2, cy-h/2), w, h, boxstyle='round,pad=0.2',
                                   facecolor=col, edgecolor=col, lw=2, alpha=bg_alpha, zorder=2)
    b  = mpatches.FancyBboxPatch((cx-w/2, cy-h/2), w, h, boxstyle='round,pad=0.2',
                                   facecolor='none', edgecolor=col, lw=2, zorder=3)
    ax.add_patch(sh); ax.add_patch(r); ax.add_patch(b)
    ax.text(cx, cy, txt, ha='center', va='center', fontsize=fs, fontweight='bold', color=TEXT, zorder=4)

def stat_badge(ax, cx, cy, txt, bg_col, text_col, fs=9):
    bb = mpatches.FancyBboxPatch((cx-1.2, cy-0.22), 2.4, 0.44, boxstyle='round,pad=0.08',
                                   facecolor=bg_col, edgecolor='none', alpha=0.9, zorder=5)
    ax.add_patch(bb)
    ax.text(cx, cy, txt, ha='center', va='center', fontsize=fs, fontweight='bold', color=text_col, zorder=6)

# ── Cortex side ──────────────────────────────────────────────
ax1.text(5, 12.0, 'Snowflake Cortex', ha='center', fontsize=20, fontweight='bold', color=CORTEX)
ax1.text(5, 11.4, 'Consistent across all 12 queries', ha='center', fontsize=11, color=SUB)

abox(ax1, 5, 10.2, 'User Question', CORTEX, fs=14)
abox(ax1, 5, 8.3, 'Cortex Agent\n(claude-opus-4-8)', CORTEX, h=1.4, fs=13)
abox(ax1, 2.6, 5.8, 'Cortex Search\n(doc retrieval)', '#1D4ED8', w=4.4, h=1.3, fs=11)
abox(ax1, 7.4, 5.8, 'Cortex Analyst\n(semantic SQL)', '#1D4ED8', w=4.4, h=1.3, fs=11)
abox(ax1, 5, 3.3, 'Synthesize +\nFlag Discrepancy', GREEN, w=5, h=1.3, fs=12)
abox(ax1, 5, 1.3, 'Answer', GREEN, fs=15)

ap = dict(arrowstyle='->', color=CORTEX, lw=2.5)
ax1.annotate('', xy=(5,8.95), xytext=(5,9.7), arrowprops=ap)
ax1.annotate('', xy=(2.6,6.45), xytext=(3.6,7.55), arrowprops=dict(arrowstyle='->',color=CORTEX_L,lw=2))
ax1.annotate('', xy=(7.4,6.45), xytext=(6.4,7.55), arrowprops=dict(arrowstyle='->',color=CORTEX_L,lw=2))
ax1.annotate('', xy=(4,3.95), xytext=(2.6,5.15), arrowprops=dict(arrowstyle='->',color=CORTEX_L,lw=2))
ax1.annotate('', xy=(6,3.95), xytext=(7.4,5.15), arrowprops=dict(arrowstyle='->',color=CORTEX_L,lw=2))
ax1.annotate('', xy=(5,1.85), xytext=(5,2.65), arrowprops=ap)

pbg = mpatches.FancyBboxPatch((3.5,7.1),3.0,0.5,boxstyle='round,pad=0.1',facecolor=GREEN,edgecolor='none',zorder=5)
ax1.add_patch(pbg)
ax1.text(5,7.35,'PARALLEL',ha='center',va='center',fontsize=14,fontweight='bold',color=WHITE,zorder=6)

# Stats column
ax1.text(5, -0.15, '4 steps  |  1 LLM call  |  avg 37s',
         ha='center', fontsize=13, fontweight='bold', color=GREEN)
ax1.text(5, -0.7, 'Same architecture every query.\nSchema awareness eliminates trial-and-error.',
         ha='center', fontsize=10, color=SUB, fontstyle='italic')

# ── DBX side (aggregate pattern) ─────────────────────────────
ax2.text(5, 12.0, 'Databricks Genie', ha='center', fontsize=20, fontweight='bold', color=DBX)
ax2.text(5, 11.4, 'Aggregate across all 12 queries', ha='center', fontsize=11, color=SUB)

abox(ax2, 5, 10.2, 'User Question', DBX, fs=14)
abox(ax2, 5, 8.8, 'Check Examples\n(always empty)', SUB, h=1.0, fs=11, w=5.5)

# Supervisor loop box
loop_bg = mpatches.FancyBboxPatch((0.3, 2.5), 9.4, 5.5, boxstyle='round,pad=0.3',
                                    facecolor=DBX, edgecolor=DBX, lw=2, alpha=0.04, zorder=0)
loop_bd = mpatches.FancyBboxPatch((0.3, 2.5), 9.4, 5.5, boxstyle='round,pad=0.3',
                                    facecolor='none', edgecolor=DBX, lw=1.5, ls='--', zorder=1)
ax2.add_patch(loop_bg); ax2.add_patch(loop_bd)
ax2.text(9.5, 7.8, 'SEQUENTIAL\nLOOP', ha='center', fontsize=9, fontweight='bold',
         color=DBX_D, rotation=0)

abox(ax2, 5, 7.2, 'Supervisor LLM\n(~3.8 calls/query)', DBX, h=1.2, fs=12, w=6)

# Three tool boxes
abox(ax2, 1.8, 5.2, 'Genie\n(SQL)', DBX_D, w=3.0, h=1.2, fs=11)
abox(ax2, 5.0, 5.2, 'Knowledge\nAgent', DBX_D, w=3.0, h=1.2, fs=11)
abox(ax2, 8.2, 5.2, 'Python\nExec', DBX_D, w=3.0, h=1.2, fs=11)

# Stats under each tool
ax2.text(1.8, 4.25, '16 calls  |  7 of 12 Qs', ha='center', fontsize=8.5, color=SUB)
ax2.text(1.8, 3.85, '~40% returned empty', ha='center', fontsize=8.5, fontweight='bold', color=DBX_D)
ax2.text(5.0, 4.25, '21 calls  |  10 of 12 Qs', ha='center', fontsize=8.5, color=SUB)
ax2.text(5.0, 3.85, 'Most-used tool', ha='center', fontsize=8.5, fontweight='bold', color='#374151')
ax2.text(8.2, 4.25, '8 calls  |  6 of 12 Qs', ha='center', fontsize=8.5, color=SUB)
ax2.text(8.2, 3.85, 'Date math / formatting', ha='center', fontsize=8.5, fontweight='bold', color='#374151')

# Loop arrows from supervisor to tools and back
for tx in [1.8, 5.0, 8.2]:
    ax2.annotate('', xy=(tx, 5.8), xytext=(tx, 6.55), arrowprops=dict(arrowstyle='->', color=DBX_L, lw=1.5))
    ax2.annotate('', xy=(tx, 6.55), xytext=(tx, 5.8),
                 arrowprops=dict(arrowstyle='->', color=DBX_L, lw=1.2, ls='--'))

abox(ax2, 5, 1.5, 'Answer', DBX, fs=15)

# Arrow from examples to loop
ax2.annotate('', xy=(5, 7.8), xytext=(5, 8.3), arrowprops=dict(arrowstyle='->', color=DBX_L, lw=1.5))
# Arrow from loop to answer
ax2.annotate('', xy=(5, 2.0), xytext=(5, 2.5), arrowprops=dict(arrowstyle='->', color=DBX_L, lw=1.5))

# Failure badge
wb = mpatches.FancyBboxPatch((0.4, 3.05), 3.6, 0.5, boxstyle='round,pad=0.08',
                               facecolor='#FEE2E2', edgecolor=DBX_D, lw=1.2, zorder=5)
ax2.add_patch(wb)
ax2.text(2.2, 3.3, '6/12 Qs had failures', ha='center', va='center',
         fontsize=9, fontweight='bold', color=DBX_D, zorder=6)

# Stats footer
ax2.text(5, 0.5, 'Avg 3.8 tool calls  |  range 1-9  |  avg 100s',
         ha='center', fontsize=13, fontweight='bold', color=DBX_D)
ax2.text(5, -0.05, 'Worst: P08 = 9 tool calls, 578K tokens, 237s',
         ha='center', fontsize=10, color=SUB, fontstyle='italic')
ax2.text(5, -0.55, '50% of queries required retries or hit dead ends.',
         ha='center', fontsize=10, color=DBX_D, fontstyle='italic')

plt.tight_layout()
plt.savefig(f'{OUT}/06_architecture.png', dpi=DPI, bbox_inches='tight', facecolor=BG)
plt.close()
print('[7/8] Architecture')


# ======================================================================
# 7  SCORECARD
# ======================================================================
fig, ax = plt.subplots(figsize=(10, 8.5))
fig.patch.set_facecolor(BG)
ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,12)

ax.text(5, 11.5, 'Final Scorecard', ha='center', fontsize=34, fontweight='bold',
        color=SF_DARK, path_effects=TITLE_FX)
ax.text(5, 10.85, 'Snowflake leads on all 8 benchmark metrics', ha='center', fontsize=17, fontweight='bold', color=GREEN)

metrics = [('Accuracy','12/12 (100%)','11/12 (92%)'),('Avg Latency','37s','100s (~1.7 min)'),
           ('Max Latency','63s','237s (3m57s)'),('Token Cost','$3.28','$14.40'),
           ('Cost / Correct','$0.27','$1.31'),('Architecture','4 steps, parallel','10 steps, seq.'),
           ('Model Selection','User chooses','Platform-managed'),
           ('Business Access','CoWork (GA)','Not in Genie One')]

hy = 10.2
hdr = mpatches.FancyBboxPatch((0.2,hy-0.35),9.6,0.7,boxstyle='round,pad=0.1',
                                facecolor=SF_DARK, edgecolor='none')
ax.add_patch(hdr)
ax.text(1.3,hy,'Metric',ha='center',fontsize=15,fontweight='bold',color=WHITE)
ax.text(4.2,hy,'Snowflake',ha='center',fontsize=15,fontweight='bold',color='#93C5FD')
ax.text(6.6,hy,'Databricks',ha='center',fontsize=15,fontweight='bold',color=DBX_L)
ax.text(9.0,hy,'Winner',ha='center',fontsize=13,fontweight='bold',color=WHITE)

for i,(m,cv,dv) in enumerate(metrics):
    yy = 9.5 - i*1.02
    bg = WHITE if i%2==0 else BG
    row = mpatches.FancyBboxPatch((0.2,yy-0.4),9.6,0.8,boxstyle='round,pad=0.06',
                                    facecolor=bg,edgecolor='none')
    ax.add_patch(row)
    ax.text(1.3,yy,m,ha='center',va='center',fontsize=14,color=TEXT)
    ax.text(4.2,yy,cv,ha='center',va='center',fontsize=14,fontweight='bold',color=CORTEX_D)
    ax.text(6.6,yy,dv,ha='center',va='center',fontsize=14,fontweight='bold',color=DBX_D)
    win = mpatches.FancyBboxPatch((8.05,yy-0.22),1.9,0.44,boxstyle='round,pad=0.08',
                                    facecolor=CORTEX,edgecolor=CORTEX_D,lw=0.8)
    ax.add_patch(win)
    ax.text(9.0,yy,'Snowflake',ha='center',va='center',fontsize=10,fontweight='bold',color=WHITE)

ax.text(5,0.3,'All costs at Anthropic Claude Sonnet 4.6 published rates',
        ha='center',fontsize=11,color=SUB,fontstyle='italic')

plt.savefig(f'{OUT}/07_scorecard.png', dpi=DPI, bbox_inches='tight', facecolor=BG)
plt.close()
print('[8/8] Scorecard')


print(f'\nAll 8 charts saved to {OUT}/')
