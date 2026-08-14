# Virtuals MEV Bot

Automated MEV extraction bot running on GitHub Actions.

## Features
- Monitors Virtuals Protocol agent wallet activity on Base
- Scans for arbitrage opportunities between DEXs
- Executes flash loan arbitrage when profitable
- Runs every 5 minutes via GitHub Actions cron

## Architecture
- **RPC**: Free public Base endpoints (drpc, 1rpc, blastapi)
- **Wallet**: funded with ETH for gas
- **Contracts**: FlashArb deployed on Base
- **Secrets**: Private key stored as GitHub Secret (never exposed)

## Monitoring
- 4,952 Virtuals agent wallets tracked
- Scans last 10 blocks per run for agent activity
- Checks WETH/USDC, VIRTUAL/USDC, AERO/USDC spreads

## Security
- Private key is a GitHub Secret (encrypted, not in logs)
- No sensitive data in code
- Public repo for unlimited Actions minutes
