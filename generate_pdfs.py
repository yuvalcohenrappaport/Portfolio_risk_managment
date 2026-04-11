#!/usr/bin/env python3
"""
Portfolio Research Report PDF Generator
Generates one PDF per company with charts + research analysis.
"""
import json
import os
import textwrap
from fpdf import FPDF

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'company_reports')
PDF_DIR = os.path.join(OUTPUT_DIR, 'pdfs')
os.makedirs(PDF_DIR, exist_ok=True)

# Load financial data
with open(os.path.join(OUTPUT_DIR, 'all_data.json'), 'r') as f:
    all_data = json.load(f)

# ── Research reports ──────────────────────────────────────────────────────────
REPORTS = {}

REPORTS['AMZN'] = """COMPANY HISTORY & MANAGEMENT
Founded 1994 by Jeff Bezos as an online bookstore, Amazon expanded into e-commerce, cloud computing (AWS, launched 2006), digital advertising, and devices. CEO Andy Jassy (since July 2021) previously ran AWS for over a decade. CFO Brian Olsavsky since 2015. Bezos remains executive chairman (~9% ownership).

BUSINESS MODEL
Three segments: North America e-commerce (~60% rev), International (~23%), AWS (~17%). AWS generates ~60-65% of operating profit despite smallest revenue share. Advertising is a rapidly growing high-margin contributor (~$55-60B run-rate). Value proposition: convenience, selection, price for consumers; scalable infrastructure for enterprise.

FINANCIAL HEALTH
FY2024 Revenue: ~$638B (+11% YoY). Operating income: ~$68-70B; margin ~10.5-11%. Net income: ~$50-52B; EPS ~$4.80-5.00. FCF: ~$35-38B. Balance sheet: ~$86B cash vs ~$135B total debt (incl. leases). Debt/equity ~0.7x. ROE: ~22-24%. Margins expanded sharply since 2022 cost-cutting.

COMPETITIVE LANDSCAPE
E-commerce: Walmart, Shopify, Temu/Shein. Cloud: Microsoft Azure (~23% share vs AWS ~31%), Google Cloud (~11%). Advertising: Google, Meta. Moat: logistics network (300+ fulfillment centers US), Prime ecosystem (200M+ members), AWS first-mover scale.

KEY RISKS & OPPORTUNITIES
Bull: AWS re-accelerates on AI workloads; advertising scales to $80B+; retail margin expansion; Project Kuiper.
Bear: Cloud price competition; FTC antitrust lawsuit; AI capex ($75B+ guided 2025) destroys FCF if returns disappoint.

MANAGEMENT COMPENSATION
Jassy's comp is equity-heavy (61K RSUs over 10 years, ~$200M+). Base salary $175K. No annual cash bonus. Well-aligned long-term but no performance-based vesting hurdles (pure time-vest). Criticized by ISS/Glass Lewis.

VALUATION ANALYSIS
P/B: ~5.4x. Forward P/E: ~22x. EV/EBITDA: ~18-20x. FCF yield: ~2.5-3.0%. Premium to market but reasonable relative to growth. Not cheap by classical value definition.

RECOMMENDATION: HOLD -- Moderate conviction. 2-3 year horizon.
Quality compounder at ~22x forward earnings priced for continued execution. Wait for pullback to ~19-20x forward P/E for value entry.

3-YEAR TIMELINE
2025: FTC antitrust trial; AWS AI product cycle. Late 2025: Project Kuiper launch.
2026: Operating margin potentially 12-13%. 2027: Capex normalization; potential EPS $6.50-7.50."""

REPORTS['GOOG'] = """COMPANY HISTORY & MANAGEMENT
Founded 1998 by Larry Page and Sergey Brin. Restructured under Alphabet in 2015. CEO Sundar Pichai since 2019. CFO Anat Ashkenazi since 2024. Page and Brin control ~51% voting power via supervoting Class B shares -- governance concern.

BUSINESS MODEL
~77% revenue from Google advertising (Search ~57%, YouTube ~10%, Google Network ~10%). Google Cloud ~12%, now profitable. "Other Bets" (Waymo, Verily) <1% revenue. Core value: targeted advertising at scale through dominant search (~90% global share) and largest video platform (YouTube, 2B+ monthly users).

FINANCIAL HEALTH
FY2024 Revenue: ~$365-370B (+14% YoY). Operating income: ~$110-115B; margin ~30-31%. Net income: ~$95-100B; EPS ~$7.50-8.00. FCF: ~$70-75B. Balance sheet: ~$100B cash vs ~$28B debt = $72B net cash. Fortress balance sheet. ROE: ~30-32%. Buybacks: ~$60-62B in FY2024. First-ever dividend initiated 2024.

COMPETITIVE LANDSCAPE
Search: Bing/Copilot (<5%), AI-native search (Perplexity, ChatGPT). Cloud: AWS (~31%), Azure (~23%), Google Cloud (~11%). Video: TikTok, Meta Reels. Moat: Search dominance, data advantage, Android/Chrome distribution, YouTube network effects, massive AI talent. Being tested by GenAI.

KEY RISKS & OPPORTUNITIES
Bull: Search maintains via AI Overviews; Cloud inflects to 25%+ growth; Waymo at scale (~150K paid rides/week); YouTube dominates CTV; massive buyback compresses share count.
Bear: AI disrupts search economics; DOJ antitrust forces structural remedies; regulatory overhang EU; Other Bets burn capital.

MANAGEMENT COMPENSATION
Pichai total comp ~$10-12M salary/bonus plus large PSU grants ($218M in 2022, tied to TSR). Equity-heavy is positive. But dual-class structure insulates management from shareholder pressure -- governance discount.

VALUATION ANALYSIS
P/B: ~9.4x. Forward P/E: ~24x. EV/EBITDA: ~14-16x. FCF yield: ~4.0-4.5%. Ex-cash P/E: ~20x. Arguably cheapest mega-cap tech. Persistent antitrust/AI disruption discount.

RECOMMENDATION: BUY -- High conviction. 2-3 year horizon.
At ~24x forward earnings with $72B net cash, 30%+ margins, dominant franchise, and aggressive buyback -- most compelling value in mega-cap tech. Antitrust likely behavioral remedies, not breakup.

3-YEAR TIMELINE
2025: DOJ remedies ruling; Waymo expansion 10+ cities; Cloud approaches $50B run-rate.
2026: AI Overviews monetization clarity; potential EPS $9-10.
2027: Antitrust resolution; cumulative 8-10% share count reduction from buybacks."""

