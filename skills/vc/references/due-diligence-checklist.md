# Due Diligence Master Checklist

This is the master reference of due diligence items. Each item is tagged
with stage applicability and sector relevance. The `vc-diligence` skill
filters and prioritizes this list based on the specific deal context.

## Tag Legend

**Stage**: `Seed`, `Series A`, `Series B+`, `All` (always included)
**Sector**: `All`, `SaaS`, `Fintech`, `Deeptech`, `HealthTech`, `Consumer`, `Marketplace`

---

## Financial Due Diligence

| # | Item | Description | Stage | Sector |
|---|------|-------------|-------|--------|
| F1 | Bank statements verification | Obtain 12-24 months of bank statements. Reconcile against reported cash position and burn rate | All | All |
| F2 | Revenue recognition review | Verify revenue recognition methodology. Check for channel stuffing, premature recognition, or non-recurring items booked as recurring | Series A | All |
| F3 | MRR/ARR reconciliation | Reconcile reported MRR/ARR against billing system or payment processor data. Verify expansion, contraction, and churn components | Series A | SaaS |
| F4 | Unit economics validation | Independently calculate CAC, LTV, payback period, and gross margin from raw data. Compare against company-reported figures | Series A | All |
| F5 | Burn rate and runway analysis | Calculate actual monthly burn from bank statements. Compare against projections. Assess runway under base and downside scenarios | All | All |
| F6 | Cap table verification | Obtain cap table from company counsel. Verify against certificate of incorporation, board minutes, and option grants. Check for errors, missing grants, or undisclosed commitments | All | All |
| F7 | Outstanding debt and obligations | Identify all debt instruments (venture debt, convertible notes, SAFEs, credit lines). Review terms, conversion triggers, and maturity dates | All | All |
| F8 | Tax compliance review | Verify federal and state tax filings are current. Check for outstanding liabilities, 409A valuations, and R&D credit claims | Series A | All |
| F9 | Financial projections stress test | Evaluate management projections against historical performance. Build downside and base case scenarios. Assess key assumptions for reasonableness | Series A | All |
| F10 | Accounts receivable aging | Review AR aging schedule. Identify concentration, delinquency patterns, and credit risk in the customer base | Series B+ | All |
| F11 | GMV and take-rate verification | Reconcile reported GMV against payment processor data. Verify take rate calculation and any subsidies or promotions that inflate volume | Series A | Marketplace |
| F12 | Transaction volume validation | Verify reported transaction volumes, payment processing data, and interchange revenue against bank and processor statements | Series A | Fintech |
| F13 | Loan book quality assessment | Analyze loan portfolio: default rates, recovery rates, vintage analysis, concentration by borrower/sector. Stress test under rising default scenarios | Series A | Fintech |
| F14 | Cohort revenue analysis | Break down revenue by customer cohort (by sign-up month/quarter). Assess retention curves, expansion patterns, and cohort LTV trends | Series A | SaaS |
| F15 | Deferred revenue and prepayments | Review deferred revenue balances and prepayment obligations. Assess impact on cash flow vs. recognized revenue | Series B+ | SaaS |
| F16 | R&D capitalization review | Verify treatment of R&D expenses vs. capitalized development costs. Assess whether capitalization policy is appropriate and consistent | Series B+ | Deeptech |
| F17 | Grant and non-dilutive funding | Inventory all grants (government, research, tax credits). Verify conditions, clawback provisions, and reporting requirements | Seed | Deeptech |
| F18 | Insurance coverage review | Review existing insurance policies (D&O, E&O, cyber, general liability). Assess adequacy of coverage relative to business risks | Series B+ | All |
| F19 | Working capital analysis | Analyze working capital cycle (inventory, payables, receivables). Assess seasonal patterns and cash conversion cycle | Series B+ | Marketplace |
| F20 | Reimbursement and payer mix analysis | Verify revenue by payer type (commercial, Medicare, Medicaid, self-pay). Assess reimbursement rates and collection rates by payer | Series A | HealthTech |

## Legal Due Diligence

