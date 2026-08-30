"""
Legal Benchmark - Coherent Table Generator
Embeds the specific entities from universe.py into the tables alongside noise data.
The key case (SEC v. Meridian Capital) and all its parties, events, rulings,
and settlement are EXPLICITLY present in the data.
"""

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta, date
import random
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from universe import (CASE, CRIMINAL_CASE, CLASS_ACTION, PARTIES, ATTORNEYS,
                      TIMELINE, FINANCIALS, STATUTES, DOCUMENTS)

fake = Faker()
Faker.seed(501)
np.random.seed(501)
random.seed(501)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "legal", "tables")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save(df, name):
    path = os.path.join(OUTPUT_DIR, f"{name}.parquet")
    df.to_parquet(path, index=False)
    print(f"  {name}: {len(df)} rows")
    return df

# Helper
def d(s): return datetime.strptime(s, "%Y-%m-%d").date() if isinstance(s, str) else s

JRSD = ["SDNY","CDCA","NDIL","EDPA","SDTX","DDC","NDGA","DMA","EDVA","SDFL"]
CASE_TYPES = ["CIV","CRM","BKR","ADM","APP"]
CASE_STS = ["OPN","CLS","STL","DSM","APL"]
PTY_ROLES = ["PLF","DEF","WIT","INT","AMC","TPD"]
EVT_TYPES = ["MTN","HRG","ORD","BRF","JDG","DSC","STL","TRL","APL"]
RULING_CDS = ["GRT","DNY","PART","MOT","DFRD","WDRN"]
MTN_TYPES = ["MTD","MSJ","MTC","MIL","MPC","MSL","MCV"]
CLAIM_TYPES = ["NEG","BRC","FRD","SEC10B","ANT","INF","EMP","ENV","RICO","DFM"]
DMG_TYPES = ["CMP","PNT","STT","NOM","LQD","TRB","ATF","INJ"]
DISP_CDS = ["AFM","REV","RMD","DISM","VACATE"]
STL_TERMS = ["CSH","STK","INJ","MON","ADM","NDL","CPN"]


# =============================================================================
# 1. TBL_CASE_MSTR — 50K cases (3 key cases + 49,997 noise)
# =============================================================================
def gen_cases():
    rows = []
    # Insert the 3 key cases
    rows.append({
        "docket_no": CASE["docket_no"], "filing_dt": d(CASE["filing_date"]),
        "case_typ_cd": "CIV", "jrsd_cd": "SDNY", "judge_id": CASE["judge_id"],
        "case_sts_cd": "STL", "cls_dt": d("2025-02-28"),
        "nat_suit_cd": "850", "jury_dmnd_flg": "N",
        "class_actn_flg": "N", "consol_flg": "N",
        "related_case_no": CRIMINAL_CASE["docket_no"],
        "amt_in_controversy": 412000000,
    })
    rows.append({
        "docket_no": CRIMINAL_CASE["docket_no"], "filing_dt": d(CRIMINAL_CASE["filing_date"]),
        "case_typ_cd": "CRM", "jrsd_cd": "SDNY", "judge_id": CRIMINAL_CASE["judge_id"],
        "case_sts_cd": "CLS", "cls_dt": d("2025-03-20"),
        "nat_suit_cd": "470", "jury_dmnd_flg": "N",
        "class_actn_flg": "N", "consol_flg": "N",
        "related_case_no": CASE["docket_no"],
        "amt_in_controversy": None,
    })
    rows.append({
        "docket_no": CLASS_ACTION["docket_no"], "filing_dt": d(CLASS_ACTION["filing_date"]),
        "case_typ_cd": "CIV", "jrsd_cd": "SDNY", "judge_id": CLASS_ACTION["judge_id"],
        "case_sts_cd": "STL", "cls_dt": d("2025-02-28"),
        "nat_suit_cd": "850", "jury_dmnd_flg": "Y",
        "class_actn_flg": "Y", "consol_flg": "Y",
        "related_case_no": CASE["docket_no"],
        "amt_in_controversy": 347500000,
    })
    # Noise cases
    for i in range(49997):
        jrsd = random.choice(JRSD)
        typ = random.choice(CASE_TYPES)
        fd = fake.date_between(start_date="-10y", end_date="today")
        rows.append({
            "docket_no": f"{jrsd}-{fd.year}-{typ}-{i+4:05d}",
            "filing_dt": fd, "case_typ_cd": typ, "jrsd_cd": jrsd,
            "judge_id": f"JDG-{random.randint(1,200):04d}",
            "case_sts_cd": random.choice(CASE_STS),
            "cls_dt": fd + timedelta(days=random.randint(90,2000)) if random.random()>0.3 else None,
            "nat_suit_cd": f"{random.randint(100,999)}",
            "jury_dmnd_flg": random.choice(["Y","N"]),
            "class_actn_flg": random.choice(["Y","N","N","N"]),
            "consol_flg": random.choice(["Y","N","N","N","N"]),
            "related_case_no": None,
            "amt_in_controversy": random.choice([None,75000,500000,5000000,50000000]) if typ=="CIV" else None,
        })
    return save(pd.DataFrame(rows), "tbl_case_mstr")


