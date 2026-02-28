def research_prompt(text):
    return f"""
You are an academic research analyst.

Analyze the following research paper and provide a structured response:

1. Title (if identifiable)
2. Research Objective
3. Problem Statement
4. Methodology Used
5. Data Source / Sample Size (if mentioned)
6. Key Findings
7. Limitations
8. Future Research Directions
9. Important Insights
10. Practical Implications
11. Summary of the entire report in an easy way so that a common man can understand what the report has found out and what is it trying to explain.
Make the explanation clear and structured.

Research Paper Content:
{text}
"""


def insurance_prompt(text):
    return f"""
You are a financial advisor explaining an insurance policy to a common person.
Use simple, non-technical language suitable for a person with no financial background.

Analyze the policy and explain in simple, easy-to-understand language:

1. Type of Insurance
2. What is Covered
3. What is NOT Covered (Exclusions)
4. Premium Details (if mentioned)
5. Waiting Period (if any)
6. Hidden Conditions or Risky Clauses
7. Claim Conditions
8. Who Should Consider This Policy
9. Key Warnings for the Customer
10. Overall Risk Level (Low/Medium/High with explanation)

Policy Document:
{text}
"""