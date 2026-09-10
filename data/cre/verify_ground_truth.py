#!/usr/bin/env python3
"""Verify ground-truth numbers for benchmark questions G01–G10."""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import date

pd.set_option("display.float_format", "{:,.2f}".format)
pd.set_option("display.max_columns", 30)
pd.set_option("display.width", 200)

BASE = Path("/Users/bsuresh/Documents/Projects/genie_cortex/data/cre/tables")

def load(name):
    df = pd.read_parquet(BASE / name)
    return df

# ── Load all tables and print columns ──────────────────────────────────────
tables = [
    "tbl_loan_mstr.parquet", "tbl_collateral.parquet", "tbl_covenant.parquet",
    "tbl_covenant_test.parquet", "tbl_workout.parquet", "tbl_concentration.parquet",
    "tbl_provision.parquet", "tbl_capital.parquet", "tbl_charge_off.parquet",
    "tbl_branch.parquet", "tbl_reo.parquet", "tbl_exam_finding.parquet",
]

dfs = {}
print("=" * 80)
print("COLUMN INSPECTION")
print("=" * 80)
for t in tables:
    df = load(t)
    dfs[t] = df
    print(f"\n{t}  ({len(df)} rows)")
    print(f"  columns: {df.columns.tolist()}")

loan = dfs["tbl_loan_mstr.parquet"]
coll = dfs["tbl_collateral.parquet"]
cov  = dfs["tbl_covenant.parquet"]
covt = dfs["tbl_covenant_test.parquet"]
wk   = dfs["tbl_workout.parquet"]
conc = dfs["tbl_concentration.parquet"]
prov = dfs["tbl_provision.parquet"]
cap  = dfs["tbl_capital.parquet"]
co   = dfs["tbl_charge_off.parquet"]
br   = dfs["tbl_branch.parquet"]
reo  = dfs["tbl_reo.parquet"]
exam = dfs["tbl_exam_finding.parquet"]

SEP = "\n" + "=" * 80

# ═══════════════════════════════════════════════════════════════════════════
# G01: CRE Office portfolio overview + concentration
# ═══════════════════════════════════════════════════════════════════════════
print(f"{SEP}\nG01: CRE Office Portfolio Overview\n{'─'*40}")

cre_offc = loan[loan["loan_typ_cd"] == "CRE_OFFC"]
print(f"CRE_OFFC total count:        {len(cre_offc)}")
print(f"CRE_OFFC total curr_bal:     ${cre_offc['curr_bal'].sum():,.2f}")

high_risk = ["5-SS", "6-SUB", "7-DBT", "8-LOSS"]
cre_hr = cre_offc[cre_offc["risk_rtg_cd"].isin(high_risk)]
print(f"High-risk count:             {len(cre_hr)}")
print(f"High-risk curr_bal sum:      ${cre_hr['curr_bal'].sum():,.2f}")
print(f"High-risk breakdown:")
print(cre_hr.groupby("risk_rtg_cd").agg(count=("loan_id","count"), bal=("curr_bal","sum")).to_string())

# Concentration
conc_sorted = conc.sort_values("report_dt")
cre_total = conc_sorted[conc_sorted["segment_cd"] == "CRE_TOTAL"]
if len(cre_total):
    latest = cre_total.iloc[-1]
    print(f"\nConcentration (latest CRE_TOTAL):")
    print(f"  report_dt:      {latest['report_dt']}")
    # Print all columns that look relevant
    for c in cre_total.columns:
        print(f"  {c}: {latest[c]}")
else:
    print("  No CRE_TOTAL rows found in tbl_concentration")

# ═══════════════════════════════════════════════════════════════════════════
# G02: Single loan deep dive CRE-2021-00847
# ═══════════════════════════════════════════════════════════════════════════
print(f"{SEP}\nG02: Loan CRE-2021-00847 Deep Dive\n{'─'*40}")

lid = "CRE-2021-00847"

# Loan master
l2 = loan[loan["loan_id"] == lid]
if len(l2):
    r = l2.iloc[0]
    for c in ["orig_amt","curr_bal","loan_sts_cd","risk_rtg_cd","int_rate","rate_typ_cd"]:
        if c in l2.columns:
            print(f"  {c}: {r[c]}")
    # print all columns for completeness
    print(f"  All columns: { {c: r[c] for c in l2.columns} }")

# Collateral
c2 = coll[coll["loan_id"] == lid]
print(f"\nCollateral ({len(c2)} rows):")
for _, r in c2.iterrows():
    for c in ["orig_appr_val","curr_appr_val","ltv_orig","ltv_curr","occup_rate","prop_typ_cd"]:
        if c in c2.columns:
            print(f"  {c}: {r[c]}")
    print()