# =============================================================================
# 2. TBL_PTY_INFO — 150K parties (10 key + 149,990 noise)
# =============================================================================
def gen_parties():
    rows = []
    for key, p in PARTIES.items():
        rows.append({
            "pty_id": p["id"], "pty_nm": p["name"], "pty_typ_cd": p["type"],
            "pty_addr_st": p["state"], "pty_addr_ctry": p["country"],
            "ein_ssn_msk": fake.bothify("***-**-####"),
            "sic_cd": p.get("sic"), "pub_co_flg": "Y" if p.get("public") else "N",
        })
    for i in range(149990):
        typ = random.choice(["IND","IND","ORG","ORG","GOV","TRT"])
        rows.append({
            "pty_id": f"PTY-{i+11:07d}",
            "pty_nm": fake.name() if typ=="IND" else fake.company()+" "+random.choice(["Inc.","LLC","Corp.","LP"]),
            "pty_typ_cd": typ, "pty_addr_st": fake.state_abbr(),
            "pty_addr_ctry": random.choice(["US"]*8+["GB","DE"]),
            "ein_ssn_msk": fake.bothify("***-**-####"),
            "sic_cd": f"{random.randint(1000,9999)}" if typ=="ORG" else None,
            "pub_co_flg": random.choice(["Y","N"]) if typ=="ORG" else "N",
        })
    return save(pd.DataFrame(rows), "tbl_pty_info")


# =============================================================================
# 3. TBL_ATTY_REG — 5K attorneys (5 key + 4995 noise)
# =============================================================================
def gen_attorneys():
    rows = []
    for key, a in ATTORNEYS.items():
        rows.append({
            "atty_id": a["id"], "atty_nm": a["name"], "bar_no": fake.bothify("######"),
            "bar_st_cd": a["bar_state"], "firm_nm": a["firm"],
            "jrsd_cd": "SDNY", "spec_cd": a["specialty"],
            "adm_dt": fake.date_between(start_date="-20y", end_date="-5y"),
            "sts_cd": "ACT", "pro_hac_flg": "N",
        })
    for i in range(4995):
        rows.append({
            "atty_id": f"ATY-{i+6:05d}", "atty_nm": fake.name(),
            "bar_no": fake.bothify("######"), "bar_st_cd": fake.state_abbr(),
            "firm_nm": fake.company()+" "+random.choice(["LLP","PC","& Associates"]),
            "jrsd_cd": random.choice(JRSD),
            "spec_cd": random.choice(["SEC","IP","ANT","EMP","ENV","TAX","BKR","CRM","CRA","MNA"]),
            "adm_dt": fake.date_between(start_date="-30y",end_date="-2y"),
            "sts_cd": random.choice(["ACT"]*8+["SUS","RET","DIS"]),
            "pro_hac_flg": random.choice(["Y","N","N","N"]),
        })
    return save(pd.DataFrame(rows), "tbl_atty_reg")


