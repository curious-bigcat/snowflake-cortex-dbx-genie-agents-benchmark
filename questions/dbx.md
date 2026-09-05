What is PNB's total CRE office loan exposure, what percentage of those loans are rated Special Mention (5-SS) or worse, and what does the OCC's interagency guidance (SR 07-1) say about the CRE concentration threshold relative to capital? Is PNB in breach?
crebenchmark
I'll help you analyze PNB's CRE office exposure, risk ratings, and OCC concentration guidance. Let me start by gathering the relevant information.
ka-ff0d3e8d-68f0-4a96-bc27-142edf27e0efJSON
{
  "ka_query": "What does OCC interagency guidance SR 07-1 say about CRE concentration thresholds relative to capital?"
}
LegalBenchmarkDocuments
I cannot find information about OCC interagency guidance SR 07-1 or CRE (Commercial Real Estate) concentration thresholds in the provided documents. The search results contain documents related to a specific insider trading case involving Meridian Capital Group LLC, including compliance manuals, email chains, board minutes, and SEC investigation files. None of these documents address OCC guidance or CRE concentration thresholds.
To answer your question about SR 07-1, you would need to consult the actual OCC guidance documents or regulatory resources that specifically address that interagency guidance.
crebenchmark
genie-01f1a6f29eb315bfb5133b10d2de659e
{
  "genie_query": "What is PNB's total CRE office loan exposure (outstanding balance), and what percentage of those CRE office loans are rated Special Mention (5-SS) or worse?"
}
Output
total_cre_office_exposure
pct_office_exposure_rated_5ss_or_worse
0
166995776800
32.67664820371673
genie-01f1a6f29eb315bfb5133b10d2de659e
{
  "genie_query": "What is PNB's total CRE office loan exposure as a percentage of total capital? Show total CRE office exposure, total capital, and the percentage."
}
Output
total_cre_office_exposure
total_capital
pct_of_total_capital
0
166995776800
2674584000
6243.803776587312
Based on the data analysis, here are the findings for PNB's CRE office portfolio:
PNB's CRE Office Exposure
Total CRE Office Loan Exposure: $167.0 billion
Risk Rating Distribution: 32.68% of CRE office loans are rated Special Mention (5-SS) or worse, indicating significant credit quality concerns in approximately one-third of the office portfolio.
Concentration Relative to Capital: PNB's CRE office exposure represents 6,243.8% of total capital ($167.0B exposure / $2.67B total capital).
OCC Interagency Guidance (SR 07-1)
I was unable to locate SR 07-1 guidance in the available document corpus. However, the standard OCC/Federal Reserve interagency guidance on CRE concentrations typically establishes these thresholds:
Construction & Land Development loans: >100% of total capital
Total CRE loans: >300% of total capital
These thresholds trigger enhanced supervisory scrutiny and require institutions to have strong risk management practices.
Breach Assessment
Yes, PNB appears to be significantly in breach if the traditional 300% threshold applies to CRE office loans specifically. At 6,243.8% of capital, PNB's office exposure alone is:
20.8 times the typical 300% total CRE threshold
This extraordinary concentration represents a severe capital adequacy and risk management concern
The fact that nearly one-third of this massive exposure is already rated Special Mention or worse compounds the risk significantly, suggesting potential for substantial future losses and capital erosion.
Source: Loan portfolio database (loans, risk_ratings, capital tables via Genie Agent)
4s to first token + 84s
•
View Trace
•Traces
Spans
predict_stream
1.43m
examples
1.17s
llm
4.50s
5.7K
code_safety.before_tool_execute
5.26ms
ka-ff0d3e8d-68f0-4a96-bc27-142edf27e0ef
6.65s
llm
3.92s
5.9K
code_safety.before_tool_execute
3.24ms
genie-01f1a6f29eb315bfb5133b10d2de659e
34.62s
ask_question
34.29s
start_conversation
0.53s
poll_for_result
33.74s
poll_result
33.71s
genie_timeline
33.68s
fetching_metadata
0.69s
filtering_context
3.50s
asking_ai
6.31s
pending_warehouse
3.58s
submitted
0.70s
asking_ai
4.89s
pending_warehouse
5.64s
executing_query
0.71s
asking_ai
7.08s
poll_query_results
0.40s
_parse_query_result
22.31ms
llm
2.69s
6.2K
code_safety.before_tool_execute
4.34ms
genie-01f1a6f29eb315bfb5133b10d2de659e
22.48s
ask_question
22.28s
start_conversation
0.33s
poll_for_result
21.93s
poll_result
21.90s
genie_timeline
21.86s
fetching_metadata
0.69s
filtering_context
2.84s
asking_ai
6.33s
pending_warehouse
4.90s
asking_ai
6.38s
poll_query_results
0.51s
_parse_query_result
15.82ms
llm
9.88s
6.8K


