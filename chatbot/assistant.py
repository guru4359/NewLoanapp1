def get_response(message):
    message = message.lower()

    if "loan" in message:
        return "We offer personal, agricultural, and education loans with flexible terms. You can apply online."

    elif "kyc" in message:
        return "KYC documents include Aadhaar, PAN card, and a recent utility bill or bank statement."

    elif "status" in message:
        return "Please enter your registered email. We’ll get back to you shortly via email or SMS."

    elif "interest" in message:
        return "Interest rates vary by bank and loan type — please choose your bank to see current rates."

    elif "help" in message:
        return "Sure! I can help you with loan application, KYC documents, and bank information."

    else:
        return "Sorry, I didn’t understand that. Please try asking about loan, KYC, or application status."
