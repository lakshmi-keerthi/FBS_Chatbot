import streamlit as st

# ---- Session Initialization ---- #
if "stage" not in st.session_state:
    st.session_state.stage = "start"
    st.session_state.flow_data = {}
    st.session_state.messages = []

def safe_rerun():
    try:
        st.experimental_rerun()
    except AttributeError:
        st.rerun()

def go_to_stage(stage_name, key=None, value=None):
    if key and value:
        st.session_state.flow_data[key] = value
    st.session_state.stage = stage_name
    safe_rerun()

# ---- Stage 1: Financial Priority ---- #
if st.session_state.stage == "start":
    st.title("💬 Chatty – FBS Financial Assistant")
    st.subheader("What is your financial priority?")

    if st.button("Investments"):
        go_to_stage("investments_goal", "priority", "Investments")
    if st.button("Retirement Solutions"):
        go_to_stage("retirement_status", "priority", "Retirement Solutions")
    if st.button("Financial Planning"):
        go_to_stage("financial_plan_type", "priority", "Financial Planning")

# ---- Investments Goal ---- #
elif st.session_state.stage == "investments_goal":
    st.title("Investments")
    st.subheader("What's your primary goal?")

    if st.button("Recurring Income"):
        go_to_stage("recurring_income", "goal", "Recurring Income")
    if st.button("Long-term Investment"):
        go_to_stage("details", "goal", "Long-term Investment")
    if st.button("Portfolio Management"):
        go_to_stage("details", "goal", "Portfolio Management")

# ---- Recurring Income Options ---- #
elif st.session_state.stage == "recurring_income":
    st.title("Recurring Income")
    st.subheader("Choose an option:")
    if st.button("Private Credit"):
        st.info("""
**Private Credit**  
• Targeted yields of 8% to 20%.  
• Direct security interests in real estate or operating assets.  
• Flexible terms with investor-aligned structuring.  
• Market independence, offering returns decoupled from public equity volatility.  

[Get Priority Access to Deals](https://chat.whatsapp.com/Gv9eQPwKxXa8LYr0ifenYh)
""")
    if st.button("Structured Note"):
        go_to_stage("structured_note")
    if st.button("Continue to Chat"):
        go_to_stage("chat")

# ---- Structured Note Section ---- #
elif st.session_state.stage == "structured_note":
    st.title("Structured Note")
    st.subheader("Details:")

    st.info("""
**Structured Notes**  
Structured Notes combine traditional bonds with derivatives to create customized investments aligned with specific risk and return goals. They can be linked to stocks, ETFs, or indices for tailored market exposure.

**Trusted Sourcing:** We work with top global institutions like JP Morgan, Morgan Stanley, Goldman Sachs, and Barclays.

**End-to-End Execution:** From auctioning to account setup, we manage the entire process for a seamless experience.

**Diversification:** Offers an alternative asset class with laddered income strategies diversified across issuers and timeframes—helping reduce overall portfolio risk.
""")

    st.subheader("What would you like to do?")
    if st.button("Explore Upcoming Notes"):
        st.info("Please explore upcoming notes through your advisor.")
    if st.button("I have questions"):
        st.info("Feel free to ask Chatty more about Structured Notes in chat.")
    if st.button("Back to Recurring Income"):
        go_to_stage("recurring_income")

# ---- Long-term Investment & Details ---- #
elif st.session_state.stage == "details":
    priority = st.session_state.flow_data["priority"]
    goal = st.session_state.flow_data["goal"]
    st.title(f"{priority} → {goal}")

    if priority == "Investments" and goal == "Long-term Investment":
        st.subheader("Our Investment Services:")
        if st.button("Private Funds"):
            st.info("""
**Private Funds**  
At FBS Securities, we provide access to carefully selected private investment opportunities aimed at enhancing diversification, targeting superior returns, and addressing the sophisticated needs of qualified investors. Each offering is backed by thorough due diligence, strategic structuring, and active oversight—with full transparency and fiduciary care.

**Key Benefits:**  
• Tax Efficiency & Credits  
• Diversification Beyond Public Markets  
• Enhanced Return Potential  
• Limited Market Correlation
""")
        if st.button("Model Portfolio"):
            st.info("""
**Model Portfolio**  
Our Investment Portfolio Management includes - Asset Allocation with Diversified Portfolios.

• Carefully curated allocations in large-cap holdings, dividend-yielding stocks, fixed-income securities, and sector-specific investments.  
• Our proprietary “GRO” model strategically combines income-generating assets, growth opportunities, and defensive sectors.  
• Crystal-clear insights, offering easy-to-understand insights into your portfolio’s performance. This empowers you to make confident, data-driven financial decisions.
""")
        if st.button("Continue to Chat"):
            go_to_stage("chat")

    elif priority == "Investments" and goal == "Portfolio Management":
        st.info("Diversified portfolios\nGRO model strategy\nClear performance insights.")
        if st.button("Continue to Chat"):
            go_to_stage("chat")

# ---- Retirement Status ---- #
elif st.session_state.stage == "retirement_status":
    st.title("Retirement Solutions")
    st.subheader("What is your employment status?")

    if st.button("Self-employed (1099)"):
        go_to_stage("self_employed", "goal", "Self-employed (1099)")
    if st.button("W2"):
        go_to_stage("w2", "goal", "W2")
    if st.button("Business owner"):
        go_to_stage("business_owner", "goal", "Business owner")