REPORTS['ONDS'] = """COMPANY HISTORY & MANAGEMENT
Small-cap technology company focused on industrial wireless (Ondas Networks) and autonomous drones (American Robotics, Airobotics). CEO Eric Brock, founder. Went public via reverse merger 2018. Management team is thin.

BUSINESS MODEL
Two segments: (1) Ondas Networks -- proprietary FullMAX wireless for critical infrastructure (rail, utilities, oil & gas); (2) Ondas Autonomous Systems -- drone platforms for industrial inspection. Revenue minimal (~$5-10M), pre-commercialization.

FINANCIAL HEALTH
Revenue: ~$5-10M (immaterial). Operating loss: ~$(35-45)M annually. Cash: ~$10-15M. Burning ~$8-10M/quarter. Goodwill heavily impaired. Going concern risk: <6 quarters runway without dilutive capital raises.

COMPETITIVE LANDSCAPE
Industrial wireless: Rajant, Cisco, Nokia/Ericsson (vastly larger). Drones: Skydio, DJI, Shield AI. No meaningful moat. FullMAX has not achieved commercial traction after years.

KEY RISKS & OPPORTUNITIES
Bull: FullMAX wins railroad/utility contract; FAA BVLOS regulations open drone market; acquisition for IP.
Bear: Continued cash burn + dilution; technology fails commercially; competitors with deeper pockets dominate.

MANAGEMENT COMPENSATION
CEO ~$1-1.5M annually. Disproportionate for <$10M revenue company burning $35M+/year. Alignment weak given persistent value destruction.

VALUATION ANALYSIS
P/B: ~7.0x (unreliable due to impaired goodwill). P/E: N/M. EV/Revenue: ~4-8x on minimal revenue. No framework makes this attractive.

RECOMMENDATION: SELL / DO NOT OWN -- High conviction.
Not appropriate for value fund. No revenue, no profitability path, impaired balance sheet, dilution risk. Speculative venture bet.

3-YEAR TIMELINE
2025: Additional equity raise likely (30-50% dilution). 2026: If solvent, potential first material contracts.
2027: Binary -- commercial inflection (10-15% probability) or acquired for pennies / delisted."""

REPORTS['RCL'] = """COMPANY HISTORY & MANAGEMENT
Founded 1968 in Norway. World's second-largest cruise operator. Five brands: Royal Caribbean International, Celebrity, Silversea, TUI Cruises (JV), Hapag-Lloyd. CEO Jason Liberty since Jan 2022 (former CFO). Strong post-COVID turnaround focused on yield management and deleveraging.

BUSINESS MODEL
Revenue from ticket sales (~70%) and onboard spending (~30%). ~65 ships, ~165K berths. FY2024 revenue ~$16.5-17B (record), driven by pricing power and 105%+ load factors. Most affordable vacation on per-day basis vs land-based alternatives.

FINANCIAL HEALTH
Revenue: ~$16.5-17B (+18-20% YoY). Operating margin: ~21-23% (record). Net income: ~$2.8-3.2B; EPS ~$10.50-11.50. FCF: ~$3.5-4.0B. Total debt: ~$18-20B (COVID legacy). Debt/equity ~3-4x. ROE: ~45-55% (inflated by low equity). P&L excellent; balance sheet concerning.

COMPETITIVE LANDSCAPE
Direct: Carnival (larger but weaker margins), Norwegian (smaller, more leveraged). Indirect: land-based resorts, Disney. RCL is best-in-class operator. Moderate moat: capital intensity barriers, brand loyalty, scale procurement.

KEY RISKS & OPPORTUNITIES
Bull: Continued yield growth 2-4% annually; rapid deleveraging; demographic tailwinds (Asia, younger demos); dividend reinstatement; credit upgrades.
Bear: Recession crushes discretionary travel; fuel spikes; pandemic risk; ~$19B debt leaves no margin for error.

MANAGEMENT COMPENSATION
CEO Liberty ~$21M total FY2024, heavily performance-based equity (PSUs tied to EPS and ROIC). Well-aligned -- right metrics for deleveraging company.

VALUATION ANALYSIS
P/B: ~9.4x (misleading -- book depressed by COVID losses). Forward P/E: ~17x on ~$14-15 EPS. EV/EBITDA: ~11-13x. PEG: ~0.6-0.7x. At upper end of historical cruise valuations but justified by superior execution.

RECOMMENDATION: HOLD -- Moderate conviction. 2-3 year horizon.
Well-run company at fair price. ~$19B debt uncomfortable for value fund. Wait for pullback to ~15x forward P/E (~$210-220) or further deleveraging.

3-YEAR TIMELINE
2025: Star of the Seas delivery; net debt/EBITDA target <3.5x; potential credit upgrade trajectory.
2026: Potential dividend reinstatement; target EPS $16-18.
2027: Net debt/EBITDA ~2.5-3.0x; EPS $18-22 supporting $300-400 stock price."""

REPORTS['VUG'] = """FUND OVERVIEW & STRUCTURE
VUG tracks the CRSP US Large Cap Growth Index. Launched Jan 2004. AUM $250B+. Managed passively by Vanguard Equity Index Group. Vanguard's mutual ownership structure keeps expenses trending down.

HOLDINGS & EXPOSURE
Top 10 holdings ~55-60%: Apple (~12%), Microsoft (~11%), NVIDIA (~10%), Amazon (~6%), Meta (~5%), Alphabet (~4%), Broadcom (~3%), Eli Lilly (~2%), Tesla (~2%), Visa (~2%). Tech-heavy (~58%), consumer discretionary (~15%), healthcare (~7%). Significant concentration risk.

EXPENSE RATIO & PERFORMANCE
Expense ratio: 0.04% (among cheapest). 1yr return ~+30-35%, 5yr annualized ~+17-18%, 10yr ~+16%. Minimal tracking error (<0.05%). Dividend yield ~0.5%.

COMPETITIVE LANDSCAPE
SCHG (Schwab) matches on cost (0.04%); IWF (iShares) broader but 0.19%. VUG's liquidity and AUM advantage for institutional investors.

KEY RISKS & OPPORTUNITIES
Bull: AI/tech capex cycle continues; cheapest way to access US growth.
Bear: Extreme concentration in 7-8 names; P/E 30-35x forward; interest rate sensitivity; value rotation risk.

SUITABILITY & VALUATION
Weighted-average P/E ~30-35x forward. P/B ~10-12x. Near upper end of historical range. For a value fund, fundamentally expensive and overweight crowded trades.

RECOMMENDATION: HOLD / AVOID for value mandates -- High conviction.
Excellent product (low cost, liquid) but not a value investment. Concentrated in expensive mega-cap tech. Use only as tactical allocation.

3-YEAR OUTLOOK
2025: AI capex supports mega-cap earnings. 2026: Risk of mean reversion if AI monetization disappoints.
2027: Possible sector rotation as value/small-cap cycles tend to follow extended growth outperformance."""