| # | Item | Description | Stage | Sector |
|---|------|-------------|-------|--------|
| L1 | Certificate of incorporation and bylaws | Review current certificate of incorporation, all amendments, and bylaws. Verify authorized shares, class rights, and governance provisions match expectations | All | All |
| L2 | Board minutes and consents | Review all board meeting minutes and written consents from inception. Look for undisclosed commitments, disputes, litigation mentions, or unusual resolutions | Series A | All |
| L3 | IP assignment agreements | Verify that all founders, employees, and contractors have signed IP assignment agreements assigning all work product to the company | All | All |
| L4 | Patent and trademark portfolio | Inventory all patents (granted and pending), trademarks, and copyrights. Verify ownership, filing status, jurisdictions, and maintenance fee status | Seed | Deeptech |
| L5 | Option plan and grant review | Review stock option plan, all option grants, exercise prices, and 409A valuation history. Check for IRC 409A compliance issues | All | All |
| L6 | Material contracts review | Obtain and review all material contracts (customers, suppliers, partners, landlords). Identify change-of-control provisions, exclusivity clauses, and termination rights | Series A | All |
| L7 | Employment agreements | Review founder and key employee employment agreements. Check for non-competes, non-solicits, IP assignment, vesting, and termination provisions | All | All |
| L8 | Prior funding documents | Review all prior financing documents (SAFEs, convertible notes, stock purchase agreements). Verify conversion terms, outstanding obligations, and investor rights | All | All |
| L9 | Litigation and disputes | Search for pending or threatened litigation, arbitration, or regulatory proceedings. Review any demand letters, cease-and-desist notices, or settlement agreements | All | All |
| L10 | Privacy policy and terms of service | Review privacy policy, terms of service, and data processing agreements. Assess compliance with GDPR, CCPA, and applicable privacy laws | Series A | All |
| L11 | Open source license compliance | Audit use of open source software. Identify copyleft licenses (GPL, AGPL) that could require source code disclosure. Verify compliance with all license terms | Series A | SaaS |
| L12 | Data processing and sub-processor agreements | Review DPAs with customers and sub-processor agreements with vendors. Verify data flow documentation and cross-border transfer mechanisms | Series A | SaaS |
| L13 | Regulatory licenses and permits | Inventory all regulatory licenses, permits, and registrations. Verify current status, renewal dates, and conditions. Identify any missing or pending licenses | All | Fintech |
| L14 | Money transmission and banking licenses | Verify state-by-state money transmission licenses or bank partnership arrangements. Review sponsor bank agreements and compliance requirements | Seed | Fintech |
| L15 | Clinical trial agreements and IRB approvals | Review clinical trial protocols, IRB/ethics approvals, informed consent documents, and data monitoring plans | Seed | HealthTech |
| L16 | FDA regulatory submissions | Review 510(k), PMA, De Novo, or other FDA submissions and correspondence. Assess timeline, completeness, and risk of rejection | Seed | HealthTech |
| L17 | Entity structure and subsidiaries | Map complete corporate structure including all subsidiaries, branches, and related entities. Verify good standing in all jurisdictions | Series A | All |
| L18 | Government contracts and security clearances | Review any government contracts, security clearances, ITAR/EAR compliance, and procurement regulations applicable to the business | Series A | Deeptech |
| L19 | Contractor classification review | Audit classification of workers as employees vs. independent contractors. Assess risk of misclassification (especially gig/marketplace workers) | Series A | Marketplace |
| L20 | Consumer protection and advertising compliance | Review marketing materials, advertising claims, and endorsement practices for compliance with FTC regulations and state consumer protection laws | Series A | Consumer |

## Technical Due Diligence

