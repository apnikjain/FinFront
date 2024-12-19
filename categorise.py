#In[]
import json
import re

# Enhanced categories with specific keywords
categories = {
    "Credit": {
        "Income": {
            "Payroll": ["salary", "payroll", "monthly wage", "income","american exp"],
            "Interest Earned": ["interest credit", "savings interest", "bank interest"],
            "Rental Income": ["rental income", "rent received"],
            "Investment Returns":["mutual","nextbillion","ugro"]
        },
        "Family & Friends": [],
        "Transfer": {
            "Refund": ["refund","settlemet"],
            "Self Transfer": ["self transfer", "own account","transfer to self", "wallet transfer","apnik"]
        },
        "Uncategorized": []
    },
    "Debit": {
        # "Business Expenses":["shiprocket"],
        "Entertainment": ["movie", "cinema", "netflix", "prime", "entertainment", "spotify", "multiplex", "concert", "show"],
        "Education": ["school", "tuition", "education", "course", "exam fee", "training", "college", "university"],
        "Financial": ["insurance", "loan", "emi", "credit card payment", "tax"],
        "Food & Dining": ["swiggy", "zomato", "food", "restaurant", "cafe", "coffee", "juice", "grocery", "pizza", "ice cream", "bar", "takeout","lunch", "chocolate"],
        "Health & Fitness": ["hospital", "doctor", "pharmacy", "medicines", "clinic", "dentist", "gym", "fitness", "health", "yoga", "meditation", "personal trainer"],
        "Home": ["rent", "utilities", "electricity", "water bill", "maintenance", "furniture", "home improvement", "mortgage"],
        "Investment": ["groww","investment", "mutual fund", "stocks", "shares", "bonds", "crypto", "real estate","nextbillionT"],
        "Shopping": ["amazon", "flipkart", "shopping", "mall", "clothing", "electronics", "furniture", "accessories", "shoes", "makeup", "gifts"],
        "Travel & Transport": ["uber", "ola", "bus", "flight", "train", "taxi", "cab", "metro", "airline", "rental car", "ride", "ticket"],
        "Cash Withdrawal":[ "atm", "cash withdrawal","cheque"],
        "Rent":["rent"],
        "Transfer": {
            "Credit Card Payment": ["credit card payment", "cc payment", "visa", "mastercard"],
            "Self Transfer": ["self transfer", "own account","transfer to self", "wallet transfer","apnik"]
        },
        "Family & Friends": ["ruchika","mukesh","ruchika.mk.jain1@ybl"],
        "Uncategorized": []
    }
}

# Function to classify transactions based on narration keywords
def categorization_category_based_on_narration(narration):
    return



# Function to extract insights
def extract_transaction_insights(narration):
    insights = {}

    # Extract transaction type
    if 'CREDIT' in narration:
        insights['Transaction Type'] = 'CREDIT'
    elif 'DEBIT' in narration:
        insights['Transaction Type'] = 'DEBIT'
    elif 'TRANSFER' in narration:
        insights['Transaction Type'] = 'TRANSFER'
    elif 'BOOK DEPOSIT' in narration:
        insights['Transaction Type'] = 'BOOK DEPOSIT'

    # Extract UPI reference ID
    upi_ref_match = re.search(r'UPI/(\d+)', narration)
    if upi_ref_match:
        insights['UPI Reference ID'] = upi_ref_match.group(1)

    # Extract payment description
    description_match = re.search(r'/(.+?)(?:XXXXX|\d{5}|\s)', narration)
    if description_match:
        insights['Description'] = description_match.group(1).strip()

    # Extract masked phone number
    phone_match = re.search(r'XXXXX(\d{5})', narration)
    if phone_match:
        insights['Phone Number (Last 5 Digits)'] = phone_match.group(1)

    # Extract UPI ID or email
    upi_email_match = re.search(r'[\w\.-]+@[\w\.-]+', narration)
    if upi_email_match:
        insights['UPI ID or Email'] = upi_email_match.group(0)

    # Extract bank IFSC code
    ifsc_match = re.search(r'\b[A-Z]{4}0[A-Z0-9]{6}\b', narration)
    if ifsc_match:
        insights['Bank IFSC Code'] = ifsc_match.group(0)

    # Extract beneficiary or payee name
    name_match = re.search(r'/([A-Z\s]+)$', narration)
    if name_match:
        insights['Beneficiary Name'] = name_match.group(1).strip()

    return insights