REPORTS['TSM'] = """COMPANY HISTORY & MANAGEMENT
Founded 1987 by Morris Chang. Pioneered pure-play foundry model. Chairman & CEO C.C. Wei (CEO since 2018, Chairman 2024). CFO Wendell Huang. Management widely regarded as best-in-class in semiconductors.

BUSINESS MODEL
Manufactures chips for fabless customers. Revenue: Smartphones ~33%, HPC/AI/data center ~51%, IoT ~6%, Automotive ~5%. Leading-edge (3nm/5nm) ~60% of revenue. Premium pricing on advanced nodes.

FINANCIAL HEALTH
FY2024 Revenue: ~NT$2.9T (~$90B USD, +30% YoY). Gross margin: ~57-58%. Operating margin: ~47-48%. ROE: ~30%. Net cash positive (~$60-70B cash, ~$30B debt). Capex: $38-42B guided for 2025, funded from operations (~$40B+ OCF). Dividend yield: ~1.2%.

COMPETITIVE LANDSCAPE
TSMC (~60% foundry share) vs Samsung (~12%), Intel Foundry (~1%), GlobalFoundries (~6%). Technology leadership 2+ years ahead, manufacturing yield superiority, customer lock-in. Every major AI chip (NVIDIA, AMD, Apple) manufactured at TSMC. No credible alternative at leading-edge.

KEY RISKS & OPPORTUNITIES
Bull: AI demand structural/multi-year; 2nm ramp extends lead; Arizona/Japan fabs diversify geopolitical risk; margins expand.
Bear: Taiwan Strait geopolitical risk (existential overhang); cyclical downturn possible 2026; customer concentration (Apple+NVIDIA ~40%).

MANAGEMENT COMPENSATION
CEO Wei ~$6-8M (modest by US standards), weighted toward base + profitability bonuses. Not US-style stock option packages. Aligned but low equity incentive.

VALUATION ANALYSIS
P/B: ~53.8x (ADR-based, reflects premium). Forward P/E: ~20x. EV/EBITDA: ~15-17x. PEG ~1.0x. Reasonable for 25%+ growth with 57% margins. Trades at geopolitical discount vs ASML (~30x) and NVIDIA (~30x).

RECOMMENDATION: BUY -- Medium-High conviction. 2-3 year horizon.
Generational franchise at geopolitical discount. AI capex provides multi-year earnings visibility. Position size 2-4% reflecting Taiwan tail risk.

3-YEAR TIMELINE
2025: 2nm ramp begins; Arizona Fab 1 volume production; revenue +25%.
2026: AI broadens training to inference; potential margin expansion to 60%+.
2027: A16 (1.6nm) enters production; Japan fab operational."""

REPORTS['IREN'] = """COMPANY HISTORY & MANAGEMENT
Formerly Iris Energy, rebranded 2024. Founded 2018 in Sydney by Daniel and William Roberts (dual co-CEOs). Started as Bitcoin miner using renewable energy, pivoting to AI/HPC data center services. Dual-CEO structure raises governance questions.

BUSINESS MODEL
Two lines: (1) Bitcoin mining (~85-90% of revenue), (2) AI Cloud/HPC hosting (nascent). Sites in British Columbia and Texas, substantially renewable powered. AI pivot involves GPU capacity (NVIDIA H100/H200 clusters).

FINANCIAL HEALTH
Revenue FY2024: ~$180-200M. Gross margin: ~40-50% (variable, Bitcoin-dependent). Earnings quality poor -- highly volatile. Debt: ~$300-400M (convertible notes). Cash: ~$100-200M. Extremely capital-hungry.

COMPETITIVE LANDSCAPE
Core Scientific (similar AI pivot), Marathon Digital (~35 EH/s), Hut 8 (~20 EH/s). IREN's renewable angle is differentiator but not decisive moat.

KEY RISKS & OPPORTUNITIES
Bull: AI/HPC data center demand exploding; power-ready sites scarce; successful pivot re-rates from "crypto miner" to "AI infrastructure" multiple.
Bear: Bitcoin mining is commodity business with no moat; AI pivot unproven/capital-intensive; dual-CEO red flag; dilution risk high; narrative-driven stock.

MANAGEMENT COMPENSATION
Roberts brothers ~$3-5M+ each including SBC. Elevated SBC relative to revenue. Alignment moderate -- meaningful equity but dilution erodes existing shareholders.

VALUATION ANALYSIS
Market cap: ~$15B. P/E: Not meaningful. P/B: ~6.1x. EV/Revenue: ~15-20x (extremely expensive). Speculative, narrative-driven valuation pricing in unproven AI pivot.

RECOMMENDATION: SELL / AVOID -- High conviction.
Antithetical to value mandate. Unprofitable on sustainable basis, tied to Bitcoin volatility, inexperienced management, governance red flag, priced for perfection. No margin of safety.

3-YEAR TIMELINE
2025: Bitcoin halving compresses mining margins; AI revenue ramp is key catalyst.
2026: Must demonstrate $100M+ AI revenue to justify valuation; likely further dilution.
2027: If AI pivot succeeds, re-rating; if fails, stock declines 50-70%."""