# =============================================================================
# 4. TBL_CASE_PTY_ATTY — 200K (key relationships + noise)
# =============================================================================
def gen_case_pty_atty(cases_df, parties_df, attorneys_df):
    rows = []
    # Key relationships for SEC v. Meridian
    key_links = [
        (CASE["docket_no"], "PTY-0000007", "ATY-00003", "PLF", "Y"),  # SEC + enforcement atty
        (CASE["docket_no"], "PTY-0000001", "ATY-00001", "DEF", "Y"),  # Meridian + defense
        (CASE["docket_no"], "PTY-0000002", "ATY-00001", "DEF", "N"),  # Hartwell + defense
        (CASE["docket_no"], "PTY-0000003", "ATY-00005", "WIT", "Y"),  # Chen + her counsel
        (CASE["docket_no"], "PTY-0000006", "ATY-00001", "DEF", "N"),  # Pacific Growth
        (CASE["docket_no"], "PTY-0000010", "ATY-00001", "DEF", "N"),  # Zhang
        (CLASS_ACTION["docket_no"], "PTY-0000008", "ATY-00004", "PLF", "Y"),  # Thornton + class counsel
        (CLASS_ACTION["docket_no"], "PTY-0000001", "ATY-00001", "DEF", "Y"),  # Meridian + defense
        (CRIMINAL_CASE["docket_no"], "PTY-0000009", "ATY-00003", "PLF", "Y"),  # DOJ
        (CRIMINAL_CASE["docket_no"], "PTY-0000002", "ATY-00002", "DEF", "Y"),  # Hartwell + criminal counsel
    ]
    for i, (dk, pty, atty, role, lead) in enumerate(key_links):
        rows.append({
            "cpa_id": i+1, "docket_no": dk, "pty_id": pty, "atty_id": atty,
            "pty_role_cd": role, "lead_counsel_flg": lead, "pro_se_flg": "N",
            "dt_entered": d(CASE["filing_date"]), "dt_withdrawn": None,
        })
    # Noise
    case_ids = cases_df["docket_no"].tolist()
    pty_ids = parties_df["pty_id"].tolist()
    atty_ids = attorneys_df["atty_id"].tolist()
    for i in range(199990):
        rows.append({
            "cpa_id": i+11, "docket_no": random.choice(case_ids),
            "pty_id": random.choice(pty_ids), "atty_id": random.choice(atty_ids),
            "pty_role_cd": random.choice(PTY_ROLES), "lead_counsel_flg": random.choice(["Y","N","N"]),
            "pro_se_flg": random.choice(["Y","N","N","N","N"]),
            "dt_entered": fake.date_between(start_date="-10y",end_date="today"),
            "dt_withdrawn": fake.date_between(start_date="-3y",end_date="today") if random.random()<0.1 else None,
        })
    return save(pd.DataFrame(rows), "tbl_case_pty_atty")


