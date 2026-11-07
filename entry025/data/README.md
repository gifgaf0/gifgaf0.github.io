# Entry 025 raw run data

The raw run files are deposited on Zenodo, not in this tree:

- **Version 2 (current):** https://doi.org/10.5281/zenodo.24028529. It is v1 plus `CMTwoAdic.lean`, with `run_log.md` updated to commit 9ef743e.
- **Version 1:** https://doi.org/10.5281/zenodo.24026058 (https://zenodo.org/records/24026058)
- **All versions (concept DOI):** https://doi.org/10.5281/zenodo.24026057

The deposit holds:
- the tarballs below;
- the freeze package (`PREREGISTRATION.md`, `predict.py`, `predictions.json`, `gen.py`, `analyze.py`, `manifest.json`, plus `calib.py` and `constants.py`);
- `results/*.json`, `run_log.md` and `provenance/*`;
- the per-run SHA-256 lists.

Before publication, all 69 deposited files were checked against this branch by MD5.

## What stays here

`*_runs.sha256` holds the SHA-256 of every run file (59,000 in total: A37_64 4,000, B37_128 5,000, CCM_128 40,000, DCM_256 10,000).

To verify a download, extract the tarballs into one directory and run `sha256sum -c` on these lists from there.

## Tarballs on Zenodo

