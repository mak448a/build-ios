import zipfile
import os


def replace_pck(ipa_path: str) -> None:
    """
    Replaces .pck file in a given IPA file.

    Args:
        ipa_path (str): The path to the IPA file.
    """

    replacement_path = f"Payload/{ipa_path[0:-4]}.app/{ipa_path[0:-4]}.pck"
    pck_file = f"{ipa_path[0:-4]}.pck"

    with zipfile.ZipFile(ipa_path) as ipa, zipfile.ZipFile(
        "temp_ipa.ipa", "w"
    ) as tmp_ipa:
        for item in ipa.infolist():
            if item.filename != replacement_path:
                tmp_ipa.writestr(item, ipa.read(item.filename))
            else:
                with open(pck_file, "rb") as file:
                    tmp_ipa.writestr(replacement_path, file.read())

    os.replace("temp_ipa.ipa", ipa_path)
