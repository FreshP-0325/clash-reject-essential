# clash-reject-essential

[English](README.md) | 简体中文

面向 iOS Clash/Mihomo 客户端的精简广告域名规则。目标不是追求“收录最多”，而是在 Network Extension 约 50 MB 的苛刻内存预算里保留更常见、更可信的拦截项。

## 精简方法

上游 `reject-list.txt` 当前约有 18.7 万个域名。直接比较 EasyList 与 AdGuard DNS Filter 后仍有约 5.5 万个共同域名，对 iOS 仍不够轻。因此默认的 `essential` 模式：

1. 以 [Loyalsoldier/v2ray-rules-dat](https://github.com/Loyalsoldier/v2ray-rules-dat) 的 reject 列表作为候选全集；
2. 只保留同时出现在 Peter Lowe 或 Dan Pollock 小型人工维护列表中的候选项；
3. 仅在父域本身已被选中时删除冗余子域，绝不推测性地把多个子域提升成父域；
4. 应用本地 `allowlist.txt` 和 `include.txt`。

按 2026-08-26 的上游数据，默认规则约 1.2 万条，相比 18.7 万条减少约 94%。文本大小不是运行内存；不同客户端和内核的内存结构不同，因此不能承诺固定内存值，请在目标 iPhone 上实测。

另外提供两个模式：

- `balanced`：EasyList 与 AdGuard DNS Filter 的交集，约 5.5 万条，覆盖更广、内存更高。
- `strict`：四个来源中至少三个确认，约 800 条，最轻但漏拦明显。

## 生成

需要 Python 3.10+，不依赖第三方包：

```bash
python3 generate.py
python3 generate.py --mode balanced --output reject-balanced.txt
```

`allowlist.txt` 每行填写一个需要放行的域名，`include.txt` 每行填写一个强制加入的域名。两者都对子域生效，allowlist 优先。

## Clash 配置

把生成文件托管到可访问的 HTTPS 地址，然后加入配置：

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

如果客户端不认识 `format: yaml`，删掉这一行即可。规则应放在会覆盖它的直连/代理规则之前。

## 取舍与验证建议

这是 DNS/域名层拦截，不能处理第一方域名同源广告，也不能替代浏览器内容过滤。建议先用 `essential` 连续使用一周，观察 Clash 的规则命中和 iOS VPN 稳定性：误杀加入 allowlist；高频漏网域名加入 include。比继续扩大一份通用清单更有效的办法，是根据自己的 DNS/Clash 命中日志定期保留真正访问过的广告域名。

数据来源及许可请分别遵循 [EasyList](https://easylist.to/)、[AdGuard DNS Filter](https://github.com/AdguardTeam/AdGuardSDNSFilter)、[Peter Lowe's list](https://pgl.yoyo.org/adservers/) 与 [Dan Pollock's hosts](https://someonewhocares.org/hosts/) 的说明。