# Covenant
cv2 = cov[cov["loan_id"] == lid]
print(f"Covenants ({len(cv2)} rows):")
for _, r in cv2.iterrows():
    for c in ["covenant_id","cov_typ_cd","threshold_val"]:
        if c in cv2.columns:
            print(f"  {c}: {r[c]}")
    print()

# Covenant tests
if len(cv2):
    cov_ids = cv2["covenant_id"].tolist()
    ct2 = covt[covt["covenant_id"].isin(cov_ids)]
    print(f"Covenant Tests ({len(ct2)} rows):")
    # Figure out pass/fail column
    pf_col = None
    for candidate in ["pass_fail_cd","test_result","result_cd"]:
        if candidate in covt.columns:
            pf_col = candidate
            break
    if pf_col:
        fail_ct = ct2[ct2[pf_col] == "FAIL"]
        print(f"  pass/fail column: {pf_col}")
        print(f"  Total tests: {len(ct2)},  FAIL: {len(fail_ct)}")
        # merge to get cov_typ_cd
        ct2m = ct2.merge(cv2[["covenant_id","cov_typ_cd"]], on="covenant_id", how="left")
        agg = ct2m.groupby("cov_typ_cd").agg(
            tests=("covenant_id","count"),
            fails=(pf_col, lambda x: (x=="FAIL").sum()),
        )
        if "actual_val" in ct2m.columns:
            agg2 = ct2m.groupby("cov_typ_cd")["actual_val"].agg(["min","max"])
            agg = agg.join(agg2)
        print(agg.to_string())
    else:
        print(f"  Could not find pass/fail column. Columns: {covt.columns.tolist()}")

# Workout
w2 = wk[wk["loan_id"] == lid]
print(f"\nWorkout ({len(w2)} rows):")
for _, r in w2.iterrows():
    for c in ["workout_typ_cd","orig_bal","modified_bal","haircut_pct","resolution_cd"]:
        if c in wk.columns:
            print(f"  {c}: {r[c]}")
    print()

# ═══════════════════════════════════════════════════════════════════════════
# G03: Provision for CRE Office
# ═══════════════════════════════════════════════════════════════════════════
print(f"{SEP}\nG03: Provision for CRE Office\n{'─'*40}")

prov_loan = prov.merge(loan[["loan_id","loan_typ_cd"]], on="loan_id", how="left")
prov_offc = prov_loan[prov_loan["loan_typ_cd"] == "CRE_OFFC"]
print(f"Sum prov_amt (CRE_OFFC): ${prov_offc['prov_amt'].sum():,.2f}")
print(f"Distinct loan_id count:  {prov_offc['loan_id'].nunique()}")
print(f"CRE_OFFC curr_bal (should match G01): ${cre_offc['curr_bal'].sum():,.2f}")

# ═══════════════════════════════════════════════════════════════════════════
# G04: DSCR covenant failures in 2023 (non-waived)
# ═══════════════════════════════════════════════════════════════════════════
print(f"{SEP}\nG04: DSCR Covenant Failures\n{'─'*40}")

# Identify pass/fail and date columns
pf_col = None
for candidate in ["pass_fail_cd","test_result","result_cd"]:
    if candidate in covt.columns:
        pf_col = candidate
        break
print(f"Pass/fail column: {pf_col}")

dt_col = None
for candidate in ["test_dt","test_date","rpt_dt"]:
    if candidate in covt.columns:
        dt_col = candidate
        break
print(f"Date column: {dt_col}")

# Identify waiver column
waiver_col = None
for candidate in ["waiver_flg","waived_flg","waiver_yn"]:
    if candidate in covt.columns:
        waiver_col = candidate
        break
print(f"Waiver column: {waiver_col}")

# Join covenant_test to covenant to get cov_typ_cd
ct_cov = covt.merge(cov[["covenant_id","cov_typ_cd","loan_id"]], on="covenant_id", how="left")
dscr = ct_cov[ct_cov["cov_typ_cd"] == "DSCR"]
print(f"Total DSCR tests: {len(dscr)}")

# Filter 2023
if dt_col:
    dscr[dt_col] = pd.to_datetime(dscr[dt_col])
    dscr_2023 = dscr[dscr[dt_col].dt.year == 2023]
    print(f"DSCR tests in 2023: {len(dscr_2023)}")
else:
    dscr_2023 = dscr
    print("WARNING: no date column found, using all DSCR tests")

