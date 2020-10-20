# keepass-extractor
A small tool to export a subset of entries from one keepass to another one.

## Usage
### Dependencies
* pykeepass

### Set attributes in existing KeePass
First you need to add a custom property to every entry in the existing KeePass that should be extracted. The default key is `extract_to`, the value specifies the group path in the output KeePass.

### Extract entries
> :exclamation: **Don't pass passwords on the command line, unless it is absolutely necessary.** You will be asked for them.

> :exclamation: **Runing this script will remove all existing entries from the output KeePass.**

> :warning: This script currently does not support creating a KeePass file. Please pass an existing one.

```
usage: extract.py [-h] [-i password] [-o password] [-a attribute] input_keepass output_keepass

positional arguments:
  input_keepass         input keepass path
  output_keepass        output keepass path

optional arguments:
  -h, --help            show this help message and exit
  -i password, --input-password password
                        input keepass password
  -o password, --output-password password
                        output keepass password
  -a attribute, --attribute attribute
                        attribute for getting entries
 ```