| # | Item | Description | Stage | Sector |
|---|------|-------------|-------|--------|
| T1 | Architecture review | Review system architecture diagrams, technology stack, and key design decisions. Assess scalability, reliability, and technical debt level | Series A | All |
| T2 | Code quality assessment | Review code repositories for quality indicators: test coverage, documentation, coding standards, dependency management, and CI/CD practices | Series A | All |
| T3 | Security posture evaluation | Assess security practices: authentication/authorization, encryption (at rest and in transit), vulnerability scanning, penetration testing history, and incident response plan | Series A | All |
| T4 | Infrastructure and scalability | Review hosting infrastructure, deployment practices, monitoring/alerting, and disaster recovery. Assess ability to handle 10x current load | Series A | All |
| T5 | Data architecture and storage | Review data models, storage systems, backup procedures, and data retention policies. Assess data quality and governance practices | Series A | All |
| T6 | Third-party dependency risk | Inventory critical third-party services, APIs, and libraries. Assess vendor concentration risk, SLA guarantees, and fallback options | Series A | All |
| T7 | SOC 2 / ISO 27001 compliance | Verify SOC 2 Type I or Type II report status. Review scope, exceptions, and remediation items. Assess timeline if not yet completed | Series A | SaaS |
| T8 | Product roadmap feasibility | Review product roadmap and assess technical feasibility, resource requirements, and timeline realism relative to team capabilities | Seed | All |
| T9 | Key-person technical dependency | Identify whether critical technical knowledge is concentrated in one or few individuals. Assess bus-factor risk and knowledge documentation | All | All |
| T10 | Algorithm and model validation | For AI/ML companies: review model performance metrics, training data provenance, bias testing, and robustness to distribution shift | Seed | Deeptech |
| T11 | Manufacturing and hardware readiness | For hardware/physical products: review manufacturing partnerships, supply chain, BOM cost, yield rates, and path to volume production | Seed | Deeptech |
| T12 | HIPAA technical safeguards | Review technical implementation of HIPAA security rule: access controls, audit logging, encryption, transmission security, and BAA coverage | Seed | HealthTech |
| T13 | Platform reliability and uptime | Review historical uptime metrics, SLA commitments to customers, incident history, and mean-time-to-recovery. Assess monitoring coverage | Series A | SaaS |
| T14 | Mobile app quality | Review app store ratings, crash rates, performance metrics, and update frequency. Assess cross-platform consistency and technical debt | Series A | Consumer |
| T15 | Payment infrastructure review | Review payment processing architecture, PCI DSS compliance, fraud detection systems, and chargeback rates | Seed | Fintech |
| T16 | Trust and safety systems | Review content moderation, fraud prevention, identity verification, and dispute resolution systems. Assess scalability of safety mechanisms | Series A | Marketplace |
| T17 | API design and partner integrations | Review API design, documentation, versioning strategy, and integration health with key partners. Assess developer experience if platform play | Series A | SaaS |
| T18 | Data pipeline and analytics | Review data collection, ETL pipelines, analytics infrastructure, and reporting capabilities. Assess data-driven decision-making maturity | Series B+ | All |
| T19 | Technical team assessment | Evaluate engineering team skill depth, seniority distribution, hiring pipeline, and retention. Assess whether team matches technical ambition | All | All |
| T20 | Open source strategy and exposure | Evaluate the company's open source strategy (if applicable). Assess community health, contribution patterns, and commercial licensing model | Series A | Deeptech |

## Commercial Due Diligence

