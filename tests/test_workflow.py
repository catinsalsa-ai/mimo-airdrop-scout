from airdrop_scout.agents import AirdropScoutWorkflow
from airdrop_scout.models import Target


def test_base_guild_is_watch_or_priority():
    report = AirdropScoutWorkflow().run(Target("Base Guild", "https://guild.xyz/base"))
    assert report.strategy.verdict in {"WATCH", "PRIORITY"}
    assert report.risk.level in {"LOW", "MEDIUM"}
    assert "Base Guild" in report.summary


def test_claim_portal_gets_higher_risk():
    safe = AirdropScoutWorkflow().run(Target("Base Guild", "https://guild.xyz/base"))
    risky = AirdropScoutWorkflow().run(Target("Free Urgent Wallet Claim Airdrop", "http://claim-free-airdrop.example"))
    assert risky.risk.score > safe.risk.score
    assert risky.risk.level == "HIGH"
    assert risky.strategy.verdict in {"SKIP", "WATCH"}