# =============================================================================
# 5. TBL_EVT_LOG — 500K (key events for our case + noise)
# =============================================================================
def gen_events(cases_df):
    rows = []
    # Key events for SEC v. Meridian (matching TIMELINE)
    key_events = [
        (CASE["docket_no"], TIMELINE["sec_complaint_filed"], "BRF", "PLF", "SEC files complaint against Meridian Capital Group LLC, Robert Hartwell, and Pacific Growth Partners"),
        (CASE["docket_no"], TIMELINE["motion_to_dismiss_filed"], "MTN", "DEF", "Defendants Motion to Dismiss pursuant to Fed.R.Civ.P. 12(b)(6)"),
        (CASE["docket_no"], TIMELINE["motion_to_dismiss_denied"], "ORD", "CRT", "ORDER: Defendants Motion to Dismiss is DENIED"),
        (CASE["docket_no"], TIMELINE["chen_deposition"], "DSC", "PLF", "Deposition of Sarah M. Chen, former CFO of Meridian Capital"),
        (CASE["docket_no"], TIMELINE["expert_report_filed"], "BRF", "PLF", "Expert Report of Dr. James R. Patterson filed - Damages calculation of $412 million"),
        (CASE["docket_no"], TIMELINE["summary_judgment_motion"], "MTN", "PLF", "SEC Motion for Summary Judgment"),
        (CASE["docket_no"], TIMELINE["summary_judgment_denied"], "ORD", "CRT", "ORDER: Motion for Summary Judgment DENIED - genuine issues of material fact remain"),
        (CASE["docket_no"], TIMELINE["settlement_reached"], "STL", "CRT", "Settlement conference - parties reach agreement in principle for $347.5 million"),
        (CLASS_ACTION["docket_no"], "2023-01-18", "BRF", "PLF", "Class Action Complaint filed by Thornton Pension Fund"),
        (CLASS_ACTION["docket_no"], TIMELINE["class_certification_motion"], "MTN", "PLF", "Motion for Class Certification pursuant to Fed.R.Civ.P. 23"),
        (CLASS_ACTION["docket_no"], TIMELINE["class_certification_granted"], "ORD", "CRT", "ORDER: Class Certification GRANTED - class of 23,847 investors"),
        (CLASS_ACTION["docket_no"], TIMELINE["settlement_preliminary_approval"], "ORD", "CRT", "ORDER: Preliminary Approval of $347.5 million class settlement"),
        (CLASS_ACTION["docket_no"], TIMELINE["settlement_final_approval"], "ORD", "CRT", "ORDER: Final Approval of Settlement - opt-out deadline December 15, 2024"),
        (CRIMINAL_CASE["docket_no"], TIMELINE["criminal_indictment"], "BRF", "PLF", "Indictment: Wire fraud and securities fraud charges against Robert J. Hartwell"),
        (CRIMINAL_CASE["docket_no"], TIMELINE["hartwell_plea_agreement"], "STL", "DEF", "Plea Agreement - Hartwell agrees to plead guilty to one count wire fraud"),
        (CRIMINAL_CASE["docket_no"], TIMELINE["hartwell_sentencing"], "JDG", "CRT", "JUDGMENT: Defendant sentenced to 84 months imprisonment, $42M forfeiture, $89.7M restitution"),
    ]
    for i, (dk, dt, typ, by, desc) in enumerate(key_events):
        rows.append({
            "evt_id": f"EVT-{i+1:08d}", "docket_no": dk, "evt_dt": d(dt),
            "evt_typ_cd": typ, "evt_desc_txt": desc, "filed_by_cd": by,
            "rsp_due_dt": d(dt)+timedelta(days=21) if typ=="MTN" else None,
            "sealed_flg": "N", "elec_filing_flg": "Y", "pg_cnt": random.randint(5,200),
        })
    # Noise events
    case_ids = cases_df["docket_no"].tolist()
    for i in range(500000-len(key_events)):
        rows.append({
            "evt_id": f"EVT-{i+len(key_events)+1:08d}", "docket_no": random.choice(case_ids),
            "evt_dt": fake.date_between(start_date="-10y",end_date="today"),
            "evt_typ_cd": random.choice(EVT_TYPES),
            "evt_desc_txt": fake.sentence(nb_words=random.randint(5,15)),
            "filed_by_cd": random.choice(["PLF","DEF","CRT","TPD","INT"]),
            "rsp_due_dt": fake.date_between(start_date="-9y",end_date="+1y") if random.random()>0.5 else None,
            "sealed_flg": random.choice(["Y","N","N","N","N","N"]),
            "elec_filing_flg": random.choice(["Y","Y","Y","N"]),
            "pg_cnt": random.randint(1,500) if random.random()>0.3 else None,
        })
    return save(pd.DataFrame(rows), "tbl_evt_log")