# ---- Self-employed Flow ---- #
elif st.session_state.stage == "self_employed":
    st.title("Self-employed (1099)")
    st.subheader("Do you have a solo 401(k)?")
    if st.button("Yes"):
        st.subheader("Are you looking to:")
        if st.button("Increase Contributions"):
            st.info("""
**CBP: Premier Retirement Solution**  
**Cash Balance Plan**  
Want to contribute significantly more to your retirement while lowering your tax burden? Cash Balance Plans offer a powerful solution for high-income business owners, doctors, and law firms looking to build wealth efficiently.

At FBS Group, we specialize in designing and implementing Cash Balance Plans that maximize tax savings and retirement growth while keeping your business financially strong.
""")
        if st.button("Reduce Taxes"):
            st.info("""
**CBP: Premier Retirement Solution**  
**Cash Balance Plan**  
Want to contribute significantly more to your retirement while lowering your tax burden? Cash Balance Plans offer a powerful solution for high-income business owners, doctors, and law firms looking to build wealth efficiently.

At FBS Group, we specialize in designing and implementing Cash Balance Plans that maximize tax savings and retirement growth while keeping your business financially strong.
""")
        if st.button("Unsure"):
            st.info("Let's explore what works best in Chatty chat.")
    if st.button("No"):
        st.info("""
**Solo 401(k): A Smart Choice for You**  
A one-participant 401(k), or a solo K, offers self-employed individuals an efficient way to save for retirement. There are no age or income restrictions, but participants must be business owners with no employees (apart from spouses).

A solo 401(k) gives you all the benefits of employer-sponsored 401(k) plans – tax breaks on savings, tax-deferred or tax-free growth, and generous annual contributions – but tailored for small businesses. You can set up the plan at a broker of your choice without restrictive investment rules.
""")
    if st.button("Continue to Chat"):
        go_to_stage("chat")

# ---- W2 Flow ---- #
elif st.session_state.stage == "w2":
    st.title("W2 Employee")
    st.subheader("What are you looking for?")
    if st.button("Changing employer"):
        st.info("Please talk to an expert at FBS.")
    if st.button("401(k) transfer"):
        st.info("Please talk to an expert at FBS.")
    if st.button("401(k) reduced in value"):
        st.info("""
**Strategic Roth Conversions:**  
Are you looking for tax-free distribution and to maximize your retirement wealth? At FBS Group, we specialize in advanced retirement strategies like the Mega Backdoor Roth and Backdoor Roth, helping high-income earners optimize their tax-free retirement savings. Our expertise ensures you get the most out of your retirement contributions while staying fully compliant with IRS rules.
""")
    if st.button("None of the above"):
        st.info("Please talk to an expert at FBS.")
    if st.button("Continue to Chat"):
        go_to_stage("chat")

# ---- Business Owner Flow ---- #
elif st.session_state.stage == "business_owner":
    st.title("Business Owner")
    st.subheader("How many employees?")
    if st.button("1 Employee"):
        go_to_stage("self_employed")
    if st.button("More than 1 Employee"):
        st.subheader("Attract and retain talent using:")
        if st.button("Traditional 401(k)"):
            st.info("Traditional 401(k)s offer flexibility and tax benefits for employers and employees.")
        if st.button("CBP"):
            st.info("""
**CBP: Premier Retirement Solution**  
**Cash Balance Plan**  
Want to contribute significantly more to your retirement while lowering your tax burden? Cash Balance Plans offer a powerful solution for high-income business owners, doctors, and law firms looking to build wealth efficiently.

At FBS Group, we specialize in designing and implementing Cash Balance Plans that maximize tax savings and retirement growth while keeping your business financially strong.
""")
        if st.button("Pension"):
            st.info("Defined benefit pensions provide fixed retirement payouts.")
        if st.button("Continue to Chat"):
            go_to_stage("chat")

# ---- Financial Planning ---- #
elif st.session_state.stage == "financial_plan_type":
    st.title("Financial Planning")
    st.subheader("Are you looking for:")
    if st.button("One-Time Comprehensive Plan"):
        st.info("""
**One-Time Comprehensive Financial Plan**  
Your full financial picture—mapped out with expert insight.

**This includes:**  
• Retirement projections  
• Investment portfolio reviews  
• Tax optimization strategies  
• Estate planning considerations  

**Flat Fee:** $5,000  
✅ Designed to give you clarity and confidence for the years ahead.
""")
    if st.button("Annual Planning & Tracking"):
        st.info("""
**Annual Planning & Tracking**  
This is an **Ongoing Support Plan**:  
Available exclusively to clients who have completed the One-Time Comprehensive Plan.

• Progress check-ins  
• Ongoing personalized advice  
• Plan updates as your life and finances evolve  

**Fee:** $1,000 annually, starting in year two  
✅ Continue your journey with expert guidance.
""")
    if st.button("Estate Planning"):
        st.info("""
**One-Time Estate Planning Package**  
Protect your legacy and ensure your wishes are honored.

**This all-inclusive package provides:**  
• Revocable Living Trust  
• Last Will and Testament  
• Healthcare Directive  
• Durable Power of Attorney  

**One-Time Fee:** $2,500  
✅ Comprehensive legal documents tailored to your needs.
""")
# ---- Chat Stage ---- #
elif st.session_state.stage == "chat":
    st.title("💬 Chatty – AI Financial Assistant")
    st.subheader("Ask me more about FBS services...")
