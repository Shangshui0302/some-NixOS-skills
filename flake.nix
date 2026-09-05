{
  description = "some-NixOS-skills: Nix and NixOS skills for coding agents";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    home-manager = {
      url = "github:nix-community/home-manager";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { nixpkgs, ... }@inputs:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "aarch64-darwin"
      ];

      skillRoot = ./skills;
      skillPath = name: skillRoot + "/${name}";
      skillNames = builtins.filter
        (name: builtins.pathExists (skillPath name + "/SKILL.md"))
        (builtins.attrNames (builtins.readDir skillRoot));

      homeManagerModule = { config, lib, ... }:
        let
          cfg = config.programs.some-nixos-skills;
        in
        {
          options.programs.some-nixos-skills = {
            enable = lib.mkEnableOption "some-NixOS-skills";

            installPath = lib.mkOption {
              type = lib.types.addCheck lib.types.nonEmptyStr (path:
                !(lib.hasPrefix "/" path)
                && !(builtins.elem ".." (lib.splitString "/" path))
              );
              default = ".agents/skills";
              description = "Home-relative Agent Skills directory without parent traversal.";
            };
          };

          config = lib.mkIf cfg.enable {
            home.file = builtins.listToAttrs (map (name: {
              name = "${cfg.installPath}/${name}";
              value.source = skillPath name;
            }) skillNames);
          };
        };

      perSystem = system: pkgs:
        let
          mkSkill = name: pkgs.runCommand "agent-skill-${name}" { } ''
            install -d "$out/share/agent-skills/${name}"
            cp -R ${skillPath name}/. "$out/share/agent-skills/${name}/"
          '';

          mkSkillCheck = name: pkgs.runCommand "agent-skill-${name}-check" {
            nativeBuildInputs = [ pkgs.python3 ];
          } ''
            python3 ${./skills/nix-packaging/scripts/validate-skill.py} ${skillPath name}
            touch "$out"
          '';

          skillPackages = builtins.listToAttrs (map (name: {
            inherit name;
            value = mkSkill name;
          }) skillNames);

          allSkills = pkgs.runCommand "agent-skills" { } ''
            install -d "$out/share/agent-skills"
            ${builtins.concatStringsSep "\n" (map (name: "cp -R ${skillPath name}/. \"$out/share/agent-skills/${name}/\"") skillNames)}
          '';

          skillChecks = builtins.listToAttrs (map (name: {
            name = "skill-${name}";
            value = mkSkillCheck name;
          }) skillNames);

          homeManagerModuleCheck =
            let
              makeConfiguration = installPath:
                inputs.home-manager.lib.homeManagerConfiguration {
                  inherit pkgs;
                  modules = [
                    homeManagerModule
                    {
                      home.username = "some-nixos-skills-check";
                      home.homeDirectory = "/tmp/some-nixos-skills-check";
                      home.stateVersion = "25.11";
                      programs.some-nixos-skills = {
                        enable = true;
                        inherit installPath;
                      };
                    }
                  ];
                };

              defaultConfiguration = makeConfiguration ".agents/skills";
              overrideConfiguration = makeConfiguration ".claude/skills";
            in
            pkgs.runCommand "home-manager-module-check" { } ''
              test -e ${defaultConfiguration.activationPackage}
              test -e ${overrideConfiguration.activationPackage}
              touch "$out"
            '';
        in
        {
          packages = skillPackages // {
            all-skills = allSkills;
            default = allSkills;
          };

          checks = skillChecks // {
            all-skills = allSkills;
            home-manager-module = homeManagerModuleCheck;
          };

          devShells.default = pkgs.mkShell {
            packages = [
              (pkgs.python3.withPackages (pythonPackages: [ pythonPackages.pyyaml ]))
            ];
          };
        };

      forSystems = f:
        nixpkgs.lib.genAttrs systems (system: f system nixpkgs.legacyPackages.${system});
    in
    {
      homeManagerModules.default = homeManagerModule;
      packages = builtins.mapAttrs (_: value: value.packages) (forSystems perSystem);
      checks = builtins.mapAttrs (_: value: value.checks) (forSystems perSystem);
      devShells = builtins.mapAttrs (_: value: value.devShells) (forSystems perSystem);
    };
}
