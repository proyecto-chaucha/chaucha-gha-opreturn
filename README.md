# Chaucha Commit Notarization

Using [_Chaucha_](https://chaucha.cl) blockchain, commits can be certified
using _OP_RETURN_. Now _Github_ history can be _notarized_.

![OP_RETURN](https://user-images.githubusercontent.com/292738/93739829-9546ec80-fbbf-11ea-9c66-a1b7c1dfca99.png)

![OP_RETURN in Explorer](https://user-images.githubusercontent.com/292738/93740190-654c1900-fbc0-11ea-898c-bc7e0e20ab9f.png)

![OP_RETURN Decoded](https://user-images.githubusercontent.com/292738/93740118-3c2b8880-fbc0-11ea-9356-f6d3a4904075.png)

## Usage

Using a mixture of `OP_RETURN` and [Git Notes](https://github.com/NinjasCL/gha-notes) we can
notarize each commit.

### Example workflow

```yaml
name: Integration Test
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Self test
        id: selftest

        uses: proyecto-chaucha/chaucha-gha-opreturn@master
        with:
          privkey: "${{secrets.PRIVKEY}}"
          pubkey: "${{secrets.PUBKEY}}"
          sendkey: "${{secrets.SENDKEY}}"
          message: "repo: ${{github.repository}};branch: ${{github.ref}};commit: ${{github.sha}}"

      # Save certification using git-notes
      - run: |
          git config user.name "$GITHUB_ACTOR"
          git config user.email "$GITHUB_ACTOR@users.noreply.github.com"
          git fetch origin "refs/notes/*:refs/notes/*"
          git notes append -m "repo: $GITHUB_REPOSITORY ; branch: $GITHUB_REF ; commit: $GITHUB_SHA ; tx: ${{steps.selftest.outputs.response}}"
          git push origin "refs/notes/*"
```

### Inputs

| Input     | Description                                                                            |
| --------- | -------------------------------------------------------------------------------------- |
| `privkey` | Private Key to sign transaction. Use _PRIVKEY_ in Github Secrets.                      |
| `pubkey`  | Public key of the Private key to verify confirmations. Use _PUBKEY_ in Github Secrets. |
| `sendkey` | Public key to send the transaction. Use _SENDKEY_ in Github Secrets.                   |
| `message` | Message to send with `OP_RETURN`. Max 255 chars.                                       |

### Outputs

| Output     | Description                                  |
| ---------- | -------------------------------------------- |
| `response` | Response with the `OP_RETURN` result message |
