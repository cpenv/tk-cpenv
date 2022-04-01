# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [v0.5.8](https://github.com/cpenv/tk-cpenv/releases/tag/v0.5.8) - 2022-04-01

<small>[Compare with v0.5.7](https://github.com/cpenv/tk-cpenv/compare/v0.5.7...v0.5.8)</small>

### Added
- Add duplicate and rename tools to ui. ([31e866e](https://github.com/cpenv/tk-cpenv/commit/31e866e0c1c2325ea22a15dd8e1ecd493a114f06) by Dan Bradham).
- Add duplicate_environment method to io object. ([778ba75](https://github.com/cpenv/tk-cpenv/commit/778ba75ddba2ecfc3a7a3e4944af3d73345a16ad) by Dan Bradham).
- Add edit icon. ([41b2d71](https://github.com/cpenv/tk-cpenv/commit/41b2d71abce008dd9b4bc0fba5abc83b9b9dccac) by Dan Bradham).


## [v0.5.7](https://github.com/cpenv/tk-cpenv/releases/tag/v0.5.7) - 2022-03-25

<small>[Compare with v0.5.6](https://github.com/cpenv/tk-cpenv/compare/v0.5.6...v0.5.7)</small>

### Fixed
- Fix super calls in progressdialog. ([75b763a](https://github.com/cpenv/tk-cpenv/commit/75b763ac6d278a52936f3449abca320f5ff2a83d) by Dan Bradham).


## [v0.5.6](https://github.com/cpenv/tk-cpenv/releases/tag/v0.5.6) - 2022-02-02

<small>[Compare with v0.5.5](https://github.com/cpenv/tk-cpenv/compare/v0.5.5...v0.5.6)</small>


## [v0.5.5](https://github.com/cpenv/tk-cpenv/releases/tag/v0.5.5) - 2021-09-30

<small>[Compare with v0.5.4](https://github.com/cpenv/tk-cpenv/compare/v0.5.4...v0.5.5)</small>

### Added
- Added deny_permissions, deny_platforms and display_name setting support ([f4543bd](https://github.com/cpenv/tk-cpenv/commit/f4543bd0c52f71e13253a00bd7077f23e637c745) by Ricardo Musch).

### Changed
- Changed names to include ui ([ec68670](https://github.com/cpenv/tk-cpenv/commit/ec686700e70edba3ddafee907f34dc1c1384b9b9) by RicardoMusch).


## [v0.5.4](https://github.com/cpenv/tk-cpenv/releases/tag/v0.5.4) - 2021-09-01

<small>[Compare with v0.5.3](https://github.com/cpenv/tk-cpenv/compare/v0.5.3...v0.5.4)</small>


## [v0.5.3](https://github.com/cpenv/tk-cpenv/releases/tag/v0.5.3) - 2021-06-16

<small>[Compare with v0.5.2](https://github.com/cpenv/tk-cpenv/compare/v0.5.2...v0.5.3)</small>


## [v0.5.2](https://github.com/cpenv/tk-cpenv/releases/tag/v0.5.2) - 2021-06-15

<small>[Compare with v0.5.1](https://github.com/cpenv/tk-cpenv/compare/v0.5.1...v0.5.2)</small>

### Fixed
- Fix lock button error when missing environment. ([051d403](https://github.com/cpenv/tk-cpenv/commit/051d403369f88b81e92bdbb738491d4aa6353a78) by Dan Bradham).
- Fix sort order of available list. ([beceb29](https://github.com/cpenv/tk-cpenv/commit/beceb293fe271424243858cf9e6e3b52388f81cb) by Dan Bradham).


## [v0.5.1](https://github.com/cpenv/tk-cpenv/releases/tag/v0.5.1) - 2021-06-11

<small>[Compare with v0.5.0](https://github.com/cpenv/tk-cpenv/compare/v0.5.0...v0.5.1)</small>


## [v0.5.0](https://github.com/cpenv/tk-cpenv/releases/tag/v0.5.0) - 2021-06-04

<small>[Compare with v0.4.0](https://github.com/cpenv/tk-cpenv/compare/v0.4.0...v0.5.0)</small>

### Added
- Add support for restricting environments to specific software versions. closes #10. ([09b3e09](https://github.com/cpenv/tk-cpenv/commit/09b3e0937674ba9087963b32f81ac142ef1b2ea8) by Dan Bradham).


## [v0.4.0](https://github.com/cpenv/tk-cpenv/releases/tag/v0.4.0) - 2021-02-12

<small>[Compare with v0.3.9](https://github.com/cpenv/tk-cpenv/compare/v0.3.9...v0.4.0)</small>

### Added
- Add and display envselector dialog when launching engine with multiple environments available. ([4b87b17](https://github.com/cpenv/tk-cpenv/commit/4b87b17f8ad593eadc8dbfe31ebc1aa0d1e7f861) by Dan Bradham).
- Add envpermissions dialog. ([0afe001](https://github.com/cpenv/tk-cpenv/commit/0afe001ebc9a9a5e7660a05fe62a032ff0a13173) by Dan Bradham).
- Add permissions tool to moduleselector. ([fef9523](https://github.com/cpenv/tk-cpenv/commit/fef95236960f29de7130b6e582ce603bad1dfc7a) by Dan Bradham).
- Add support for environment permissions. ([771f40d](https://github.com/cpenv/tk-cpenv/commit/771f40dd92661f04dd6f07477cb2b4cec2d7e215) by Dan Bradham).

### Fixed
- Fix notice width. ensure it's the full width of it's parent widget. ([252f43f](https://github.com/cpenv/tk-cpenv/commit/252f43f95109b7a3f525d5cd398234bc388ae3da) by Dan Bradham).
- Fix bug where the icon in moduleinfo would not properly update. ([4369494](https://github.com/cpenv/tk-cpenv/commit/436949403ab3fb84ed29ce6bffcd0245a808e62f) by Dan Bradham).
- Fix bug in envtree when encountering an int value. ([614f558](https://github.com/cpenv/tk-cpenv/commit/614f55843f18bed9231d31bafe5669aa0583d9a0) by Dan Bradham).


## [v0.3.9](https://github.com/cpenv/tk-cpenv/releases/tag/v0.3.9) - 2021-02-10

<small>[Compare with v0.3.8](https://github.com/cpenv/tk-cpenv/compare/v0.3.8...v0.3.9)</small>

### Changed
- Change: update cpenv to 0.5.21 ([3fbb404](https://github.com/cpenv/tk-cpenv/commit/3fbb4042f4364784af22c2d748263c9078cebd33) by Dan Bradham).


## [v0.3.8](https://github.com/cpenv/tk-cpenv/releases/tag/v0.3.8) - 2020-10-09

<small>[Compare with v0.3.7](https://github.com/cpenv/tk-cpenv/compare/v0.3.7...v0.3.8)</small>

### Changed
- Change: manually set environment in cpenvapp.activate ([fe9998e](https://github.com/cpenv/tk-cpenv/commit/fe9998e3cfe242d3621f435e3933a89ae1d91311) by Dan Bradham).
- Change: update cpenv to 0.5.14 ([51413d5](https://github.com/cpenv/tk-cpenv/commit/51413d5ba8fb3adb86356ab11efc35f535a2dadf) by Dan Bradham).


## [v0.3.7](https://github.com/cpenv/tk-cpenv/releases/tag/v0.3.7) - 2020-08-28

<small>[Compare with v0.3.6](https://github.com/cpenv/tk-cpenv/compare/v0.3.6...v0.3.7)</small>

### Changed
- Change: update cpenv to 0.5.13 ([c357b0a](https://github.com/cpenv/tk-cpenv/commit/c357b0a077c832dedaf0cc54485000e6c944386c) by Dan Bradham).


## [v0.3.6](https://github.com/cpenv/tk-cpenv/releases/tag/v0.3.6) - 2020-08-27

<small>[Compare with v0.3.5](https://github.com/cpenv/tk-cpenv/compare/v0.3.5...v0.3.6)</small>

### Changed
- Change: pass instantiated reporter to cpenv.set_reporter ([469fb90](https://github.com/cpenv/tk-cpenv/commit/469fb90a404a2e796736b8c9f42222e0a0432673) by Dan Bradham).
- Change: update cpenv to 0.5.12 ([f204353](https://github.com/cpenv/tk-cpenv/commit/f2043534a963daffd5abfd49e62c8ec5b91da2a3) by Dan Bradham).

### Fixed
- Fix: remove called to preprocess_dict when generating environ preview ([dc05363](https://github.com/cpenv/tk-cpenv/commit/dc053636cfcbeed664fceffb516caeba4780b078) by Dan Bradham).


## [v0.3.5](https://github.com/cpenv/tk-cpenv/releases/tag/v0.3.5) - 2020-08-12

<small>[Compare with v0.3.4](https://github.com/cpenv/tk-cpenv/compare/v0.3.4...v0.3.5)</small>

### Added
- Add: popup notification when saving changes. ([a26af1b](https://github.com/cpenv/tk-cpenv/commit/a26af1b6fb5890923a95d61f0f56892e89230f8a) by Dan Bradham).
- Add: copy icon add: docstring to res.__init__ ([96beb47](https://github.com/cpenv/tk-cpenv/commit/96beb47c2936a13cd573245578d54d7d6ff160da) by Dan Bradham).
- Add: minimizedlist widget ([4f2fcc5](https://github.com/cpenv/tk-cpenv/commit/4f2fcc549c54ddd395d65d2f75705df40ac582ba) by Dan Bradham).
- Add: copy to clipboard button to envdisplay ([8c19d4c](https://github.com/cpenv/tk-cpenv/commit/8c19d4cd3c39a3b1e715775500271d7b26813a43) by Dan Bradham).
- Add: notice dialog ([13173e1](https://github.com/cpenv/tk-cpenv/commit/13173e1184fe20f44b81ee054a45cb2318868dd7) by Dan Bradham).
- Add: support for nested dictionaries to envtree ([2c32fa0](https://github.com/cpenv/tk-cpenv/commit/2c32fa09adfd6fa71581b82fae29787401a1f932) by Dan Bradham).

### Changed
- Change: update set_modules_dialog.png ([cf5fbc4](https://github.com/cpenv/tk-cpenv/commit/cf5fbc4ccaabdeb0b78033206d587e3332052658) by Dan Bradham).
- Change: improve layout of moduleinfo add: ability to copy environment and requires from moduleinfo ([3c8c183](https://github.com/cpenv/tk-cpenv/commit/3c8c18377cb63f85ffd1019c58f9ff76e9c16e61) by Dan Bradham).
- Change: update cpenv to 0.5.11 ([357cc75](https://github.com/cpenv/tk-cpenv/commit/357cc758e64183ab83717366ab44887311bfb0a4) by Dan Bradham).

### Removed
- Remove: extraneous logging ([4831b5c](https://github.com/cpenv/tk-cpenv/commit/4831b5c09c87173ad6d078e714e7c52dc1c1abb7) by Dan Bradham).


## [v0.3.4](https://github.com/cpenv/tk-cpenv/releases/tag/v0.3.4) - 2020-08-07

<small>[Compare with v0.3.3](https://github.com/cpenv/tk-cpenv/compare/v0.3.3...v0.3.4)</small>

### Changed
- Change: update changelog ([9d40258](https://github.com/cpenv/tk-cpenv/commit/9d40258c7ca0ffa4de80ac7880fb8bb5c91b3add) by Dan Bradham).

### Fixed
- Fix: #5 - resolve nameerror in on_import_clicked ([a50c093](https://github.com/cpenv/tk-cpenv/commit/a50c093190dc950070b78ed40b96f7131735ce36) by Dan Bradham).


## [v0.3.3](https://github.com/cpenv/tk-cpenv/releases/tag/v0.3.3) - 2020-08-07

<small>[Compare with v0.3.2](https://github.com/cpenv/tk-cpenv/compare/v0.3.2...v0.3.3)</small>

### Added
- Add: show_error method ([1901556](https://github.com/cpenv/tk-cpenv/commit/190155697f2c4fddb363bf86913c5c6e5980bbf4) by Dan Bradham).
- Add: changelog ([4035071](https://github.com/cpenv/tk-cpenv/commit/4035071e843b6654b8e5208c17638694ec301936) by Dan Bradham).

### Changed
- Change: bump version to v0.3.3 ([94386df](https://github.com/cpenv/tk-cpenv/commit/94386df9bfe985223670c47a323ae43d9872482c) by Dan Bradham).
- Change: remove try-except block from example before_app_launch ([412cbfc](https://github.com/cpenv/tk-cpenv/commit/412cbfc81d5f8dd5d39d23d6242d7afd1b378046) by Dan Bradham).
- Change: wrap _before_app_launch in try-except block add: error dialog of _before_app_launch raises an exception ([c826b0b](https://github.com/cpenv/tk-cpenv/commit/c826b0bae5748ce745d91e02798bf1a5a361fced) by Dan Bradham).
- Change: move before_app_launch functionality into private method also improves legibility of the before_app_launch procedure. ([ff24f79](https://github.com/cpenv/tk-cpenv/commit/ff24f79f44b2305470f2bfc51e623c9c60e3ba64) by Dan Bradham).
- Change: cpenvio docstring ([d53bc2a](https://github.com/cpenv/tk-cpenv/commit/d53bc2a0be1b5de84e533603cc63f03a3f965da7) by Dan Bradham).
- Change: tense of log message ([8ee4718](https://github.com/cpenv/tk-cpenv/commit/8ee4718ba4e3b05746a7a107d68985e2f7989bb1) by Dan Bradham).
- Change: ensure that we log exceptions in key methoods ([9bf0502](https://github.com/cpenv/tk-cpenv/commit/9bf05023534f576eb8cc595e55a4625809a27174) by Dan Bradham).
- Change: inject app and engine to uireporter class allows us to use engine._get_dialog_parent to ensure we have a valid parent for the progress dialog. ([1fe9ea3](https://github.com/cpenv/tk-cpenv/commit/1fe9ea35ad2ce0992372e7c4e780b12bc07965ef) by Dan Bradham).
- Change: make sure dialogs can be used with engine.show methods ([247a9e0](https://github.com/cpenv/tk-cpenv/commit/247a9e055a0ea67eb2e84580b9a403382801dc2a) by Dan Bradham).


## [v0.3.2](https://github.com/cpenv/tk-cpenv/releases/tag/v0.3.2) - 2020-08-05

<small>[Compare with v0.3.1](https://github.com/cpenv/tk-cpenv/compare/v0.3.1...v0.3.2)</small>

### Added
- Add: preview environment tool ([8baf4ce](https://github.com/cpenv/tk-cpenv/commit/8baf4ce870a102fca51fa8a6ffab89045a054bf4) by Dan Bradham).

### Changed
- Change: update readme.md - add "use set modules dialog" section ([920fdad](https://github.com/cpenv/tk-cpenv/commit/920fdadc23e208ec14806b0798a14da52f0146f7) by Dan Bradham).
- Change: maintain user ordering of selected modules list ([5fa4a08](https://github.com/cpenv/tk-cpenv/commit/5fa4a08b6534342c2a3cee94d46bc7efa965ff67) by Dan Bradham).
- Change: update cpenv to 0.5.8 ([d1e11ad](https://github.com/cpenv/tk-cpenv/commit/d1e11ad75f3bc53b5bf82d727acd74228cd8eeb1) by Dan Bradham).
- Change: update readme.md ([091a497](https://github.com/cpenv/tk-cpenv/commit/091a497d8096936985ed0024d502e516756cfa12) by Dan Bradham).

### Fixed
- Fix: patch cpenv imports ([7ea6554](https://github.com/cpenv/tk-cpenv/commit/7ea655442285858ef2d3ab5bae1dee49354f84d8) by Dan Bradham).


## [v0.3.1](https://github.com/cpenv/tk-cpenv/releases/tag/v0.3.1) - 2020-06-30

<small>[Compare with v0.2.2](https://github.com/cpenv/tk-cpenv/compare/v0.2.2...v0.3.1)</small>

### Added
- Add: store environments directly in the shotgun database. closes #3 add: create environments per project / engine add: import environments from other projects fix: fix progress reporting. closes #2 ([dcf0658](https://github.com/cpenv/tk-cpenv/commit/dcf0658899ed17fc731e99ec986439637990d99d) by Dan Bradham).

### Changed
- Change: update cpenv to 0.5.7 ([9fdeb7f](https://github.com/cpenv/tk-cpenv/commit/9fdeb7f97e4bc17e040ed3ce5081574396ec6979) by Dan Bradham).
- Change: bump version in example_config ([55924f4](https://github.com/cpenv/tk-cpenv/commit/55924f49583885c04985e8c521809a8bd6ff0b1d) by Dan Bradham).

### Fixed
- Fix: include shotgun_api3.lib package ([341c32d](https://github.com/cpenv/tk-cpenv/commit/341c32d084daa434d62ef0cb415d3719e38fd744) by Dan Bradham).
- Fix: attributeerror in before_app_launch ([e35eedc](https://github.com/cpenv/tk-cpenv/commit/e35eedc1978e3caf0aaaa4fb7bbf492bfdcdfeb1) by Dan Bradham).


## [v0.2.2](https://github.com/cpenv/tk-cpenv/releases/tag/v0.2.2) - 2020-05-26

<small>[Compare with v0.2.1](https://github.com/cpenv/tk-cpenv/compare/v0.2.1...v0.2.2)</small>

### Changed
- Change: update cpenv to 0.5.4 ([3c93ea5](https://github.com/cpenv/tk-cpenv/commit/3c93ea5186a79fed46186f729152697146f95b0d) by Dan Bradham).


## [v0.2.1](https://github.com/cpenv/tk-cpenv/releases/tag/v0.2.1) - 2020-05-18

<small>[Compare with v0.2.0](https://github.com/cpenv/tk-cpenv/compare/v0.2.0...v0.2.1)</small>

### Added
- Add: uireporter, progressdialog and errordialog ([c21f616](https://github.com/cpenv/tk-cpenv/commit/c21f6160c7de75f08d0d50a5f5cef72af9285eec) by Dan Bradham).

### Changed
- Change: bump version in example_config ([aacc658](https://github.com/cpenv/tk-cpenv/commit/aacc65817e87e73b47dc1688a635398ab073e733) by Dan Bradham).
- Change: update readme ([88e1427](https://github.com/cpenv/tk-cpenv/commit/88e142731c6fae9ec24095418673f865761717ec) by Dan Bradham).
- Change: update cpenv to 0.5.2 ([267c299](https://github.com/cpenv/tk-cpenv/commit/267c299c8c74acf0fb5b000e27b341c00a768d98) by Dan Bradham).


## [v0.2.0](https://github.com/cpenv/tk-cpenv/releases/tag/v0.2.0) - 2020-05-12

<small>[Compare with v0.1.2](https://github.com/cpenv/tk-cpenv/compare/v0.1.2...v0.2.0)</small>

### Added
- Add: modulespecset to maintain multiple versions of a single module ([acfe882](https://github.com/cpenv/tk-cpenv/commit/acfe8820f28f11406ba61e37a2c22524a1021682) by Dan Bradham).
- Add: module_entity and home_path config keys ([29fcb9e](https://github.com/cpenv/tk-cpenv/commit/29fcb9e3563ded8ec820b1cb5ef2a08375517a04) by Dan Bradham).
- Add: dark and light icons ([fa9990d](https://github.com/cpenv/tk-cpenv/commit/fa9990d86c4ceef9bcafab644ac87e3c408c5762) by Dan Bradham).

### Changed
- Change: update ui to group all versions of a module in a single row add: module info panel ([acbe866](https://github.com/cpenv/tk-cpenv/commit/acbe8667a3a14fe2439483c037e98be37b2a1ab8) by Dan Bradham).
- Change: initialize shotgunrepo in init_app this repo is used to find and download modules from shotgun ([ad98099](https://github.com/cpenv/tk-cpenv/commit/ad980997cd997b00aca0306703cb154f1a85389d) by Dan Bradham).
- Change: update cpenv to 0.5.1 ([22a5f46](https://github.com/cpenv/tk-cpenv/commit/22a5f46143a93de3ab00707dc677c55fddd15eaa) by Dan Bradham).

### Fixed
- Fix: activate requires a list rather than single file path ([633fb9a](https://github.com/cpenv/tk-cpenv/commit/633fb9ac28a1fd69a270ae87b5885477fc7e7d5e) by Dan Bradham).


## [v0.1.2](https://github.com/cpenv/tk-cpenv/releases/tag/v0.1.2) - 2020-04-23

<small>[Compare with v0.1.1](https://github.com/cpenv/tk-cpenv/compare/v0.1.1...v0.1.2)</small>

### Fixed
- Fix: return resolved modules from activate ([89f7872](https://github.com/cpenv/tk-cpenv/commit/89f7872bb5dde304bdff746928d457ebcb65d6f7) by Dan Bradham).


## [v0.1.1](https://github.com/cpenv/tk-cpenv/releases/tag/v0.1.1) - 2020-04-23

<small>[Compare with v0.1.0](https://github.com/cpenv/tk-cpenv/compare/v0.1.0...v0.1.1)</small>

### Added
- Add: example tk-shotgun.yml config - enables tk-cpenv for website ([51f6fd9](https://github.com/cpenv/tk-cpenv/commit/51f6fd96249e3bb55087f9812a03fe64f939ae78) by Dan Bradham).

### Changed
- Change: bump to v0.1.1 ([0199249](https://github.com/cpenv/tk-cpenv/commit/01992497498ae147b6ac03d2c741976428090107) by Dan Bradham).
- Change: update cpenv to 0.4.4 ([5b071af](https://github.com/cpenv/tk-cpenv/commit/5b071aff695fb37f9f083712e32bb011e3497747) by Dan Bradham).

### Fixed
- Fix: use software_entity engine key fallback to engine_name ([4136049](https://github.com/cpenv/tk-cpenv/commit/4136049b8d594c9c9f3caec8b872322868f434b4) by Dan Bradham).


## [v0.1.0](https://github.com/cpenv/tk-cpenv/releases/tag/v0.1.0) - 2020-04-22

<small>[Compare with first commit](https://github.com/cpenv/tk-cpenv/compare/98904ad3c2b7fcb8790e7756e78f67c35a74700b...v0.1.0)</small>

### Added
- Add: shotgun desktop preview ([c9161e9](https://github.com/cpenv/tk-cpenv/commit/c9161e9bd0426dccc6a8f5f8d39c4cec5877a172) by Dan Bradham).


