#!/usr/bin/env python3
"""
VIRTUALS MEV BOT — Runs on GitHub Actions
Monitors Virtuals agent trades and executes arbitrage/sandwich
"""
import os, json, time, sys
from web3 import Web3
from datetime import datetime

# Config from GitHub Secrets
PRIVATE_KEY = os.environ.get("PRIVATE_KEY", "")
WALLET = os.environ.get("WALLET_ADDRESS", "")
FLASHARB = os.environ.get("FLASHARB_CONTRACT", "")
ARBFIX = os.environ.get("ARBFIX_CONTRACT", "")

# RPC endpoints (free, public)
RPCS = [
    "https://base.drpc.org",
    "https://1rpc.io/base",
    "https://mainnet.base.org",
    "https://base-mainnet.public.blastapi.io",
]

# Virtuals infrastructure
AERO_ROUTER = "0xcF77A3Ba9A5cA399b7c7f1B1d6D2c025B4cF3f6a"
UNI_ROUTER = "0x4752BA5DBc23F44D878962d56231cD4bAfd48b9d"
WETH = "0x4200000000000000000000000000000000000006"
USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
VIRTUAL_TOKEN = "0xb3eE5DbD5Cf1F4E30638829096Aa9299D6774977"

# Virtuals agent wallets to monitor (loaded from file)
AGENT_WALLETS_FILE = "virtuals_wallets.json"

def connect():
    for rpc in RPCS:
        try:
            w3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={"timeout": 10}))
            if w3.is_connected():
                return w3, rpc
        except:
            continue
    return None, None

def load_agent_wallets():
    """Load Virtuals agent wallets"""
    try:
        with open(AGENT_WALLETS_FILE) as f:
            return set(w.lower() for w in json.load(f))
    except:
        return set()

def get_balance(w3, addr):
    try:
        return w3.from_wei(w3.eth.get_balance(addr), "ether")
    except:
        return 0

def scan_block_for_virtuals(w3, block_num, agent_wallets):
    """Scan a block for Virtuals agent activity"""
    try:
        block = w3.eth.get_block(block_num, full_transactions=True)
        txs = block.get("transactions", [])
        virtuals_txs = []
        
        for tx in txs:
            from_addr = (tx.get("from", "") or "").lower()
            to_addr = (tx.get("to", "") or "").lower()
            
            # Check if any Virtuals agent wallet is involved
            if from_addr in agent_wallets or to_addr in agent_wallets:
                value = w3.from_wei(tx.get("value", 0), "ether")
                input_data = tx.get("input", "")
                virtuals_txs.append({
                    "hash": tx.get("hash", "")[:20],
                    "from": from_addr,
                    "to": to_addr,
                    "value": float(value),
                    "input_sig": input_data[:10] if input_data else "0x",
                    "is_aero": to_addr == AERO_ROUTER.lower(),
                    "is_uni": to_addr == UNI_ROUTER.lower(),
                })
        
        return virtuals_txs, len(txs)
    except Exception as e:
        return [], 0

def check_arb_opportunity(w3):
    """Check for arbitrage spreads between DEXs"""
    router_abi = json.loads('''
    [{"inputs":[{"name":"amountIn","type":"uint256"},{"name":"path","type":"address[]"}],
    "name":"getAmountsOut","outputs":[{"name":"amounts","type":"uint256[]"}],
    "stateMutability":"view","type":"function"}]
    ''')
    
    tokens = [
        ("WETH", WETH),
        ("VIRTUAL", VIRTUAL_TOKEN),
        ("AERO", "0x940181a98A6c00e2Fe1AF90e6414a64d5ec5c2c4"),
    ]
    
    opportunities = []
    
    for name, token in tokens:
        try:
            token = Web3.to_checksum_address(token)
            usdc = Web3.to_checksum_address(USDC)
            path = [token, usdc]
            
            # Check Aerodrome
            aero = w3.eth.contract(
                address=Web3.to_checksum_address(AERO_ROUTER),
                abi=router_abi
            )
            aero_out = aero.functions.getAmountsOut(w3.to_wei(0.01, "ether"), path).call()
            
            # Check Uniswap
            uni = w3.eth.contract(
                address=Web3.to_checksum_address(UNI_ROUTER),
                abi=router_abi
            )
            uni_out = uni.functions.getAmountsOut(w3.to_wei(0.01, "ether"), path).call()
            
            if aero_out[1] > 0 and uni_out[1] > 0:
                spread = abs(aero_out[1] - uni_out[1]) / max(aero_out[1], uni_out[1]) * 100
                if spread > 0.3:
                    direction = "AERO->UNI" if aero_out[1] < uni_out[1] else "UNI->AERO"
                    opportunities.append({
                        "token": name,
                        "spread": spread,
                        "direction": direction,
                        "aero_price": aero_out[1],
                        "uni_price": uni_out[1],
                    })
        except:
            continue
    
    return opportunities

