## REMOVED Requirements

### Requirement: Do not reselect an already handled hidden-sex discoverer
**Reason**: After upstream PR #206 is merged and verified, the source hidden-sex discovery path owns this guarantee and the overlapping local patch is retired.

**Migration**: Use the `hidden-sex-discovery` capability as the durable behavior contract and remove only the duplicate filter and dedicated coverage from `local_group_participant_admission_fix`.