REPORTS['LPTH'] = """COMPANY HISTORY & MANAGEMENT
Founded 1985, Orlando FL. Micro-cap manufacturer of precision optical and infrared components. CEO Sam Rubin (since 2019, ex-II-VI/Coherent). Long history of underperformance and restructuring.

BUSINESS MODEL
Designs/manufactures optical and IR lenses. Infrared products (~55-60%): chalcogenide glass for thermal imaging, defense, industrial. Visible optics (~40-45%): precision molded glass for telecom, medical. Key customers: L3Harris, Teledyne FLIR. Manufacturing in Orlando, Riga (Latvia), Jinan (China).

FINANCIAL HEALTH
Revenue FY2024: ~$35-40M (flat). Gross margin: ~35-40%. Net income: near breakeven. Debt: ~$10-15M. Cash: ~$5-10M. Thin liquidity. Operating cash flow near breakeven.

COMPETITIVE LANDSCAPE
Dwarfed by II-VI/Coherent ($5B+ rev), Zygo/Ametek ($300M+), Ophir/MKS ($200M+). Niche player. Black Diamond (BD6) chalcogenide glass is closest to a moat but lacks scale.

KEY RISKS & OPPORTUNITIES
Bull: Defense spending tailwinds; ITAR-compliant US manufacturing advantage; BD glass adoption in automotive ADAS thermal sensing; acquisition target.
Bear: Perpetually "almost profitable" -- classic value trap; micro-cap with low liquidity; China manufacturing creates geopolitical risk.

MANAGEMENT COMPENSATION
CEO ~$1-2M total. Reasonable for micro-cap. SBC relative to profitability is a concern. Board small, insider ownership moderate.

VALUATION ANALYSIS
P/B: ~23.6x (elevated for negligible earnings). P/E: N/M. EV/Revenue: ~3-4x (above ~2x typical). Stock periodically spikes on defense narratives then gives back gains.

RECOMMENDATION: AVOID / SPECULATIVE HOLD -- Medium conviction. 3+ years if held.
Classic micro-cap value trap. Interesting technology (BD chalcogenide) but unable to translate to profitability. Illiquid. Only case is acquisition target -- not disciplined value strategy. If held, <0.5% position.

3-YEAR TIMELINE
2025: Defense budget increases; IR bookings key metric. 2026: Revenue must hit $45M+ for profitability inflection.
2027: Either validates as profitable niche player ($8-12+ stock) or remains stuck ($3-5)."""

REPORTS['CCJ'] = """COMPANY HISTORY & MANAGEMENT
Founded 1988 via merger of Eldorado Nuclear and Saskatchewan Mining. World's largest publicly traded uranium producer. Headquartered Saskatoon, Canada. CEO Tim Gitzel since 2011. Strong operational track record. Acquired 49% of Westinghouse Electric (nuclear services) in 2023.

BUSINESS MODEL
Three segments: Uranium (~55% revenue), Fuel Services (~15%), and Westinghouse (~30%). Mines in northern Saskatchewan (McArthur River/Key Lake -- world's highest-grade uranium). Long-term contracts with utilities at fixed/market-related pricing. Value proposition: reliable uranium supply to nuclear power plants globally.

FINANCIAL HEALTH
Revenue FY2024: ~CAD$3.5-4B. Margins improving as legacy low-price contracts roll off. Net income volatile due to mark-to-market on uranium inventory. Balance sheet solid: moderate debt, ample liquidity. Westinghouse acquisition funded via equity + debt. FCF improving.

COMPETITIVE LANDSCAPE
Kazatomprom (Kazakhstan, ~25% global production), Orano (France), Uranium Energy Corp (US). Cameco holds ~15% global uranium market share. Moat: high-grade reserves, regulatory expertise, long-term utility relationships, Westinghouse vertical integration.

KEY RISKS & OPPORTUNITIES
Bull: Nuclear renaissance driven by AI data center power demand; uranium supply deficit; contract repricing at higher levels; Westinghouse synergies.
Bear: Uranium price volatility; geopolitical risks in Kazakhstan reduce competitor supply (already happened); regulatory delays on reactor builds; long commodity cycles.

MANAGEMENT COMPENSATION
CEO Gitzel ~CAD$8-10M total comp. Mix of base, bonus (tied to operational/financial targets), and equity. Reasonable for a major mining CEO. Aligned with long-term uranium cycle thesis.

VALUATION ANALYSIS
P/B: ~10.6x. P/E: ~137x trailing (depressed by accounting items). Forward P/E: ~85x. EV/EBITDA elevated. Priced for nuclear renaissance. Expensive on traditional metrics but uranium bull market may justify premium.

RECOMMENDATION: HOLD -- Moderate conviction. 2-3 year horizon.
Compelling thematic (nuclear/AI power demand) but valuation is stretched at ~85x forward earnings. Best entry on a pullback toward $80-90 range. Quality franchise in right place at right time.

3-YEAR TIMELINE
2025: McArthur River/Key Lake ramp to full production; uranium contract repricing cycle.
2026: Westinghouse synergy realization; new reactor builds begin globally.
2027: Potential uranium supply crunch if secondary supplies exhausted."""

REPORTS['SMR'] = """COMPANY HISTORY & MANAGEMENT
Founded 2007, Portland OR. Only company with NRC-approved small modular reactor design (VOYGR). Went public via SPAC 2022. CEO John Hopkins since 2018. Backed by Fluor Corp (~60% ownership). Canceled first project (UAMPS) in 2023 due to cost overruns, then pivoted to new opportunities.

BUSINESS MODEL
Pre-revenue company developing small modular nuclear reactors (77 MWe per module, deployable in arrays). Revenue: effectively zero (some DOE funding and engineering services). Business model relies on future reactor sales and services to utilities, industrial customers, and government. VOYGR design is the key asset.

FINANCIAL HEALTH
Revenue: minimal (~$10-20M from DOE/engineering). Operating loss: ~$(100-130)M annually. Cash: ~$200-300M (post-equity raises). Burn rate ~$25-30M/quarter. No debt (unusual for this stage). Cash runway ~2-3 years. Pre-revenue, pre-commercial.

COMPETITIVE LANDSCAPE
X-energy (TRISO fuel, Xe-100 reactor), Kairos Power (molten salt), TerraPower (Bill Gates-backed, sodium reactor), GE Hitachi (BWRX-300). NuScale's advantage: only NRC-certified design. Disadvantage: UAMPS cancellation damaged credibility; competitors catching up.

KEY RISKS & OPPORTUNITIES
Bull: Nuclear renaissance creates massive TAM; only NRC-certified SMR; AI data center demand for reliable baseload power; government support (DOE funding).
Bear: No orders since UAMPS cancellation; cost economics unproven at scale; competitors may leapfrog; massive cash burn with no revenue timeline; equity dilution risk.

MANAGEMENT COMPENSATION
CEO Hopkins ~$5-8M total, equity-heavy. Fluor's ownership provides alignment but also conflicts (Fluor as construction partner). Compensation high relative to pre-revenue stage.

VALUATION ANALYSIS
P/B: ~3.6x. Market cap: ~$5B. No P/E (negative earnings). EV/Revenue: extreme (100x+). Valuation entirely based on optionality and nuclear narrative. No fundamentals support current price.

RECOMMENDATION: SELL / AVOID -- High conviction.
Pre-revenue, cash-burning, with failed first project. NRC certification is valuable but unproven commercially. At ~$5B market cap for a company with no orders and $0 product revenue, this is pure speculation. Not suitable for value fund.

3-YEAR TIMELINE
2025: Must secure first commercial order to restore credibility; continued DOE funding.
2026: Site preparation for first deployment if order secured; manufacturing partnerships.
2027: Earliest possible construction start; still years from first revenue generation."""

