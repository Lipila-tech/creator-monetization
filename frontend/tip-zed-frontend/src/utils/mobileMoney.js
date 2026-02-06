export const PROVIDERS = {
  mtn: {
    id: 'MTN_MOMO_ZMB',
    name: 'MTN Money',
    color: 'bg-yellow-400',
    logo: 'https://static-content.pawapay.io/provider_logos/mtn.png',
    prefixes: ['096', '076', '056']
  },
  airtel: {
    id: 'AIRTEL_OAPI_ZMB',
    name: 'Airtel Money',
    color: 'bg-red-500',
    logo: 'https://static-content.pawapay.io/provider_logos/airtel.png',
    prefixes: ['097', '077', '057']
  },
  zamtel: {
    id: 'ZAMTEL_ZMB',
    name: 'Zamtel Kwacha',
    color: 'bg-green-600',
    logo: 'https://static-content.pawapay.io/provider_logos/zamtel.png',
    prefixes: ['095', '075', '055']
  }
};

export const detectProvider = (phoneNumber) => {
  // Remove spaces and non-numeric chars
  const cleanNumber = phoneNumber.replace(/\D/g, '');

  const mobilePattern = /^(0?(95|96|76|97|77|75|55|56|57)\d{7})$/;
  
  if (cleanNumber.length < 3) return null;

  if (!mobilePattern.test(cleanNumber))
    return null;

  // Check prefixes
  if (PROVIDERS.mtn.prefixes.some(p => cleanNumber.startsWith(p))) return PROVIDERS.mtn;
  if (PROVIDERS.airtel.prefixes.some(p => cleanNumber.startsWith(p))) return PROVIDERS.airtel;
  if (PROVIDERS.zamtel.prefixes.some(p => cleanNumber.startsWith(p))) return PROVIDERS.zamtel;

  return null;
};