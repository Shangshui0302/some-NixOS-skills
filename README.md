# some-NixOS-skills

[![License: 0BSD](https://img.shields.io/badge/license-0BSD-blue.svg)](LICENSE)
[![Nix](https://img.shields.io/badge/Nix-flakes-5277C3.svg)](https://nixos.org/)
[![NixOS](https://img.shields.io/badge/NixOS-workflows-5277C3.svg)](https://nixos.org/)

本项目提供两个可安装的 Agent Skills，帮助 coding agent 开发 Nix 包、管理 NixOS 配置，并分层验证构建与部署结果。

This project provides two installable Agent Skills for developing Nix packages, managing NixOS configurations, and separating build evidence from deployment results.

## 目录 / Contents

- [Skills / 技能](#skills--技能)
- [项目级原生安装 / Project-level native installation](#项目级原生安装--project-level-native-installation)
- [许可证 / License](#许可证--license)

## Skills / 技能

- `nix-packaging`：开发、升级、修复和验证 Nix package。
- `nixos-ecosystem`：管理 Nix、NixOS、Home Manager、服务、部署和恢复流程。

- `nix-packaging`: develop, upgrade, repair, and verify Nix packages.
- `nixos-ecosystem`: manage Nix, NixOS, Home Manager, services, deployment, and recovery workflows.

## 项目级原生安装 / Project-level native installation

### 命令行 / CLI

在目标项目根目录运行跨 Agent 的 [`skills` CLI](https://github.com/vercel-labs/skills)，安装到该项目的 `.agents/skills`：

Run the cross-agent [`skills` CLI](https://github.com/vercel-labs/skills) from the target project root. It installs both skills into that project's `.agents/skills`:

```bash
cd /path/to/your/project
npx skills add \
  Shangshui0302/some-NixOS-skills \
  --skill nix-packaging \
  --skill nixos-ecosystem \
  --agent '*' \
  --yes
```

### Prompt

把下面的提示词发给支持 Agent Skills 的 coding agent：

Send the following prompt to a coding agent that supports Agent Skills:

```text
请在当前项目根目录使用你自己的 Agent Skills 原生安装机制，从
https://github.com/Shangshui0302/some-NixOS-skills
以 project scope 安装 nix-packaging 和 nixos-ecosystem，覆盖项目已有的 Nix/NixOS skill。
安装完成后确认两个 skill 都能被发现。不要使用 Nix、flake 或 global scope。

Use your native Agent Skills installation mechanism from the current project root to install
nix-packaging and nixos-ecosystem from
https://github.com/Shangshui0302/some-NixOS-skills
with project scope, replacing the project's existing Nix/NixOS skills.
Verify that both skills are discoverable afterwards. Do not use Nix, flakes, or global scope.
```

## 许可证 / License

本项目采用 [0BSD（Zero-Clause BSD）](LICENSE)。

Released under the permissive [0BSD (Zero-Clause BSD)](LICENSE) license.