# Filter FAIL + no waiver
if pf_col and waiver_col:
    fails = dscr_2023[(dscr_2023[pf_col] == "FAIL") & (dscr_2023[waiver_col] == "N")]
    print(f"DSCR 2023 FAIL + waiver=N: {len(fails)} records")
    print(f"Distinct loan_ids: {fails['loan_id'].nunique()}")
    fail_loans = fails["loan_id"].unique()

    # Sum curr_bal
    fail_loan_data = loan[loan["loan_id"].isin(fail_loans)]
    # filter to CRE loans
    cre_fail = fail_loan_data[fail_loan_data["loan_typ_cd"].str.startswith("CRE")]
    print(f"Of those, CRE loans: {len(cre_fail)}")
    print(f"Sum curr_bal: ${cre_fail['curr_bal'].sum():,.2f}")
    print(f"loan_sts_cd breakdown:")
    print(cre_fail["loan_sts_cd"].value_counts().to_string())

    # Workout count
    wk_match = wk[wk["loan_id"].isin(fail_loans)]
    print(f"Workout records for those loans: {len(wk_match)}")

    # Charge-off sum
    co_match = co[co["loan_id"].isin(fail_loans)]
    print(f"Charge-off records: {len(co_match)}")
    if "co_amt" in co.columns:
        print(f"Sum co_amt: ${co_match['co_amt'].sum():,.2f}")
elif pf_col:
    fails = dscr_2023[dscr_2023[pf_col] == "FAIL"]
    print(f"DSCR 2023 FAIL (no waiver column): {len(fails)}")

# ═══════════════════════════════════════════════════════════════════════════
# G05: Capital ratios, charge-offs, provisions
# ═══════════════════════════════════════════════════════════════════════════
print(f"{SEP}\nG05: Capital, Charge-offs, Provisions\n{'─'*40}")

cap_sorted = cap.sort_values("report_dt")
print("Capital history:")
cap_display_cols = [c for c in ["report_dt","cet1_ratio","tier1_ratio","total_ratio","rwa","leverage_ratio"] if c in cap.columns]
print(cap_sorted[cap_display_cols].to_string(index=False))

print(f"\nCharge-offs:")
if "co_amt" in co.columns:
    print(f"  Total co_amt: ${co['co_amt'].sum():,.2f}")
    # By year
    co_dt_col = None
    for candidate in ["co_dt","charge_off_dt","rpt_dt","co_date"]:
        if candidate in co.columns:
            co_dt_col = candidate
            break
    if co_dt_col:
        co_copy = co.copy()
        co_copy[co_dt_col] = pd.to_datetime(co_copy[co_dt_col])
        co_copy["year"] = co_copy[co_dt_col].dt.year
        print(co_copy.groupby("year")["co_amt"].sum().to_string())

print(f"\nProvisions:")
print(f"  Total prov_amt: ${prov['prov_amt'].sum():,.2f}")

# ═══════════════════════════════════════════════════════════════════════════
# G06: Charge-offs by property type
# ═══════════════════════════════════════════════════════════════════════════
print(f"{SEP}\nG06: Charge-offs by Property Type\n{'─'*40}")

co_loan = co.merge(loan[["loan_id","loan_typ_cd"]], on="loan_id", how="left")

# Find join key for collateral
join_key = "loan_id" if "loan_id" in coll.columns else "collateral_id"
co_coll = co_loan.merge(coll[["loan_id","prop_typ_cd"]].drop_duplicates("loan_id") if "loan_id" in coll.columns else coll, on=join_key, how="left")

rec_col = None
for candidate in ["recovery_amt","recovery_val","recovered_amt"]:
    if candidate in co.columns:
        rec_col = candidate
        break
print(f"Recovery column: {rec_col}")

if "prop_typ_cd" in co_coll.columns:
    grp = co_coll.groupby("prop_typ_cd", dropna=False)
    agg = grp.agg(count=("loan_id","count"), co_amt_sum=("co_amt","sum"))
    if rec_col and rec_col in co_coll.columns:
        agg["recovery_sum"] = grp[rec_col].sum()
        agg["net_loss"] = agg["co_amt_sum"] - agg["recovery_sum"]
    print(agg.to_string())
    null_prop = co_coll[co_coll["prop_typ_cd"].isna()]
    print(f"\nRows with NULL prop_typ_cd: {len(null_prop)}")
else:
    print("prop_typ_cd not available after join")
    print(f"co_coll columns: {co_coll.columns.tolist()}")

