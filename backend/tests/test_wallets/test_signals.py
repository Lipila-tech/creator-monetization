import pytest
from tests.factories import UserFactory

@pytest.mark.django_db
def test_creating_a_creator_creates_a_wallet():
    """Test that creating a creator also creates a Wallet."""
    user = UserFactory()
    creator_profile = user.creator_profile

    assert hasattr(creator_profile, 'wallet')
    assert creator_profile.wallet.creator == creator_profile
    assert creator_profile.wallet.balance == 0


@pytest.mark.django_db
def test_creating_a_wallet_creates_wallet_kyc():
    """Test that creating a Wallet also creates a WalletKYC."""
    user = UserFactory()
    creator_profile = user.creator_profile
    wallet = creator_profile.wallet

    assert hasattr(wallet, 'kyc')
    assert wallet.kyc.wallet == wallet
    assert wallet.kyc.verified is False