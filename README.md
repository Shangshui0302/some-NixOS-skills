# some-NixOS-skills

[![License: 0BSD](https://img.shields.io/badge/license-0BSD-blue.svg)](LICENSE)
[![Nix](https://img.shields.io/badge/Nix-flakes-5277C3.svg)](https://nixos.org/)
[![NixOS](https://img.shields.io/badge/NixOS-workflows-5277C3.svg)](https://nixos.org/)

面向 coding agent 的证据驱动 Nix 与 NixOS skill 集合。它覆盖 Nix 打包、配置、部署、测试、恢复和持续维护。

Evidence-driven Nix and NixOS skills for coding agents. The project covers packaging, configuration, deployment, testing, recovery, and ongoing maintenance.

**GitHub topics / GitHub 主题：** `nix` `nixos` `nix-flakes` `home-manager` `agent-skills` `declarative-configuration` `continuous-integration`

## Table of Contents / 目录

- [Overview / 概览](#overview)
- [Skills / 技能](#skills)
- [Use / 使用](#use)
- [Distribution / 分发](#distribution)
- [Freshness and updates / 新鲜度与更新](#freshness-and-updates)
- [Design principles / 设计原则](#design-principles)
- [Scope and safety / 范围与安全](#scope-and-safety)
- [License / 许可证](#license)

## Overview

**概览：** 本项目不是 NixOS 模块、软件包仓库或自动安装器，而是一套可复用的工作流程 skill。每个 `skills/<name>/` 目录都是稳定的 consumer-facing 接口，flake 会自动发现其中包含 `SKILL.md` 的目录。

**English:** This project is a reusable workflow skill set, not a NixOS module, package registry, or automatic installer. Each `skills/<name>/` directory is a stable consumer-facing interface, and the flake discovers every directory containing `SKILL.md`.

## Skills

| Skill | 中文用途 | English use |
| --- | --- | --- |
| `nix-packaging` | 添加、升级、修复或审查 Nix derivation，并验证构建产物和运行时边界。 | Add, upgrade, repair, or review Nix derivations and their build/runtime evidence. |
| `nixos-ecosystem` | 管理 Nix、NixOS、Home Manager、硬件、Secrets、服务、VM、部署、CI 和跨平台边界。 | Manage Nix, NixOS, Home Manager, hardware, secrets, services, VMs, deployment, CI, and cross-platform boundaries. |

`nixos-ecosystem` 是工作流路由器，不是安装器，也不替代版本匹配的官方手册。

`nixos-ecosystem` is a workflow router, not an installer or a replacement for version-matched official manuals.

## Use

**在仓库根目录运行 / Run from the repository root:**

```bash
nix flake check
nix build .#nix-packaging
nix build .#nixos-ecosystem
nix build .#all-skills

python3 skills/nix-packaging/scripts/validate-skill.py skills/nix-packaging
python3 skills/nix-packaging/scripts/validate-skill.py skills/nixos-ecosystem
```

这些命令分别检查 flake、构建单个或全部 skill，并验证 skill 结构。

These commands check the flake, build individual or aggregate skill outputs, and validate skill structure.

主机集成应通过宿主的正常配置机制完成；仓库不会未经授权修改 `~/.codex/skills` 或其他用户目录。

Host integration should use the host's normal configuration mechanism; this repository never modifies `~/.codex/skills` or another user directory without authorization.

## Distribution

flake 暴露以下 package output：

The flake exposes these package outputs:

- `.#nix-packaging`
- `.#nixos-ecosystem`
- `.#all-skills`
- `.#default`（等同于 `.#all-skills` / equivalent to `.#all-skills`）

例如：

For example:

```bash
nix profile install .#nix-packaging
```

构建产物位于 `/nix/store/.../share/agent-skills/<name>/`。这提供可复现的 Nix 分发入口，但不会自动注册或覆盖 Agent 的 skill 目录。

Built outputs live under `/nix/store/.../share/agent-skills/<name>/`. This provides a reproducible Nix distribution entry point, but it does not automatically register or overwrite an Agent skill directory.

## Freshness and updates

**新鲜度门禁：** 每个适用任务都要读取锁定输入，并在使用陌生选项或 API 前核对版本匹配的官方文档。

**Freshness gate:** Every applicable task reads locked inputs and checks version-matched official documentation before using an unfamiliar option or API.

本地报告：

Local report:

```bash
python3 scripts/check-freshness.py
```

`.github/workflows/freshness.yml` 每周或手动运行：它在临时路径生成候选 `nixpkgs` lock，执行 freshness 报告、flake 检查和 skill 构建；发现 lock 漂移或文档复核到期时要求人工审阅。

`.github/workflows/freshness.yml` runs weekly or by manual dispatch. It creates a candidate `nixpkgs` lock in a temporary path, runs the freshness report, checks the flake, and builds the skills; lock drift or an overdue documentation review requires human review.

自动化不会修改真实 `flake.lock`、提交、推送、创建 PR、激活系统或删除 generation。日期检查是提醒器，不是网页语义 diff；Agent 仍必须阅读当前官方文档。

Automation does not modify the real `flake.lock`, commit, push, open a PR, activate a system, or delete generations. The date check is a reminder rather than a semantic web-page diff; the Agent must still read current official documentation.

## Design principles

- **证据优先 / Evidence first：** 先记录锁定输入、版本匹配接口和不可变上游事实，再编辑。
- **分层验证 / Layered validation：** 区分 parse/eval、build、dry-build、VM、activation 和 live runtime。
- **渐进加载 / Progressive disclosure：** `SKILL.md` 负责路由，详细规则只在任务需要时加载。
- **声明式分发 / Declarative distribution：** flake 提供不可变的 skill 产物，消费者自行 pin 和集成。
- **人工确认边界 / Human approval boundaries：** activation、远程部署、commit、push 和 PR 创建都需要明确授权。
- **可审阅更新 / Reviewable updates：** freshness 只发现和报告变化，不静默改写本地规则。

## Scope and safety

这些 skill 指导 Agent 收集证据、选择最小实现、保留所有权和恢复边界，并准确报告验证层级。它们不会默示允许执行：

These skills guide agents to gather evidence, choose the smallest implementation, preserve ownership and recovery boundaries, and report validation layers precisely. They never imply permission to:

- `nixos-rebuild switch`
- 远程部署 / remote deployment
- 磁盘格式化 / disk formatting
- 删除 generation 或垃圾回收 / deleting generations or garbage collection
- 未经授权的 commit、push 或 PR / unauthorized commit, push, or pull request

## License

本项目采用 [0BSD（Zero-Clause BSD）](LICENSE)，这是宽松、无署名义务的开源许可证。

This project is released under the [0BSD (Zero-Clause BSD)](LICENSE), a highly permissive license with no attribution requirement.
