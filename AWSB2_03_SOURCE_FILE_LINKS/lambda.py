import json
from datetime import datetime

def lambda_handler(event, context):
    # Extract headers safely
    headers = event.get('headers') or {}
    username = str(headers.get('x-username', '')).strip().lower()
    user_code = str(headers.get('x-totp-code', '')).strip()
    
    # Allowed roles
    VALID_ROLES = {"doctor", "nurse", "admin"}
    
    # Get caller's public IP (from API Gateway)
    try:
        ip_address = event['requestContext']['http']['sourceIp']
        last_octet = int(ip_address.split('.')[-1])  # e.g., 12 from 103.25.120.12
    except (KeyError, ValueError, IndexError):
        ip_address = "unknown"
        last_octet = 0

    # === VALIDATION: Missing Headers ===
    if not username:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Missing required header: x-username",
                "example": "x-username: doctor"
            })
        }
    
    if not user_code:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Missing required header: x-totp-code",
                "tip": "Code = (floor(UTC_minute/2) + last_IP_octet) % 100"
            })
        }

    # === VALIDATION: Invalid Role ===
    if username not in VALID_ROLES:
        return {
            "statusCode": 403,
            "body": json.dumps({
                "error": f"Invalid role: '{username}'",
                "allowed_roles": list(VALID_ROLES)
            })
        }

    # === GENERATE EXPECTED TOTP ===
    current_minute = datetime.utcnow().minute
    time_window = current_minute // 4  # 4-minute window (0-1 → 0, 2-3 → 1, ..., 58-59 → 29)
    expected_code = (time_window + last_octet) % 100
    expected_str = f"{expected_code:02d}"  # Always 2 digits (e.g., "05")

    # === DECISION: Success or Failure ===
    if user_code == expected_str:
        return {
            "statusCode": 200,
            "body": json.dumps({
                "status": "✅ SUCCESS",
                "message": "MFA verified. Access granted to healthcare system.",
                "role": username,
                "ip_address": ip_address,
                "code_used": user_code,
                "valid_for": "120 seconds (2-minute window)"
            }, indent=2)
        }
    else:
        return {
            "statusCode": 403,
            "body": json.dumps({
                "status": "❌ FAILED",
                "message": f"You entered {user_code}, but the correct code right now is {expected_str}.",
                "tip": "Recalculate using (floor(UTC_minute/2) + last IP octet) % 100.",
                "ip_used": ip_address,
                "utc_minute": current_minute,
                "time_window": time_window,
                "last_ip_octet": last_octet
            }, indent=2)
        }