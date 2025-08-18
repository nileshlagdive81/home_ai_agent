"""
Real Estate Knowledge Base Service
Comprehensive Q&A system for real estate knowledge in India
"""

from typing import Dict, List, Optional, Tuple
import re

class RealEstateKnowledgeBase:
    """Knowledge base for real estate queries in India"""
    
    def __init__(self):
        """Initialize the knowledge base with comprehensive Q&A pairs"""
        self.knowledge_base = self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self) -> Dict[str, List[Dict]]:
        """Initialize the knowledge base with categorized Q&A pairs"""
        return {
            "terminology": [
                {
                    "question": "what is carpet area",
                    "keywords": ["carpet area", "carpet", "area", "what is carpet", "carpet area meaning"],
                    "answer": """<strong>🏠 Carpet Area:</strong><br><br>
                    <strong>Definition:</strong> Carpet area is the actual usable area within the walls of your apartment/house where you can lay a carpet.<br><br>
                    <strong>What's Included:</strong>
                    • Living room, bedrooms, kitchen, bathrooms<br>
                    • Internal walls and columns<br>
                    • Balcony area (50% of balcony)<br><br>
                    <strong>What's NOT Included:</strong>
                    • External walls thickness<br>
                    • Common areas (lobby, stairs, lift)<br>
                    • Terrace, garden, parking<br><br>
                    <strong>Formula:</strong> Carpet Area = Built-up Area - (Wall thickness + Common areas)<br><br>
                    <strong>Example:</strong> If built-up area is 1000 sq ft, carpet area might be 800-850 sq ft."""
                },
                {
                    "question": "what is built up area",
                    "keywords": ["built up area", "built-up", "builtup", "what is built up", "built up meaning"],
                    "answer": """<strong>🏗️ Built-up Area:</strong><br><br>
                    <strong>Definition:</strong> Built-up area includes carpet area plus the thickness of external walls, internal walls, and common areas.<br><br>
                    <strong>What's Included:</strong>
                    • Carpet area (usable space)<br>
                    • External wall thickness<br>
                    • Internal wall thickness<br>
                    • Common areas (lobby, stairs, lift)<br>
                    • Balcony (100% of balcony)<br><br>
                    <strong>Formula:</strong> Built-up Area = Carpet Area + Wall thickness + Common areas<br><br>
                    <strong>Example:</strong> If carpet area is 800 sq ft, built-up area might be 1000 sq ft."""
                },
                {
                    "question": "what is super built up area",
                    "keywords": ["super built up area", "super built-up", "super builtup", "what is super built up"],
                    "answer": """<strong>🏢 Super Built-up Area:</strong><br><br>
                    <strong>Definition:</strong> Super built-up area includes built-up area plus common facilities and amenities.<br><br>
                    <strong>What's Included:</strong>
                    • Built-up area<br>
                    • Common facilities (gym, pool, garden)<br>
                    • Corridors and lobbies<br>
                    • Lift and staircases<br>
                    • Parking areas<br>
                    • Clubhouse and amenities<br><br>
                    <strong>Formula:</strong> Super Built-up Area = Built-up Area + Common facilities + Amenities<br><br>
                    <strong>Example:</strong> If built-up area is 1000 sq ft, super built-up might be 1200-1400 sq ft.<br><br>
                    <strong>Note:</strong> This is what developers often quote as the total area."""
                },
                {
                    "question": "what is bhk",
                    "keywords": ["bhk", "bedroom", "bed room", "what is bhk", "bhk meaning", "bedroom hall kitchen"],
                    "answer": """<strong>🛏️ BHK (Bedroom, Hall, Kitchen):</strong><br><br>
                    <strong>Definition:</strong> BHK is a standard way to describe the layout of residential properties in India.<br><br>
                    <strong>Components:</strong>
                    • <strong>B</strong> = Bedroom(s)<br>
                    • <strong>H</strong> = Hall (Living room)<br>
                    • <strong>K</strong> = Kitchen<br><br>
                    <strong>Common BHK Types:</strong>
                    • <strong>1 BHK:</strong> 1 Bedroom + 1 Hall + 1 Kitchen<br>
                    • <strong>2 BHK:</strong> 2 Bedrooms + 1 Hall + 1 Kitchen<br>
                    • <strong>3 BHK:</strong> 3 Bedrooms + 1 Hall + 1 Kitchen<br>
                    • <strong>2.5 BHK:</strong> 2 Bedrooms + 1 Hall + 1 Kitchen + 1 Study/Pooja room<br><br>
                    <strong>Example:</strong> 2 BHK means you get 2 bedrooms, 1 living room, and 1 kitchen."""
                },
                {
                    "question": "what is roi in real estate",
                    "keywords": ["roi", "return on investment", "what is roi", "roi meaning", "return on investment real estate"],
                    "answer": """<strong>💰 ROI (Return on Investment):</strong><br><br>
                    <strong>Definition:</strong> ROI measures the profitability of your real estate investment.<br><br>
                    <strong>Formula:</strong> ROI = ((Current Value - Purchase Price) / Purchase Price) × 100<br><br>
                    <strong>Types of ROI:</strong>
                    • <strong>Rental ROI:</strong> Annual rental income / Property cost<br>
                    • <strong>Appreciation ROI:</strong> Increase in property value over time<br>
                    • <strong>Total ROI:</strong> Rental income + Appreciation<br><br>
                    <strong>Example:</strong> If you bought a property for ₹50 lakhs and it's now worth ₹60 lakhs:<br>
                    ROI = ((60 - 50) / 50) × 100 = 20%<br><br>
                    <strong>Good ROI Range:</strong> 6-12% annually for rental properties."""
                }
            ],
            "legal_regulatory": [
                {
                    "question": "what is rera",
                    "keywords": ["rera", "real estate regulation act", "what is rera", "rera act", "real estate regulation"],
                    "answer": """<strong>⚖️ RERA (Real Estate Regulation and Development Act):</strong><br><br>
                    <strong>Definition:</strong> RERA is a law enacted by the Indian government to protect homebuyers and bring transparency to the real estate sector.<br><br>
                    <strong>Key Features:</strong>
                    • <strong>Project Registration:</strong> All projects must be registered with RERA<br>
                    • <strong>Transparency:</strong> Developers must disclose project details, approvals, and timelines<br>
                    • <strong>Escrow Account:</strong> 70% of project funds must be in separate bank accounts<br>
                    • <strong>Timeline Compliance:</strong> Developers must complete projects on time<br>
                    • <strong>Compensation:</strong> Homebuyers can claim compensation for delays<br><br>
                    <strong>Benefits for Buyers:</strong>
                    • Protection against project delays<br>
                    • Transparent project information<br>
                    • Legal recourse for grievances<br>
                    • Standardized sale agreements<br><br>
                    <strong>RERA Website:</strong> Check your state's RERA website for project details."""
                },
                {
                    "question": "what documents needed for home loan",
                    "keywords": ["documents", "home loan", "documents needed", "home loan documents", "required documents"],
                    "answer": """<strong>📋 Documents Required for Home Loan:</strong><br><br>
                    <strong>Personal Documents:</strong>
                    • PAN Card<br>
                    • Aadhaar Card<br>
                    • Passport size photographs<br>
                    • Address proof (Utility bills, Rental agreement)<br><br>
                    <strong>Income Documents:</strong>
                    • Salary slips (last 3 months)<br>
                    • Bank statements (last 6 months)<br>
                    • Form 16 or IT returns (last 2 years)<br>
                    • Employment certificate<br><br>
                    <strong>Property Documents:</strong>
                    • Sale deed/Agreement to sell<br>
                    • Property tax receipts<br>
                    • NOC from society/builder<br>
                    • Approved building plan<br>
                    • Encumbrance certificate<br><br>
                    <strong>Additional Documents:</strong>
                    • Down payment proof<br>
                    • Property insurance<br>
                    • Legal opinion report<br><br>
                    <strong>Note:</strong> Requirements may vary between banks and loan types."""
                },
                {
                    "question": "what is stamp duty",
                    "keywords": ["stamp duty", "what is stamp duty", "stamp duty meaning", "registration charges"],
                    "answer": """<strong>🖋️ Stamp Duty:</strong><br><br>
                    <strong>Definition:</strong> Stamp duty is a tax levied by state governments on property transactions.<br><br>
                    <strong>When Applicable:</strong>
                    • Property purchase<br>
                    • Property sale<br>
                    • Property transfer<br>
                    • Lease agreements<br><br>
                    <strong>Rates (Varies by State):</strong>
                    • <strong>Maharashtra:</strong> 5-6% of property value<br>
                    • <strong>Delhi:</strong> 4-6% of property value<br>
                    • <strong>Karnataka:</strong> 5-6% of property value<br>
                    • <strong>Tamil Nadu:</strong> 7-8% of property value<br><br>
                    <strong>Calculation:</strong> Stamp Duty = Property Value × State Rate<br><br>
                    <strong>Example:</strong> For ₹50 lakh property in Maharashtra:<br>
                    Stamp Duty = 50,00,000 × 0.06 = ₹3,00,000<br><br>
                    <strong>Payment:</strong> Must be paid before property registration."""
                },
                {
                    "question": "what is gst in real estate",
                    "keywords": ["gst", "goods and services tax", "what is gst", "gst real estate", "gst property"],
                    "answer": """<strong>🏢 GST in Real Estate:</strong><br><br>
                    <strong>Definition:</strong> GST is a tax levied on construction and real estate services.<br><br>
                    <strong>Applicability:</strong>
                    • Under-construction properties<br>
                    • Ready-to-move properties (if construction completed after July 2017)<br>
                    • Commercial properties<br><br>
                    <strong>GST Rates:</strong>
                    • <strong>Affordable Housing:</strong> 1% (without ITC)<br>
                    • <strong>Regular Housing:</strong> 5% (without ITC)<br>
                    • <strong>Commercial Properties:</strong> 18%<br><br>
                    <strong>What's Included:</strong>
                    • Construction costs<br>
                    • Development charges<br>
                    • Basic amenities<br><br>
                    <strong>What's NOT Included:</strong>
                    • Land cost<br>
                    • Stamp duty<br>
                    • Registration charges<br><br>
                    <strong>Note:</strong> Ready-to-move properties are generally GST-free."""
                }
            ],
            "processes": [
                {
                    "question": "how to buy property in india",
                    "keywords": ["how to buy", "buying process", "property buying", "steps to buy", "buying home"],
                    "answer": """<strong>🏠 Complete Property Buying Process in India:</strong><br><br>
                    <strong>Step 1: Planning & Research</strong>
                    • Determine budget and requirements<br>
                    • Research locations and property types<br>
                    • Check property prices and trends<br><br>
                    <strong>Step 2: Property Search</strong>
                    • Visit properties and projects<br>
                    • Compare different options<br>
                    • Check developer reputation<br><br>
                    <strong>Step 3: Legal Verification</strong>
                    • Verify property documents<br>
                    • Check title and ownership<br>
                    • Verify approvals and NOCs<br><br>
                    <strong>Step 4: Financial Planning</strong>
                    • Arrange down payment<br>
                    • Apply for home loan<br>
                    • Calculate total costs (including taxes)<br><br>
                    <strong>Step 5: Negotiation & Agreement</strong>
                    • Negotiate price and terms<br>
                    • Sign agreement to sell<br>
                    • Pay booking amount<br><br>
                    <strong>Step 6: Documentation & Registration</strong>
                    • Complete loan formalities<br>
                    • Pay stamp duty and registration<br>
                    • Register sale deed<br><br>
                    <strong>Step 7: Possession</strong>
                    • Take property possession<br>
                    • Transfer utilities<br>
                    • Move in or rent out<br><br>
                    <strong>Timeline:</strong> 3-6 months for complete process"""
                },
                {
                    "question": "how to apply for home loan",
                    "keywords": ["home loan", "apply home loan", "how to apply", "loan application", "home loan process"],
                    "answer": """<strong>🏦 Home Loan Application Process:</strong><br><br>
                    <strong>Step 1: Eligibility Check</strong>
                    • Age: 21-65 years<br>
                    • Income: Minimum ₹25,000 per month<br>
                    • Credit score: 750+ (preferred)<br>
                    • Employment: Minimum 2 years experience<br><br>
                    <strong>Step 2: Choose Bank/NBFC</strong>
                    • Compare interest rates<br>
                    • Check processing fees<br>
                    • Compare loan terms<br>
                    • Read customer reviews<br><br>
                    <strong>Step 3: Calculate Loan Amount</strong>
                    • Down payment: 20-30% of property value<br>
                    • Loan amount: 70-80% of property value<br>
                    • EMI calculation based on income<br><br>
                    <strong>Step 4: Gather Documents</strong>
                    • Personal documents (PAN, Aadhaar)<br>
                    • Income documents (Salary slips, IT returns)<br>
                    • Property documents<br>
                    • Bank statements<br><br>
                    <strong>Step 5: Apply Online/Offline</strong>
                    • Fill application form<br>
                    • Submit documents<br>
                    • Pay processing fee<br><br>
                    <strong>Step 6: Verification & Approval</strong>
                    • Document verification<br>
                    • Property inspection<br>
                    • Credit appraisal<br>
                    • Loan sanction<br><br>
                    <strong>Step 7: Disbursement</strong>
                    • Sign loan agreement<br>
                    • Pay down payment<br>
                    • Loan disbursement<br><br>
                    <strong>Timeline:</strong> 15-30 days for approval"""
                },
                {
                    "question": "how to check property documents",
                    "keywords": ["check documents", "verify documents", "property verification", "document verification", "how to check"],
                    "answer": """<strong>📋 Property Document Verification Process:</strong><br><br>
                    <strong>Essential Documents to Check:</strong><br><br>
                    <strong>1. Title Documents:</strong>
                    • Sale Deed/Conveyance Deed<br>
                    • Mother Deed (original sale deed)<br>
                    • Partition Deed (if applicable)<br>
                    • Gift Deed (if applicable)<br><br>
                    <strong>2. Land Records:</strong>
                    • 7/12 Extract (Maharashtra)<br>
                    • Patta (Tamil Nadu)<br>
                    • Khata (Karnataka)<br>
                    • Mutation records<br><br>
                    <strong>3. Approvals & NOCs:</strong>
                    • Building approval plan<br>
                    • NOC from society/builder<br>
                    • Fire safety certificate<br>
                    • Environmental clearance<br><br>
                    <strong>4. Tax Documents:</strong>
                    • Property tax receipts<br>
                    • Water tax receipts<br>
                    • Electricity bills<br>
                    • Maintenance receipts<br><br>
                    <strong>Verification Steps:</strong>
                    • Visit local municipal office<br>
                    • Check with sub-registrar office<br>
                    • Verify with society/association<br>
                    • Consult legal expert<br><br>
                    <strong>Red Flags:</strong>
                    • Missing original documents<br>
                    • Pending litigation<br>
                    • Multiple owners without consent<br>
                    • Encroachment issues"""
                },
                {
                    "question": "what document to check for buying a flat",
                    "keywords": ["what document", "check for buying", "buying flat", "flat documents", "documents to check", "flat purchase documents", "what documents needed", "documents required", "documents to verify", "flat purchase verification", "buying apartment documents", "apartment documents", "flat buying checklist"],
                    "answer": """<strong>📋 Essential Documents to Check When Buying a Flat:</strong><br><br>
                    <strong>🏗️ Builder/Developer Documents:</strong>
                    • <strong>RERA Registration:</strong> Verify project is registered with RERA<br>
                    • <strong>Building Approval:</strong> Municipal corporation approval<br>
                    • <strong>Commencement Certificate:</strong> Permission to start construction<br>
                    • <strong>Completion Certificate:</strong> Building completion approval<br>
                    • <strong>Occupancy Certificate:</strong> Permission to occupy<br><br>
                    <strong>🏠 Property Title Documents:</strong>
                    • <strong>Sale Deed:</strong> Original property ownership document<br>
                    • <strong>Mother Deed:</strong> Previous sale deeds in chain<br>
                    • <strong>Land Records:</strong> 7/12 extract, mutation records<br>
                    • <strong>NOC from Society:</strong> If buying in existing society<br><br>
                    <strong>📋 Legal & Compliance:</strong>
                    • <strong>Encumbrance Certificate:</strong> No pending loans/liens<br>
                    • <strong>Property Tax Receipts:</strong> Up-to-date tax payments<br>
                    • <strong>Water & Electricity Bills:</strong> Current utility status<br>
                    • <strong>Fire Safety Certificate:</strong> Safety compliance<br><br>
                    <strong>💰 Financial Documents:</strong>
                    • <strong>Payment Receipts:</strong> All payment proofs<br>
                    • <strong>Loan Documents:</strong> If taking home loan<br>
                    • <strong>Insurance Papers:</strong> Property insurance<br><br>
                    <strong>🔍 Verification Checklist:</strong>
                    • Visit municipal office to verify approvals<br>
                    • Check RERA website for project status<br>
                    • Verify with sub-registrar office<br>
                    • Consult legal expert for title verification<br>
                    • Check for pending litigation<br><br>
                    <strong>⚠️ Red Flags to Watch:</strong>
                    • Missing original documents<br>
                    • Pending approvals or NOCs<br>
                    • Multiple owners without consent<br>
                    • Encroachment or litigation issues<br>
                    • Unregistered project (RERA violation)"""
                }
            ],
            "investment": [
                {
                    "question": "is real estate good investment",
                    "keywords": ["investment", "good investment", "real estate investment", "worth investing", "investment advice"],
                    "answer": """<strong>💰 Real Estate as an Investment:</strong><br><br>
                    <strong>Pros:</strong>
                    • <strong>Tangible Asset:</strong> Physical property you can see and touch<br>
                    • <strong>Appreciation:</strong> Property values generally increase over time<br>
                    • <strong>Rental Income:</strong> Regular monthly income from tenants<br>
                    • <strong>Tax Benefits:</strong> Deductions on home loan interest and property tax<br>
                    • <strong>Hedge Against Inflation:</strong> Property values rise with inflation<br>
                    • <strong>Leverage:</strong> Can buy with 20-30% down payment<br><br>
                    <strong>Cons:</strong>
                    • <strong>Illiquid:</strong> Takes time to sell<br>
                    • <strong>High Transaction Costs:</strong> Stamp duty, registration, brokerage<br>
                    • <strong>Maintenance:</strong> Regular repairs and upkeep required<br>
                    • <strong>Market Risk:</strong> Property values can decrease<br>
                    • <strong>Management:</strong> Finding tenants and managing property<br><br>
                    <strong>Best Investment Scenarios:</strong>
                    • Long-term investment (5+ years)<br>
                    • High-growth locations<br>
                    • Good rental demand<br>
                    • Stable income source<br><br>
                    <strong>Alternative Options:</strong>
                    • REITs (Real Estate Investment Trusts)<br>
                    • Real estate mutual funds<br>
                    • Property crowdfunding"""
                },
                {
                    "question": "how to calculate rental yield",
                    "keywords": ["rental yield", "calculate rental", "rental return", "yield calculation", "how to calculate"],
                    "answer": """<strong>📊 Rental Yield Calculation:</strong><br><br>
                    <strong>Definition:</strong> Rental yield is the annual rental income as a percentage of property value.<br><br>
                    <strong>Formula:</strong> Rental Yield = (Annual Rental Income / Property Value) × 100<br><br>
                    <strong>Example Calculation:</strong><br>
                    • Property Value: ₹50,00,000<br>
                    • Monthly Rent: ₹15,000<br>
                    • Annual Rent: ₹15,000 × 12 = ₹1,80,000<br>
                    • Rental Yield: (1,80,000 / 50,00,000) × 100 = 3.6%<br><br>
                    <strong>Types of Rental Yield:</strong>
                    • <strong>Gross Yield:</strong> Before expenses<br>
                    • <strong>Net Yield:</strong> After expenses<br><br>
                    <strong>Expenses to Consider:</strong>
                    • Property tax<br>
                    • Maintenance charges<br>
                    • Insurance<br>
                    • Repairs<br>
                    • Vacancy periods<br><br>
                    <strong>Good Rental Yield Range:</strong>
                    • <strong>Residential:</strong> 2-4% annually<br>
                    • <strong>Commercial:</strong> 6-10% annually<br>
                    • <strong>Retail:</strong> 8-12% annually<br><br>
                    <strong>Factors Affecting Yield:</strong>
                    • Location and demand<br>
                    • Property type and condition<br>
                    • Market conditions<br>
                    • Property management"""
                }
            ]
        }
    
    def search_knowledge(self, query: str) -> Optional[Dict]:
        """Search the knowledge base for relevant answers"""
        query_lower = query.lower().strip()
        
        # Search through all categories
        for category, qa_pairs in self.knowledge_base.items():
            for qa in qa_pairs:
                # Check if any keywords match
                if any(keyword in query_lower for keyword in qa["keywords"]):
                    return {
                        "category": category,
                        "question": qa["question"],
                        "answer": qa["answer"],
                        "confidence": 0.9
                    }
        
        # If no exact match, try fuzzy matching
        return self._fuzzy_search(query_lower)
    
    def _fuzzy_search(self, query: str) -> Optional[Dict]:
        """Perform fuzzy search for better matching"""
        best_match = None
        best_score = 0
        
        for category, qa_pairs in self.knowledge_base.items():
            for qa in qa_pairs:
                score = self._calculate_similarity(query, qa["question"])
                if score > best_score and score > 0.3:  # Minimum threshold
                    best_score = score
                    best_match = {
                        "category": category,
                        "question": qa["question"],
                        "answer": qa["answer"],
                        "confidence": score
                    }
        
        return best_match
    
    def _calculate_similarity(self, query: str, question: str) -> float:
        """Calculate similarity between query and question"""
        query_words = set(query.split())
        question_words = set(question.split())
        
        if not query_words or not question_words:
            return 0.0
        
        intersection = query_words.intersection(question_words)
        union = query_words.union(question_words)
        
        return len(intersection) / len(union)
    
    def get_knowledge_categories(self) -> List[str]:
        """Get list of available knowledge categories"""
        return list(self.knowledge_base.keys())
    
    def get_category_qa_pairs(self, category: str) -> List[Dict]:
        """Get all Q&A pairs for a specific category"""
        return self.knowledge_base.get(category, [])
    
    def add_qa_pair(self, category: str, question: str, keywords: List[str], answer: str):
        """Add a new Q&A pair to the knowledge base"""
        if category not in self.knowledge_base:
            self.knowledge_base[category] = []
        
        self.knowledge_base[category].append({
            "question": question.lower(),
            "keywords": [kw.lower() for kw in keywords],
            "answer": answer
        })
    
    def get_suggested_questions(self, category: str = None) -> List[str]:
        """Get suggested questions for users"""
        questions = []
        
        if category:
            qa_pairs = self.knowledge_base.get(category, [])
        else:
            # Get questions from all categories
            qa_pairs = []
            for cat_qa in self.knowledge_base.values():
                qa_pairs.extend(cat_qa)
        
        # Return first 5 questions as suggestions
        for qa in qa_pairs[:5]:
            questions.append(qa["question"].title())
        
        return questions