# =============================================================================
# 6-12: Remaining tables (abbreviated for space — same pattern)
# =============================================================================
def gen_doc_ref(cases_df):
    rows = []
    # Key docs
    key_docs = [
        (CASE["docket_no"], "CMP", "Complaint: SEC v. Meridian Capital Group LLC et al.", "2022-06-15", 87),
        (CASE["docket_no"], "MTD", "Defendants Motion to Dismiss", "2022-09-15", 45),
        (CASE["docket_no"], "BRF", "Opposition to Motion to Dismiss", "2022-10-30", 62),
        (CASE["docket_no"], "ORD", "Order Denying Motion to Dismiss", "2023-01-08", 38),
        (CASE["docket_no"], "EXH", "Expert Report - Dr. Patterson Damages Calculation", "2023-08-20", 156),
        (CASE["docket_no"], "STL", "Settlement Agreement - $347.5 Million", "2024-08-01", 234),
        (CASE["docket_no"], "DEC", "Declaration of Sarah M. Chen in Support of Settlement", "2024-08-01", 23),
        (CLASS_ACTION["docket_no"], "CMP", "Class Action Complaint - Thornton Pension Fund v. Meridian", "2023-01-18", 112),
        (CLASS_ACTION["docket_no"], "ORD", "Order Granting Class Certification", "2023-09-15", 42),
    ]
    for i, (dk, typ, title, dt, pgs) in enumerate(key_docs):
        rows.append({
            "doc_id": f"DOC-{i+1:08d}", "docket_no": dk, "doc_typ_cd": typ,
            "doc_title_txt": title, "filed_dt": d(dt), "pg_cnt": pgs,
            "seal_flg": "N", "doc_seq_no": i+1, "att_cnt": random.randint(0,5),
            "file_sz_kb": pgs*50, "ocr_flg": "N",
        })
    # Noise
    case_ids = cases_df["docket_no"].tolist()
    for i in range(299991):
        rows.append({
            "doc_id": f"DOC-{i+10:08d}", "docket_no": random.choice(case_ids),
            "doc_typ_cd": random.choice(["CMP","ANS","MTD","MSJ","BRF","EXH","DEC","ORD","JDG","STL"]),
            "doc_title_txt": fake.sentence(nb_words=random.randint(3,10)),
            "filed_dt": fake.date_between(start_date="-10y",end_date="today"),
            "pg_cnt": random.randint(1,500), "seal_flg": random.choice(["Y","N","N","N","N"]),
            "doc_seq_no": random.randint(1,500), "att_cnt": random.randint(0,20),
            "file_sz_kb": random.randint(10,50000), "ocr_flg": random.choice(["Y","N","N"]),
        })
    return save(pd.DataFrame(rows), "tbl_doc_ref")


def gen_rulings(cases_df):
    rows = []
    # Key rulings
    key_rulings = [
        (CASE["docket_no"], TIMELINE["motion_to_dismiss_denied"], "DNY", "MTD", CASE["judge_id"],
         "SEC adequately pleaded scienter through trading pattern. Motion DENIED.", "Tellabs, Inc. v. Makor Issues & Rights, Ltd."),
        (CASE["docket_no"], TIMELINE["summary_judgment_denied"], "DNY", "MSJ", CASE["judge_id"],
         "Genuine issues of material fact remain regarding defendants knowledge. DENIED.", "Celotex v. Catrett"),
        (CLASS_ACTION["docket_no"], TIMELINE["class_certification_granted"], "GRT", "MCV", CLASS_ACTION["judge_id"],
         "Class of 23,847 investors certified. Numerosity, commonality, typicality, adequacy all satisfied under Rule 23(a).", None),
    ]
    for i, (dk, dt, cd, mtn, jdg, txt, prec) in enumerate(key_rulings):
        rows.append({
            "ruling_id": f"RUL-{i+1:07d}", "docket_no": dk, "ruling_dt": d(dt),
            "ruling_cd": cd, "mtn_typ_cd": mtn, "judge_id": jdg,
            "reasoning_txt": txt, "precedent_cited": prec, "pub_flg": "Y", "slip_op_no": None,
        })
    # Noise
    case_ids = cases_df["docket_no"].tolist()
    for i in range(99997):
        rows.append({
            "ruling_id": f"RUL-{i+4:07d}", "docket_no": random.choice(case_ids),
            "ruling_dt": fake.date_between(start_date="-10y",end_date="today"),
            "ruling_cd": random.choice(RULING_CDS), "mtn_typ_cd": random.choice(MTN_TYPES),
            "judge_id": f"JDG-{random.randint(1,200):04d}",
            "reasoning_txt": fake.paragraph(nb_sentences=random.randint(2,5)),
            "precedent_cited": random.choice([None,None,"Chevron v. NRDC","Erie v. Tompkins","Iqbal v. Ashcroft","Twombly v. Bell Atlantic"]),
            "pub_flg": random.choice(["Y","N"]), "slip_op_no": None,
        })
    return save(pd.DataFrame(rows), "tbl_ruling")