| # | Item | Description | Stage | Sector |
|---|------|-------------|-------|--------|
| C1 | Customer reference calls | Conduct 5-10 reference calls with current customers. Assess satisfaction, willingness to renew/expand, competitive alternatives considered, and NPS | Series A | All |
| C2 | Customer concentration analysis | Calculate revenue share of top 1, 5, and 10 customers. Assess risk if any single customer churns. Review contract terms for largest accounts | Series A | All |
| C3 | Market size validation | Independently size TAM/SAM/SOM using bottom-up methodology. Cross-reference against industry reports and analyst estimates | All | All |
| C4 | Competitive landscape mapping | Map all direct and indirect competitors. Assess positioning, pricing, market share, funding, and recent strategic moves | All | All |
| C5 | Sales pipeline review | Review CRM data: pipeline volume, conversion rates by stage, average deal size, sales cycle length, and win/loss reasons | Series A | All |
| C6 | Churn analysis and retention | Analyze gross and net churn by cohort, customer segment, and reason. Review retention improvement initiatives and their impact | Series A | SaaS |
| C7 | Pricing power assessment | Evaluate pricing strategy relative to value delivered and competition. Assess ability to raise prices, history of price increases, and customer response | Series A | All |
| C8 | Channel and distribution review | Map all customer acquisition channels. Assess channel concentration risk, CAC by channel, and scalability of primary channels | Series A | All |
| C9 | Partnership validation | Contact key partners to verify relationship health, exclusivity, and strategic importance. Assess dependency risk | Series A | All |
| C10 | Net Promoter Score verification | Verify reported NPS through independent survey or call sampling. Assess trends and response rates | Series B+ | All |
| C11 | Supply-side diligence | For marketplaces: interview supply-side participants (sellers, service providers). Assess satisfaction, multi-homing behavior, and churn risk | Series A | Marketplace |
| C12 | Demand-side diligence | For marketplaces: interview demand-side participants (buyers, consumers). Assess satisfaction, alternatives used, and willingness to pay | Series A | Marketplace |
| C13 | Content and engagement metrics | Verify engagement metrics: DAU/MAU ratio, session length, content consumption, and social sharing. Assess organic vs. paid engagement | Seed | Consumer |
| C14 | User acquisition channel health | Audit user acquisition channels for sustainability. Assess paid channel efficiency trends, organic growth contribution, and channel diversity | Series A | Consumer |
| C15 | Clinical and health outcomes validation | Review clinical evidence, outcomes data, and patient/provider satisfaction. Assess strength of evidence vs. regulatory and payer requirements | Series A | HealthTech |
| C16 | KOL and advisory board engagement | Verify engagement and endorsement from key opinion leaders, medical advisory board, and clinical champions | Seed | HealthTech |
| C17 | Contract value and renewal pipeline | Review weighted contract pipeline, renewal rates, multi-year agreements, and upcoming renewals at risk | Series B+ | SaaS |
| C18 | Geographic expansion feasibility | Assess readiness for geographic expansion: market research, localization requirements, regulatory differences, and go-to-market plan | Series B+ | All |
| C19 | Brand and reputation assessment | Review online presence, media coverage, social media sentiment, and Glassdoor ratings. Assess brand strength relative to competitors | Series A | Consumer |
| C20 | Regulatory moat assessment | Evaluate whether regulatory requirements create barriers to entry that benefit the company. Assess risk of regulatory change | Series A | Fintech |

## Team & HR Due Diligence

| # | Item | Description | Stage | Sector |
|---|------|-------------|-------|--------|
| H1 | Founder background checks | Conduct background checks on all founders: criminal records, credit history, litigation history, prior company outcomes, and reference checks | All | All |
| H2 | Founder reference calls | Conduct 3-5 back-channel reference calls per founder (former colleagues, investors, board members). Assess leadership, integrity, and resilience | All | All |
| H3 | Employment agreement review (founders) | Verify all founders have signed employment agreements with IP assignment, non-compete, and vesting provisions. Check for outside commitments | All | All |
| H4 | Key employee retention risk | Identify key employees beyond founders. Assess retention risk: vesting schedules, equity positions, market compensation, and flight risk | Series A | All |
| H5 | Organizational chart and hiring plan | Review current org chart and 12-month hiring plan. Assess whether planned hires align with strategic priorities and whether budget supports the plan | Series A | All |
| H6 | Compensation benchmarking | Benchmark founder and key employee compensation against market data. Identify under/over compensation and equity allocation reasonableness | Series A | All |
| H7 | Culture and Glassdoor review | Review Glassdoor, Blind, and other employee review platforms. Assess culture themes, management ratings, and any recurring complaints | Series A | All |
| H8 | Diversity and inclusion assessment | Review team composition and D&I initiatives. Assess leadership commitment and progress on inclusive hiring and culture | Series B+ | All |
| H9 | Advisory board value assessment | Interview advisors to assess actual engagement level, contribution frequency, and strategic value vs. name-only association | Seed | All |
| H10 | Technical team depth (engineering) | Assess engineering team seniority distribution, specialization coverage, and ability to execute on technical roadmap without over-reliance on founders | Series A | All |
| H11 | Sales team effectiveness | Review sales team structure, quota attainment, ramp times, and turnover. Assess whether sales process is repeatable and founder-independent | Series A | All |
| H12 | Founder-market fit deep dive | Assess why these founders are uniquely positioned for this market. Evaluate domain expertise depth, network relevance, and personal motivation | All | All |
| H13 | Board composition and governance | Review board composition, meeting frequency, committee structure, and governance practices. Assess board effectiveness and independence | Series B+ | All |
| H14 | Employee option pool adequacy | Verify unallocated option pool size relative to hiring plan. Assess whether pool refresh will require dilution at next round | Series A | All |
| H15 | Scientific and medical team credentials | Verify credentials and publication records of scientific/medical team members. Assess domain authority and clinical network | Seed | HealthTech |
| H16 | R&D team assessment | Evaluate research team depth, publication record, patent contributions, and ability to execute on technical milestones | Seed | Deeptech |
| H17 | Compliance team and officer | Verify existence and qualifications of compliance function. Assess whether compliance team is adequately resourced for regulatory requirements | Series A | Fintech |
| H18 | Contractor and vendor management | Review contractor relationships, key vendor dependencies, and any risks from contractor-to-employee conversion requirements | Series A | All |
| H19 | Succession and continuity planning | Assess whether key-person risk is mitigated by documentation, cross-training, or identified successors for critical roles | Series B+ | All |
| H20 | International team considerations | For distributed teams: review employment arrangements by jurisdiction, compliance with local labor laws, and data residency implications | Series A | All |

