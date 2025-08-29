# shop/sms_parser.py
import re
from decimal import Decimal, InvalidOperation

# regex tolérante: "recu" ou "reçu", décimales . ou , et Ref: XXXX
SMS_REGEX = re.compile(
    r"re[çc]u\s+([\d\.,]+)\s*CDF.*?Ref[:\s]+([A-Z0-9\.]+)",
    flags=re.IGNORECASE | re.DOTALL
)

def parse_payment_sms(sms_text: str):
    """
    Retourne (amount_decimal, reference) ou (None, None) si non trouvé.
    """
    m = SMS_REGEX.search(sms_text or "")
    if not m:
        return None, None

    raw_amount = m.group(1).strip()
    reference = m.group(2).strip()

    # Normaliser le montant: remplacer virgule par point, enlever espaces
    normalized = raw_amount.replace(" ", "").replace(",", ".")
    try:
        amount = Decimal(normalized)
    except InvalidOperation:
        return None, None

    return amount, reference