def gen_statute_cite(rulings_df):
    rows = []
    # Key citations for our case
    key_cites = [
        ("RUL-0000001", "15 USC 78j(b)", "PRI"),
        ("RUL-0000001", "17 CFR 240.10b-5", "PRI"),
        ("RUL-0000001", "Fed.R.Civ.P. 12(b)(6)", "PRI"),
        ("RUL-0000002", "Fed.R.Civ.P. 56", "PRI"),
        ("RUL-0000003", "Fed.R.Civ.P. 23", "PRI"),
    ]
    for i, (rid, ref, typ) in enumerate(key_cites):
        rows.append({"cite_id": i+1, "ruling_id": rid, "statute_ref": ref, "cite_typ_cd": typ, "pin_cite_txt": None})
    # Noise
    ruling_ids = rulings_df["ruling_id"].tolist()
    statutes = ["15 USC 78j(b)","17 CFR 240.10b-5","28 USC 1332","42 USC 1983","Fed.R.Civ.P. 12(b)(6)","Fed.R.Civ.P. 56","Fed.R.Civ.P. 23","35 USC 271","15 USC 1","18 USC 1961"]
    for i in range(199995):
        rows.append({
            "cite_id": i+6, "ruling_id": random.choice(ruling_ids),
            "statute_ref": random.choice(statutes),
            "cite_typ_cd": random.choice(["PRI","SEC","DIS","OVR"]),
            "pin_cite_txt": f"at {random.randint(1,2000)}" if random.random()>0.5 else None,
        })
    return save(pd.DataFrame(rows), "tbl_statute_cite")


def gen_claims(cases_df):
    rows = []
    # Key claims
    key_claims = [
        (CASE["docket_no"], "SEC10B", 1, "ACT", "2022-06-15", "15 USC 78j(b)"),
        (CASE["docket_no"], "FRD", 2, "ACT", "2022-06-15", "18 USC 1343"),
        (CLASS_ACTION["docket_no"], "SEC10B", 1, "STL", "2023-01-18", "15 USC 78j(b)"),
        (CRIMINAL_CASE["docket_no"], "FRD", 1, "JDG", "2022-08-03", "18 USC 1343"),
    ]
    for i, (dk, typ, num, sts, dt, stat) in enumerate(key_claims):
        rows.append({
            "claim_id": f"CLM-{i+1:07d}", "docket_no": dk, "claim_typ_cd": typ,
            "claim_no": num, "sts_cd": sts, "filed_dt": d(dt), "dsm_dt": None,
            "statute_basis": stat, "class_cert_flg": "Y" if dk==CLASS_ACTION["docket_no"] else "N",
        })
    # Noise
    case_ids = cases_df["docket_no"].tolist()
    for i in range(79996):
        rows.append({
            "claim_id": f"CLM-{i+5:07d}", "docket_no": random.choice(case_ids),
            "claim_typ_cd": random.choice(CLAIM_TYPES), "claim_no": random.randint(1,10),
            "sts_cd": random.choice(["ACT","DSM","STL","JDG","WDRN"]),
            "filed_dt": fake.date_between(start_date="-10y",end_date="today"),
            "dsm_dt": fake.date_between(start_date="-5y",end_date="today") if random.random()<0.3 else None,
            "statute_basis": random.choice(["15 USC 78j(b)","42 USC 1983","35 USC 271","15 USC 1",None]),
            "class_cert_flg": random.choice(["Y","N","N","N"]),
        })
    return save(pd.DataFrame(rows), "tbl_claim")


