import re
from typing import Optional, Tuple

class PhoneValidator:
    """
    Simple Zambian phone number validator with configurable formats
    """

    # Common Zambian phone number patterns
    PATTERNS = {
        'generic': r'^0[0-9]{9}$',  # Local format: 0XXXXXXXXX (10 digits)
        'international': r'^(\+?260|260)[0-9]{9}$',  # +260XXXXXXXXX or 260XXXXXXXXX
        'mtn': r'^0(96|76)[0-9]{7}$',  # MTN: 096XXXXXXX or 076XXXXXXX
        'airtel': r'^0[97|77|57][0-9]{7}$',  # Airtel: 097XXXXXXX 077XXXXXXX 057XXXXXXX
        'zamtel': r'^0[95][0-9]{7}$',  # Zamtel: 095XXXXXXX
    }

    @classmethod
    def validate_phone_number(
        cls,
        phone: str,
        pattern: str = 'generic',
        country_code: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Validate phone number
        
        :param phone: Phone number string
        :param pattern: Pattern to validate against (generic, international, mtn, airtel, vodacom)
        :param country_code: Zambia (260)

        returns:
            Tuple of (is_valid, message)
        """
        if not phone:
            return False, "Phone number is required"

        # Clean phone number: remove spaces, dashes, parentheses
        cleaned_phone = re.sub(r'[\s\-\(\)]+', '', str(phone))

        # Extract digits only for length check
        digits_only = re.sub(r'[^0-9]', '', cleaned_phone)

        # Check minimum length
        if len(digits_only) < 10:
            return False, "Phone number must contain at least 10 digits"

        # Try to match pattern
        if pattern == 'international':
            # For international, try both with and without country code
            if cleaned_phone.startswith('+260') or cleaned_phone.startswith('260'):
                # Already has country code
                pass
            elif cleaned_phone.startswith('0'):
                # Local format, convert to international
                cleaned_phone = '260' + cleaned_phone[1:]

        # Get the regex pattern
        regex_pattern = cls.PATTERNS.get(pattern, cls.PATTERNS['generic'])

        # For generic pattern, also accept numbers without leading 0 but with 10 digits
        if pattern == 'generic' and len(digits_only) == 10:
            if digits_only.startswith('0') or digits_only.startswith('7') or digits_only.startswith('9') or digits_only.startswith('5'):
                if len(digits_only) == 10:
                    return True, "Valid phone number"

        # Match against pattern
        if re.match(regex_pattern, cleaned_phone):
            return True, "Valid phone number"

        return False, f"Phone number does not match {pattern} format"