REPORTS['V'] = """COMPANY HISTORY & MANAGEMENT
Founded 1958 as BankAmericard by Bank of America. IPO 2008 (largest US IPO at time). CEO Ryan McInerney since Feb 2023 (former President). CFO Chris Suh. World's largest payment network by transaction volume. One of the most durable franchises in financial services.

BUSINESS MODEL
Visa operates a payment network (not a bank -- takes no credit risk). Revenue from: service fees (~40%, based on payment volume), data processing fees (~40%, per-transaction), international transaction fees (~20%). Processes ~$15 trillion in payment volume annually across 200+ countries. 4.3B+ cards in circulation.

FINANCIAL HEALTH
FY2024 (Sept) Revenue: ~$35-36B (+10% YoY). Operating margin: ~67% (among highest of any public company). Net income: ~$20-21B. ROE: ~45-50%. FCF: ~$19-20B. Balance sheet: moderate debt (~$20B) but overwhelmed by cash generation. Buybacks: ~$15B+ annually. Dividend yield: ~0.8%.

COMPETITIVE LANDSCAPE
Mastercard (similar model, slightly smaller). PayPal, Square/Block (digital payments). Apple Pay, Google Pay (wallet layer). Stripe, Adyen (merchant acquiring). Visa's moat is enormous: network effects, ubiquitous acceptance, regulatory barriers, brand trust.

KEY RISKS & OPPORTUNITIES
Bull: Digital payments penetration still growing (85% of transactions globally still cash); cross-border volumes recovering; new flows (B2B payments, real-time via Visa Direct); value-added services.
Bear: DOJ antitrust (debit routing practices); fintech disruption; central bank digital currencies; real-time payment networks (FedNow, PIX) bypass card rails.

MANAGEMENT COMPENSATION
CEO McInerney ~$20-25M total, heavily equity-based (PSUs tied to EPS growth, revenue, TSR). Well-aligned. Strong board governance.

VALUATION ANALYSIS
P/B: ~16.3x. Forward P/E: ~22x. EV/EBITDA: ~20x. FCF yield: ~3.0-3.5%. Historically trades 25-35x forward P/E. At ~22x forward, below 5-year average. Premium justified by quality -- 67% operating margins, 10%+ revenue growth, dominant market position.

RECOMMENDATION: BUY -- High conviction. 2-3 year horizon.
Visa is a best-in-class compounder trading slightly below historical multiples. The 67% operating margin, massive FCF, and secular tailwind (cash-to-digital conversion) create a rare combination. Antitrust risk is manageable. One of few stocks a value fund can own for quality at a reasonable price.

3-YEAR TIMELINE
2025: Cross-border volumes normalize; Visa Direct ramp; DOJ case developments.
2026: B2B payments and value-added services drive revenue diversification; potential EPS $12+.
2027: Digital payments penetration deepens; EPS potentially $14+ supporting $350+ stock price."""

REPORTS['FORM'] = """COMPANY HISTORY & MANAGEMENT
Founded 1993, Livermore CA. Leading provider of semiconductor probe cards and test sockets. CEO Mike Slessor since 2018. IPO 2003. Serves virtually all major semiconductor manufacturers. Key beneficiary of advanced packaging and HBM (High Bandwidth Memory) trends.

BUSINESS MODEL
Two segments: Probe Cards (~80% revenue) and Systems (~20%). Probe cards are consumable test interfaces used in semiconductor wafer testing. Key customers: Samsung, SK Hynix, Micron, Intel, TSMC, and AI chip designers. Revenue FY2024: ~$710-750M. Value proposition: precision test technology critical for yield optimization in advanced semiconductor manufacturing.

FINANCIAL HEALTH
Revenue: ~$710-750M (+20%+ YoY, driven by HBM and AI chip demand). Gross margin: ~45-48%. Operating margin: ~15-18%. Net income: ~$80-100M. Balance sheet: net cash (~$250M cash, minimal debt). ROE: ~12-15%. FCF: ~$100-120M. Strong financial position with no leverage concerns.

COMPETITIVE LANDSCAPE
Japan-based competitors: MPI Corp, Technoprobe (Italy). FormFactor is the clear #1 in advanced probe cards, especially for DRAM/HBM testing. Moat: technology leadership in advanced node probe cards, customer switching costs, long qualification cycles.

KEY RISKS & OPPORTUNITIES
Bull: HBM demand explosion (AI training requires massive HBM capacity); advanced packaging drives probe card complexity and ASP growth; market consolidation benefits leader; potential $1B+ revenue by 2026.
Bear: Customer concentration risk (Samsung, SK Hynix); semiconductor cycle downturn; technology disruption in testing methodology; competition from Asian manufacturers.

MANAGEMENT COMPENSATION
CEO Slessor ~$8-10M total, equity-heavy. Metrics tied to revenue growth and operating margins. Well-aligned with semiconductor cycle upside.

VALUATION ANALYSIS
P/B: ~7.1x. Trailing P/E: ~138x (reflecting ramp year). Forward P/E: ~43x. EV/Revenue: ~10x. Rich on trailing metrics but forward earnings are key -- consensus expects significant earnings ramp. For a semiconductor equipment company with 45%+ gross margins benefiting from AI/HBM megatrend, the multiple may be justified.

RECOMMENDATION: HOLD -- Moderate conviction. 18-24 month horizon.
Quality niche player in the right market at the right time. At ~43x forward P/E, priced for significant execution. Would become a BUY on pullback to ~30x forward P/E. AI/HBM tailwind is real but already reflected in price.

3-YEAR TIMELINE
2025: HBM3e probe card ramp; potential revenue approaching $800M-$1B.
2026: Next-gen HBM4 testing; advanced packaging expansion; $1B+ revenue target.
2027: AI infrastructure buildout matures -- watch for cyclical peak signals."""

