{
  description = "Composable Nix and NixOS ecosystem skills for coding agents";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { nixpkgs, ... }:
    let
      skillRoot = ./skills;
      skillPath = name: skillRoot + "/${name}";
      skillNames = builtins.filter
        (name: builtins.pathExists (skillPath name + "/SKILL.md"))
        (builtins.attrNames (builtins.readDir skillRoot));

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
        in
        {
          packages = skillPackages // {
            all-skills = allSkills;
            default = allSkills;
          };

          checks = skillChecks // {
            all-skills = allSkills;
          };

          devShells.default = pkgs.mkShell {
            packages = [
              (pkgs.python3.withPackages (pythonPackages: [ pythonPackages.pyyaml ]))
            ];
          };
        };
    in
    {
      packages = builtins.mapAttrs (_: value: value.packages) (
        builtins.mapAttrs perSystem nixpkgs.legacyPackages
      );
      checks = builtins.mapAttrs (_: value: value.checks) (
        builtins.mapAttrs perSystem nixpkgs.legacyPackages
      );
      devShells = builtins.mapAttrs (_: value: value.devShells) (
        builtins.mapAttrs perSystem nixpkgs.legacyPackages
      );
    };
}