## Regulatory Due Diligence

| # | Item | Description | Stage | Sector |
|---|------|-------------|-------|--------|
| R1 | Regulatory landscape mapping | Map all regulatory bodies, laws, and regulations applicable to the business. Assess current compliance status and upcoming regulatory changes | All | All |
| R2 | Data privacy compliance (GDPR/CCPA) | Audit data collection, processing, and storage practices against GDPR, CCPA, and other applicable privacy regulations. Review data protection officer appointment | Series A | All |
| R3 | Industry-specific license inventory | Inventory all required licenses and permits. Verify current status, renewal timelines, and compliance with conditions | All | Fintech |
| R4 | AML/KYC program review | Review anti-money laundering and know-your-customer programs. Assess BSA compliance, SAR filing history, and OFAC screening procedures | Seed | Fintech |
| R5 | FDA regulatory pathway assessment | Assess FDA classification (Class I/II/III), selected regulatory pathway, and timeline to clearance/approval. Review pre-submission meeting history | Seed | HealthTech |
| R6 | HIPAA compliance audit | Conduct HIPAA compliance assessment: administrative, physical, and technical safeguards. Review BAAs, risk assessments, and breach notification procedures | Seed | HealthTech |
| R7 | Securities law compliance | Verify compliance with securities laws for all prior fundraises. Review Reg D filings, blue sky compliance, and accredited investor verification | Series A | All |
| R8 | Export control and sanctions | Assess applicability of ITAR, EAR, and sanctions regulations. Review export classification, screening procedures, and any technology transfer risks | Seed | Deeptech |
| R9 | Consumer protection compliance | Review compliance with FTC Act, Truth in Lending, Fair Credit Reporting, and other consumer protection regulations applicable to the product | Series A | Consumer |
| R10 | Environmental and safety regulations | Assess applicability of environmental, health, and safety regulations. Review compliance history and any pending remediation requirements | Series A | Deeptech |
| R11 | State-by-state regulatory analysis | For businesses with state-level regulation: map compliance status across all operating states. Identify gaps and remediation timelines | Series A | Fintech |
| R12 | Advertising and marketing compliance | Review advertising claims, testimonials, and marketing materials for regulatory compliance (FTC, state AG, sector-specific rules) | Series A | Consumer |
| R13 | COPPA compliance (if applicable) | If product may be used by children under 13: review COPPA compliance including parental consent mechanisms and data handling procedures | Seed | Consumer |
| R14 | Clinical regulatory compliance | Review compliance with Good Clinical Practice (GCP), Institutional Review Board requirements, and clinical data integrity | Series A | HealthTech |
| R15 | Payment Card Industry (PCI) compliance | Verify PCI DSS compliance level, most recent assessment date, and any outstanding remediation items | Seed | Fintech |
| R16 | Marketplace regulatory exposure | Assess regulatory risk from contractor classification, tax collection obligations, and platform liability laws in operating jurisdictions | Series A | Marketplace |
| R17 | International regulatory requirements | For companies operating internationally: map regulatory requirements by jurisdiction, assess compliance status, and identify material gaps | Series B+ | All |
| R18 | Accessibility compliance (ADA/WCAG) | Review product accessibility against WCAG 2.1 AA standards and ADA requirements. Assess litigation risk and remediation needs | Series B+ | All |
| R19 | AI and algorithmic governance | If AI/ML is core to the product: review algorithmic fairness testing, model transparency, and compliance with emerging AI regulations (EU AI Act, state laws) | Series A | Deeptech |
| R20 | Intellectual property regulatory (Bayh-Dole) | For university spin-outs or government-funded IP: verify compliance with Bayh-Dole Act, review license agreements, and assess IP encumbrances | Seed | Deeptech |