def execute_flash_arb(w3, account, contract_addr, token, direction):
    """Execute flash loan arbitrage via FlashArb contract"""
    try:
        nonce = w3.eth.get_transaction_count(account.address)
        gas_price = w3.eth.gas_price
        
        # Simple execution: call executeArbitrage on FlashArb
        # This is a placeholder — actual execution depends on contract ABI
        print(f"  [EXEC] Would execute arb for {token} {direction}")
        print(f"  [EXEC] Nonce: {nonce}, Gas: {gas_price/1e9:.4f} Gwei")
        return True
    except Exception as e:
        print(f"  [EXEC] Error: {e}")
        return False

def main():
    print(f"\n{'='*60}")
    print(f"VIRTUALS MEV BOT — GitHub Actions")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"{'='*60}")
    
    if not PRIVATE_KEY:
        print("ERROR: PRIVATE_KEY not set")
        sys.exit(1)
    
    # Connect
    w3, rpc = connect()
    if not w3:
        print("ERROR: Cannot connect to Base")
        sys.exit(1)
    
    print(f"Connected: {rpc}")
    print(f"Block: {w3.eth.block_number:,}")
    
    # Account
    account = w3.eth.account.from_key(PRIVATE_KEY)
    print(f"Wallet: {account.address}")
    
    bal = get_balance(w3, account.address)
    print(f"ETH: {bal:.6f}")
    
    if bal < 0.0001:
        print("WARNING: Low balance for gas")
    
    nonce = w3.eth.get_transaction_count(account.address)
    print(f"Nonce: {nonce}")
    
    # Load agent wallets
    agent_wallets = load_agent_wallets()
    print(f"Monitoring {len(agent_wallets)} Virtuals agent wallets")
    
    # Scan last 10 blocks
    print(f"\n{'='*60}")
    print("BLOCK SCANNING")
    print(f"{'='*60}")
    
    current = w3.eth.block_number
    total_virtuals_txs = 0
    
    for i in range(10):
        block_num = current - i
        v_txs, total_txs = scan_block_for_virtuals(w3, block_num, agent_wallets)
        
        if v_txs:
            print(f"\n  Block {block_num} ({total_txs} txs, {len(v_txs)} Virtuals):")
            for tx in v_txs[:5]:
                dex = "AERO" if tx["is_aero"] else "UNI" if tx["is_uni"] else "other"
                print(f"    {tx['hash']}... | {tx['value']:.4f} ETH | {dex} | {tx['input_sig']}")
            total_virtuals_txs += len(v_txs)
    
    print(f"\n  Total Virtuals txs found: {total_virtuals_txs}")
    
    # Check arbitrage
    print(f"\n{'='*60}")
    print("ARBITRAGE SCAN")
    print(f"{'='*60}")
    
    opps = check_arb_opportunity(w3)
    if opps:
        print(f"  Found {len(opps)} opportunities:")
        for o in opps:
            print(f"    {o['token']}: {o['spread']:.2f}% spread | {o['direction']}")
            if bal > 0.0001:
                execute_flash_arb(w3, account, FLASHARB, o["token"], o["direction"])
    else:
        print("  No profitable spreads found (>0.3%)")
    
    # Check wallet status
    print(f"\n{'='*60}")
    print("WALLET STATUS")
    print(f"{'='*60}")
    print(f"  Address: {account.address}")
    print(f"  ETH: {bal:.6f}")
    print(f"  Nonce: {nonce}")
    print(f"  Gas price: {w3.eth.gas_price/1e9:.4f} Gwei")
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"  Blocks scanned: 10")
    print(f"  Virtuals txs: {total_virtuals_txs}")
    print(f"  Arb opportunities: {len(opps)}")
    print(f"  Wallet ETH: {bal:.6f}")
    print(f"  Status: {'ACTIVE' if bal > 0.0001 else 'NEED GAS'}")
    
    # Write summary for GitHub Actions artifact
    summary = {
        "timestamp": datetime.now().isoformat(),
        "block": current,
        "wallet": account.address,
        "eth_balance": float(bal),
        "virtuals_txs": total_virtuals_txs,
        "arb_opportunities": len(opps),
        "opportunities": opps,
    }
    
    with open("bot_summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n  Summary saved to bot_summary.json")

if __name__ == "__main__":
    main()