# ═══════════════════════════════════════════════════════════════════════════
# G07: Underwriting exceptions 2021-2022
# ═══════════════════════════════════════════════════════════════════════════
print(f"{SEP}\nG07: Underwriting Exceptions\n{'─'*40}")

# Check for uw_exception_flg column
uw_col = None
for candidate in ["uw_exception_flg","exception_flg","uw_except_flg"]:
    if candidate in loan.columns:
        uw_col = candidate
        break
print(f"UW exception column: {uw_col}")

loan_copy = loan.copy()
loan_copy["orig_dt"] = pd.to_datetime(loan_copy["orig_dt"])
cre_all = loan_copy[loan_copy["loan_typ_cd"].str.startswith("CRE")]
cre_2122 = cre_all[cre_all["orig_dt"].dt.year.isin([2021, 2022])]
print(f"CRE loans originated 2021-2022: {len(cre_2122)}")

if uw_col:
    exceptions = cre_2122[cre_2122[uw_col] == "Y"]
    print(f"With exception=Y: {len(exceptions)}")
    print(f"Exception rate: {len(exceptions)/len(cre_2122)*100:.1f}%")

    # Branch breakdown
    branch_col = None
    branch_col = "branch_cd" if "branch_cd" in loan.columns else None
    if branch_col:
        br_exc = cre_2122.groupby(branch_col).agg(
            total=("loan_id","count"),
            exceptions=(uw_col, lambda x: (x=="Y").sum())
        )
        br_exc["exc_rate"] = br_exc["exceptions"] / br_exc["total"]
        br_exc = br_exc.sort_values("exc_rate", ascending=False)
        # Join branch name
        br_exc = br_exc.reset_index().merge(br[["branch_cd","branch_nm"]].drop_duplicates(), on="branch_cd", how="left")
        br_exc = br_exc.sort_values("exc_rate", ascending=False)
        print(f"\nTop 5 branches by exception rate:")
        print(br_exc.head(5).to_string(index=False))

# ═══════════════════════════════════════════════════════════════════════════
# G08: REO analysis
# ═══════════════════════════════════════════════════════════════════════════
print(f"{SEP}\nG08: REO Analysis\n{'─'*40}")

print(f"Total REO count: {len(reo)}")
print(f"REO columns: {reo.columns.tolist()}")

# sale_dt
sale_col = None
for candidate in ["sale_dt","sold_dt","disposition_dt"]:
    if candidate in reo.columns:
        sale_col = candidate
        break
print(f"Sale date column: {sale_col}")

acq_col = None
for candidate in ["acq_dt","acquisition_dt","reo_dt"]:
    if candidate in reo.columns:
        acq_col = candidate
        break
print(f"Acquisition date column: {acq_col}")

if sale_col:
    sold = reo[reo[sale_col].notna()]
    unsold = reo[reo[sale_col].isna()]
    print(f"Sold (sale_dt not null): {len(sold)}")
    print(f"Unsold (sale_dt null):   {len(unsold)}")

# carrying_cost
cc_col = None
for candidate in ["carrying_cost","carry_cost","holding_cost"]:
    if candidate in reo.columns:
        cc_col = candidate
        break
if cc_col:
    print(f"Sum carrying_cost: ${reo[cc_col].sum():,.2f}")

# Days held
if sale_col and acq_col:
    reo_copy = reo.copy()
    reo_copy[acq_col] = pd.to_datetime(reo_copy[acq_col])
    reo_copy[sale_col] = pd.to_datetime(reo_copy[sale_col])
    today = pd.Timestamp("2026-09-09")

    sold_reo = reo_copy[reo_copy[sale_col].notna()]
    unsold_reo = reo_copy[reo_copy[sale_col].isna()]

    if len(sold_reo):
        sold_reo = sold_reo.copy()
        sold_reo["days_held"] = (sold_reo[sale_col] - sold_reo[acq_col]).dt.days
        print(f"Avg days held (sold): {sold_reo['days_held'].mean():.1f}")

    if len(unsold_reo):
        unsold_reo = unsold_reo.copy()
        unsold_reo["days_held"] = (today - unsold_reo[acq_col]).dt.days
        print(f"Avg days held (unsold, as of 2026-09-09): {unsold_reo['days_held'].mean():.1f}")

# Loss on sold REOs
sale_val_col = None
for candidate in ["sale_val","sale_price","disposition_amt","sale_amt"]:
    if candidate in reo.columns:
        sale_val_col = candidate
        break
acq_val_col = None
for candidate in ["acq_val","acq_cost","acquisition_val","book_val"]:
    if candidate in reo.columns:
        acq_val_col = candidate
        break