## Additional Sector-Specific Items

These items address niche areas that arise frequently in specific
sectors but do not fit neatly into the standard categories above.

| # | Item | Description | Stage | Sector |
|---|------|-------------|-------|--------|
| S1 | Multi-tenancy and data isolation | Verify tenant data isolation architecture. Assess risk of data leakage between customers and compliance with enterprise customer requirements | Series A | SaaS |
| S2 | Embedded finance compliance | If offering embedded financial services (payments, lending, insurance): verify regulatory structure, sponsor relationships, and consumer disclosures | Series A | Fintech |
| S3 | Clinical evidence strength assessment | Evaluate quality and relevance of clinical evidence: study design (RCT vs. observational), sample sizes, peer review status, and reproducibility | Seed | HealthTech |
| S4 | App store dependency risk | Assess dependency on Apple App Store and Google Play Store. Review compliance with store policies, commission impact on unit economics, and rejection history | Seed | Consumer |
| S5 | Seller and provider quality controls | Review quality assurance processes for supply-side participants. Assess vetting procedures, performance monitoring, and removal policies | Series A | Marketplace |

---

## Cross-Category Considerations

The following items span multiple categories and should be addressed
holistically rather than in isolation:

| # | Item | Description | Stage | Sector |
|---|------|-------------|-------|--------|
| X1 | Data room completeness audit | Verify that all requested documents have been provided. Track missing items and assess whether gaps are administrative or intentional | All | All |
| X2 | Related-party transaction review | Identify all transactions between the company and founder-related entities, investor affiliates, or board member interests. Assess fairness and disclosure | Series A | All |
| X3 | Insurance adequacy review | Assess D&O, E&O, cyber liability, and general liability coverage relative to company stage, sector risks, and upcoming round size | Series A | All |
| X4 | ESG and sustainability assessment | Evaluate environmental, social, and governance practices. Assess alignment with LP requirements and emerging ESG reporting standards | Series B+ | All |
| X5 | Post-closing integration items | Identify governance changes, reporting requirements, board observer rights, and operational support items to implement immediately after closing | All | All |
| X6 | Comparable transaction analysis | Research recent comparable acquisitions and funding rounds in the same sector and stage. Validate valuation expectations against market data | All | All |
| X7 | Customer data portability and lock-in | Assess customer switching costs, data export capabilities, and contractual lock-in mechanisms. Evaluate both defensibility and regulatory risk | Series A | SaaS |
| X8 | Supply chain and vendor concentration | Map critical suppliers and vendors. Assess concentration risk, contract terms, and availability of alternative suppliers | Series A | Deeptech |
| X9 | Community and ecosystem health | For products with community/ecosystem moats: assess community size, engagement, growth trajectory, and dependency on company resources | Series A | Consumer |
| X10 | Fraud and abuse detection | Review systems and processes for detecting and preventing fraud, abuse, and platform manipulation. Assess historical incident rate | Series A | Marketplace |

---

## Usage Notes

1. This checklist is a master reference. The `vc-diligence` skill filters
   items based on stage and sector before presenting to the user.
2. Items tagged `All` in the Stage column apply to every deal regardless
   of stage. Items tagged `All` in the Sector column apply regardless of
   sector.
3. The `#` codes (F1, L1, T1, etc.) are stable identifiers that can be
   referenced in DD tracking and status updates.
4. Priority assignment (Critical / Important / Nice-to-have) is handled
   by the `vc-diligence` skill based on deal context, not in this
   reference file.
5. Companies may span multiple sectors (e.g., fintech + marketplace).
   When this occurs, include sector-specific items from all applicable
   sectors.
