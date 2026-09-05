# Hardware, storage, persistence, and secrets

Use this reference for hardware profiles, boot paths, disks, encryption,
impermanence, backups, agenix, or sops-nix.

## Hardware and boot

Collect evidence before changing kernel parameters, firmware, graphics, input, or
power settings: `nixos-version`, hardware model, kernel logs, PCI/USB devices,
current module imports, and the active generation. Use a focused `nixos-hardware`
profile only when it matches the machine; audit the profile before adding it.

Boot, display, network, and storage changes are high-risk. Build a VM or a second
generation when possible, and write the rescue or rollback path before activation.

## Disks and persistence

For `disko` or any formatter:

1. confirm the exact target device and backup status;
2. render or inspect the intended partition table and mount map;
3. distinguish a dry plan from an irreversible apply;
4. confirm encryption keys and recovery material are available;
5. only then authorize formatting or installation.

For impermanent roots, list every directory that must survive reboot: machine
identity, SSH host keys, Nix database, user data, service databases, and secret keys.
Persistence declarations are not backups; test restore separately.

## Secrets

With `sops-nix` or `agenix`, keep encrypted inputs in source control only when the
repository policy allows it, and never expose plaintext to evaluation, logs, store
paths, or command arguments. Verify:

- the decryption key exists at activation time;
- the secret path, owner, group, and mode match the consuming service;
- system and Home Manager secrets use the correct activation boundary;
- services start after the secret is materialized;
- rotation and recovery do not depend on a single unavailable host key.

When debugging, inspect path existence, permissions, unit ordering, and journal
messages without printing the secret content.