REPORTS['ANF'] = """COMPANY HISTORY & MANAGEMENT
Founded 1892 as outdoor sporting goods. Reinvented 1990s as youth lifestyle brand. Prolonged decline 2012-2020 followed by remarkable turnaround under CEO Fran Horowitz (since 2017, ex-Ann Taylor/Express). Shifted brand to mid-20s to 30s demographic, cleaned marketing, invested in digital.

BUSINESS MODEL
Two brands: Abercrombie & Fitch (~55% revenue) and Hollister (~45%). ~750 stores globally + e-commerce (~30%+ of sales). Accessible premium casual wear ($40-$120). FY2024 revenue ~$4.3B (+16% YoY). North America ~80%.

FINANCIAL HEALTH
Operating margins expanded to ~15% (from low single digits 2020). ROE >60%. Net cash position (~$600M+ cash, minimal debt). FCF ~$500M. Inventory management disciplined, reducing markdown risk.

COMPETITIVE LANDSCAPE
American Eagle (AEO), Gap Inc, PVH, Lululemon. No durable moat -- edge is execution (brand repositioning, assortment, supply chain agility). Fashion business; moats thin and fleeting.

KEY RISKS & OPPORTUNITIES
Bull: Share gains in $300B+ US apparel market; international expansion; margin expansion toward 18%+ as DTC grows.
Bear: Fashion risk -- one bad season resets sentiment. Comps increasingly difficult. Consumer spending softening. Stock already re-rated from $15 (2020) to $150+.

MANAGEMENT COMPENSATION
CEO Horowitz ~$17M FY2023. 15% base, 20% cash bonus, 65% equity (PSUs tied to revenue, margin, TSR). Reasonably aligned.

VALUATION ANALYSIS
P/B: ~3.2x. P/E: ~9x. EV/Sales: ~1.0x. Reasonable for retailer but assumes sustained execution. Historical P/B was <1x from 2017-2020. Premium on growth, but apparel multiples compress fast.

RECOMMENDATION: HOLD -- Moderate conviction. 12-18 months.
Turnaround is real but stock has re-rated substantially. At 9x earnings, not cheap for fashion retailer with no structural moat. BUY on pullback to ~$70 (7-8x earnings).

3-YEAR TIMELINE
2025: Watch for comp deceleration. 2025-2026: International expansion (Middle East, APAC).
2026: Hollister brand refresh cycle -- key test. 2027: Capital allocation (buybacks vs reinvestment) critical."""

REPORTS['AMD'] = """COMPANY HISTORY & MANAGEMENT
Founded 1969. CEO Lisa Su (since 2014) engineered one of tech's greatest turnarounds. PhD EE from MIT. Oversaw Zen architecture, Xilinx acquisition ($49B, 2022), AI accelerator entry. CFO Jean Hu (since 2022, ex-Marvell).

BUSINESS MODEL
Revenue ~$23B FY2024: Data Center (~50%, EPYC CPUs + MI300 AI GPUs + Xilinx FPGAs), Client (~25%, Ryzen CPUs), Gaming (~10%), Embedded (~15%). Key growth: Data Center gaining share in compute (vs Intel) and AI (vs NVIDIA).

FINANCIAL HEALTH
Revenue ~$23B (+10% YoY). Gross margins ~52%, expanding with Data Center mix. Operating margin ~22%. Net income ~$4B. Net cash ~$4B ($6B cash, $2B debt). FCF ~$4.5B. ROE ~5-6% (depressed by $49B Xilinx goodwill). Healthy balance sheet.

COMPETITIVE LANDSCAPE
Server CPU: gaining vs Intel (~25% share, from <5% in 2018). AI GPU: distant #2 to NVIDIA (80%+ AI training share, CUDA moat). Client: strong #2 in x86. FPGA: co-leader. Moderate moat: TSMC access, Zen IP, but CUDA dominance is key headwind.

KEY RISKS & OPPORTUNITIES
Bull: AI GPU revenue ramps to $10B+; EPYC takes 40%+ server share; $35B+ revenue by 2027 with margin expansion.
Bear: CUDA lock-in limits MI300/MI400; custom silicon (Google TPU, Amazon Trainium) disintermediates; Xilinx underdelivers.

MANAGEMENT COMPENSATION
CEO Su ~$30M total FY2023. PSUs tied to revenue, EPS, TSR. Heavy equity weighting aligned. Pay-for-performance arguably excellent ($200B+ value created since 2014).

VALUATION ANALYSIS
P/B: ~5.6x. Forward P/E: ~20x. EV/Sales: ~15x. Rich vs Intel (~15x) but discounted vs NVIDIA (~30x forward). Justified only if AI GPU scales. PEG ~1.0x reasonable.

RECOMMENDATION: HOLD -- Moderate conviction. 18-24 months.
High-quality at fair-to-full price. At ~20x forward, digestible. BUY on pullback below $180 (~17x forward) or clear MI300/MI400 hyperscaler wins.

3-YEAR TIMELINE
2025: MI350 launch (critical for AI relevance); EPYC Turin ramp; 30%+ server share target.
2026: MI400 series; Xilinx AI inference FPGA refresh.
2027: AI market maturation -- does AMD hold 15%+ GPU share or get squeezed?"""

REPORTS['BTU'] = """COMPANY HISTORY & MANAGEMENT
World's largest private-sector coal company. Founded 1883. Chapter 11 bankruptcy 2016, emerged 2017. CEO Jim Grech (since 2020, ex-Foresight Energy). CFO Mark Spurbeck. Post-bankruptcy management focused on deleveraging and cash returns.

BUSINESS MODEL
Revenue ~$4.2B FY2024: Seaborne Thermal & Met coal (~55%, higher margin, sold to Asian/European utilities and steelmakers) and US Thermal (~45%, domestic utility contracts). Mines in Wyoming (PRB), Illinois Basin, Australia (Queensland). Commodity producer with limited pricing power.

FINANCIAL HEALTH
Revenue ~$4.2B (down from $5.5B peak FY2022). Operating margins ~15%. Net income ~$500M. Balance sheet dramatically repaired: net cash (~$800M cash vs ~$300M debt). FCF yield ~15-20%. Aggressive buybacks ($1B+ authorized). Mine reclamation liabilities ~$700M (hidden obligation).

COMPETITIVE LANDSCAPE
Arch Resources/CONSOL (higher met exposure), Alliance Resource (IL Basin, strong dividend), Glencore (largest coal trader), Whitehaven (Australian). Peabody's advantage: scale + geographic diversification. No moat -- commodity business. Low-cost position in PRB provides some advantage.

KEY RISKS & OPPORTUNITIES
Bull: Global coal demand resilient (India, SE Asia); seaborne prices elevated ($100+/ton); deep value at 3-4x earnings with 15%+ FCF yield; buybacks highly accretive.
Bear: Structural coal demand decline (renewables); ESG capital flight; US thermal contracts roll lower; carbon tax risk; reclamation liabilities.

MANAGEMENT COMPENSATION
CEO Grech ~$7M total FY2023. EBITDA/FCF/safety metrics. Appropriate for commodity business. Aggressive buyback signals alignment.

VALUATION ANALYSIS
P/B: ~1.3x. Forward P/E: ~10x. EV/Sales: ~0.7x. Optically cheap but reflects terminal value concerns. Coal stocks always look cheap -- question is value trap vs genuine deep value.

RECOMMENDATION: SPECULATIVE BUY -- Low conviction. 12-18 months.
Interesting for contrarian value fund. At <10x forward earnings and net cash, downside limited if coal prices hold. Buyback highly accretive. But structurally declining industry + ESG constraints = persistent discount. Position 1-2% max. Cash return story, not growth.

3-YEAR TIMELINE
2025: Seaborne prices key driver; continued buybacks. 2025-2026: Indian demand trajectory bullish for seaborne.
2026: US thermal contract renewals -- pricing critical. 2027: Coal demand durability test."""

