## Context

Scene and map identifiers are game room addresses assembled with `os.sep` and persisted in pickle saves. A Windows save therefore contains backslash-separated addresses that do not match the slash-separated addresses generated on Linux. Before the fix, map reconciliation interpreted the foreign-form keys as deleted scenes and replaced them with new empty scene objects, losing the saved character registrations.

The local `local_cross_platform_save_fix` established the field inventory and load-boundary approach. Upstream PR #207 carries the source version and demonstrates the failure and fix through the ordinary Tk scene shown immediately after loading.

## Goals / Non-Goals

**Goals:**

- Preserve scene, map, character housing, hypnosis-location, and facility-location data across operating systems.
- Normalize only fields known to contain structured game room addresses.
- Perform compatibility work before version migration and map reconciliation inspect those addresses.
- Define a safe transition from the local mod to upstream ownership.

**Non-Goals:**

- Change the pickle save format or the platform-native format used when writing saves.
- Recursively rewrite every string in the cache.
- Change map generation, character movement, Tk rendering, or Web rendering.
- Use a special H-state or group-state flow as the compatibility contract.

## Decisions

### Normalize at deserialization

`load_save()` normalizes the loaded cache immediately after unpickling. This is earlier and narrower than repairing map state after `update_map()` has already discarded unmatched keys, and it gives later version migrations native-form addresses.

### Enumerate structural fields

Normalization covers scene and map dictionary keys and their stored paths, character dormitory fields, the dormitory-administrator target room, the air-hypnosis position, facility-damage dictionary keys, and maintenance-place values. A recursive string walk is rejected because ordinary text can legitimately contain slash characters.

### Preserve native objects when no conversion is needed

Path-keyed dictionaries remain the same objects when no foreign separator is present. This minimizes changes for saves created on the current operating system and avoids rebuilding data unnecessarily.

### Retire the local mod after verified upstream adoption

PR #207 merged on 2026-07-13 as `16960e1b89e72da0d5a31ef5e716c0368cd0b924`. Current `main` contains the merged implementation, the focused foreign-path/native-path/ordinary-text and ordinary post-load checks pass, and the duplicate local replacement and configuration entries have been removed.

## Risks / Trade-offs

- **A structured address field is missing from the inventory** -> retain inventory-based tests and extend the explicit list when a new field is proven.
- **Normalization changes ordinary text** -> never recurse through arbitrary strings; operate only on named structural fields.
- **Both local and upstream implementations run temporarily** -> remove the local replacement immediately after merged-source verification, but not before.
- **PR behavior changes during review** -> compare the merged implementation with this field and ordering contract before syncing the spec.

## Migration Plan

1. Keep `local_cross_platform_save_fix` enabled while PR #207 is under review.
2. After merge, update the private branch from an upstream revision containing the fix.
3. Load a foreign-separator ordinary save and verify the normal scene appears with its saved nearby characters.
4. Rerun field-inventory, native-path, and ordinary-text coverage against the upstream implementation.
5. Remove the local replacement, its default configuration entry, and duplicate tests after that verification passes.
6. Sync the new capability into the main specifications and archive the change.

Rollback is to restore and re-enable the local mod if upstream normalization is reverted or fails compatibility verification.

## Open Questions

The change remains active only because the full configured `mod/tests` suite is not green for two unrelated active-change failures recorded in the implementation notes.
