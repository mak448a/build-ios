# build-ios
This is a tutorial repository for building a Godot Project IPA with GitHub actions. Check it out here: https://mak448a.github.io/blog/compile-ios-godot-without-mac
Please give this repo a star if it helps! :)

> [!NOTE]
> If you're tired of this taking too long, try https://github.com/mak448a/ipa-tools! It's an easy cli to edit the IPA without rebuilding.

If you can't upload to GitHub successfully, you may need to upload the file to dropbox and download it. Replace the contents of build.yml with this. Copy the link to your dropbox file. Replace YOURLINKHERE with it. MAKE SURE TO CHANGE `dl=0` in the URL to `dl=1`.

Also, if you don't want the repository building on every push, you can configure it with `on: [workflow_dispatch]` instead of `on: [push]`.




```yaml
name: "Build iOS app"

on: [push]

jobs:
  build_ios:
    runs-on: macos-latest
    steps:
      - name: checkout repository
        uses: actions/checkout@v4

      - name: build archive and ipaify
        run: |
          wget -O archive.zip "YOURLINKHERE"
          unzip archive.zip -d .

          xcodebuild archive -project Example-Project.xcodeproj -scheme 'Example-Project' -archivePath Example-Project.xcarchive -configuration Release CODE_SIGN_IDENTITY="" CODE_SIGNING_REQUIRED=NO

          mkdir Payload
          mv Example-Project.xcarchive/Products/Applications/Example-Project.app Payload/Example-Project.app

          zip -r "Example-Project.ipa" "Payload"

          mv Example-Project.ipa ${{ runner.temp }}/Example-Project.ipa


      - name: Upload application
        uses: actions/upload-artifact@v4
        with:
          name: Example-Project
          path: ${{ runner.temp }}/Example-Project.ipa
          # you can also archive the entire directory
          # path: ${{ runner.temp }}/build
          retention-days: 3
```