REPORTS['SGMO'] = """COMPANY HISTORY & MANAGEMENT
Founded 1995, Richmond CA. Genomic medicine company using proprietary zinc finger nuclease (ZFN) platform. CEO Sandy MacRae (since 2020, ex-Sarepta). Turbulent history -- promising technology but persistent clinical/commercial failures. Multiple leadership changes.

BUSINESS MODEL
Clinical-stage biotech with effectively zero product revenue. Income from collaboration agreements (Pfizer, Sanofi, Biogen -- several terminated). Burns cash for R&D on ZFN gene editing/therapy pipeline. Key programs: hemophilia A (with Pfizer, terminated), Fabry disease, neurological conditions.

FINANCIAL HEALTH
Cash: ~$50-80M (declining, ~$25-35M quarterly burn). Revenue negligible (~$20-40M from declining collaborations). Operating losses ~$100-150M/year. Repeated dilutive equity offerings. Cash runway 6-12 months without new financing. Book value eroding steadily.

COMPETITIVE LANDSCAPE
CRISPR Therapeutics (FDA-approved Casgevy), Editas, Intellia (in-vivo lead), Beam (base editing). ZFN technology largely leapfrogged by CRISPR approaches -- cheaper, more flexible, further along. Negligible competitive moat.

KEY RISKS & OPPORTUNITIES
Bull: ZFN validated in clinical readout; pharma partnership restores funding; acquisition for IP; epigenetic editing pivot differentiates.
Bear: Cash runs out; further dilution; pipeline fails; technology obsolete vs CRISPR; delisting risk. Going concern situation.

MANAGEMENT COMPENSATION
CEO ~$5-7M (FY2023), heavy on equity (arguably worthless given stock decline from $20 to <$2). Cash burn on G&A relative to market cap raises alignment questions.

VALUATION ANALYSIS
Market cap: ~$149M. P/B: ~21x but book is essentially burning cash. No meaningful earnings-based valuation. Priced for optionality (pipeline success or acquisition) but probability-weighted value questionable.

RECOMMENDATION: SELL / AVOID -- High conviction. Immediate.
Not appropriate for value fund. No margin of safety, no earnings, no competitive advantage, going concern risk. ZFN competitively surpassed. Speculative biotech lottery ticket.

3-YEAR TIMELINE
2025: Critical cash runway -- needs financing or partnership.
2025-2026: Pipeline readouts (binary but low probability of success given track record).
2026-2027: Likely acquisition at modest premium, reverse merger, further dilution, or wind-down."""

REPORTS['BMNR'] = """COMPANY HISTORY & MANAGEMENT
Originally Comportment Inc. (shell company). Pivoted to Bitcoin mining with immersion cooling, rebranding as BitMine Immersion Technologies. OTC-listed -- immediate governance and liquidity red flags. Management has limited public track records. Information sparse.

BUSINESS MODEL
Bitcoin mining facilities using immersion cooling (hardware submerged in dielectric fluid). Revenue from mining rewards and potentially hosting. Operations in multiple US states. Revenue minimal (<$5M/year). Entirely Bitcoin price dependent, no diversification.

FINANCIAL HEALTH
OTC-listed nano-cap with limited/less reliable disclosures. Revenue minimal. Unprofitable. Cash reserves negligible. Funded through repeated dilutive equity issuances (classic OTC red flag). Share count expanded dramatically. No meaningful balance sheet strength.

COMPETITIVE LANDSCAPE
Marathon Digital (~25 EH/s, NYSE), Riot Platforms (~12 EH/s), CleanSpark, Hut 8. BMNR's hash rate is a rounding error. No competitive advantage -- immersion cooling available to all. No scale, no power purchase agreements, no moat.

KEY RISKS & OPPORTUNITIES
Bull: Bitcoin $200K+ lifts all miners; immersion cooling proves differentiator; scaling plan executes.
Bear: Chronic dilution destroys per-share value regardless of BTC price; OTC governance insufficient; management self-enrichment risk; never reaches scale; illiquid exit.

MANAGEMENT COMPENSATION
Detailed data unavailable (OTC). In typical OTC mining micro-caps: stock issuance, consulting fees, related-party transactions. Opacity is serious concern.

VALUATION ANALYSIS
P/B: ~0.8x (optically cheap but asset values questionable). No reliable P/E (no earnings). EV/Sales astronomical. Highly volatile stock. Speculative instrument, not value investment. Shell company origin + dilution history = extreme skepticism warranted.

RECOMMENDATION: STRONG SELL / DO NOT TOUCH -- Maximum conviction.
Entirely unsuitable for institutional fund. OTC, nano-cap, chronic dilution, opaque governance, shell origins, commodity BTC dependence. Near-complete absence of value investing qualities. No price acceptable for fiduciary.

3-YEAR TIMELINE
2025: Continued share issuance; potential reverse splits.
2025-2026: Secures capital and scales (low probability) or continues to dilute.
2027: Most probable: minimal operations, further dilution, or shell restructuring."""

# ── PDF Generation ────────────────────────────────────────────────────────────

