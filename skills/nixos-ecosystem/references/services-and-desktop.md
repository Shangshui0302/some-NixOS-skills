# Services, systemd, networking, and desktop runtime

Use this reference for NixOS services, user services, systemd units, networking,
desktop sessions, graphics, audio, input, and compositor integrations.

## Native service first

Ask whether nixpkgs already provides a NixOS or Home Manager module. Prefer the
native module when it owns package, unit, user, state directory, firewall, and
reload behavior together. Use a hand-written unit only when the module is absent or
cannot express the requirement; document the missing boundary.

## Unit diagnosis

Check the generated unit and its runtime context, not only the Nix expression:

```bash
systemctl cat <unit>
systemctl show <unit> -p User,Group,Environment,ExecStart,After,Requires
systemctl status <unit>
journalctl -b -u <unit> --no-pager
```

For user services substitute `systemctl --user`. Verify state directories, dynamic
users, environment variables, `PATH`, capabilities, sandboxing, and ordering. A
service that starts manually may still fail under systemd's restricted environment.

## Network and firewall

Identify the listening address, port, interface, firewall rule, DNS dependency,
reverse proxy, and secret source separately. Do not open a port merely because a
service failed; first establish whether it is listening and whether the client is
using the expected address family.

## Desktop sessions

Treat greetd/display manager, session entrypoint, compositor, portals, input method,
audio, GPU, theme, and user services as separate runtime layers. Test the exact
session the user launches. A configuration that evaluates for Hyprland does not prove
niri or GNOME behavior, and a desktop file that builds does not prove a Wayland
launcher starts.

For runtime issues, collect the active session environment, unit logs, compositor
logs/IPC state, and the active generation before editing. Record which checks require
the user to log in or switch sessions.
