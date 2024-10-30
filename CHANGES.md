# 0.2.2 - 2024-10-30

## Python

- Continuous integration
- pyproject based project
- crypto dependency is now obsolete, using cryptodome

# 0.2.1

- Minor documentation changes

# 0.2

## Common: Protocol and Docs

- Architecture diagram: common and reimplemented modules
- Schema for peerinfo yamls
- Validation scripts to validate peerinfos (in python implementation)
- `publickey` attribute in peerinfo defined as RSA key in PEM format
- Examples: Mes Opcions peerinfo yaml added as example

## Python

- Now compatible with Python versions 2.7 up to 3.6
- New `Catalog` class generalizes common operations in portals
- Classes in `packaging` have been replaced by functions `parse` and `generate`
- New `KeyRing` class that relies on the `publickey` on peerinfo yaml
- `ApiClient` and `Catalog` raise `BackendError`s.
- Examples: Color in branded examples tell you in which site you are
- Examples: Som Energia implementation of UserInfo interface as example

## PHP

- Added PHP implementation


# 0.1

- First public release