def gen_damages(claims_df):
    rows = []
    # Key damages
    key_dmg = [
        ("CLM-0000001", "STT", FINANCIALS["class_damages_estimated"], FINANCIALS["meridian_illegal_profits"], "USD"),
        ("CLM-0000001", "PNT", 50000000, 15000000, "USD"),
        ("CLM-0000003", "CMP", FINANCIALS["class_damages_estimated"], FINANCIALS["settlement_amount"], "USD"),
        ("CLM-0000003", "ATF", FINANCIALS["attorney_fees_amount"], FINANCIALS["attorney_fees_amount"], "USD"),
    ]
    for i, (cid, typ, sought, awarded, curr) in enumerate(key_dmg):
        rows.append({
            "dmg_id": i+1, "claim_id": cid, "dmg_typ_cd": typ,
            "amt_sought": sought, "amt_awarded": awarded, "curr_cd": curr,
            "pre_jdg_int_flg": "Y", "mult_cd": None,
        })
    # Noise
    claim_ids = claims_df["claim_id"].tolist()
    for i in range(59996):
        rows.append({
            "dmg_id": i+5, "claim_id": random.choice(claim_ids),
            "dmg_typ_cd": random.choice(DMG_TYPES),
            "amt_sought": round(random.uniform(10000,500000000),2) if random.random()>0.1 else None,
            "amt_awarded": round(random.uniform(0,200000000),2) if random.random()<0.3 else None,
            "curr_cd": "USD", "pre_jdg_int_flg": random.choice(["Y","N"]),
            "mult_cd": random.choice([None,None,None,"2X","3X"]),
        })
    return save(pd.DataFrame(rows), "tbl_damages")


def gen_appeals(cases_df):
    rows = []
    # No appeal for our key case (settled), but add one related
    # Noise
    case_ids = cases_df["docket_no"].tolist()
    for i in range(20000):
        fd = fake.date_between(start_date="-8y",end_date="-6m")
        rows.append({
            "appeal_id": f"APL-{i+1:06d}", "orig_docket_no": random.choice(case_ids),
            "appeal_docket_no": f"APP-{random.choice(['2dCir','9thCir','3dCir','5thCir','DCCir'])}-{fd.year}-{i+1:05d}",
            "circuit_cd": random.choice(["2d Cir.","3d Cir.","5th Cir.","9th Cir.","D.C. Cir."]),
            "panel_judges": ",".join([f"JDG-{random.randint(1,200):04d}" for _ in range(3)]),
            "filed_dt": fd,
            "oral_arg_dt": fd+timedelta(days=random.randint(90,365)) if random.random()>0.3 else None,
            "decision_dt": fd+timedelta(days=random.randint(180,730)) if random.random()>0.4 else None,
            "disposition_cd": random.choice(DISP_CDS) if random.random()>0.4 else None,
            "en_banc_flg": random.choice(["Y","N","N","N","N"]),
            "cert_petition_flg": random.choice(["Y","N","N","N"]),
        })
    return save(pd.DataFrame(rows), "tbl_appeal")