class CompanyPDF(FPDF):
    def __init__(self, company_name, ticker):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.company_name = company_name
        self.ticker = ticker

    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, f'{self.company_name} ({self.ticker}) - Equity Research Report', align='R', new_x="LMARGIN", new_y="NEXT")
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()} | Generated Feb 2026 | Data sources: yfinance, SEC filings, public data', align='C')


def fmt_num(val, prefix='', suffix='', decimals=2):
    if val is None:
        return 'N/A'
    if isinstance(val, str):
        return val
    if abs(val) >= 1e12:
        return f'{prefix}{val/1e12:.1f}T{suffix}'
    if abs(val) >= 1e9:
        return f'{prefix}{val/1e9:.1f}B{suffix}'
    if abs(val) >= 1e6:
        return f'{prefix}{val/1e6:.1f}M{suffix}'
    return f'{prefix}{val:.{decimals}f}{suffix}'


def generate_pdf(ticker, data, report_text):
    company_name = data.get('company_name', ticker)
    pdf = CompanyPDF(company_name, ticker)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # ── Title ──
    pdf.set_font('Helvetica', 'B', 18)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 12, company_name, new_x="LMARGIN", new_y="NEXT")

    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(80, 80, 80)
    sector = data.get('sector', 'N/A')
    industry = data.get('industry', 'N/A')
    pdf.cell(0, 6, f'Ticker: {ticker}  |  Sector: {sector}  |  Industry: {industry}', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # ── Key Metrics Box ──
    pdf.set_fill_color(240, 245, 250)
    pdf.set_draw_color(180, 200, 220)
    y_start = pdf.get_y()
    pdf.rect(10, y_start, 190, 22, style='DF')

    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(0, 51, 102)

    metrics = [
        ('Price', fmt_num(data.get('current_price'), prefix='$')),
        ('Mkt Cap', fmt_num(data.get('market_cap'), prefix='$')),
        ('P/B', fmt_num(data.get('pb_ratio'), decimals=1) + 'x' if data.get('pb_ratio') else 'N/A'),
        ('P/E', fmt_num(data.get('pe_ratio'), decimals=1) + 'x' if data.get('pe_ratio') else 'N/A'),
        ('Fwd P/E', fmt_num(data.get('forward_pe'), decimals=1) + 'x' if data.get('forward_pe') else 'N/A'),
        ('12M Chg', fmt_num(data.get('price_change_12m'), suffix='%', decimals=1)),
    ]

    col_w = 190 / len(metrics)
    pdf.set_xy(10, y_start + 2)
    for label, val in metrics:
        pdf.cell(col_w, 5, label, align='C')
    pdf.ln()
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_x(10)
    for label, val in metrics:
        pdf.cell(col_w, 6, val, align='C')
    pdf.ln()

    extra_metrics = [
        ('52W High', fmt_num(data.get('price_52w_high'), prefix='$')),
        ('52W Low', fmt_num(data.get('price_52w_low'), prefix='$')),
        ('Book Value', fmt_num(data.get('book_value'), prefix='$')),
        ('Div Yield', fmt_num(data.get('dividend_yield'), suffix='%') if data.get('dividend_yield') else 'N/A'),
    ]
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(80, 80, 80)
    pdf.set_x(10)
    ex_w = 190 / len(extra_metrics)
    for label, val in extra_metrics:
        pdf.cell(ex_w, 5, f'{label}: {val}', align='C')

    pdf.set_xy(10, y_start + 24)
    pdf.ln(3)

    # ── Charts ──
    chart_path = data.get('chart_path', '')
    if chart_path and os.path.exists(chart_path):
        pdf.set_font('Helvetica', 'B', 12)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 8, 'Price History & P/B Ratio (12 Months)', new_x="LMARGIN", new_y="NEXT")
        pdf.image(chart_path, x=10, w=190)
        pdf.ln(5)

    # ── Research Report ──
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, 'Equity Research Report', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # Parse and render the report text by paragraphs
    paragraphs = report_text.strip().split('\n\n')
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        lines = para.split('\n')
        first_line = lines[0].strip()

        # Section headers (ALL CAPS lines)
        is_header = (first_line.isupper() and len(first_line) > 5) or \
                    first_line.startswith('RECOMMENDATION:') or \
                    first_line.startswith('3-YEAR')

        if is_header:
            pdf.ln(3)
            pdf.set_font('Helvetica', 'B', 10)
            pdf.set_text_color(0, 51, 102)
            pdf.set_x(10)
            pdf.multi_cell(w=190, h=5, text=first_line)
            pdf.ln(1)
            # Render remaining lines in the paragraph as body text
            body = ' '.join(l.strip() for l in lines[1:]).strip()
            if body:
                pdf.set_font('Helvetica', '', 9)
                pdf.set_text_color(30, 30, 30)
                pdf.set_x(10)
                pdf.multi_cell(w=190, h=4.5, text=body)
        else:
            # Combine all lines in paragraph
            full_text = ' '.join(l.strip() for l in lines).strip()
            if full_text.startswith('Bull:') or full_text.startswith('Bear:'):
                pdf.set_font('Helvetica', 'BI', 9)
                pdf.set_text_color(0, 0, 0)
            else:
                pdf.set_font('Helvetica', '', 9)
                pdf.set_text_color(30, 30, 30)
            pdf.set_x(10)
            pdf.multi_cell(w=190, h=4.5, text=full_text)
            pdf.ln(1)

    # ── Disclaimer ──
    pdf.ln(5)
    pdf.set_font('Helvetica', 'I', 7)
    pdf.set_text_color(128, 128, 128)
    pdf.multi_cell(0, 3.5, 'DISCLAIMER: This report is for informational purposes only and does not constitute investment advice. '
                   'Financial data sourced from yfinance and public filings (data through Q4 2025 or latest available). '
                   'All forward-looking statements involve uncertainty. Verify all figures against current SEC filings before making investment decisions.')

    # Save
    pdf_path = os.path.join(PDF_DIR, f'{ticker}_research_report.pdf')
    pdf.output(pdf_path)
    print(f'  Generated: {pdf_path}')
    return pdf_path


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('Generating PDF reports...\n')
    generated = []

    for ticker in all_data:
        data = all_data[ticker]
        if 'error' in data:
            print(f'  Skipping {ticker}: {data["error"]}')
            continue

        report = REPORTS.get(ticker, f'No research report available for {ticker}.')
        pdf_path = generate_pdf(ticker, data, report)
        generated.append(pdf_path)

    print(f'\nDone! Generated {len(generated)} PDFs in {PDF_DIR}')