# Function to classify transactions based on narration keywords
def classify_transaction(transaction, categories):
    narration = transaction["_narration"].lower()  # Convert to lowercase for matching
    txn_type = transaction["_type"]  # Credit or Debit
    
    if txn_type == "CREDIT":
        for category, subcategories in categories["Credit"].items():
            if isinstance(subcategories, dict):
                for subcategory, keywords in subcategories.items():
                    for keyword in keywords:    
                        pattern = re.escape(keyword)
                        if re.search(pattern,narration,re.IGNORECASE):
                            return f"Credit -> {category} -> {subcategory}"
            else:
                if any(keyword in narration for keyword in subcategories):
                    return f"Credit -> {category}"
        return "Credit -> Uncategorized"

    elif txn_type == "DEBIT":
        for category, subcategories in categories["Debit"].items():
            if isinstance(subcategories, dict):
                for subcategory, keywords in subcategories.items():
                    for keyword in keywords:    
                        pattern = re.escape(keyword)
                        if re.search(pattern,narration,re.IGNORECASE):
                            return f"Debit -> {category} -> {subcategory}"
            else:
                if any(keyword in narration for keyword in subcategories):
                    return f"Debit -> {category}"
        return "Debit -> Uncategorized"
    
    return "Uncategorized"

# Function to process all transactions in the dataset and save in the required format
def process_transactions(transactions, categories):
    categorized_transactions = []
    for txn in transactions:
        category = classify_transaction(txn, categories)
        insights = extract_transaction_insights(txn["_narration"])
        txn_result = {
            "amount": txn["_amount"],
            "date": txn["_transactionTimestamp"],
            "narration": txn["_narration"],
            "Category": category,
            "insights":insights
        }
        categorized_transactions.append(txn_result)
    return categorized_transactions

# Save the processed transactions to a new JSON file
def save_to_file(categorized_transactions, output_file):
    with open(output_file, "w") as f:
        json.dump(categorized_transactions, f, indent=4)

# Example usage:
if __name__ == "__main__":
    # Load transactions from a JSON file
    with open("output.json", "r") as f:
        transactions = json.load(f)
    
    # Process and categorize all transactions
    categorized_transactions = process_transactions(transactions, categories)
    
    # Save categorized transactions to a new file
    save_to_file(categorized_transactions, "categorized_transactions.json")
    
    # Print success message
    print(f"Categorized transactions have been saved to 'categorized_transactions.json'.")

    desc = {
    "Credit": {
        "Income": {
            "Payroll": {
                "narration":[],
                "total":0
                },
            "Interest Earned": {
                "narration":[],
                "total":0
                },
            "Rental Income": {
                "narration":[],
                "total":0
                },
            "Investment Returns":{
                "narration":[],
                "total":0
                }
        },
        "Family & Friends": {
                "narration":[],
                "total":0
                },
        "Transfer": {
            "Refund": {
                "narration":[],
                "total":0
                },
            "Self Transfer": {
                "narration":[],
                "total":0
                }
        },
        "Uncategorized": {
                "narration":[],
                "total":0
                },
    },
    "Debit": {
        "Entertainment": {
                "narration":[],
                "total":0
                },
        "Family & Friends": {
                "narration":[],
                "total":0
                },
        "Education": {
                "narration":[],
                "total":0
                },
        "Financial": {
                "narration":[],
                "total":0
                },
        "Food & Dining": {
                "narration":[],
                "total":0
                },
        "Health & Fitness": {
                "narration":[],
                "total":0
                },
        "Home": {
                "narration":[],
                "total":0
                },
        "Investment": {
                "narration":[],
                "total":0
                },
        "Shopping": {
                "narration":[],
                "total":0
                },
        "Travel & Transport": {
                "narration":[],
                "total":0
                },
        "Cash Withdrawal":{
                "narration":[],
                "total":0
                },
        "Transfer": {
            "Credit Card Payment": {
                "narration":[],
                "total":0
                },
            "Self Transfer": {
                "narration":[],
                "total":0
                }
        },
        "Uncategorized": {
                "narration":[],
                "total":0
                }
        }
    }

    for txn in categorized_transactions:
        temp = txn["Category"].split("->")
        temp1= {
                "Narration":txn["narration"],
                "Ammount":txn["amount"],
                "Date":txn["date"],
                "Insights":txn["insights"]
            }
        if(len(temp) == 2):
            desc[temp[0].strip()][temp[1].strip()]["narration"].append(temp1)
            desc[temp[0].strip()][temp[1].strip()]["total"] += float(txn["amount"])
        if(len(temp) == 3):
            desc[temp[0].strip()][temp[1].strip()][temp[2].strip()]["narration"].append(temp1)
            desc[temp[0].strip()][temp[1].strip()][temp[2].strip()]["total"] += float(txn["amount"])
    save_to_file(desc, "desc.json")
    print(f"Desc Categorized transactions have been saved to 'desc.json'.")


        