def gen_settlements(cases_df):
    rows = []
    # THE key settlement
    rows.append({
        "stl_id": "STL-000001", "docket_no": CLASS_ACTION["docket_no"],
        "stl_dt": d(TIMELINE["settlement_reached"]),
        "stl_amt": FINANCIALS["settlement_amount"],
        "stl_terms_cd": "CSH", "conf_flg": "N", "ct_approval_flg": "Y",
        "opt_out_cnt": 342, "class_sz": CLASS_ACTION["estimated_class_size"],
        "atty_fee_pct": FINANCIALS["attorney_fees_pct"],
        "fund_admin": "Epiq Class Action & Claims Solutions",
    })
    # Noise
    case_ids = cases_df["docket_no"].tolist()
    for i in range(29999):
        rows.append({
            "stl_id": f"STL-{i+2:06d}", "docket_no": random.choice(case_ids),
            "stl_dt": fake.date_between(start_date="-8y",end_date="today"),
            "stl_amt": round(random.uniform(10000,1000000000),2),
            "stl_terms_cd": random.choice(STL_TERMS),
            "conf_flg": random.choice(["Y","Y","N"]),
            "ct_approval_flg": random.choice(["Y","N"]),
            "opt_out_cnt": random.randint(0,5000) if random.random()<0.3 else None,
            "class_sz": random.randint(100,5000000) if random.random()<0.3 else None,
            "atty_fee_pct": round(random.uniform(15,40),1) if random.random()>0.5 else None,
            "fund_admin": fake.company()+" Claims Admin" if random.random()>0.5 else None,
        })
    return save(pd.DataFrame(rows), "tbl_settlement")


# =============================================================================
# MAIN
# =============================================================================
def main():
    print("="*60)
    print("COHERENT LEGAL BENCHMARK — TABLE GENERATOR")
    print("All key entities from universe.py embedded in data")
    print("="*60)
    print()
    
    print("[1/12] tbl_case_mstr (3 key cases + noise)...")
    cases = gen_cases()
    print("[2/12] tbl_pty_info (10 key parties + noise)...")
    parties = gen_parties()
    print("[3/12] tbl_atty_reg (5 key attorneys + noise)...")
    attorneys = gen_attorneys()
    print("[4/12] tbl_case_pty_atty (key relationships + noise)...")
    gen_case_pty_atty(cases, parties, attorneys)
    print("[5/12] tbl_evt_log (16 key events + noise)...")
    gen_events(cases)
    print("[6/12] tbl_doc_ref (9 key docs + noise)...")
    gen_doc_ref(cases)
    print("[7/12] tbl_ruling (3 key rulings + noise)...")
    rulings = gen_rulings(cases)
    print("[8/12] tbl_statute_cite (5 key cites + noise)...")
    gen_statute_cite(rulings)
    print("[9/12] tbl_claim (4 key claims + noise)...")
    claims = gen_claims(cases)
    print("[10/12] tbl_damages (4 key damages + noise)...")
    gen_damages(claims)
    print("[11/12] tbl_appeal (noise only — key case settled)...")
    gen_appeals(cases)
    print("[12/12] tbl_settlement (1 key settlement + noise)...")
    gen_settlements(cases)
    
    print()
    print("="*60)
    print("VERIFICATION — Key entities present:")
    # Quick verify
    c = pd.read_parquet(os.path.join(OUTPUT_DIR, "tbl_case_mstr.parquet"))
    print(f"  Case SDNY-2022-CIV-04851 exists: {CASE['docket_no'] in c['docket_no'].values}")
    p = pd.read_parquet(os.path.join(OUTPUT_DIR, "tbl_pty_info.parquet"))
    print(f"  Meridian Capital exists: {'Meridian Capital Group LLC' in p['pty_nm'].values}")
    s = pd.read_parquet(os.path.join(OUTPUT_DIR, "tbl_settlement.parquet"))
    key_stl = s[s['stl_id']=='STL-000001']
    print(f"  Settlement $347.5M exists: {len(key_stl)>0 and key_stl.iloc[0]['stl_amt']==347500000}")
    print("="*60)


if __name__ == "__main__":
    main()