if sale_val_col and acq_val_col and cc_col and sale_col:
    sold_reo2 = reo[reo[sale_col].notna()].copy()
    sold_reo2["loss"] = sold_reo2[sale_val_col] - sold_reo2[acq_val_col] - sold_reo2[cc_col]
    worst = sold_reo2.loc[sold_reo2["loss"].idxmin()]
    print(f"\nWorst loss on sold REO:")
    for c in reo.columns.tolist() + ["loss"]:
        if c in sold_reo2.columns:
            print(f"  {c}: {worst[c]}")

    # Unsold exposure
    unsold_reo2 = reo[reo[sale_col].isna()].copy()
    unsold_exposure = (unsold_reo2[acq_val_col] + unsold_reo2[cc_col]).sum()
    print(f"\nUnsold REO exposure (acq_val + carrying_cost): ${unsold_exposure:,.2f}")

# ═══════════════════════════════════════════════════════════════════════════
# G09: Exam findings - open MRIAs
# ═══════════════════════════════════════════════════════════════════════════
print(f"{SEP}\nG09: Exam Findings (Open MRIAs)\n{'─'*40}")

print(f"Exam columns: {exam.columns.tolist()}")

# Check available values
for c in ["severity_cd","exam_typ_cd","remediation_sts_cd","category_cd"]:
    if c in exam.columns:
        print(f"  {c} values: {exam[c].unique().tolist()}")

sev_col = None
for candidate in ["severity_cd","severity","finding_severity"]:
    if candidate in exam.columns:
        sev_col = candidate
        break

exam_typ_col = None
for candidate in ["exam_typ_cd","exam_type","exam_cd"]:
    if candidate in exam.columns:
        exam_typ_col = candidate
        break

rem_col = None
for candidate in ["remediation_sts_cd","remediation_status","status_cd"]:
    if candidate in exam.columns:
        rem_col = candidate
        break

cat_col = None
for candidate in ["category_cd","finding_category","category"]:
    if candidate in exam.columns:
        cat_col = candidate
        break

due_col = None
for candidate in ["due_dt","due_date","target_dt","remediation_dt"]:
    if candidate in exam.columns:
        due_col = candidate
        break

print(f"Using: severity={sev_col}, exam_typ={exam_typ_col}, rem_sts={rem_col}, cat={cat_col}, due={due_col}")

if sev_col and exam_typ_col and rem_col:
    filt = exam[
        (exam[sev_col] == "MRIA") &
        (exam[exam_typ_col].isin(["OCC_FULL","OCC_TARG"])) &
        (exam[rem_col].isin(["OPEN","IN_PROGRESS"]))
    ]
    print(f"\nOpen/In-Progress MRIAs from OCC exams: {len(filt)}")
    if rem_col:
        print(f"By remediation status:")
        print(filt[rem_col].value_counts().to_string())
    if cat_col:
        print(f"By category:")
        print(filt[cat_col].value_counts().to_string())
    if due_col:
        filt_copy = filt.copy()
        filt_copy[due_col] = pd.to_datetime(filt_copy[due_col])
        overdue = filt_copy[filt_copy[due_col] < pd.Timestamp("2026-09-09")]
        print(f"Overdue (due_dt < 2026-09-09): {len(overdue)}")

# ═══════════════════════════════════════════════════════════════════════════
# G10: Capital adequacy
# ═══════════════════════════════════════════════════════════════════════════
print(f"{SEP}\nG10: Capital Adequacy\n{'─'*40}")

cap_sorted = cap.sort_values("report_dt")
latest_cap = cap_sorted.iloc[-1]
print(f"Latest capital row (report_dt={latest_cap['report_dt']}):")
for c in cap.columns:
    print(f"  {c}: {latest_cap[c]}")

if "cet1_ratio" in cap.columns and "rwa" in cap.columns:
    cet1_r = latest_cap["cet1_ratio"]
    rwa_val = latest_cap["rwa"]
    # cet1_ratio might be stored as pct (e.g. 10.5) or decimal (0.105)
    if cet1_r > 1:
        cet1_capital = (cet1_r / 100) * rwa_val
        print(f"\n  CET1 capital = ({cet1_r}/100) * {rwa_val:,.2f} = ${cet1_capital:,.2f}")
    else:
        cet1_capital = cet1_r * rwa_val
        print(f"\n  CET1 capital = {cet1_r} * {rwa_val:,.2f} = ${cet1_capital:,.2f}")

print(f"\n{'='*80}")
print("VERIFICATION COMPLETE")
print(f"{'='*80}")
