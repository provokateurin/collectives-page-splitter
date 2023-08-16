# collectives-page-splitter

This is a tool to split a [Nextcloud Collectives](https://github.com/nextcloud/collectives) page into multiple pages.
This tool might not be complete, I only implemented what was necessary for my use case.
I take no responsibility if you do something wrong or the tool behaves in unexpected ways.
Make sure to take backups before running this.
Proceed with caution.

The tool will always only split on the headings with the highest level, but you can just run the tool again on the new pages to split them even further.

## Steps

1. Download the relevant page using the Files app. If you have attachments or sub-pages you should download the whole folder of the page.
2. Extract the page and all its content
3. Run the following command with the correct paths (you can skip the attachments folder if you don't have any attachments): `./split.py /path/to/markdown.md /path/to/.attachments.xxx`
4. Afterward you can upload the output again into your Collective using the Files app (don't forget your attachments folder if you have one)
5. The attachments will work fine, but because the news pages are new files they have a different file ID and new attachments would be put in a different folder than the existing ones. Fixing this can be very tedious and is technically not necessary.
   1. To fix this you can find out the IDs of the new pages by browsing them using the Files app and opening in Text them by clicking on them.
   2. You will have the file ID in the URL bar. You can close the file again.
   3. Rename the `.attachments.xxx` folder such that the `xxx` is replaced with your file ID.
   4. Update all the references to the attachments folder in your page.
