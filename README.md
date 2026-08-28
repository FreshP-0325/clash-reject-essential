# clash-reject-essential

English | [简体中文](README.zh-CN.md)

A compact ad-domain ruleset for Clash/Mihomo clients on iOS. Rather than maximizing the number of blocked domains, this project keeps more common and trustworthy entries within the tight memory budget of an iOS Network Extension, which is typically around 50 MB.

## Reduction strategy

The upstream `reject-list.txt` currently contains about 187,000 domains. The intersection of EasyList and AdGuard DNS Filter alone still contains about 55,000 domains, which remains relatively heavy for iOS. The default `essential` mode therefore:

1. Uses the reject list from [Loyalsoldier/v2ray-rules-dat](https://github.com/Loyalsoldier/v2ray-rules-dat) as the complete candidate set.
2. Keeps candidates that also appear in either Peter Lowe's or Dan Pollock's smaller, manually maintained lists.
3. Removes a redundant child domain only when its parent domain was explicitly selected. It never promotes a group of child domains to an inferred parent rule.
4. Applies the local `allowlist.txt` and `include.txt` overrides.

Using upstream data from 2026-08-26, the default output contains about 12,000 rules, a reduction of roughly 94% from the original 187,000. File size is not the same as runtime memory usage. Clients and cores use different in-memory representations, so no fixed memory footprint can be guaranteed; test the ruleset on the target iPhone.

Two additional modes are available:

- `balanced`: the intersection of EasyList and AdGuard DNS Filter, with about 55,000 rules. It provides broader coverage at a higher memory cost.
- `strict`: domains confirmed by at least three of the four sources, with about 800 rules. It is the lightest option but misses substantially more ads.

## Generate the ruleset

Python 3.10 or later is required. There are no third-party dependencies:

```bash
python3 generate.py
python3 generate.py --mode balanced --output reject-balanced.txt
```

Add one domain per line to `allowlist.txt` to exclude it, or to `include.txt` to force it into the output. Both files apply to the listed domain and all of its subdomains. The allowlist takes precedence.

## Clash configuration

Host the generated file at an accessible HTTPS URL, then add it to your configuration:

```yaml
rule-providers:
  reject-essential:
    type: http
    behavior: domain
    format: yaml
    url: "https://example.com/reject-essential.txt"
    path: ./ruleset/reject-essential.yaml
    interval: 86400

rules:
  - RULE-SET,reject-essential,REJECT
```

Remove `format: yaml` if your client does not recognize that option. Place the rule before any direct or proxy rule that would otherwise match the same domains.

## Trade-offs and validation

This is DNS/domain-level blocking. It cannot block first-party, same-origin ads and does not replace browser content filtering. Start with `essential` for a week and monitor rule hits and iOS VPN stability. Add false positives to the allowlist and frequently encountered misses to the include list.

Periodically retaining ad domains that actually appear in your own DNS or Clash logs is generally more effective than continually expanding a universal list.

For source and licensing information, refer to [EasyList](https://easylist.to/), [AdGuard DNS Filter](https://github.com/AdguardTeam/AdGuardSDNSFilter), [Peter Lowe's list](https://pgl.yoyo.org/adservers/), and [Dan Pollock's hosts](https://someonewhocares.org/hosts/).