| file | bytes | SHA-256 |
|---|---|---|
| `A37_64_chunk000.tar` | 215,040 | `1b86730ef5fc8c9c40263c79855e596269c7eedea81f841b29d71b61fd3c6d51` |
| `A37_64_chunk001.tar` | 3,491,840 | `7525c24433fed69a384fb8b97b90d6a9b382b2f00c6f9753eff1eca6c46e91a0` |
| `A37_64_chunk002.tar` | 3,799,040 | `4ddc5fd04c1e2fa39b9bd6095fe0ff49d68e505ce28d6e7d5a4623ce100b80c6` |
| `A37_64_chunk003.tar` | 1,044,480 | `2e75efb56c8c2c68fefdcde564fdc3e2b35b7eec45814c3da33ad45fe7abd1e7` |
| `A37_64_chunk004.tar` | 2,037,760 | `616d81f136f45171af80d5c35e28bb3be171f869c651cb7f6b633749e240aed3` |
| `A37_64_chunk005.tar` | 1,740,800 | `d352b6f6f592cb5e2c285bc125d739c59c31a46ca3547097d15d7c97fd7704f5` |
| `B37_128_chunk000.tar` | 102,400 | `7aa52e469b6cc2217728bb69b580893e86bbe90377fb52de0967f7e9bf5d05c3` |
| `B37_128_chunk001.tar` | 604,160 | `9862c8bf13fecc5f1ff37d1adc2c903a65ab5375c7ac3b55f375970a2eb51b4b` |
| `B37_128_chunk002.tar` | 604,160 | `7b62b04c0efe00b70ac89160a97580e873536d9de8dcb1cc12f5c6a66b36b841` |
| `B37_128_chunk003.tar` | 604,160 | `e4edc5649b3cb8f46a7af1c0179ab9c286a972f00148303a7a59f38b5f72d5ac` |
| `B37_128_chunk004.tar` | 614,400 | `e9716299bbfdebc8c40ab186ce95c684633dcad75c2c435d37826981611f03c3` |
| `B37_128_chunk005.tar` | 604,160 | `ff73b37d377a35179aa0c7177e5afa405d7fb1d1db3ad5b7f03ee335d8a3ba1e` |
| `B37_128_chunk006.tar` | 593,920 | `e49c022c8570a8e53df283cb15f4d240e7db8666b096118e6a719bea53736b1c` |
| `B37_128_chunk007.tar` | 593,920 | `625ad7d126a4dc0bc2f9edb112a00eff52db8e08647bf2e4cd3cdd86de8fe74a` |
| `B37_128_chunk008.tar` | 593,920 | `4c605df93a4eb4f58390134761ef5af250c04215b6bd3a4e08a6ac01432753fa` |
| `B37_128_chunk009.tar` | 593,920 | `2ff60180c4e1bdd7fdb372a4ce2671f7cfd9f33d15c6b237fdebb22b2b2f528d` |
| `B37_128_chunk010.tar` | 593,920 | `fd3cf1635441216247f6262260c1b8711b6519d96f4d2fc2a023ecc585a2a44b` |
| `B37_128_chunk011.tar` | 604,160 | `806367069c25a41f05bc49073198a85778013f5db93a27584a684e0766980208` |
| `B37_128_chunk012.tar` | 604,160 | `4059c344be215793900e25e03c86c5f7cfb61335582f07ef1490d3069f421773` |
| `B37_128_chunk013.tar` | 593,920 | `279f9ae895e8e9483f0e6f688226102c414b37fcdfdd6aa8332cfce1cc95b9f0` |
| `B37_128_chunk014.tar` | 604,160 | `5db511e3ed353640f1572d90d2d022c9a3fc5718d27bac068550467ca4942e4b` |
| `B37_128_chunk015.tar` | 593,920 | `6c20ffdf7358b99fe0508198ff247416e604e77dcf271073afe764dbd72fb561` |
| `B37_128_chunk016.tar` | 593,920 | `d87393e25b68342d60a8635fec5b40897857dba44bd1e1c9e2935be108ce639e` |
| `B37_128_chunk017.tar` | 593,920 | `7eeb367f61464f457754022763e1854939277538dd8f5ffe38e2847cd6c839bd` |
| `B37_128_chunk018.tar` | 604,160 | `6282f670b2d571cfbb71a6d76f35e9604493abacb0340cd60659d1df4a99b96c` |
| `B37_128_chunk019.tar` | 593,920 | `4d1d8fab9db8e2397be25e26e2e7f02344ca1e8ea6063bf1fc46c3e9e10a8c41` |
| `B37_128_chunk020.tar` | 614,400 | `7ce5496942e7a0e2568d5bc76fbf9b6c2cdf8d7631f3e5eeee01c22b11841d4c` |
| `B37_128_chunk021.tar` | 604,160 | `860d2958552ae6c3c5725c1a0c45f6b1bab7d7731ce2f0924f6b3c99ec917e3d` |
| `B37_128_chunk022.tar` | 593,920 | `75e3fcec42a199ca207f2e28d1624d172cde7c88f7ad9f27952be6e583863d0a` |
| `B37_128_chunk023.tar` | 593,920 | `6ee856c8d68a7a96265c8219cab50dbf2b265b0039891f84a3c52b49088ab05f` |
| `B37_128_chunk024.tar` | 604,160 | `8bad53c9b54a4c9cdf965413b0ba61c9a71b14309d5634a95b0d77d4762acbe0` |
| `B37_128_chunk025.tar` | 604,160 | `f1b160da5bc97d3387d0690dc28489d97612ea73d52441aeb6c9cbc6ecd68285` |
| `B37_128_chunk026.tar` | 266,240 | `a4232a412f147ca93b73af9f59a8d9b955d5d498ae62809106887d1e47daf91f` |
| `B37_128_chunk027.tar` | 122,880 | `db3ae237f250c9952bc3bddded66d69f7fa3f30e550995d71be7cee1547aeb51` |
| `B37_128_chunk028.tar` | 30,720 | `036f4696c0901d5effecd66f8db82f1272ad52664aa7fdd9a59b17954146b181` |
| `CCM_128_runs.tar.part00` | 99,614,720 | `24d9aa7679f6034e8f2c7bf35fda2e4b3ffe3a2b996324d3382cb7d79022cd18` |
| `CCM_128_runs.tar.part01` | 99,614,720 | `80dbcdcf62178b1ec759664d18cb8ac64c719f1a4d133d3efb7612c570112af2` |
| `CCM_128_runs.tar.part02` | 99,614,720 | `820aaab852edc871353949406e2e17f83bbdc9d52ed9de33853f68f8ac7a6725` |
| `CCM_128_runs.tar.part03` | 99,614,720 | `5792a0b3f7b6b0df218e345a581bc7b289fe417e9771f6d27b14717545dd5b06` |
| `CCM_128_runs.tar.part04` | 21,237,760 | `d01d6b6b1d62e008ba1bfd061bd947d6a19f0c25d0be6551c1f3c0cedd7e70e1` |
| `DCM_256_runs.tar.part00` | 47,185,920 | `87f65c33f84401d843cf1105811e1e3b314ae77c0f7cfb03f9428ea4e976c0df` |
| `DCM_256_runs.tar.part01` | 47,185,920 | `841a045a6fefba20311e5939411d93071295ff1286520095ef76f951226cc578` |
| `DCM_256_runs.tar.part02` | 12,185,600 | `ad118e14d78e7a2528fc2c5deb985fc40f8a781e793ee071aba08b3218d9e5a8` |

## Reassembling

```sh
# CM arms: split tarballs
cat CCM_128_runs.tar.part0* | tar -x
cat DCM_256_runs.tar.part0* | tar -x
# 37a1 arms: each chunk holds the runs archived at one checkpoint
for f in A37_64_chunk*.tar B37_128_chunk*.tar; do tar -xf "$f"; done
sha256sum -c A37_64_runs.sha256 B37_128_runs.sha256 CCM_128_runs.sha256 DCM_256_runs.sha256
```

Then run `analyze.py <dir> <ARM>` from `entry025/` to reproduce `results/<ARM>.json`.

## Git history

The tarballs were removed from this directory after the Zenodo deposit. The commits that added them stay on branch `ccr-8b0a23fb-g0djgx`:
- the CM-arm data commits;
- the 37a1 checkpoint commits cited in `run_log.md`, the last being `601f968`.

Any of those commits can be checked out to retrieve the files from git instead of Zenodo.
