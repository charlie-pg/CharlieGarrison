from statistics import median

# Target
target = {
    "name": "Eli Lilly (LLY)",
    "price": 1160.00,
    "eps": 22.95,
}

# Peers
peers = [
    {"name": "Merck (MRK)", "price": 149.86, "eps": 7.28},
    {"name": "AbbVie (ABBV)", "price": 259.99, "eps": 2.36},
]

# Remove duplicate peers, exclude target, and require positive price/EPS
valid_peers = []
seen = set()

for peer in peers:
    name = peer["name"]

    if name == target["name"] or name in seen:
        continue

    seen.add(name)

    if peer["price"] > 0 and peer["eps"] > 0:
        peer["pe"] = peer["price"] / peer["eps"]
        valid_peers.append(peer)

print("Peer P/E multiples:")
for peer in valid_peers:
    print(f'{peer["name"]}: {peer["pe"]:.6f}x')

if len(valid_peers) == 0:
    print("No usable peers.")

else:
    pes = [peer["pe"] for peer in valid_peers]
    med_pe = median(pes)

    print(f"\nPeer median P/E: {med_pe:.6f}x")

    if target["eps"] <= 0:
        print("Target EPS is nonpositive; implied prices are not meaningful.")
    else:
        implied_min = min(pes) * target["eps"]
        implied_median = med_pe * target["eps"]
        implied_max = max(pes) * target["eps"]

        print(f"Implied price minimum: ${implied_min:.2f}")
        print(f"Implied price median: ${implied_median:.2f}")
        print(f"Implied price maximum: ${implied_max:.2f}")

        full_peer_estimate = implied_median

        print("\nLeave-one-peer-out:")
        for removed in valid_peers:
            remaining = [p for p in valid_peers if p["name"] != removed["name"]]

            if len(remaining) == 0:
                print(f'Remove {removed["name"]}: no estimate')
            else:
                remaining_pes = [p["pe"] for p in remaining]
                remaining_median = median(remaining_pes)
                remaining_price = remaining_median * target["eps"]
                change = remaining_price - full_peer_estimate

                print(
                    f'Remove {removed["name"]}: '
                    f'remaining median-implied price = ${remaining_price:.2f}, '
                    f'change = ${change:.2f}'
                )