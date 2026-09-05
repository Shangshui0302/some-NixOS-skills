# some-NixOS-skills

[![License: 0BSD](https://img.shields.io/badge/license-0BSD-blue.svg)](LICENSE)
[![Nix](https://img.shields.io/badge/Nix-flakes-5277C3.svg)](https://nixos.org/)
[![NixOS](https://img.shields.io/badge/NixOS-workflows-5277C3.svg)](https://nixos.org/)

本项目提供两个可安装的 Agent Skills，帮助 coding agent 开发 Nix 包、管理 NixOS 配置，并分层验证构建与部署结果。

This project provides two installable Agent Skills for developing Nix packages, managing NixOS configurations, and separating build evidence from deployment results.

## 目录 / Contents

- [Skills / 技能](#skills--技能)
- [1. 原生 Agent Skills 安装 / Native installation](#1-原生-agent-skills-安装--native-installation)
- [2. Nix + Home Manager 安装 / Nix + Home Manager installation](#2-nix--home-manager-安装--nix--home-manager-installation)
- [许可证 / License](#许可证--license)

## Skills / 技能

- `nix-packaging`：开发、升级、修复和验证 Nix package。
- `nixos-ecosystem`：管理 Nix、NixOS、Home Manager、服务、部署和恢复流程。

- `nix-packaging`: develop, upgrade, repair, and verify Nix packages.
- `nixos-ecosystem`: manage Nix, NixOS, Home Manager, services, deployment, and recovery workflows.

## 1. 原生 Agent Skills 安装 / Native installation

### 命令行 / CLI

使用跨 Agent 的 [`skills` CLI](https://github.com/vercel-labs/skills) 安装到用户级目录：

Use the cross-agent [`skills` CLI](https://github.com/vercel-labs/skills) to install both skills globally:

```bash
npx skills add \
  https://github.com/Shangshui0302/some-NixOS-skills \
  --skill nix-packaging \
  --skill nixos-ecosystem \
  --global \
  --agent '*' \
  --yes
```

### Prompt

把下面的提示词发给支持 Agent Skills 的 coding agent：

Send the following prompt to a coding agent that supports Agent Skills:

```text
请使用你自己的 Agent Skills 原生安装机制，从
https://github.com/Shangshui0302/some-NixOS-skills
安装 nix-packaging 和 nixos-ecosystem，使用用户级/global scope。
安装完成后确认两个 skill 都能被发现。不要使用 Nix，也不要把仓库内容复制到项目目录。

Use your native Agent Skills installation mechanism to install
nix-packaging and nixos-ecosystem from
https://github.com/Shangshui0302/some-NixOS-skills
for the user/global scope. Verify that both skills are discoverable afterwards.
Do not use Nix or copy the repository into the project directory.
```

## 2. Nix + Home Manager 安装 / Nix + Home Manager installation

通过 Home Manager 声明式安装。flake input 文件位于 `/nix/store`，Home Manager generation 会为每个 skill 建立符号链接到用户目录，默认目标是 `~/.agents/skills`。

Install declaratively through Home Manager. The flake input lives in `/nix/store`, and the Home Manager generation creates one symlink per skill in the user directory. The default target is `~/.agents/skills`.

先在 NixOS flake 中添加 input：

Add the input to your NixOS flake:

```nix
inputs.some-nixos-skills = {
  url = "github:Shangshui0302/some-NixOS-skills";
  inputs.nixpkgs.follows = "nixpkgs";
};
```

然后在现有的 Home Manager 用户模块中导入并启用：

Then import and enable it in your existing Home Manager user module:

```nix
{ inputs, ... }:
{
  imports = [ inputs.some-nixos-skills.homeManagerModules.default ];

  programs.some-nixos-skills.enable = true;
}
```

生成后得到：

The resulting links are:

```text
~/.agents/skills/nix-packaging
~/.agents/skills/nixos-ecosystem
        -> /nix/store/...-source/skills/<skill>
```

如需使用其他 Agent 的目录，只覆盖安装路径；路径始终相对于用户 Home：

To use another Agent directory, override only the install path. The path is relative to the user Home:

```nix
programs.some-nixos-skills.installPath = ".claude/skills";
```

## 许可证 / License

本项目采用 [0BSD（Zero-Clause BSD）](LICENSE)。

Released under the permissive [0BSD (Zero-Clause BSD)](LICENSE) license.