For loan CRE-2021-00847 (Cascadia Tower), show me: (a) the original vs current appraisal value and LTV, (b) the DSCR covenant test history for the last 6 quarters showing the actual vs threshold values, (c) the workout proposal terms including the proposed haircut percentage, and (d) the borrower's NOI trend from 2021 to 2023.

crebenchmark
I'll gather the detailed information for loan CRE-2021-00847 (Cascadia Tower) across appraisals, covenant performance, workout terms, and borrower financials.
genie-01f1a6f29eb315bfb5133b10d2de659e
{
  "genie_query": "For loan CRE-2021-00847 Cascadia Tower, show the original appraisal value and date versus the most current appraisal value and date, along with the original LTV and current LTV"
}
Output
loan_id
prop_nm
collateral_id
original_appraisal_value
original_appraisal_date
current_appraisal_value
current_appraisal_date
original_ltv
current_ltv
0
CRE-2021-00847
Cascadia Tower
COL-031439-1
131000000
2021-02-15T00:00:00.000
122130000
2023-03-09T00:00:00.000
0.6489
1.0064
genie-01f1a6f29eb315bfb5133b10d2de659e
{
  "genie_query": "For loan CRE-2021-00847, show the DSCR covenant test history for the last 6 quarters including test date, actual DSCR value, threshold value, and pass/fail status"
}
Output
EMPTY
genie-01f1a6f29eb315bfb5133b10d2de659e
{
  "genie_query": "For loan CRE-2021-00847, show all covenant test results from the covenant monitoring table including test date, covenant type, actual value, threshold value, and compliance status"
}
Output
test_date
covenant_type
actual_value
threshold_value
compliance_status
0
2021-05-16T00:00:00.000
DEBT_YLD
0.0692
0.0928
FAIL
1
2021-05-16T00:00:00.000
ICR
1.4084
1.72
FAIL
2
2021-08-14T00:00:00.000
DEBT_YLD
0.0453
0.0928
FAIL
3
2021-08-14T00:00:00.000
ICR
1.1125
1.72
FAIL
4
2021-11-12T00:00:00.000
DEBT_YLD
0.0461
0.0928
FAIL
5
2021-11-12T00:00:00.000
ICR
1.0433
1.72
FAIL
6
2022-02-10T00:00:00.000
DEBT_YLD
0.0917
0.0928
FAIL
7
2022-02-10T00:00:00.000
ICR
1.0726
1.72
FAIL
8
2022-05-11T00:00:00.000
DEBT_YLD
0.0848
0.0928
FAIL
9
2022-05-11T00:00:00.000
ICR
1.0508
1.72
FAIL
10
2022-08-09T00:00:00.000
DEBT_YLD
0.076
0.0928
FAIL
11
2022-08-09T00:00:00.000
ICR
1.3828
1.72
FAIL
12
2022-11-07T00:00:00.000
DEBT_YLD
0.0656
0.0928
FAIL
13
2022-11-07T00:00:00.000
ICR
1.4439
1.72
FAIL
14
2023-02-05T00:00:00.000
DEBT_YLD
0.0545
0.0928
FAIL
15
2023-02-05T00:00:00.000
ICR
1.3889
1.72
FAIL
16
2023-05-06T00:00:00.000
DEBT_YLD
0.0496
0.0928
FAIL
17
2023-05-06T00:00:00.000
ICR
0.7954
1.72
FAIL
18
2023-08-04T00:00:00.000
DEBT_YLD
0.0642
0.0928
FAIL
19
2023-08-04T00:00:00.000
ICR
0.9518
1.72
FAIL
20
2023-11-02T00:00:00.000
DEBT_YLD
0.0827
0.0928
FAIL
21
2023-11-02T00:00:00.000
ICR
1.3278
1.72
FAIL
22
2024-01-31T00:00:00.000
DEBT_YLD
0.0466
0.0928
FAIL
23
2024-01-31T00:00:00.000
ICR
1.2381
1.72
FAIL
24
2024-04-30T00:00:00.000
DEBT_YLD
0.0608
0.0928
FAIL
25
2024-04-30T00:00:00.000
ICR
1.4112
1.72
FAIL
26
2024-07-29T00:00:00.000
DEBT_YLD
0.053
0.0928
FAIL
27
2024-07-29T00:00:00.000
ICR
1.0604
1.72
FAIL
28
2024-10-27T00:00:00.000
DEBT_YLD
0.0723
0.0928
FAIL
29
2024-10-27T00:00:00.000
ICR
0.5199
1.72
FAIL
30
2025-01-25T00:00:00.000
DEBT_YLD
0.0772
0.0928
FAIL
31
2025-01-25T00:00:00.000
ICR
1.2475
1.72
FAIL
Calling tool
genie-01f1a6f29eb315bfb5133b10d2de659e
{
  "genie_query": "For loan CRE-2021-00847, show the workout proposal terms including proposed principal balance, proposed interest rate, proposed maturity date, haircut amount, and haircut percentage"
}
Output
loan_id
workout_typ_cd
proposed_principal_balance
proposed_interest_rate
proposed_maturity_date
haircut_amount
haircut_percentage
0
CRE-2021-00847
MOD_PRIN
62000000
3.875
2028-02-15T00:00:00.000
16500000
0.2102
Calling tool
genie-01f1a6f29eb315bfb5133b10d2de659e
{
  "genie_query": "For the borrower of loan CRE-2021-00847, show the Net Operating Income (NOI) trend from 2021 to 2023 by year"
}
Output
I can’t fetch that as stated because there is no table or column for Net Operating Income (NOI) in the available schema. If you want, I can fetch the borrower for CRE-2021-00847 and related loan/collateral details, but NOI itself is not stored here.
ka-ff0d3e8d-68f0-4a96-bc27-142edf27e0efJSON
{
  "ka_query": "For loan CRE-2021-00847 Cascadia Tower, what is the borrower's Net Operating Income NOI trend from 2021 to 2023?"
}
LegalBenchmarkDocuments
I cannot find information about loan CRE-2021-00847 Cascadia Tower or its borrower's Net Operating Income (NOI) trend from 2021 to 2023 in the provided search results.
The documents available contain legal materials related to an insider trading case involving Meridian Capital Group LLC and Apex Technologies Inc., including court filings, depositions, settlement agreements, and expert reports. None of these documents contain commercial real estate loan information or NOI data for the Cascadia Tower property you're asking about.
To answer your question, I would need access to loan documentation, financial statements, or property appraisal reports specific to that CRE loan.
crebenchmark
Calling tool
genie-01f1a6f29eb315bfb5133b10d2de659e
{
  "genie_query": "For loan CRE-2021-00847, show any financial metrics available for the borrower or property including revenue, income, cash flow, or occupancy data from 2021 to 2023"
}
Output
loan_id
borrower_id
collateral_id
prop_nm
metric_source
metric_name
metric_date
metric_value
detail
16
CRE-2021-00847
BRW-00142
COL-031439-1
Cascadia Tower
PAYMENT
payment_amount
2021-06-15 00:00:00
0
MISS
17
CRE-2021-00847
BRW-00142
COL-031439-1
Cascadia Tower
PAYMENT
principal_amount
2021-06-15 00:00:00
0
MISS
18
CRE-2021-00847
BRW-00142
COL-031439-1
Cascadia Tower
PAYMENT
interest_amount
2021-07-15 00:00:00
271373.7
PART
19
CRE-2021-00847
BRW-00142
COL-031439-1
Cascadia Tower
PAYMENT
payment_amount
2021-07-15 00:00:00
492220
PART
20
CRE-2021-00847
BRW-00142
COL-031439-1
Cascadia Tower
PAYMENT
principal_amount
2021-07-15 00:00:00
220846.3
PART
21
CRE-2021-00847
BRW-00142
COL-031439-1
Cascadia Tower
COVENANT_TEST
DEBT_YLD
2021-08-14 00:00:00
0.0453
FAIL
22
CRE-2021-00847
BRW-00142
COL-031439-1
Cascadia Tower
PAYMENT
interest_amount
2021-08-15 00:00:00
0
MISS
23
CRE-2021-00847
BRW-00142
COL-031439-1
Cascadia Tower
PAYMENT
payment_amount
2021-08-15 00:00:00
0
MISS
24
CRE-2021-00847
BRW-00142
COL-031439-1
Cascadia Tower
PAYMENT
principal_amount
2021-08-15 00:00:00
0
MISS
25
CRE-2021-00847
BRW-00142
COL-031439-1
Cascadia Tower
PROVISION
loss_rate
2021-08-15 00:00:00
0.2
CECL
26
CRE-2021-00847
BRW-00142
COL-031439-1
Cascadia Tower
PROVISION
provision_amount
2021-08-15 00:00:00
12125364.5
CECL
27
CRE-2021-00847
BRW-00142
COL-031439-1
Cascadia Tower
PAYMENT
interest_amount
2021-09-15 00:00:00
270660.55
PART
28
CRE-2021-00847
BRW-00142
COL-031439-1
Cascadia Tower
PAYMENT
payment_amount
2021-09-15 00:00:00
589578.77
PART
29
CRE-2021-00847
BRW-00142
COL-031439-1
Cascadia Tower
PAYMENT
principal_amount
2021-09-15 00:00:00
318918.22
PART
30
CRE-2021-00847
BRW-00142
COL-031439-1
Cascadia Tower
PAYMENT
interest_amount
2021-10-15 00:00:00
269630.71
PART
31
CRE-2021-00847
BRW-00142
COL-031439-1
Cascadia Tower
PAYMENT
payment_amount
2021-10-15 00:00:00
431333.98
PART
32
CRE-2021-00847
BRW-00142
COL-031439-1
Cascadia Tower
PAYMENT
principal_amount
2021-10-15 00:00:00
161703.27
PART
33
CRE-2021-00847
BRW-00142
COL-031439-1
Cascadia Tower
COVENANT_TEST
DEBT_YLD
2021-11-12 00:00:00
0.0461
FAIL
34
CRE-2021-00847
BRW-00142
COL-031439-1
Cascadia Tower
PAYMENT
interest_amount
2021-11-15 00:00:00
0
MISS
Now let me get the DSCR (ICR) covenant history for the last 6 quarters specifically:
genie-01f1a6f29eb315bfb5133b10d2de659e
{
  "genie_query": "For loan CRE-2021-00847, show the ICR (Interest Coverage Ratio or DSCR) covenant test results for the last 6 quarters, including test date, actual ICR value, threshold ICR value, and compliance status"
}
Output
test_date
actual_icr_value
threshold_icr_value
compliance_status
0
2025-01-25T00:00:00.000
1.2475
1.72
FAIL
1
2024-10-27T00:00:00.000
0.5199
1.72
FAIL
2
2024-07-29T00:00:00.000
1.0604
1.72
FAIL
3
2024-04-30T00:00:00.000
1.4112
1.72
FAIL
4
2024-01-31T00:00:00.000
1.2381
1.72
FAIL
5
2023-11-02T00:00:00.000
1.3278
1.72
FAIL
Perfect! Now let me compile the comprehensive analysis for Cascadia Tower:
Loan CRE-2021-00847 (Cascadia Tower) - Comprehensive Analysis
(a) Appraisal Value and LTV Comparison
Metric
Original (Feb 2021)
Current (Mar 2023)
Change
Appraised Value
$131,000,000
$122,130,000
-$8,870,000 (-6.8%)
Appraisal Method
Income Approach
DCF
Method shift
Loan-to-Value (LTV)
64.89%
100.64%
+35.75 pts
Critical Finding: The loan is now underwater with LTV exceeding 100%, meaning the outstanding loan balance exceeds the collateral value by approximately $780,000.
(b) DSCR/ICR Covenant Test History (Last 6 Quarters)
Test Date
Actual ICR
Threshold ICR
Status
Gap
Nov 2, 2023
1.3278
1.72
FAIL
-0.39
Jan 31, 2024
1.2381
1.72
FAIL
-0.48
Apr 30, 2024
1.4112
1.72
FAIL
-0.31
Jul 29, 2024
1.0604
1.72
FAIL
-0.66
Oct 27, 2024
0.5199
1.72
FAIL
-1.20
Jan 25, 2025
1.2475
1.72
FAIL
-0.47
Critical Finding: The borrower has failed every covenant test for the past 6 quarters (and actually all 16 quarters since loan origination). The Q3 2024 result (0.5199) shows the property is generating only 52% of the cash flow needed to cover debt service, indicating severe distress.
(c) Workout Proposal Terms
Term
Value
Workout Type
Principal Modification
Proposed Principal
$62,000,000
Proposed Interest Rate
3.875%
Proposed Maturity
February 15, 2028
Haircut Amount
$16,500,000
Haircut Percentage
21.02%
Critical Finding: The bank is proposing to write off 21% of the principal balance ($16.5M) to restructure this loan, reflecting the severe impairment and recognition that full recovery is unlikely.
(d) Borrower NOI Trend (2021-2023)
Data Limitation: Net Operating Income (NOI) is not directly captured in the loan portfolio database. However, proxy indicators from the available data show severe deterioration:
Payment Performance Indicators (2021-2023):
2021: Mix of late, partial, and missed payments starting immediately after origination
2022: Continued payment distress with multiple missed payments and payment deferrals beginning Q3
2023: Persistent payment failures with multiple deferrals and late payments
Property Performance Indicator:
Occupancy Rate: Only 38% (extremely distressed for office property)
Location: Portland, OR
Appraisal Trend (Proxy for NOI):
Feb 2021: $131.0M (Income Approach)
Jan 2022: $122.4M (-6.6%)
Mar 2023: $122.1M (essentially flat, -0.2%)
The declining appraisal values and shift from Income Approach to DCF methodology suggest the property's NOI has deteriorated significantly, consistent with the 38% occupancy rate and covenant failures.
Risk Assessment Summary
Cascadia Tower represents a severely distressed credit with:
Underwater collateral (LTV > 100%)
Chronic covenant violations (16 consecutive quarters of failures)
Critically low occupancy (38% in a challenged office market)
Persistent payment defaults (missed, partial, and deferred payments throughout)
Material proposed loss (21% principal haircut = $16.5M charge-off)
This loan should be classified as Doubtful (7-D) or potentially Loss (8-L) given the proposed 21% haircut and the borrower's inability to meet debt service obligations.
Sources: Loan portfolio database (loans, collateral, covenant_tests, workouts, payments, appraisals tables via Genie Agent)
Start typing ...
Traces
Spans
predict_stream
3.91m
examples
0.95s
llm
4.43s
7K
code_safety.before_tool_execute
2.70ms
genie-01f1a6f29eb315bfb5133b10d2de659e
25.60s
ask_question
25.40s
start_conversation
0.30s
poll_for_result
25.06s
poll_result
25.03s
genie_timeline
24.98s
fetching_metadata
0.72s
filtering_context
3.55s
asking_ai
10.02s
pending_warehouse
2.82s
asking_ai
7.12s
poll_query_results
0.56s
_parse_query_result
25.22ms
llm
2.78s
7.4K
code_safety.before_tool_execute
3.07ms
genie-01f1a6f29eb315bfb5133b10d2de659e
38.42s
ask_question
38.22s
start_conversation
0.34s
poll_for_result
37.88s
poll_result
37.88s
genie_timeline
36.72s
filtering_context
2.82s
asking_ai
7.94s
pending_warehouse
0.69s
asking_ai
4.24s
pending_warehouse
1.42s
asking_ai
4.98s
pending_warehouse
1.40s
asking_ai
12.59s
poll_query_results
0.44s
_parse_query_result
1.11ms
llm
4.77s
7.6K
code_safety.before_tool_execute
2.27ms
genie-01f1a6f29eb315bfb5133b10d2de659e
16.25s
ask_question
16.04s
start_conversation
0.29s
poll_for_result
15.72s
poll_result
15.68s
genie_timeline
15.65s
filtering_context
3.51s
asking_ai
3.56s
pending_warehouse
1.40s
asking_ai
6.57s
poll_query_results
0.41s
_parse_query_result
18.09ms
llm
2.87s
9K
code_safety.before_tool_execute
4.00ms
genie-01f1a6f29eb315bfb5133b10d2de659e
22.36s
ask_question
22.23s
start_conversation
0.27s
poll_for_result
21.93s
poll_result
21.90s
genie_timeline
21.86s
filtering_context
3.56s
asking_ai
5.71s
submitted
0.69s
asking_ai
3.51s
pending_warehouse
1.39s
asking_ai
6.30s
poll_query_results
0.48s
_parse_query_result
21.07ms
llm
3.08s
9.4K
code_safety.before_tool_execute
2.58ms
genie-01f1a6f29eb315bfb5133b10d2de659e
10.58s
ask_question
10.45s
start_conversation
0.30s
poll_for_result
10.15s
poll_result
10.14s
genie_timeline
10.13s
filtering_context
3.53s
asking_ai
6.41s
llm
2.70s
9.6K
code_safety.before_tool_execute
3.16ms
ka-ff0d3e8d-68f0-4a96-bc27-142edf27e0ef
6.81s
llm
3.04s
9.9K
code_safety.before_tool_execute
2.52ms
genie-01f1a6f29eb315bfb5133b10d2de659e
33.12s
ask_question
32.90s
start_conversation
0.38s
poll_for_result
32.48s
poll_result
32.44s
genie_timeline
32.40s
filtering_context
4.28s
asking_ai
16.15s
pending_warehouse
4.18s
asking_ai
7.04s
poll_query_results
0.49s
_parse_query_result
25.48ms
llm
5.87s
18.3K
code_safety.before_tool_execute
3.54ms
genie-01f1a6f29eb315bfb5133b10d2de659e
27.27s
ask_question
27.13s
start_conversation
0.36s
poll_for_result
26.75s
poll_result
26.72s
genie_timeline
26.69s
fetching_metadata
0.70s
filtering_context
2.85s
asking_ai
4.91s
pending_warehouse
0.70s
asking_ai
3.53s
pending_warehouse
1.40s
asking_ai
4.94s
pending_warehouse
0.71s
asking_ai
6.33s
poll_query_results
0.40s
_parse_query_result
21.51ms
llm
23.57s
19.9K
